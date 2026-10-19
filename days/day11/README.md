# Day 11: Corporate Policy

https://adventofcode.com/2015/day/11

**Part 1:** the input is a password of eight lowercase letters; increase it like a number in base 26 (a to z, carrying to the left) until it has an increasing straight of three letters, no i, o or l, and two different pairs of equal letters, and find that password.

**Part 2:** find the next valid password after that one.

There is no visualization for this day. Each letter is a point, and a repeat zone moves to the next password and checks the rules until one passes. Next Password finds the letters to increase with an Accumulate Field: the last letter, and every letter followed only by z's. A password with an i, o or l jumps straight past every password that still has that letter.

The thumbnail of this day was made with AI: a frame of a test visualization that is not part of this repository. That is all its AI badge means; the node trees are made by hand.

## Notes

- Paste the input into the "Puzzle Input" node. The number of iterations starts at 1000 so the file opens quickly: press Bake in the Bake node (Still) first, so the tree stops recomputing on every change, then raise it (about a million for my input) and bake again. The repeat zone keeps the first valid password, so it takes a while.
- The answer is in the Viewer. For part 2, paste the part 1 answer as the input and bake again.

## Solution

### Day 11

The main tree turns the input into one point per letter, with its position in the alphabet in `letter`, and runs the repeat zone: Next Password, then Is Valid, until a password is valid. Points to Password turns the points back into text.

![Day 11 main tree](media/main-tree.png)

### Next Password

Adds one to the last letter and to every letter followed only by z's, wrapping z around to a.

![Next Password group](media/next-password.png)

### Is Valid

Checks the three rules, one frame each, and also returns the next password without forbidden letters: the first i, o or l becomes the next letter and everything after it becomes a.

![Is Valid group](media/is-valid.png)

### Points to Password

Joins the letters of the points into a string.

![Points to Password group](media/points-to-password.png)

### Char to ID

Turns a letter into its position in the alphabet.

![Char to ID group](media/char-to-id.png)

### ID to Char

Turns a position in the alphabet back into its letter.

![ID to Char group](media/id-to-char.png)

### Lower Case Alphabet

The alphabet that Char to ID and ID to Char use.

![Lower Case Alphabet group](media/lower-case-alphabet.png)
