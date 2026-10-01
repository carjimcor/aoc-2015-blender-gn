# Project conventions

Advent of Code 2015 solutions built with Blender Geometry Nodes (GN). Repository: https://github.com/carjimcor/aoc-2015-blender-gn.

## Writing style

- Keep every file short, simple and professional. English only (files, commits, PRs), even if the chat is in Spanish.
- No emojis, no badges, no filler.

## Private and local details

This repository is public. Never put machine-specific or personal details in tracked files: local paths, user names, operating system or tool setup, accounts, email addresses. They live in `CLAUDE.local.md`, which is git-ignored and loaded automatically next to this file. Use generic placeholders in commands (`blender`, `<tmp_dir>`) and look up the real values there.

## Layout

- `README.md`: overview, how to use, a note that puzzle text and inputs are not included (Advent of Code FAQ), AI use note. No license or conventions sections.
- `LICENSE`: official CC BY 4.0 text, unmodified. Never write it from memory; download it from creativecommons.org.
- `days/dayXX/`: one folder per day, `XX` zero-padded.
  - `aoc-2015-XX.blend`
  - `README.md`
  - `media/`: GIF and screenshots, kebab-case names (`main-tree.png`, `material-floor.png`).
- `fonts/`: every font a `.blend` uses, once, with its license (see Fonts).
- Day titles and links: `https://adventofcode.com/2015/day/N`. Day 1 is the model for a finished day README.

## Puzzle input and puzzle text

- Never commit puzzle inputs or puzzle text. `.gitignore` covers `input*.txt` and `inputs/`.
- The puzzle input goes in a String node labelled "Puzzle Input" somewhere in the tree (a String node accepts multi-line paste; a group input socket does not). It must be empty in every committed `.blend`. The user checks this. Node trees are always the user's own work: edit a `.blend` only for a file-level fix the user asks for (such as a font path), changing as few bytes as possible, then load it with `blender -b` to verify.
- The user may re-save a `.blend` at any time. Review `git status` and the diff before staging, and do not use `git add -A` blindly.
- The user may leave a `todo.txt` with instructions in a day folder. It is git-ignored and can hold puzzle text and answers: follow it, copy nothing from the puzzle text, and delete it when done.
- Media may show the user's own answers. That is fine, but mention it when adding it.

## Day README

1. Title and puzzle link, then a one-sentence summary of each part in your own words (`**Part 1:**`, `**Part 2:**`). Part 2 is only visible on the site after solving part 1, so the README is where readers learn it. Never copy the puzzle text, its story, examples or answers. Then a short note from the user about the solution (ask if unsure).
2. The GIF, centered with HTML and a fixed width (`<p align="center"><img src="media/animation.gif" alt="..." width="480"></p>`, or `animation.webp`).
3. Sections in order: Solution (main tree, then each group), Visualization (overview, one image per frame), Materials (a `###` heading with the name above each material), Compositor. Skip what does not exist. Images come from `media/`.
4. Blender 5.2 is the default. If a day needs another version, say so in that day's README.

## Media

- Upload an animation, not the MP4: GitHub does not play relative MP4 links. The user may send an MP4; keep it outside the repo and commit only `media/animation.gif`, or `media/animation.webp` when a GIF's 256 colours show artifacts (renders with many colours or shading, like day 2).
- Convert with `python .claude/scripts/mp4_to_gif.py in.mp4 out.gif|out.webp [width] [fps]`. Defaults are 480 px wide and 20 fps. Any source rate works (60 or 24 fps in, 20 or 24 fps out), and the 10 s duration stays exact. The script uses one palette and no dithering. A 10 s clip is about 0.8 MB. Keep GIFs under a few MB.
- Node tree screenshots are captured automatically (next section). If the user sends screenshots instead, join them with `python .claude/scripts/stitch_images.py out.png img1.png img2.png ...`. It works for any number of images, in any order, horizontally or vertically. They must share one zoom and overlap; an image with no node content cannot be placed.
- Do not use Git LFS. Files are small, and "Download ZIP" on GitHub does not include LFS files.
- GitHub rejects files over 100 MB and warns over 50 MB.

## Capturing node trees

`capture_node_tree.py` drives Blender's own UI, so no manual screenshots are needed. It needs Blender 5.2 or newer; the executable path is in `CLAUDE.local.md`.

```
blender file.blend --python .claude/scripts/capture_node_tree.py -- <tmp_dir> 1.0 "main-tree=Day 1" "arrows=Day 1 Visualization|Arrows" "material-floor=Floor"
python .claude/scripts/stitch_images.py --dir <tmp_dir> days/dayXX/media
```

- One run captures every target, so Blender opens once (about 10 s per target). Each target is `slug=Name` or `slug=Name|Frame`, and the slug becomes the image file name.
- Name can be a Geometry Nodes group, the compositor group or a material. Frame is the name or label of a Frame node and captures only that part.
- For a day, capture every group, the compositor and every material it uses, plus one image per top-level frame of a big group. List them with a quick Blender script (`bpy.data.node_groups`, `bpy.data.materials`).
- Use a scratch folder for `<tmp_dir>`, never the repo. The script never saves, so it can run on the `.blend` in place, or on a copy whose font path still resolves. Run it in the foreground and wait for it to exit.
- The second argument is the zoom in screen pixels per node unit. Use 1.0 for every image of a day, so all are readable and share one scale. Lower it (about 0.5) only for an overview.
- Tiles use the editor size, so a bigger Blender window means fewer tiles. They are whole pixels apart, `layout.json` places them exactly, and the stitched image is cropped to the tree with a border (extra room above Geometry Nodes trees for the timing badges).
- Wide images are scaled down when shown inline on GitHub. They are sharp when opened, so split a very wide tree by frame if it must be readable inline.
- The script blanks the "Puzzle Input" String node in memory, so the input never reaches an image, and keeps an editor the file was saved with maximized. The stitcher re-checks every tile against its neighbours, because Blender can land a pan a pixel or two off near the edge of the tree.
- How it works: Blender only sizes new nodes after a redraw, so the script waits between steps. It frames the tree with two temporary reroutes, then pans with `view2d.pan` (whole pixels) and saves each tile with `screen.screenshot_area`. The temporary nodes exist only in memory, and editor regions and the context path overlay are hidden.

## Fonts

- `fonts/` at the repo root holds each font once, even when several days use it, next to its license as `fonts/<Family>-LICENSE.txt`.
- A `.blend` points to the font with a relative path (`//../../fonts/<File>.ttf` from `days/dayXX/`). The user sets this in Blender, or asks for a minimal path patch.
- Each day README lists the fonts it uses, with a link to the license, for example: `Fonts: IBM Plex Mono, SIL Open Font License 1.1 ([license](../../fonts/IBMPlexMono-LICENSE.txt)).`
- Before adding a font, check its license. The SIL Open Font License allows redistribution with the license text included (IBM Plex: https://github.com/IBM/plex). Never write a license from memory; copy the official text.

## Git and pull requests

- Never push to `main`. One branch per PR, branched from an up-to-date `main`. Unrelated changes go in separate PRs.
- One commit per PR. To change it, `git commit --amend` and `git push --force-with-lease`.
- End commit messages with the `Co-Authored-By` line and PR descriptions with the "Generated with Claude Code" line given by the session.
- PR description: short, with the list of files. Reply with the PR URL.
- The user reviews and merges. When asked to show changes first, do not push.
- Update the PR description when the files change.

## AI use

The README says AI is used for administrative work and git, and that the Blender files and GN are made by hand. Keep it accurate: do not present generated work as the user's node trees.

## Environment

- Python helpers need `pip install av pillow numpy`. Install to a temporary folder (`pip install --target <dir> ...`, then set `PYTHONPATH`) to keep the machine clean.
- A `.blend` stores no save times, user names or absolute paths. File times exist only on disk, not in git.
