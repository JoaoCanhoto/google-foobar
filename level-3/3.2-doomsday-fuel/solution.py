"""
Commander Lambda has six suits, three dress uniforms, four casual outfits, and one Dress-Uniform-For-Important-Speeches-Only. You know this because you've already had to take all of them to the dry cleaner's. Twice!
"""
"""
Doomsday Fuel
=============
Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel.

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state). You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly.

For example, consider the matrix m:
[
[0,1,0,0,0,1], # s0, the initial state, goes to s1 and s5 with equal probability
[4,0,0,3,2,0], # s1 can become s0, s3, or s4, but with different probabilities
[0,0,0,0,0,0], # s2 is terminal, and unreachable (never observed in practice)
[0,0,0,0,0,0], # s3 is terminal
[0,0,0,0,0,0], # s4 is terminal
[0,0,0,0,0,0], # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases --
Input:
Solution.solution({{0, 1, 0, 0, 0, 1}, {4, 0, 0, 3, 2, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}})
Output:
    [0, 3, 2, 9, 14]

Input:
Solution.solution({{0, 2, 1, 0, 0}, {0, 0, 0, 3, 4}, {0, 0, 0, 0, 0}, {0, 0, 0, 0,0}, {0, 0, 0, 0, 0}})
Output:
    [7, 6, 8, 21]

-- Python cases --
Input:
solution.solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
Output:
    [7, 6, 8, 21]

Input:
solution.solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
Output:
    [0, 3, 2, 9, 14]
"""

"""
Python
======
Your code will run inside a Python 2.7.13 sandbox. All tests will be run by calling the solution() function.

Standard libraries are supported except for bz2, crypt, fcntl, mmap, pwd, pyexpat, select, signal, termios, thread, time, unicodedata, zipimport, zlib.

Input/output operations are not allowed.

Your solution must be under 32000 characters in length including new lines and other non-printing characters.
"""

import numpy as np
from fractions import Fraction
import copy


def calc_lcm(list_x):
    greater = max(list_x)
    while True:
        if all([greater % x == 0 for x in list_x]):
            lcm = greater
            break
        greater += 1
    return lcm


def do_matrix_inverse(m):
    size_m = len(m)
    diag = np.identity(size_m)
    for i in range(size_m):
        diag[i] = [mi / m[i][i] for mi in diag[i]]
        m[i] = [mi / m[i][i] for mi in m[i]]

        for j in range(i + 1, size_m):
            ratio = m[j][i] / m[i][i]
            m[j] = [m[j][k] - m[i][k] * ratio for k in range(0, size_m)]
            diag[j] = [diag[j][k] - diag[i][k] * ratio for k in range(0, size_m)]

    for i in range(size_m - 1, -1, -1):
        diag[i] = [mi / m[i][i] for mi in diag[i]]
        m[i] = [mi / m[i][i] for mi in m[i]]
        for j in range(i - 1, -1, -1):
            ratio = m[j][i] / m[i][i]
            m[j] = [m[j][k] - m[i][k] * ratio for k in range(0, size_m)]
            diag[j] = [diag[j][k] - diag[i][k] * ratio for k in range(0, size_m)]
    return diag


def solution(m):
    def calc_lcm(list_x):
        greater = max(list_x)
        while True:
            if all([greater % x == 0 for x in list_x]):
                lcm = greater
                break
            greater += 1
        return lcm

    # for the case with no change from state 0
    if sum(m[0]) == 0:
        return [1, 1]
    m_np = np.array(m)

    size_m = len(m_np)
    index_non_zero = [i for i in range(0, size_m) if sum(m_np[i]) != 0]
    index_zeros = [i for i in range(0, size_m) if sum(m_np[i]) == 0]

    # convert to prob
    m_np = np.array(
        [
            [float(ir) / sum(r) for ir in r] if sum(r) != 0 else [0] * size_m
            for r in m_np
        ]
    )

    if len(index_zeros) == 0:
        m_prob = m_np
        for i in range(100):
            m_prob = np.matmul(m_prob, m_np)
        m_fr = m_prob
    else:
        # calc Q
        m_q = np.array([r[index_non_zero] for r in m_np[index_non_zero]])

        # calc FR
        m_I = np.identity(len(m_q))
        m_f = np.linalg.inv(m_I - m_q)
        m_f = do_inverse(m_I - m_q)
        m_r = np.array([r[index_zeros] for r in m_np[index_non_zero]])

        m_fr = np.matmul(m_f, m_r)

    m_fr = m_fr[0, :]  # solution for state 0

    # convert to rational
    m_fr = np.array([Fraction(i).limit_denominator() for i in m_fr])

    # get The Least Common Multiple of the denominator
    lcm = np.lcm.reduce([m.denominator for m in m_fr])
    # lcm = calc_lcm([m.denominator for m in m_fr])

    # remove denominator
    m_fr_norm = m_fr * lcm
    result = [int(i) for i in m_fr_norm] + [lcm]

    return result


m_trans = np.array(
    [
        [
            0,
            1,
            0,
            0,
            0,
            1,
        ],  # s0, the initial state, goes to s1 and s5 with equal probability
        [
            4,
            0,
            0,
            3,
            2,
            0,
        ],  # s1 can become s0, s3, or s4, but with different probabilities
        [
            0,
            0,
            0,
            0,
            0,
            0,
        ],  # s2 is terminal, and unreachable (never observed in practice)
        [0, 0, 0, 0, 0, 0],  # s3 is terminal
        [0, 0, 0, 0, 0, 0],  # s4 is terminal
        [0, 0, 0, 0, 0, 0],  # s5 is terminal
    ]
)
m_trans = [
    [0, 1, 0, 0, 0, 1],
    [4, 0, 0, 3, 2, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]
print("\n\n-----------------")
print("m_trans\n", m_trans)
print("solution\n", solution(m_trans))
print("expected", [0, 3, 2, 9, 14])


m_trans = [
    [0, 2, 1, 0, 0],
    [0, 0, 0, 3, 4],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]
print("\n\n-----------------")
print("m_trans\n", m_trans)
print("solution\n", solution(m_trans))


# m_trans = [[0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0],  [0, 0, 0, 0, 0, 0]]
m_trans = [
    [1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1],
]
m_trans = [
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
]
m_trans = [
    [2 / 8, 1 / 8, 1 / 8, 1 / 8, 3 / 8],
    [2 / 14, 7 / 14, 1 / 14, 3 / 14, 1 / 14],
    [2 / 10, 1 / 10, 1 / 10, 4 / 10, 2 / 10],
    [3 / 9, 2 / 9, 2 / 9, 1 / 9, 1 / 9],
    [1 / 8, 2 / 8, 2 / 8, 2 / 8, 1 / 8],
]
m_trans = [[2]]
print("\n\n-----------------")
print("m_trans\n", m_trans)
print("solution\n", solution(m_trans))

m_trans = [
    [1, 2, 3, 0, 0, 0],
    [4, 5, 6, 0, 0, 0],
    [7, 8, 9, 1, 0, 0],
    [0, 0, 0, 0, 1, 2],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]
print("\n\n----------------- TEST 3")
print("m_trans\n", m_trans)
print("solution\n", solution(m_trans))

m_trans = [[0]]
print("\n\n----------------- TEST 4")
print("m_trans\n", m_trans)
print("solution\n", solution(m_trans))

m_trans = [
    [0, 0, 12, 0, 15, 0, 0, 0, 1, 8],
    [0, 0, 60, 0, 0, 7, 13, 0, 0, 0],
    [0, 15, 0, 8, 7, 0, 0, 1, 9, 0],
    [23, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [37, 35, 0, 0, 0, 0, 3, 21, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
print("\n\n----------------- TEST 5")
print("m_trans\n", m_trans)
print("solution\n", solution(m_trans))

m_trans = [
    [0, 7, 0, 17, 0, 1, 0, 5, 0, 2],
    [0, 0, 29, 0, 28, 0, 3, 0, 16, 0],
    [0, 3, 0, 0, 0, 1, 0, 0, 0, 0],
    [48, 0, 3, 0, 0, 0, 17, 0, 0, 0],
    [0, 6, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
print("\n\n----------------- TEST 6")
print("m_trans\n", m_trans)
print("solution\n", solution(m_trans))

m_trans = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
print("\n\n----------------- TEST 7")
print("m_trans\n", m_trans)
print("solution\n", solution(m_trans))

m_trans = [
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
print("\n\n----------------- TEST 8")
print("m_trans\n", m_trans)
print("solution\n", solution(m_trans))

m_trans = [
    [0, 86, 61, 189, 0, 18, 12, 33, 66, 39],
    [0, 0, 2, 0, 0, 1, 0, 0, 0, 0],
    [15, 187, 0, 0, 18, 23, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
print("\n\n----------------- TEST 9")
print("m_trans\n", m_trans)
print("solution\n", solution(m_trans))

m_trans = [
    [0, 0, 0, 0, 3, 5, 0, 0, 0, 2],
    [0, 0, 4, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 4, 4, 0, 0, 0, 1, 1],
    [13, 0, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 1, 8, 7, 0, 0, 0, 1, 3, 0],
    [1, 7, 0, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
print("\n\n----------------- TEST 10")
print("m_trans\n", m_trans)
print("solution\n", solution(m_trans))
