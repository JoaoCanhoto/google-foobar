"""The latest gossip in the henchman breakroom is that "LAMBCHOP" stands for "Lambda's Anti-Matter Biofuel Collision Hadron Oxidating Potentiator". You're pretty sure it runs on diesel, not biofuel, but you can at least give the commander credit for trying."""
"""
As a henchman on Commander Lambda's space station, you're expected to be resourceful, smart, and a quick thinker. It's not easy building a doomsday device and ordering the bunnies around at the same time, after all! In order to make sure that everyone is sufficiently quick-witted, Commander Lambda has installed new flooring outside the henchman dormitories. It looks like a chessboard, and every morning and evening you have to solve a new movement puzzle in order to cross the floor. That would be fine if you got to be the rook or the queen, but instead, you have to be the knight. Worse, if you take too much time solving the puzzle, you get "volunteered" as a test subject for the LAMBCHOP doomsday device!

To help yourself get to and from your bunk every day, write a function called solution(src, dest) which takes in two parameters: the source square, on which you start, and the destination square, which is where you need to land to solve the puzzle. The function should return an integer representing the smallest number of moves it will take for you to travel from the source square to the destination square using a chess knight's moves (that is, two squares in any direction immediately followed by one square perpendicular to that direction, or vice versa, in an "L" shape). Both the source and destination squares will be an integer between 0 and 63, inclusive, and are numbered like the example chessboard below:

-------------------------
| 0| 1| 2| 3| 4| 5| 6| 7|
-------------------------
| 8| 9|10|11|12|13|14|15|
-------------------------
|16|17|18|19|20|21|22|23|
-------------------------
|24|25|26|27|28|29|30|31|
-------------------------
|32|33|34|35|36|37|38|39|
-------------------------
|40|41|42|43|44|45|46|47|
-------------------------
|48|49|50|51|52|53|54|55|
-------------------------
|56|57|58|59|60|61|62|63|
-------------------------

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit Solution.java

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution(19, 36)
Output:
    1

Input:
solution.solution(0, 1)
Output:
    3

-- Java cases --
Input:
Solution.solution(19, 36)
Output:
    1

Input:
Solution.solution(0, 1)
Output:
    3
"""

import math


def solution(src, dest):
    # Your code here
    def do_moves(n_m, x, y, xf, yf):
        n_m += 1
        dx = xf - x
        dy = yf - y
        for l in [
            [math.copysign(1, dx), math.copysign(2, dy)],
            [math.copysign(2, dx), math.copysign(1, dy)],
        ]:
            x_n = x + l[0]
            y_n = y + l[1]
            if (x_n == xf) and (y_n == yf):
                return n_m
        if n_m > 4:
            return 6
        deep_m = 6
        for l in [
            [1, 2],
            [2, 1],
            [-1, 2],
            [-2, 1],
            [1, -2],
            [2, -1],
            [-1, -2],
            [-2, -1],
        ]:
            x_n = x + l[0]
            y_n = y + l[1]
            if not (x_n < 0 or x_n > 7 or y_n < 0 or y_n > 7):
                deep_m = min(do_moves(n_m, x_n, y_n, xf, yf), deep_m)
                if deep_m == n_m + 1:
                    return deep_m
        return deep_m

    if src == dest:
        return 0
    yi = int(src / 8)
    xi = src - yi * 8
    yf = int(dest / 8)
    xf = dest - yf * 8
    return int(do_moves(0, xi, yi, xf, yf))


print("\n\n----------------- TEST 1")
print("solution of 12: ", solution(19, 36))
print("      expected: ", 1)

print("\n\n----------------- TEST 2")
print("solution of 12: ", solution(0, 1))
print("      expected: ", 3)

print("\n\n----------------- TEST 3")
print("solution of 12: ", solution(0, 8))
print("      expected: ", 3)

print("\n\n----------------- TEST 4")
print("solution of 12: ", solution(19, 19))
print("      expected: ", 0)

print("\n\n----------------- TEST 5")
print("solution of 12: ", solution(0, 63))
print("      expected: ", 6)
