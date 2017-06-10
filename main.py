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

def backtracking(sudoku, counter):
    rowNumber, columnNumber, found = findFirstEmptySpot(sudoku)
    counter.up()
    #print prettyPrint(sudoku)

    if not found:
        return True, counter.count()

    for number in range(1, len(sudoku) + 1):
        if acceptNumber(sudoku, rowNumber, columnNumber, number):
            sudoku[rowNumber][columnNumber] = number

            if backtracking(sudoku, counter):
                return True, counter.count()

            sudoku[rowNumber][columnNumber] = 0

    return False

def reverseBacktracking(sudoku, counter):
    rowNumber, columnNumber, found = findFirstEmptySpotReverse(sudoku)
    counter.up()
    #print prettyPrint(sudoku)

    if not found:
        return True, counter.count()

    for number in range(1, len(sudoku) + 1):
        if acceptNumber(sudoku, rowNumber, columnNumber, number):
            sudoku[rowNumber][columnNumber] = number

            if reverseBacktracking(sudoku, counter):
                return True, counter.count()

            sudoku[rowNumber][columnNumber] = 0

    return False

def domainSizeBacktracking(sudoku, sortedList, counter, index = 0):
    counter.up()
    if index < len(sortedList):
        rowNumber, columnNumber, ignore = sortedList[index]
    else:
        return True, counter.count()

    #print prettyPrint(sudoku)

    for number in range(1, len(sudoku) + 1):
        if acceptNumber(sudoku, rowNumber, columnNumber, number):
            sudoku[rowNumber][columnNumber] = number
            index += 1

            if domainSizeBacktracking(sudoku, sortedList, counter, index):
                return True, counter.count()

            sudoku[rowNumber][columnNumber] = 0
            index -= 1

    return False

def getListExpandByDomainSize(sudoku):
    l = []
    for x in range(len(sudoku)):
        for y in range(len(sudoku)):
            if sudoku[x][y] == 0:
                l.append((x, y, getDomainSize(sudoku, x, y)))

    return sorted(l, key = lambda x: x[2])

def getDomainSize(sudoku, rowNumber, columnNumber):
    domain = set()

    for x in range(len(sudoku)):
        if sudoku[rowNumber][x] != 0:
            domain.add(sudoku[rowNumber][x])

    for y in range(len(sudoku)):
        if sudoku[y][columnNumber] != 0:
            domain.add(sudoku[y][columnNumber])

    blockLength = int(math.sqrt(len(sudoku)))
    blockRow = rowNumber - rowNumber % blockLength
    blockColumn = columnNumber - columnNumber % blockLength
    for x in range(blockLength):
        for y in range(blockLength):
            if sudoku[blockRow + x][blockColumn + y] != 0:
                domain.add(sudoku[blockRow + x][blockColumn + y])

    return len(sudoku) - len(domain)

class Counter:
    i = 0

    def up(self):
        self.i = self.i + 1

    def count(self):
        return self.i

if __name__ == '__main__':
    sudoku = getSudoku("sudoku.txt")
    start_time = time.time()
    counter = Counter()

    sortedList = getListExpandByDomainSize(sudoku)
    try:
        solved, recursion = domainSizeBacktracking(sudoku, sortedList, counter)
    #solved, recursion = reverseBacktracking(sudoku, counter)
    #solved, recursion = backtracking(sudoku, counter)
        if solved:
            print sudoku
        else:
            print "Geen oplossing"

        print "Recursions:", recursion, "times"
    except TypeError:
        solved = domainSizeBacktracking(sudoku, sortedList, counter)
        if solved:
            print sudoku
        else:
            print "Geen oplossing"
    print "Run Time:", (time.time() - start_time) * 1000, "milliseconds"