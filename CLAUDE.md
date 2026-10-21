# Project conventions

Advent of Code 2015 solutions built with Blender Geometry Nodes (GN). Repository: https://github.com/carjimcor/aoc-2015-blender-gn.

## Writing style

- Keep every file short, simple and professional. English only (files, commits, PRs), even if the chat is in Spanish.
- No emojis, no shield badges, no filler.

## Private and local details

This repository is public. Never put machine-specific or personal details in tracked files: local paths, user names, operating system or tool setup, accounts, email addresses. They live in `CLAUDE.local.md`, which is git-ignored and loaded automatically next to this file. Use generic placeholders in commands (`blender`, `<tmp_dir>`) and look up the real values there.

## Layout

- `README.md`: overview, a Days grid (see Media), how to use, a note that puzzle text and inputs are not included (Advent of Code FAQ), AI use note. No license or conventions sections.
- `LICENSE`: official CC BY 4.0 text, unmodified. Never write it from memory; download it from creativecommons.org.
- `days/dayXX/`: one folder per day, `XX` zero-padded.
  - `aoc-2015-XX.blend`, plus `aoc-2015-XX-viz.blend` when the visualization lives in its own file (day 5)
  - `README.md`
  - `media/`: GIF and screenshots, kebab-case names (`main-tree.png`, `material-floor.png`).
- `fonts/`: every font a `.blend` uses, once, with its license (see Fonts).
- A big self-contained part of a day (day 4: MD5) gets its own page next to the README (`MD5.md`), linked both ways, with its images in `media/<name>/`.
- Day titles and links: `https://adventofcode.com/2015/day/N`. Day 1 is the model for a finished day README.

## Puzzle input and puzzle text

- Never commit puzzle inputs or puzzle text. `.gitignore` covers `input*.txt` and `inputs/`.
- The puzzle input goes in a String node labelled "Puzzle Input" somewhere in the tree (a String node accepts multi-line paste; a group input socket does not). It must be empty in every committed `.blend`. The user checks this. Node trees are always the user's own work: edit a `.blend` only for a file-level fix the user asks for (such as a font path), changing as few bytes as possible, then load it with `blender -b` to verify.
- Check hidden values too: a socket that is linked keeps the last value typed into it, invisible in the UI (day 4 had the input there). Search the decompressed `.blend` for the input and the answers, and show the user where anything is.
- A Bake node can pack its result inside the `.blend` (day 7), and that data can hold the input or the answers. Bakes must be empty in a committed file.
- The user may re-save a `.blend` at any time. Review `git status` and the diff before staging, and do not use `git add -A` blindly.
- The user may leave a `todo.txt` with instructions in a day folder. It is git-ignored and can hold puzzle text and answers: follow it, copy nothing from the puzzle text, and delete it when done.
- Media may show the user's own answers. That is fine, but mention it when adding it.
- If an animation shows parts of the input (day 5 scrolls through every string), tell the user before adding it and let them decide. On day 5 they accepted it, since a thousand strings pass in 10 seconds, and on day 10, where the short input is the start of the sequence.

## Day README

1. Title and puzzle link, then a one-sentence summary of each part in your own words (`**Part 1:**`, `**Part 2:**`). Part 2 is only visible on the site after solving part 1, so the README is where readers learn it. Never copy the puzzle text, its story, examples or answers. Then a short note from the user about the solution (ask if unsure).
2. The animation, centered with HTML and a fixed width (`<p align="center"><img src="media/animation.gif" alt="..." width="480"></p>`, or `animation.webp`). Several animations (day 3) are named `animation-<name>.webp` and stacked, each in its own centered paragraph at the same `width="480"` with a caption below the image (`<br>` then `<em>Part 1</em>`).
3. A Notes list when the file needs explaining: which inputs to change, baking before playing, camera tweaks, what the visualization shows beyond the puzzle.
4. Sections in order: Solution (main tree, then each group), Visualization (overview and its groups, no image per animation frame), Materials (a `###` heading with the name above each material), Compositor. Skip what does not exist. Images come from `media/`.
   Above every node tree image goes a `###` heading with the tree's exact name in the `.blend` (the main tree's too: `### Day 1`, not "Main tree"), then a sentence about it, then the image. When one sentence covers several trees, each later tree gets its heading right above its image. A frame of a big tree has a heading with the frame's name. This applies to every page with tree images, `MD5.md` included.
5. Blender 5.2 is the default. If a day needs another version, say so in that day's README.

## Media

- Upload an animation, not the MP4: GitHub does not play relative MP4 links. The user may send an MP4; keep it outside the repo and commit only `media/animation.gif`, or `media/animation.webp` when a GIF's 256 colours show artifacts (renders with many colours or shading, like day 2).
- Every day has `media/thumbnail.webp` for the Days grid in the root README: `python .claude/scripts/make_thumbnail.py <day> days/dayXX/media/thumbnail.webp [video.mp4] [webp_quality]` (quality 40 for busy clips such as day 5, to stay near 1 MB). With a video it is the animation (240x320) with a "Day 01" label below, in IBM Plex Mono from `fonts/`. A day without animation uses a still image the user picks, usually a node capture; its editor background becomes the dark blue of the day 1 render. Without either it is a plain placeholder of the same size. A day with several animations uses its main one (day 3: part 2). When a day is finished, replace its placeholder.
- The Days grid is a centered paragraph of images, 5 per line (`<p align="center">` with `<img ... width="19%">`), not a table: GitHub always draws table borders and sizes columns by content. Finished days are wrapped in a link to their folder; placeholders are not.
- Convert with `python .claude/scripts/mp4_to_gif.py in.mp4 out.gif|out.webp [width] [fps] [webp_quality] [slow]`. `slow` plays part of the clip at another speed: `30-570x0.5` plays source frames 30 to 570 at half speed (day 7). Busy clips such as scrolling text get large; WebP quality 50 keeps them readable at about half the size (day 5). Defaults are 480 px wide and 20 fps. Any source rate works (60 or 24 fps in, 20 or 24 fps out), and the 10 s duration stays exact. The script uses one palette and no dithering. A 10 s clip is about 0.8 MB. Keep GIFs under a few MB.
- Node tree images are captured with nodefmt (next section). If the user captures a tree by hand, they use the Capture Tree button of the nodefmt add-on, which saves the whole tree as one image.
- Thumbnails carry round badges in their top corners: `noviz` (crossed-out eye, top left) for a day without a visualization in Blender (days 4, 8, 9, 11, 12 and 13), `ai` (top right) for a day with a node group or image made with AI (days 9 and 13; day 11 only for its thumbnail, a frame of an AI test visualization that is not in the repository; day 12 for its visualization idea image and thumbnail). Add them last, once, to a fresh thumbnail: `python .claude/scripts/add_badges.py thumbnail.webp out.webp noviz ai`. The root README explains them under the Days grid.
- A day without a visualization may show an idea for one, drawn with Python and made-up data (`media/visualization-idea.png`, day 9), never the puzzle input. Say in the README that it was made with AI outside Blender. The image goes at the top of the README and again at the end, in the Visualization idea section that explains it. Several images of the idea (day 13: the worst and the best plan) go in that section, and the main one also at the top. The idea can also be an animation made the same way (day 13: `visualization-idea.webp`, also its thumbnail).
- Do not use Git LFS. Files are small, and "Download ZIP" on GitHub does not include LFS files.
- GitHub rejects files over 100 MB and warns over 50 MB.

## Capturing node trees

Node tree images come from the Capture Tree tool of [blender-nodefmt](https://github.com/carjimcor/blender-nodefmt), from its command line. Use `nodefmt_cli.py` from the latest `main` of blender-nodefmt (export it with `git archive` to a scratch folder; the local clone may be on another branch). Blender runs with its window and the user's own profile, so the UI scale is theirs (also in `CLAUDE.local.md`). The executable path is in `CLAUDE.local.md`.

```
blender days/dayXX/aoc-2015-XX.blend --python nodefmt_cli.py -- --check
blender days/dayXX/aoc-2015-XX.blend --python nodefmt_cli.py -- --capture "Day 1" --out days/dayXX/media/main-tree.png --zoom 1.0
```

- The user sorts every tree with nodefmt, latest release, with the settings in `nodefmt.toml` at the repo root (every rule on, including opt-in and new ones, and the UI scale). Before capturing, only check, from inside the repo so it finds `nodefmt.toml`. Never `--fix` the user's file, and never check or sort with other settings: the CLI defaults leave opt-in rules off and report sorted trees as unsorted. If the check fails, tell the user.
- Capture does not hide the puzzle input: check that the "Puzzle Input" node is empty first (it must be empty in every committed file anyway).
- One Blender run per tree. TREE is a Geometry Nodes group, the compositor group, or `Material: <name>`. The capture never saves the file, so it can run on the `.blend` in place.
- For a day, capture every group, the compositor and every material it uses, named in kebab-case (`main-tree.png`, `material-floor.png`). List them with a quick Blender script (`bpy.data.node_groups`, `bpy.data.materials`).
- Use zoom 1.0 for every image of a day, so all are readable and share one scale.
- Wide images are scaled down when shown inline on GitHub. They are sharp when opened.

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

The README says AI is used for administrative work and git, and that the Blender files and GN are made by hand. Keep it accurate: do not present generated work as the user's node trees. A node group made with AI has a name ending in "(AI)" (day 9: Permutations (AI)); the day's README says so where it describes the group, and the thumbnail gets the `ai` badge.

## Environment

- Python helpers need `pip install av pillow numpy`. Install to a temporary folder (`pip install --target <dir> ...`, then set `PYTHONPATH`) to keep the machine clean.
- A `.blend` stores no save times, but it can store absolute paths with the user name: the file browser of the Shading workspace keeps its last folder in a fixed-size buffer. The user accepts these paths in the committed files. File times exist only on disk, not in git.
