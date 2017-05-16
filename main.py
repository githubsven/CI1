def getSudoku(fileName):
    f = open(fileName, "r")
    rows = f.read().split("\n")

    width, height = len(rows[0].split()), len(rows)
    sudoku = [[0 for x in range(width)] for y in range(height)]

    for index in range(len(rows)):
        columns = rows[index].split()
        for counter, column in enumerate(columns):
            sudoku[index][counter] = columns[counter]

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

def inBlock(sudoku, rowNumber, number):

    return False

def findFirstEmptySpot(sudoku):
    for x in range(len(sudoku[0])):
        for y in range(len(sudoku)):
            if sudoku[x][y] == 0:
                return x, y
    return None

def nextSuccessor(rowNumber, columnNumber, sudoku):
    #check if valid successor
    return sudoku

def backtracking(sudoku):
    rowNumber, columnNumber = findFirstEmptySpot(sudoku)

    #once: findFirstEmpySpot
    #keep track of row and column numbers (so you know which number you're changing)
    return sudoku

if __name__ == '__main__':
    print getSudoku("sudoku.txt")
