import itertools


def solution(times, time_limit):
    def get_time(permutation):
        permutation = [0] + list(permutation) + [-1]
        steps = list(zip(permutation, permutation[1:]))
        total_time = 0
        for start, end in steps:
            total_time += times[start][end]
        return total_time

    # do Floyd–Warshall algorithm
    def get_fw_matrix(dist_matrix):
        n_rows = len(dist_matrix)
        for k in range(n_rows):
            for i in range(n_rows):
                for j in range(n_rows):
                    if dist_matrix[i][j] > dist_matrix[i][k] + dist_matrix[k][j]:
                        dist_matrix[i][j] = dist_matrix[i][k] + dist_matrix[k][j]
        return dist_matrix

    n_rows = len(times)
    bunnies = len(times) - 2

    # do Floyd–Warshall algorithm
    times = get_fw_matrix(times)

    # Check if there is a negative cycles (or inifinite loops)
    # ie non zeros in the diagonal, so returning all bunnies
    if any([times[i][i] != 0 for i in range(n_rows)]):
        return [i for i in range(bunnies)]

    for i in reversed(range(bunnies + 1)):
        for permutation in itertools.permutations(range(1, bunnies + 1), i):
            total_time = get_time(permutation)
            # the permutations are already ordered by lowest id
            if total_time <= time_limit:
                return sorted(list(i - 1 for i in permutation))
    return None


# If there are multiple sets of bunnies of the same size, return the set of bunnies with the lowest prisoner IDs (as indexes) in sorted order

print("\n\n###################################################################")
print("\n\n----------------- TEST 1")
# S - 0 - 1 - E
# 3 - 2 - 1 - 0
# S 0  1  2  E
times = [
    [0, 1, 1, 1, 1],  # S
    [1, 0, 1, 1, 1],  # 0
    [1, 1, 0, 1, 1],  # 1
    [1, 1, 1, 0, 1],  # 2
    [1, 1, 1, 1, 0]  # E
]
sol = solution(times, 3)
print(f"solution of solution({times}, 3): \n solution: ", sol)
print(" expected: ", [0, 1])
assert sol == [0, 1]

print("\n\n----------------- TEST 2")
# S - E - 1 - E - 2 - E
# 1 - 2 - 0 - 1 - (-1) - 0

# S 0  1  2   E
times = [[0, 2, 2, 2, -1],  # S
         [9, 0, 2, 2, -1],  # 0
         [9, 3, 0, 2, -1],  # 1
         [9, 3, 2, 0, -1],  # 2
         [9, 3, 2, 2, 0]  # E
         ]
sol = solution(times, 1)
print(f"solution of solution({times}, 3): \n solution: ", sol)
print(" expected: ", [1, 2])
assert sol == [1, 2]

[[0, 2, 2, 2, -1],
 [9, 0, 2, 2, -1],
 [9, 3, 0, 2, -1],
 [9, 3, 2, 0, -1],
 [9, 3, 2, 2, 0]]
[[0, 2, 1, 1, -1],
 [8, 0, 1, 1, -1],
 [8, 2, 0, 1, -1],
 [8, 2, 1, 0, -1],
 [9, 3, 2, 2, 0]]

print("\n\n----------------- TEST 3")
# (S-E-S)* - 0 - 1 - 2 - 3 - 4 - E
# CYCLE FOUND, RETURN ALL
# 495 - 495 - 396 - 297 - 198 - 99 - 0
# S   0   1   2   3   4   E
times = [[0, 99, 99, 99, 99, 99, -1],  # S
         [99, 0, 99, 99, 99, 99, 99],  # 0
         [99, 99, 0, 99, 99, 99, 99],  # 1
         [99, 99, 99, 0, 99, 99, 99],  # 2
         [99, 99, 99, 99, 0, 99, 99],  # 3
         [99, 99, 99, 99, 0, 0, 99],  # 4
         [0, 99, 99, 99, 99, 99, 0]  # E
         ]
sol = solution(times, 1)
print(f"solution of solution({times}, 3): \n solution: ", sol)
print(" expected: ", [0, 1, 2, 3, 4])
assert sol == [0, 1, 2, 3, 4]

print("\n\n----------------- TEST 4")
# S-2-3-0 - S-2-3-4 - S-2-3-E
# 14-13-12-10-9-8-7-4-3-2-1-0
# S 0  1  2  3  4  E
times = [[0, 9, 9, 1, 9, 9, 9],  # S
         [1, 0, 9, 9, 9, 9, 9],  # 0
         [1, 9, 0, 9, 9, 9, 9],  # 1
         [9, 9, 9, 0, 1, 9, 9],  # 2
         [9, 2, 4, 9, 0, 3, 1],  # 3
         [1, 9, 9, 9, 9, 0, 9],  # 4
         [1, 9, 9, 9, 9, 9, 0]  # E
         ]
sol = solution(times, 14)
print(f"solution of solution({times}, 14): \n solution: ", sol)
print(" expected: ", [0, 2, 3, 4])
assert sol == [0, 2, 3, 4]

print("\n\n----------------- TEST 5")
# S-1-4-3-2-0-E
# 0-2-1-(-2)-(-3)-(-1)-0
# S   0   1  2   3   4   E
times = [[0, 1, -2, 3, 2, -1, 0],  # S
         [-1, 0, -3, 2, 1, -2, -1],  # 0
         [2, 3, 0, 5, 4, 1, 2],  # 1
         [-3, -2, -5, 0, -1, -4, -3],  # 2
         [-2, -1, -4, 1, 0, -3, -2],  # 3
         [1, 2, -1, 4, 3, 0, 1],  # 4
         [0, 1, -2, 3, 2, -1, 0]  # E
         ]
sol = solution(times, 0)
print(f"solution of solution({times}, 3): \n solution: ", sol)
print(" expected: ", [0, 1, 2, 3, 4])
assert sol == [0, 1, 2, 3, 4]

print("\n\n----------------- TEST 6")
# S 0  1  E
times = [[0, 2, 2, 2],  # S
         [2, 0, 2, 2],  # 0
         [2, 2, 0, 2],  # 1
         [2, 2, 2, 0]  # E
         ]
sol = solution(times, 3)
print(f"solution of solution({times}, 3): \n solution: ", sol)
print(" expected: ", [])
assert sol == []

print("\n\n----------------- TEST 7")
# S-0-3-2-1-4-E
# 999-996-990-966-961-917
# S-0-1-4-2-3-E
# 999-996-989-984-975-930-925
# S   0   1   2   3   4   E
times = [[0, 3, 82, 91, 15, 24, 77],  # S
         [8, 0, 7, 32, 6, 33, 14],  # 0
         [66, 98, 0, 62, 59, 5, 39],  # 1
         [64, 97, 5, 0, 45, 84, 21],  # 2
         [3, 33, 81, 24, 0, 53, 5],  # 3
         [73, 93, 29, 9, 78, 0, 44],  # 4
         [70, 76, 15, 0, 43, 58, 0]  # E
         ]
sol = solution(times, 999)
print(f"solution of solution({times}, 999): \n solution: ", sol)
print(" expected: ", [0, 1, 2, 3, 4])
assert sol == [0, 1, 2, 3, 4]

print("\n\n----------------- TEST 8")
# S-1-2-0-E
# 3-8-6-4-0
# S  0   1   2   3   4  E
times = [[0, -3, -5, -4, -1, -2, 0],  # S
         [5, 0, -1, 0, 3, 2, 4],  # 0
         [7, 3, 0, 2, 5, 4, 6],  # 1
         [6, 2, 0, 0, 4, 3, 5],  # 2
         [3, -1, -3, -2, 0, 0, 2],  # 3
         [4, 0, -2, -1, 2, 0, 3],  # 4
         [2, -2, -4, -3, 0, -1, 0]  # E
         ]
sol = solution(times, 3)
print(f"solution of solution({times}, 3): \n solution: ", sol)
print(" expected: ", [0, 1, 2])
assert sol == [0, 1, 2]

print("\n\n----------------- TEST 9")
# S-4-0-2-E
# 6-8-3-(-1)-0
# S-4-2-0-E
# 6-8-2-2-0
# S  0   1   2   3   4   E
times = [[0, 1, -1, 2, -3, -2, 0],  # S
         [2, 0, 1, 4, -1, 0, 2],  # 0
         [5, 6, 0, 7, 2, 3, 5],  # 1
         [-1, 0, -2, 0, -4, -3, -1],  # 2
         [8, 9, 7, 10, 0, 6, 8],  # 3
         [4, 5, 3, 6, 1, 0, 4],  # 4
         [0, 1, -1, 2, -3, 2, 0]  # E
         ]
sol = solution(times, 6)
print(f"solution of solution({times}, 6): \n solution: ", sol)
print(" expected: ", [0, 2, 4])
assert sol == [0, 2, 4]

print("\n\n----------------- TEST 10")
# S-3-2-3-1-E
# 7-8-8-8-4-1
# S   0   1   2   3   4   E
times = [[0, 15, 19, 10, -1, 12, 4],  # S
         [7, 0, 19, 4, 19, 17, 7],  # 0
         [15, 8, 0, 14, 8, 4, 3],  # 1
         [10, 14, 6, 0, 0, 5, 9],  # 2
         [18, 8, 4, 0, 0, 12, 16],  # 3
         [0, 13, 1, -1, 12, 0, 4],  # 4
         [8, 5, 2, 11, 12, 16, 0]  # E
         ]
sol = solution(times, 7)
print(f"solution of solution({times}, 7): \n solution: ", sol)
print(" expected: ", [1, 2, 3])
assert sol == [1, 2, 3]
