from solutions.util import read_input


lines = read_input(9)

startSum = 0
endSum = 0
for line in lines:
    rows = [list(map(int, line.split()))]
    while any(x != 0 for x in rows[-1]):
        newRow = []
        for idx in range(1, len(rows[-1])):
            newRow.append(rows[-1][idx] - rows[-1][idx - 1])
        rows.append(newRow)

    rows[-1].insert(0, 0)
    rows[-1].append(0)
    for rowIdx in reversed(range(len(rows) - 1)):
        rows[rowIdx].insert(0, rows[rowIdx][0] - rows[rowIdx + 1][0])
        rows[rowIdx].append(rows[rowIdx][-1] + rows[rowIdx + 1][-1])

    endSum += rows[0][-1]
    startSum += rows[0][0]

print(endSum)
print(startSum)