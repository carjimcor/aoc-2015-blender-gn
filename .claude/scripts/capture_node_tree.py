"""Screenshot a node tree in overlapping tiles using Blender's own UI.

Usage (one Blender window opens, captures every target and closes; the .blend is never saved,
and any String node labelled "Puzzle Input" is blanked in memory first):
  blender file.blend --python capture_node_tree.py -- out_dir px_per_unit "slug=Name" "slug=Name|Frame" ...
Then join each target's tiles into media_dir/<slug>.png:
  python stitch_images.py --dir out_dir media_dir

Name is a Geometry Nodes group, the compositor group, or a material (shader tree).
Frame (optional) is the name or label of a Frame node, to capture only that part, or "@NodeName" for one node.
px_per_unit sets the zoom: about 1.0 keeps node text readable, 0.5 fits a mid-size group in one image.
Tiles use the editor's current size, so a larger Blender window gives fewer tiles.
"""
import json
import math
import os
import sys

import bpy

args = sys.argv[sys.argv.index("--") + 1:]
OUT = os.path.abspath(args[0])
TARGET = float(args[1])  # screen pixels per node unit
TARGETS = [a.split("=", 1) for a in args[2:]]  # [slug, "Name" or "Name|Frame"]
OVERLAP = 0.3  # fraction of a tile shared with its neighbour
CROP = 40  # pixels dropped from every tile edge (scrollbars and region arrows)
PAD = 40  # pixels of empty space kept around the result
PAD_TOP = 90  # more room above Geometry Nodes trees, for the timing badges Blender draws over nodes
MARGIN = (CROP + PAD) / TARGET  # node units the tiles cover around the tree


bpy.context.preferences.view.smooth_view = 0  # apply view changes immediately (in memory only)


def find():
    win = bpy.context.window_manager.windows[0]
    area = next(a for a in win.screen.areas if a.type == 'NODE_EDITOR')
    return win, area, next(r for r in area.regions if r.type == 'WINDOW')


def reaches(root, target):
    """True if target is root or a group used somewhere inside it."""
    try:
        find_route(root, target)
        return True
    except SystemExit:
        return False


def find_route(root, target):
    """Group nodes to enter, in order, to get from the root tree to the target group."""
    queue, seen = [(root, [])], set()
    while queue:
        tree, route = queue.pop(0)
        if tree == target:
            return route
        if tree in seen:
            continue
        seen.add(tree)
        for n in tree.nodes:
            if n.bl_idname.endswith('Group') and n.node_tree:
                queue.append((n.node_tree, route + [n]))
    raise SystemExit(f"{target.name} is not reachable from {root.name}")


def pan(dx, dy):
    """Move the view by whole screen pixels (positive dx: right, negative dy: down)."""
    win, area, region = find()
    with bpy.context.temp_override(window=win, area=area, region=region):
        bpy.ops.view2d.pan(deltax=dx, deltay=dy)


def marker():
    """Screen position of a fixed point of the tree, to check where the view really is."""
    return find()[2].view2d.view_to_region(0, 0, clip=False)


def settle(expected):
    """Re-pan until the view is where it should be (Blender can overshoot a pan)."""
    for _ in range(4):
        yield 0.4
        x, y = marker()
        if abs(x - expected[0]) <= 1 and abs(y - expected[1]) <= 1:
            return
        pan(x - expected[0], y - expected[1])
    print("warning: view is not where expected", flush=True)


def fit_view(tree, cx, cy, half_w, half_h):
    """Zoom the node editor so the given window (node units) fills the region.

    Places two temporary reroutes at the window corners and frames them. Blender only knows
    a new node's size after a redraw, hence the waits. Returns the reroutes for the caller to remove.
    """
    corners = [tree.nodes.new('NodeReroute') for _ in range(2)]
    corners[0].location = (cx - half_w, cy - half_h)
    corners[1].location = (cx + half_w, cy + half_h)
    yield 0.6
    for n in tree.nodes:
        n.select = n in corners
    win, area, region = find()
    with bpy.context.temp_override(window=win, area=area, region=region):
        bpy.ops.node.view_selected()
    yield 0.6
    return corners


def hide_puzzle_input():
    """Blank every String node labelled "Puzzle Input" (in memory only), so no input reaches an image."""
    for tree in bpy.data.node_groups:
        for n in tree.nodes:
            if n.bl_idname == 'FunctionNodeInputString' and "Puzzle Input" in (n.name, n.label):
                n.string = ""


def capture():
    hide_puzzle_input()
    win, area, region = find()
    if not win.screen.show_fullscreen:  # the toggle would undo a file saved already maximized
        with bpy.context.temp_override(window=win, area=area, region=region):
            bpy.ops.screen.screen_full_area(use_hide_panels=False)
        yield 1.0
    initial_object = bpy.context.view_layer.objects.active
    for slug, target in TARGETS:
        name, _, frame = target.partition("|")
        yield from capture_one(os.path.join(OUT, slug), name, frame or None, initial_object)
        print(f"captured {slug}", flush=True)
    print("done", flush=True)
    os._exit(0)


def capture_one(out, name, frame, initial_object):
    tree = bpy.data.node_groups.get(name)
    material = None if tree else bpy.data.materials[name]
    tree = tree or material.node_tree
    bpy.context.view_layer.objects.active = initial_object
    if tree.bl_idname == 'GeometryNodeTree':  # several objects can each have their own tree (day 6)
        for obj in bpy.data.objects:
            mod = next((m for m in obj.modifiers if m.type == 'NODES' and m.node_group and reaches(m.node_group, tree)), None)
            if mod:
                bpy.context.view_layer.objects.active = obj
                obj.modifiers.active = mod
                yield 1.0
                break
    if material:  # the shader editor shows the active material of the active object
        obj = next(o for o in bpy.data.objects if material.name in [sl.material.name for sl in o.material_slots if sl.material])
        bpy.context.view_layer.objects.active = obj
        obj.active_material_index = [sl.material for sl in obj.material_slots].index(material)
        yield 1.0  # the editor follows the active material after a redraw
    win, area, region = find()
    if area.ui_type != tree.bl_idname:
        area.ui_type = tree.bl_idname
        yield 1.0
    win, area, region = find()
    space = area.spaces.active
    if material:
        space.shader_type = 'OBJECT'
    for region_name in ("show_region_toolbar", "show_region_ui", "show_region_header"):
        setattr(space, region_name, False)
    space.overlay.show_context_path = False
    if tree.bl_idname == 'GeometryNodeTree':  # groups are entered from the tree the file opens on
        route = find_route(space.path[0].node_tree, tree)
        while len(space.path) > 1:
            win, area, region = find()
            with bpy.context.temp_override(window=win, area=area, region=region):
                bpy.ops.node.tree_path_parent()
        for group_node in route:
            for n in space.edit_tree.nodes:
                n.select = n == group_node
            space.edit_tree.nodes.active = group_node
            win, area, region = find()
            with bpy.context.temp_override(window=win, area=area, region=region):
                bpy.ops.node.group_edit(exit=False)
    assert space.edit_tree == tree, f"could not open {name}"
    yield 1.5

    ui = bpy.context.preferences.system.ui_scale
    xs, ys = [], []
    for n in tree.nodes:
        if frame and frame.startswith("@"):  # a single node, by name
            if n.name != frame[1:]:
                continue
        elif frame and not (n.bl_idname == 'NodeFrame' and frame in (n.name, n.label)):  # reroutes can share a label
            continue
        x, y = n.location_absolute
        xs += [x, x + n.dimensions.x / ui]
        ys += [y, y - n.dimensions.y / ui]
    tight = min(xs), max(xs), min(ys), max(ys)  # left, right, bottom, top
    pad_top = PAD_TOP if tree.bl_idname == 'GeometryNodeTree' and (not frame or frame.startswith("@")) else PAD  # a frame holds its badges
    left, right = tight[0] - MARGIN, tight[1] + MARGIN
    bottom, top = tight[2] - MARGIN, tight[3] + (CROP + pad_top) / TARGET
    region = find()[2]
    rw, rh = region.width, region.height
    half_w, half_h = rw / TARGET / 2, rh / TARGET / 2

    # Calibrate: the editor frames a window with some padding, so measure the zoom it really
    # settles on and rescale the window until it matches the target.
    center = (left + right) / 2, (bottom + top) / 2
    for attempt in range(4):
        corners = yield from fit_view(tree, *center, half_w, half_h)
        v = find()[2].view2d
        p0, p1 = v.view_to_region(0, 0, clip=False), v.view_to_region(100, 0, clip=False)
        zoom = (p1[0] - p0[0]) / 100 * ui  # pixels per node unit (view space is node space times UI scale)
        for n in corners:
            tree.nodes.remove(n)
        if abs(zoom / TARGET - 1) < 0.01 or attempt == 3:
            break
        half_w *= zoom / TARGET
        half_h = half_w * rh / rw

    # Tiles are whole pixels apart, so overlaps match exactly.
    step_x, step_y = round(rw * (1 - OVERLAP)), round(rh * (1 - OVERLAP))
    view_w, view_h = rw / zoom, rh / zoom
    nx = max(1, math.ceil((right - left - view_w) * zoom / step_x) + 1)
    ny = max(1, math.ceil((top - bottom - view_h) * zoom / step_y) + 1)
    print(f"zoom {zoom:.3f} px/unit, grid {nx}x{ny}", flush=True)

    # Frame the top-left tile once; every other tile is a pixel pan away.
    cx = left + view_w / 2 if nx > 1 else (left + right) / 2
    cy = top - view_h / 2 if ny > 1 else (bottom + top) / 2
    corners = yield from fit_view(tree, cx, cy, half_w, half_h)
    for n in corners:
        tree.nodes.remove(n)
    yield 0.5

    # Where the tree sits in the top-left tile, so the stitched image can be cropped to it.
    v = find()[2].view2d
    x0, y0 = v.view_to_region((tight[0] - PAD / zoom) * ui, (tight[3] + pad_top / zoom) * ui, clip=False)
    x1, y1 = v.view_to_region((tight[1] + PAD / zoom) * ui, (tight[2] - PAD / zoom) * ui, clip=False)
    box = [math.floor(x0), math.floor(rh - y0), math.ceil(x1), math.ceil(rh - y1)]

    os.makedirs(out, exist_ok=True)
    tiles = []
    start = marker()  # tile (0, 0)
    for j in range(ny):
        for i in range(nx):
            tile = f"tile_r{j}_c{i}.png"
            win, area, region = find()
            with bpy.context.temp_override(window=win, area=area, region=region):
                bpy.ops.screen.screenshot_area(filepath=os.path.join(out, tile))
            yield 0.8
            tiles.append({"file": tile, "x": i * step_x, "y": j * step_y})
            if i < nx - 1:
                pan(step_x, 0)
                yield from settle((start[0] - (i + 1) * step_x, start[1] + j * step_y))
        if j < ny - 1:
            pan(-(nx - 1) * step_x, -step_y)
            yield from settle((start[0], start[1] + (j + 1) * step_y))
    json.dump({"crop": CROP, "box": box, "tiles": tiles}, open(os.path.join(out, "layout.json"), "w"), indent=1)


gen = capture()


def tick():
    try:
        return next(gen)
    except StopIteration:
        return None
    except BaseException:
        import traceback
        traceback.print_exc()
        os._exit(1)


bpy.app.timers.register(tick, first_interval=3.0)
