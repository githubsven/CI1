import math, time

def getSudoku(fileName):
    f = open(fileName, "r")
    rows = f.read().split("\n")

    width, height = len(rows[0].split()), len(rows)
    sudoku = [[0 for x in range(width)] for y in range(height)]

    for index in range(len(rows)):
        columns = rows[index].split()
        for counter, column in enumerate(columns):
            sudoku[index][counter] = (int)(columns[counter])

    return sudoku

def inRow(sudoku, rowNumber, number):
    for i in range(len(sudoku[0])):
        if sudoku[rowNumber][i] == number:
            return True
    return False

def inColumn(sudoku, columnNumber, number):
    for i in range(len(sudoku)):
        if sudoku[i][columnNumber] == number:
            return True
    return False

def inBlock(sudoku, rowNumber, columnNumber, number):
    length = int(math.sqrt(len(sudoku)))
    blockRow = rowNumber - rowNumber % length
    blockColumn = columnNumber - columnNumber % length
    for x in range(length):
        for y in range(length):
            if sudoku[blockRow + x][blockColumn + y] == number:
                return True
    return False

def acceptNumber(sudoku, rowNumber, columnNumber, number):
    return not inRow(sudoku, rowNumber, number) and not inColumn(sudoku, columnNumber, number) and not inBlock(sudoku, rowNumber, columnNumber, number)

def findFirstEmptySpot(sudoku):
    for x in range(len(sudoku)):
        for y in range(len(sudoku[0])):
            if sudoku[x][y] == 0:
                return x, y, True
    return 0, 0, False

def findFirstEmptySpotReverse(sudoku):
    for x in range(len(sudoku))[::-1]:
        for y in range(len(sudoku[0]))[::-1]:
            if sudoku[x][y] == 0:
                return x, y, True
    return 0, 0, False

def prettyPrint(sudoku):
    length = len(sudoku)
    result = ""
    for x in range(length):
        for y in range(length):
            result += str(sudoku[x][y]) + " "
        result += "\n"

    return result

def backtracking(sudoku):
    rowNumber, columnNumber, found = findFirstEmptySpot(sudoku)

    #print prettyPrint(sudoku)

    if not found:
        return True

    for number in range(1, len(sudoku) + 1):
        if acceptNumber(sudoku, rowNumber, columnNumber, number):
            sudoku[rowNumber][columnNumber] = number

            if backtracking(sudoku):
                return True

            sudoku[rowNumber][columnNumber] = 0

    return False

def reverseBacktracking(sudoku):
    rowNumber, columnNumber, found = findFirstEmptySpotReverse(sudoku)

    #print prettyPrint(sudoku)

    if not found:
        return True

    for number in range(1, len(sudoku) + 1):
        if acceptNumber(sudoku, rowNumber, columnNumber, number):
            sudoku[rowNumber][columnNumber] = number

            if reverseBacktracking(sudoku):
                return True

            sudoku[rowNumber][columnNumber] = 0

    return False

def domainSizeBacktracking(sudoku, sortedList, index = 0):
    if index < len(sortedList):
        rowNumber, columnNumber, ignore = sortedList[index]
    else:
        return True

    #print prettyPrint(sudoku)

    for number in range(1, len(sudoku) + 1):
        if acceptNumber(sudoku, rowNumber, columnNumber, number):
            sudoku[rowNumber][columnNumber] = number
            index += 1

            if domainSizeBacktracking(sudoku, sortedList, index):
                return True

            sudoku[rowNumber][columnNumber] = 0
            index -= 1

    return False

def getListExpandByDomainSize(sudoku):
    l = []
    for x in range(len(sudoku)):
        for y in range(len(sudoku)):
            if sudoku[x][y] == 0:
                l.append((x, y, getDomainSize(sudoku, x, y)))

    return sorted(l, key = lambda x: x[2])[::-1]

def getDomainSize(soduko, rowNumber, columnNumber):
    counter = 0

    for x in range(len(sudoku)):
        if sudoku[rowNumber][x] != 0:
            counter += 1

    for y in range(len(sudoku)):
        if sudoku[y][columnNumber] != 0:
            counter += 1

    length = int(math.sqrt(len(sudoku)))
    blockRow = rowNumber - rowNumber % length
    blockColumn = columnNumber - columnNumber % length
    for x in range(length):
        for y in range(length):
            if sudoku[blockRow + x][blockColumn + y] != 0:
                counter += 1

    return counter

if __name__ == '__main__':
    sudoku = getSudoku("sudoku.txt")
    start_time = time.time()

    sortedList = getListExpandByDomainSize(sudoku)
    if domainSizeBacktracking(sudoku, sortedList):
        print sudoku
    else:
        print "Geen oplossing"

    print "Recursions: unknown"
    print "Run Time:", time.time() - start_time, "seconds"
