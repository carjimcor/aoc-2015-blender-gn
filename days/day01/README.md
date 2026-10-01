# Day 1: Not Quite Lisp

https://adventofcode.com/2015/day/1

**Part 1:** follow a string of `(` (up one floor) and `)` (down one floor) from floor 0 and find the final floor.

**Part 2:** find the position of the first character that takes you below floor 0.

I was not sure how to represent this problem visually, so I made a panel like an elevator display. Each part fills in once its value is known.

<p align="center">
  <img src="media/animation.gif" alt="Day 1 animation" width="480">
</p>

Fonts: IBM Plex Mono, SIL Open Font License 1.1 ([license](../../fonts/IBMPlexMono-LICENSE.txt)).

## Solution

The main tree reads the instructions, runs them and sends the result to the visualization.

![Main tree](media/main-tree.png)

The Process Instructions group walks through the string one character at a time.

![Process Instructions group](media/process-instructions.png)

The A / B group builds the "Processed / Total" text.

![A / B group](media/a-b.png)

## Visualization

![Day 1 Visualization group](media/visualization.png)

### P1 / P2

![P1 / P2 frame](media/visualization-p1-p2.png)

### Arrows

![Arrows frame](media/visualization-arrows.png)

### Floor

![Floor frame](media/visualization-floor.png)

### Progress Bar

![Progress Bar frame](media/visualization-progress-bar.png)

## Materials

### P1 / P2

![P1 / P2 material](media/material-p1-p2.png)

### Arrows

![Arrows material](media/material-arrows.png)

### Progress Bar

![Progress Bar material](media/material-progress-bar.png)

### Floor

![Floor material](media/material-floor.png)

## Compositor

![Compositor nodes](media/compositor.png)
