import math
import numpy as np


def solution(dimensions, your_position, trainer_position, distance):
    # create a list of reflection for a lvl, lvl=1-> [(-1,-1),(-1,0),(-1,1)...]; lvl=2->[(-2,-2),(-1,-2)..(2,-1)...]
    def create_reflections(level=1):  # return list of different possible reflections
        return [(x, y) for y in range(-level, level + 1, 1) for x in range(-level, level + 1, 1) if
                (abs(x) == level) or (abs(y) == level)]

    # gives the max number of possible reflections , given the distance and the geometry
    def get_max_relfections(dimensions, distance):
        return int(math.ceil(distance / float(min(dimensions))))

    # get the reflected point, for a given dimension, given a specific reflection coordinate refl_lvl
    def get_reflected_pos(dimensions, pt, refl_lvl):
        x = pt[0] + \
            2 * ((dimensions[0] - pt[0]) * math.ceil(refl_lvl[0] / 2.) + (pt[0]) * math.floor(refl_lvl[0] / 2.))
        y = pt[1] + \
            2 * ((dimensions[1] - pt[1]) * math.ceil(refl_lvl[1] / 2.) + (pt[1]) * math.floor(refl_lvl[1] / 2.))
        return [x, y]

    def get_distance(p1, p2):
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    def get_gcd(x, y):
        while (y):
            x, y = y, x % y
        return abs(x)

    # return the actual  base direction vector (divided by gcd
    # you could use tangent (could be cosine, or sin), but might have problems with the numeric precision
    # and would have needed to return the quadrant as well
    def get_direction(p1, p2):
        v_x = (p2[0] - p1[0])
        v_y = (p2[1] - p1[1])
        gcd = get_gcd(v_x, v_y)
        # gcd = math.gcd(v_x, v_y)
        return [int(v_x / gcd), int(v_y / gcd)] if gcd != 0 else [v_x, v_y]

    def check_dir_unavailability(dir_pt):
        return unavail_pos[dir_pt[0] + x_shift, dir_pt[1] + y_sift]

    def append_direction(dir_pt):
        unavail_pos[dir_pt[0] + x_shift, dir_pt[1] + y_sift] = 1

    if your_position == trainer_position:
        return 0

    if get_distance(your_position, trainer_position) > distance:
        return 0

    max_reflections = get_max_relfections(dimensions, distance)

    unavail_pos = np.zeros(((2 * max_reflections + 1) * dimensions[0], (2 * max_reflections + 1) * dimensions[1]))
    x_shift = max_reflections * dimensions[0]
    y_sift = max_reflections * dimensions[1]
    count_shots = 1
    for lvl in range(1, max_reflections + 1):
        list_refl = create_reflections(lvl)
        for refl in list_refl:
            refct_my_pos = get_reflected_pos(dimensions, your_position, refl)
            refct_trainer = get_reflected_pos(dimensions, trainer_position, refl)
            dist_trainer = get_distance(your_position, refct_trainer)
            if dist_trainer > distance:
                if get_distance(your_position, refct_my_pos) < distance:
                    dir_my_refct = get_direction(your_position, refct_my_pos)
                    append_direction(dir_my_refct)
                continue

            dir_my_refct = get_direction(your_position, refct_my_pos)
            dir_trainer = get_direction(your_position, refct_trainer)
            if dir_my_refct == dir_trainer:
                dist_my_refct = get_distance(your_position, refct_my_pos)
                if dist_my_refct < dist_trainer:
                    append_direction(dir_my_refct)
                    continue

            append_direction(dir_my_refct)
            if check_dir_unavailability(dir_trainer):
                continue

            append_direction(dir_trainer)
            count_shots += 1

    return count_shots


print("\n\n###################################################################")
print("\n\n----------------- TEST 1")
print("solution of solution([3, 2], [1, 1], [2, 1], 4): ", solution([3, 2], [1, 1], [2, 1], 4))
print("      expected: ", 7)
#
print("\n\n----------------- TEST 2")
print("solution of solution([300, 275], [150, 150], [185, 100], 500): ",
      solution([300, 275], [150, 150], [185, 100], 500))
print("      expected: ", 9)

print("\n\n----------------- TEST 3")
print("solution of solution([30, 20], [10, 10], [20, 10], 5): ",
      solution([40, 40], [10, 10], [20, 30], 60))
print("      expected: ", 7)

print("\n\n----------------- TEST 4")
print("solution of solution([30, 20], [10, 10], [20, 10], 5): ",
      solution([30, 20], [10, 10], [20, 10], 5))
print("      expected: ", 0)

print("\n\n----------------- TEST 5")
print("solution of solution([30, 20], [10, 10], [20, 10], 11): ",
      solution([30, 20], [10, 10], [20, 10], 11))
print("      expected: ", 1)
print("\n\n----------------- TEST 5.1")
print("solution of solution([30, 20], [5, 10], [26, 10], 21): ",
      solution([30, 20], [5, 10], [26, 10], 21))
print("      expected: ", 1)

print("\n\n----------------- TEST 6")
print("solution of solution([2,5], [1,2], [1,4], 8): ",
      solution([2, 5], [1, 2], [1, 4], 8))
print("      expected: ", 15)

print("\n\n----------------- TEST 7")
print("solution of solution([2,5], [1,2], [1,4], 9): ",
      solution([2, 5], [1, 2], [1, 4], 9))
print("      expected: ", 19)

print("\n\n----------------- TEST 8")
print("solution of solution([2,5], [1,2], [1,4], 11): ",
      solution([2, 5], [1, 2], [1, 4], 11))
print("      expected: ", 27)

print("\n\n----------------- TEST 9")
print("solution of solution([23,10], [6,4], [3,2], 23): ",
      solution([23, 10], [6, 4], [3, 2], 23))
print("      expected: ", 8)

print("\n\n----------------- TEST 710")
print("solution of solution([23,10], [6,4], [3,2], 23): ",
      solution([10, 10], [4, 4], [6, 6], 50))
print("      expected: ", 65)

import time

start = time.time()
print("\n\n----------------- TEST Slow")
print("solution of solution([23,10], [6,4], [3,2], 23): ",
      solution([10, 10], [4, 4], [3, 3], 5000))
print("      expected: ", 739323)
end = time.time()
print("it took", end - start)
