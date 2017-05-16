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

def backtracking():
    #once: findFirstEmpySpot
    #keep track of row and column numbers (so you know which number you're changing)
    if empty(L) then return nil
    else
        t ← first(L);
    if goal(t) then return t
    else
        while there are unexplored successors of t
    and not found
    do
    t’ ← next - successor(t);
    L ← push(L, t’);
    backtrack(L)
    endwhile;
    L ← pop(L)

def nextSuccessor(rowNumber, columnNuber, sudoku):
    #check if valid successor
    return sudoku

def findFirstEmptySpot(sudoku):
    for x in range(len(sudoku[0])):
        for y in range(len(sudoku)):
            if sudoku[x][y] == 0:
                return x, y
    return None

if __name__ == '__main__':
    print getSudoku("sudoku.txt")
