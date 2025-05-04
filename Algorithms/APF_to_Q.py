def adjacent_cases(matrix, i, j):
    adjacent = []
    cols = len(matrix)
    rows = len(matrix[0])

    if j > 0:
        adjacent.append((i, j - 1))
    else:
        adjacent.append(None)

    if cols - 1 > i:
        adjacent.append((i + 1, j))
    else:
        adjacent.append(None)

    if rows - 1 > j:
        adjacent.append((i, j + 1))
    else:
        adjacent.append(None)

    if i > 0:
        adjacent.append((i - 1, j))
    else:
        adjacent.append(None)

    return adjacent


def minus(matrix):
    new_matrix = []
    for row in matrix:
        new_row = [-i for i in row]
        new_matrix.append(new_row)

    return new_matrix


def create_Q_matrix(apf_matrix):
    Q = []
    temp = minus(apf_matrix)
    for i in range(len(apf_matrix)):
        row = []
        for j in range(len(apf_matrix[0])):
            Q_case = []
            for adjacent in adjacent_cases(apf_matrix, i, j):
                if adjacent is None:
                    Q_case.append(-float("inf"))
                else:
                    Q_case.append(temp[adjacent[0]][adjacent[1]])
            row.append(Q_case)
        Q.append(row)
    return Q
