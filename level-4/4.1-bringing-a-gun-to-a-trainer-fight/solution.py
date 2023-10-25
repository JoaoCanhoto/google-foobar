import math
import numpy as np


def solution(dimensions, your_position, trainer_position, distance):
    # gives the max number of possible reflections , given the distance and the geometry
    def get_max_relfections(dimensions, distance):
        return int(math.ceil(distance / float(min(dimensions))))

    # get the reflected point, for a given dimension, given a specific reflection coordinate refl_lvl
    def get_reflected_pos(dimensions, pt, refl_lvl):
        x = dimensions[0] * refl_lvl[0] + (
            dimensions[0] - pt[0] if refl_lvl[0] % 2 else pt[0]
        )
        y = dimensions[1] * refl_lvl[1] + (
            dimensions[1] - pt[1] if refl_lvl[1] % 2 else pt[1]
        )
        return [x, y]

    def get_distance(p1, p2):
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    def get_gcd(x, y):
        while y:
            x, y = y, x % y
        return abs(x)

    # return the actual  base direction vector (divided by gcd
    # you could use tangent (could be cosine, or sin), but might have problems with the numeric precision
    # and would have needed to return the quadrant as well
    def get_direction(p1, p2):
        v_x = p2[0] - p1[0]
        v_y = p2[1] - p1[1]
        gcd = get_gcd(v_x, v_y)
        gcd = 1 if gcd == 0 else gcd
        return [int(v_x / gcd), int(v_y / gcd)]

    # we should do is_trainer=1 for trainer direction and is_trainer=-1 for my directions
    def append_direction_with_dist(dir_pt, matrix, d, is_trainer=1):
        x_pos = dir_pt[0] + x_dir_shift
        y_pos = dir_pt[1] + y_dir_shift
        dist_0 = matrix[x_pos, y_pos]
        matrix[x_pos, y_pos] = (
            (is_trainer * d) if (dist_0 == 0) or (abs(dist_0) > d) else dist_0
        )

    if your_position == trainer_position:
        return 0

    if get_distance(your_position, trainer_position) > distance:
        return 0

    # set a matrix to define the distances vs directions
    max_reflections = get_max_relfections(dimensions, distance)
    shape = (
        (2 * max_reflections + 1) * dimensions[0],
        (2 * max_reflections + 1) * dimensions[1],
    )
    matrix_pos_trainer = np.zeros(shape)
    # do a shift in from the negative points to use the direction as indexes of the matrix
    x_dir_shift = max_reflections * dimensions[0] + your_position[0]
    y_dir_shift = max_reflections * dimensions[1] + your_position[1]

    # loop over the reflection boxes
    for i in range(-max_reflections, max_reflections + 1, 1):
        for j in range(-max_reflections, max_reflections + 1, 1):
            refl_lvl = [i, j]
            # do for the trainer reflected position
            refct_trainer = get_reflected_pos(dimensions, trainer_position, refl_lvl)
            dist_trainer = get_distance(your_position, refct_trainer)
            if dist_trainer < distance:
                dir_trainer = get_direction(your_position, refct_trainer)
                append_direction_with_dist(
                    dir_trainer, matrix_pos_trainer, dist_trainer
                )

            # do for my reflected position
            refct_my_pos = get_reflected_pos(dimensions, your_position, refl_lvl)
            dist_my_refct = get_distance(your_position, refct_my_pos)
            if dist_my_refct < distance:
                dir_my_refct = get_direction(your_position, refct_my_pos)
                append_direction_with_dist(
                    dir_my_refct, matrix_pos_trainer, dist_my_refct, is_trainer=-1
                )

    # get the direction which didn't target me before the trainer
    matrix_pos_trainer = matrix_pos_trainer > 0
    count_shots = int(matrix_pos_trainer.sum())

    # for the case with only direct shot
    if (count_shots == 0) and (
        get_distance(your_position, trainer_position) <= distance
    ):
        return 1

    return count_shots


print("\n\n###################################################################")
print("\n\n----------------- TEST 1")
print(
    "solution of solution([3, 2], [1, 1], [2, 1], 4): ",
    solution([3, 2], [1, 1], [2, 1], 4),
)
print("      expected: ", 7)


print("\n\n----------------- TEST 2")
print(
    "solution of solution([300, 275], [150, 150], [185, 100], 500): ",
    solution([300, 275], [150, 150], [185, 100], 500),
)
print("      expected: ", 9)

print("\n\n----------------- TEST 3")
print(
    "solution of solution([30, 20], [10, 10], [20, 10], 5): ",
    solution([40, 40], [10, 10], [20, 30], 60),
)
print("      expected: ", 7)

print("\n\n----------------- TEST 4")
print(
    "solution of solution([30, 20], [10, 10], [20, 10], 5): ",
    solution([30, 20], [10, 10], [20, 10], 5),
)
print("      expected: ", 0)

print("\n\n----------------- TEST 5")
print(
    "solution of solution([30, 20], [10, 10], [20, 10], 11): ",
    solution([30, 20], [10, 10], [20, 10], 11),
)
print("      expected: ", 1)
print("\n\n----------------- TEST 5.1")
print(
    "solution of solution([30, 20], [5, 10], [26, 10], 21): ",
    solution([30, 20], [5, 10], [26, 10], 21),
)
print("      expected: ", 1)

print("\n\n----------------- TEST 6")
print(
    "solution of solution([2,5], [1,2], [1,4], 8): ",
    solution([2, 5], [1, 2], [1, 4], 8),
)
print("      expected: ", 15)

print("\n\n----------------- TEST 7")
print(
    "solution of solution([2,5], [1,2], [1,4], 9): ",
    solution([2, 5], [1, 2], [1, 4], 9),
)
print("      expected: ", 19)

print("\n\n----------------- TEST 8")
print(
    "solution of solution([2,5], [1,2], [1,4], 11): ",
    solution([2, 5], [1, 2], [1, 4], 11),
)
print("      expected: ", 27)

print("\n\n----------------- TEST 9")
print(
    "solution of solution([23,10], [6,4], [3,2], 23): ",
    solution([23, 10], [6, 4], [3, 2], 23),
)
print("      expected: ", 8)

print("\n\n----------------- TEST 710")
print(
    "solution of solution([23,10], [6,4], [3,2], 23): ",
    solution([10, 10], [4, 4], [6, 6], 50),
)
print("      expected: ", 65)

import time

start = time.time()
print("\n\n----------------- TEST Slow")
print(
    "solution of solution([23,10], [6,4], [3,2], 23): ",
    solution([10, 10], [4, 4], [3, 3], 5000),
)
print("      expected: ", 739323)
end = time.time()
print("it took", end - start)


"""
Submission: SUCCESSFUL. Completed in: 1 day, 7 hrs, 2 mins, 56 secs..
"""
