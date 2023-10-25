def solution(x, y):
    t = x + y - 1
    max_diag = (t * t + t) / 2
    return str(int(max_diag - (t - x)))


print(solution([[1, 2],[4, 3]], [[3, 7],[4, 5]]))
