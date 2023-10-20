"""
Solar Doomsday
==============

Who would've guessed? Doomsday devices take a LOT of power. Commander Lambda wants to supplement the LAMBCHOP's quantum antimatter reactor core with solar arrays, and she's tasked you with setting up the solar panels.

Due to the nature of the space station's outer paneling, all of its solar panels must be squares. Fortunately, you have one very large and flat area of solar material, a pair of industrial-strength scissors, and enough MegaCorp Solar Tape(TM) to piece together any excess panel material into more squares. For example, if you had a total area of 12 square yards of solar material, you would be able to make one 3x3 square panel (with a total area of 9). That would leave 3 square yards, so you can turn those into three 1x1 square solar panels.

Write a function answer(area) that takes as its input a single unit of measure representing the total area of solar panels you have (between 1 and 1000000 inclusive) and returns a list of the areas of the largest squares you could make out of those panels, starting with the largest squares first. So, following the example above, answer(12) would return [9, 1, 1, 1].


Languages
=========

To provide a Python solution, edit solution.py

To provide a Java solution, edit solution.java


Test cases
==========

Inputs:

(int) area = 12

Output:

(int list) [9, 1, 1, 1]

Inputs:

(int) area = 15324

Output:

(int list) [15129, 169, 25, 1]
"""

import math


def solution(area):
    # Your code here
    first_sq = math.isqrt(area)
    first_sq = first_sq * first_sq
    remain = area - first_sq
    if remain == 0:
        return [int(first_sq)]
    return [int(first_sq)] + solution(remain)

print("\n\n----------------- TEST 1")
print("solution of 12: ", solution(12))
print("      expected: ", [9, 1, 1, 1])


print("\n\n----------------- TEST 2")
print("solution of 15324: ", solution(15324))
print("         expected: ", [15129, 169, 25, 1])

