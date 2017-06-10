import math, time

def getSudoku(fileName):
    f = open(fileName, "r")
    rows = f.read().split("\n")

    width, height = len(rows[0].split()), len(rows)
    sudoku = [[0 for x in range(width)] for y in range(height)]

    for index in range(height):
        columns = rows[index].split()
        for counter, column in enumerate(columns):
            sudoku[index][counter] = (int)(columns[counter])

    return sudoku

def getSudokuWithSquares(fileName):
    f = open(fileName, "r")
    rows = f.read().split("\n")

    width, height = len(rows[0].split()), len(rows)
    sudoku = [[Square() for x in range(width)] for y in range(height)]

    for index in range(height):
        columns = rows[index].split()
        for counter, column in enumerate(columns):
            sudoku[index][counter].value = (int)(columns[counter])

    for row in range(height):
        for column in range(width):
            sudoku[row][column].fillDomain(sudoku, row, column)

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

def prettyPrintSquares(sudoku):
    length = len(sudoku)
    result = ""
    for x in range(length):
        for y in range(length):
            result += str(sudoku[x][y].value) + " "
        result += "\n"

    return result

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

def forwardChecking(sudoku, counter):
    counter.up()
    #print prettyPrintSquares(sudoku)
    sortedMCVList = getSortedMCVList(sudoku)
    if len(sortedMCVList) == 0:
        return True, counter.count()
    else:
        rowNumber, columnNumber, domainSize = sortedMCVList[0]

    for number in sudoku[rowNumber][columnNumber].getDomain():
        sudoku[rowNumber][columnNumber].value = number
        sudoku[rowNumber][columnNumber].updateNeighboursDomain(sudoku, rowNumber, columnNumber)

        if forwardChecking(sudoku, counter):
            return True, counter.count()

        sudoku[rowNumber][columnNumber].value = 0
        sudoku[rowNumber][columnNumber].updateNeighboursDomain(sudoku, rowNumber, columnNumber)

    return False

def getSortedMCVList(sudoku):
    l = []
    for x in range(len(sudoku)):
        for y in range(len(sudoku)):
            if sudoku[x][y].value == 0:
                l.append((x, y, len(sudoku[x][y].getDomain())))

    return sorted(l, key=lambda x: x[2])

class Square:
    value = 0
    domain = set()

    def getDomain(self):
        return list(self.domain)

    def fillDomain(self, sudoku, rowNumber, columnNumber):
        sudokuSize = len(sudoku)
        self.domain = set(i + 1 for i in range(sudokuSize))

        for x in range(sudokuSize):
            self.domain.discard(sudoku[rowNumber][x].value)

        for y in range(sudokuSize):
            self.domain.discard(sudoku[y][columnNumber].value)

        blockLength = int(math.sqrt(sudokuSize))
        blockRow = rowNumber - rowNumber % blockLength
        blockColumn = columnNumber - columnNumber % blockLength
        for x in range(blockLength):
            for y in range(blockLength):
                self.domain.discard(sudoku[blockRow + x][blockColumn + y].value)


    def updateNeighboursDomain(self, sudoku, rowNumber, columnNumber):
        sudokuSize = len(sudoku)

        for x in range(sudokuSize):
            sudoku[rowNumber][x].fillDomain(sudoku, rowNumber, x)

        for y in range(sudokuSize):
            sudoku[y][columnNumber].fillDomain(sudoku, y, columnNumber)

        blockLength = int(math.sqrt(sudokuSize))
        blockRow = rowNumber - rowNumber % blockLength
        blockColumn = columnNumber - columnNumber % blockLength
        for x in range(blockLength):
            for y in range(blockLength):
                sudoku[blockRow + x][blockColumn + y].fillDomain(sudoku, blockRow + x, blockColumn + y)

    def isDomainEmpty(self):
        return len(self.domain) == 0

    def removeFromDomain(self, val):
        self.domain.discard(val)


class Counter:
    i = 0

    def up(self):
        self.i = self.i + 1

    def count(self):
        return self.i

if __name__ == '__main__':
    sudoku = getSudokuWithSquares("sudoku2.txt")
    #sudoku2 = getSudoku("sudoku2.txt")
    start_time = time.time()
    counter = Counter()

    #sortedList = getListExpandByDomainSize(sudoku)
    #solved, recursion = domainSizeBacktracking(sudoku, sortedList, counter)
    #solved, recursion = reverseBacktracking(sudoku2, counter)
    #solved, recursion = backtracking(sudoku, counter)
    solved, recursion = forwardChecking(sudoku, counter)
    if solved:
        print prettyPrintSquares(sudoku)
    else:
        print "Geen oplossing"

    print "Recursions:", recursion, "times"
    print "Run Time:", (time.time() - start_time) * 1000, "milliseconds"