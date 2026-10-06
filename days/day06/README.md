# Day 6: Probably a Fire Hazard

https://adventofcode.com/2015/day/6

**Part 1:** a 1000 by 1000 grid of lights follows a list of instructions that turn on, turn off or toggle rectangles of lights; count the lights that end up on.

**Part 2:** each light has a brightness instead: turning on adds 1, turning off removes 1 (never below 0) and toggling adds 2; add up the total brightness.

Each part has its own visualization, on its own object: "Day 6 - Part 1" and "Day 6 - Part 2". Every light is a face of a grid, lit by its state in part 1 and by its brightness in part 2.

<p align="center">
  <img src="media/animation-part-1.webp" alt="Day 6 animation, part 1" width="480"><br>
  <em>Part 1</em>
</p>

<p align="center">
  <img src="media/animation-part-2.webp" alt="Day 6 animation, part 2" width="480"><br>
  <em>Part 2</em>
</p>

## Notes

- Show the object of the part you want and hide the other one. Paste the input into the "Puzzle Input" node of that object's tree.
- The answer is in the Viewer: the number of lights on for part 1, the total brightness for part 2.
- Each tree has Bake nodes; bake them before playing the animation.

## Solution

Each part has its own main tree. It builds the grid, stores the position of every light, then runs a repeat zone over the instructions, one per iteration. At the end, the lights that are off are removed and the result is added up.

![Main tree, part 1](media/main-tree-part-1.png)

![Main tree, part 2](media/main-tree-part-2.png)

Parse Line reads an instruction: the action (toggle, turn on or turn off) and the two corners of the rectangle.

![Parse Line group](media/parse-line.png)

Apply Action P1 turns the lights inside the rectangle on or off, or toggles them.

![Apply Action P1 group](media/apply-action-p1.png)

Apply Action P2 changes the brightness of the lights inside the rectangle, never going below 0.

![Apply Action P2 group](media/apply-action-p2.png)

## Materials

### Lights P1

![Lights P1 material](media/material-lights-p1.png)

### Lights P2

![Lights P2 material](media/material-lights-p2.png)

## Compositor

![Compositor nodes](media/compositor.png)
