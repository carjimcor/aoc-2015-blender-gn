# MD5 in Geometry Nodes

Part of [Day 4](README.md).

An implementation of MD5 in Geometry Nodes, following [RFC 1321](https://www.rfc-editor.org/rfc/rfc1321). The `MD5` node group takes a string and returns its digest as 32 hexadecimal characters.

To reuse it, append the `MD5` node group from `aoc-2015-04.blend` (File > Append > NodeTree); its sub-groups come with it.

Limits, enough for this puzzle:

- One 512-bit block only, so messages of up to 55 characters.
- Digits and lowercase letters only. Ord shows an error for any other character.

Bits are handled as strings of `0` and `1`, and 32-bit words as integers, with the bitwise nodes doing the rest.

## Overview

The steps of RFC 1321, from left to right: convert the message to bits, pad it, append its length, split it into words, run the 64 operations and write the result as hex.

![MD5 group](media/md5/md5.png)

## 1. Message to bits

String to Bits turns every character into 8 bits.

![String to Bits group](media/md5/string-to-bits.png)

Ord returns the character code of a digit or a lowercase letter.

![Ord group](media/md5/ord.png)

is_digit and is_alpha tell which kind of character it is.

![is_digit group](media/md5/is-digit.png)

![is_alpha group](media/md5/is-alpha.png)

## 2. Padding and length

Append Padding Bits adds a `1` and then zeros up to 448 bits.

![Append Padding Bits group](media/md5/append-padding-bits.png)

Append Length adds the message length in bits as 64 bits, low-order byte first.

![Append Length group](media/md5/append-length.png)

## 3. Words

Block to Words splits the 512 bits into 16 words of 32 bits.

![Block to Words group](media/md5/block-to-words.png)

Bits to Word reads 32 bits as a word, low-order byte first.

![Bits to Word group](media/md5/bits-to-word.png)

## 4. Buffer

Initialize MD Buffer sets A, B, C and D to the four starting values of RFC 1321.

![Initialize MD Buffer group](media/md5/initialize-md-buffer.png)

## 5. The 64 operations

Process Block runs the 64 operations in a repeat zone and adds the starting buffer to the result.

![Process Block group](media/md5/process-block.png)

Schedule gives, for each operation, its round, which word of the message to use and how far to rotate.

![Schedule group](media/md5/schedule.png)

T holds the 64 constants, `floor(2^32 * |sin(i)|)`, hard-coded.

![T group](media/md5/t.png)

Operation picks F, G, H or I by round, adds the result, the message word and the constant to A, rotates it and adds B.

![Operation group](media/md5/operation.png)

F, G, H and I are the four bitwise functions of the rounds.

![F group](media/md5/f.png)

![G group](media/md5/g.png)

![H group](media/md5/h.png)

![I group](media/md5/i.png)

## 6. Output

Output writes A, B, C and D as hex and joins them into the digest.

![Output group](media/md5/output.png)

Word to Hex writes a word as 8 hex characters, low-order byte first.

![Word to Hex group](media/md5/word-to-hex.png)
