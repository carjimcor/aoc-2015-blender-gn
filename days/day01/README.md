# Day 1: Not Quite Lisp

https://adventofcode.com/2015/day/1

I was not sure how to represent this problem visually, so I made a panel like an elevator display. Each part fills in once its value is known.

<p align="center">
  <img src="media/animation.gif" alt="Day 1 animation" width="480">
</p>

Font: IBM Plex Mono, used under the SIL Open Font License 1.1 ([license](IBMPlexMono-LICENSE.txt)).

## Solution

The main tree reads the instructions, runs them and sends the result to the visualization.

![Main tree](media/main-tree.png)

The Process Instructions group walks through the string one character at a time.

![Process Instructions group](media/process-instructions.png)

## Visualization

![Day 1 Visualization group](media/visualization.png)

### Materials

![P1 / P2](media/material-p1-p2.png)

![Arrows](media/material-arrows.png)

![Progress Bar](media/material-progress-bar.png)

![Floor](media/material-floor.png)
