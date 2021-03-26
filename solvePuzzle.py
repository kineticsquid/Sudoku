class SudokuPuzzle(object):
    def __init__(self, size):

        # matrixSize is the size of the overall puzzle matrix. subMatrixSize is 1/3 of the matrixSize.
        self.matrixSize = size
        self.subMatrixSize = int(self.matrixSize / 3)
        self.solutionMatrix = None
        self.subMatrixIndex = []
        for row in range(0, self.matrixSize):
            self.subMatrixIndex.append([])
            for col in range(0, self.matrixSize):
                index = int(row - (row % self.subMatrixSize) + (col - (col % self.subMatrixSize)) / 3)
                self.subMatrixIndex[row].append(index)

        # Array of Arrays that contains the puzzle values. 0 indicates an element has no value. inputElements
        # indicates which are input (initial) values.
        self.values = [[0 for row in range(0, self.matrixSize)] for col in range(0, self.matrixSize)]

        # * Array of Arrays that define if a row, column, and submatrix contains a value. The size of the element
        # Arrays are are matrixSize + 1. The submatrices are numbered starting in the upper left, moving across the
        # columns, and then down to the next row. For example, in a 9x9 puzzle, if element [0,4] contains a "9". Then
        # rowContents[0][9] == true, columnContents[4][9] == true, and submatrixContents[3][9] == true.
        # getSubMatrixFor(i, i) returns the submatrix index for a given row and column.
        self.rowContents = [[False for row in range(0, self.matrixSize + 1)] for col in range(0, self.matrixSize + 1)]
        self.columnContents = [[False for row in range(0, self.matrixSize + 1)] for col in
                               range(0, self.matrixSize + 1)]
        self.subMatrixContents = [[False for row in range(0, self.matrixSize + 1)] for col in
                                  range(0, self.matrixSize + 1)]

        # Variables to indicate which rows, columns, and submatrices have errors. E.g. invalidRows.[2] == true means
        # there is an error in the third row.
        self.invalidRows = [False for i in range(0, self.matrixSize)]
        self.invalidColumns = [False for i in range(0, self.matrixSize)]
        self.invalidSubMatrices = [False for i in range(0, self.matrixSize)]

        # matrix (Array of Arrays) of Arrays that indicate for each element in the matrix, what are the valid values
        # that element can contain. E.g. choicesRemainingForEmptyElement[1][2] == an Array of numbers that represent
        # the valid choices remaining for that element.
        self.choicesRemainingForEmptyElement = [[[i + 1 for i in range(0, 9)] for row in range(0, 9)] for col in
                                                range(0, 9)]

        # These two variables contain the row and column of the empty matrix element that has the least number of
        # remaining valid values. If more than one empty element have the same number of fewest choices, these
        # variables refer to the first one encountered.
        self.rowOfEmptyElementWithFewestRemainingChoices = 0
        self.columnOfEmptyElementWithFewestRemainingChoices = 0

        # Indicates a solution exists for the puzzle. The solution is defined in solutionMatrix.
        self.solutionKnown = False

    """
    Method to, given the row and column indices for an element, return it's submatrix index, an integer between 0 and 8
    """

    def get_submatrix_for(self, row, column):
        return self.subMatrixIndex[row][column]

    """
    Method to return row, column representing the upper left element of a given subMatrix
    """

    def get_upper_left_for_submatrix(self, subMatrix):
        row = subMatrix - (subMatrix % 3)
        column = subMatrix % 3 * 3
        return row, column

    """
    Method to return whether or not the matrix is valid    
    """

    def is_matrix_valid(self):
        matrixIsValid = True
        for i in range(0, self.matrixSize):
            if self.invalidRows[i] or self.invalidColumns[i] or self.invalidSubMatrices[i]:
                matrixIsValid = False # lgtm [py/unused-local-variable]
                break
            return matrixIsValid

    """
    Method to an array of valid choices for cell [row, column]. Returns empty array if there are no valid choices.
    """

    def compute_choices(self):
        self.columnOfEmptyElementWithFewestRemainingChoices = -1
        self.rowOfEmptyElementWithFewestRemainingChoices = -1
        for row in range(0, self.matrixSize):
            for column in range(0, self.matrixSize):
                if self.values[row][column] == 0:
                    # this element is blank so construct an Array with the valid remaining choices
                    choices = []
                    for i in range(1, self.matrixSize + 1):
                        if not self.rowContents[row][i] and not self.columnContents[column][i] and not \
                                self.subMatrixContents[self.get_submatrix_for(row, column)][i]:
                            choices.append(i)
                    self.choicesRemainingForEmptyElement[row][column] = choices
                    # Now if this number of choices is a new minimum, set the fields which hold the row and column
                    # indices of this element
                    if self.columnOfEmptyElementWithFewestRemainingChoices < 0:
                        self.rowOfEmptyElementWithFewestRemainingChoices = row
                        self.columnOfEmptyElementWithFewestRemainingChoices = column
                    else:
                        if len(self.choicesRemainingForEmptyElement[self.rowOfEmptyElementWithFewestRemainingChoices][
                                   self.columnOfEmptyElementWithFewestRemainingChoices]) > len(choices):
                            self.rowOfEmptyElementWithFewestRemainingChoices = row
                            self.columnOfEmptyElementWithFewestRemainingChoices = column
                else:
                    # Else, element has a value, so it has no possible remaining choices
                    self.choicesRemainingForEmptyElement[row][column] = []

    """
    Whenever a matrix element changes, this method is called to validate the resulting matrix. It marks invalid cells,
    and tracks which currently empty element can take the fewest values row - row index of changed element
    column - column index of changed element
    """

    def validate_matrix(self, row, column):
        rowValues = [False for i in range(0, self.matrixSize + 1)]
        self.invalidRows[row] = False
        # Check for invalid rows. Loop through each column in this row.
        for iColumn in range(0, self.matrixSize):
            # If the element has a value and we've already seen this value in this row, indicate an error in this row.
            if self.values[row][iColumn] > 0:
                if rowValues[self.values[row][iColumn]]:
                    self.invalidRows[row] = True
                # Indicate that we've seen this value in this row.
                rowValues[self.values[row][iColumn]] = True
        self.rowContents[row] = rowValues

        columnValues = [False for i in range(0, self.matrixSize + 1)]
        self.invalidColumns[column] = False
        # Check for invalid columns. Loop through each row in this column.
        for iRow in range(0, self.matrixSize):
            # If the element has a value and we've already seen this value in this column, indicate an error in this
            # column.
            if self.values[iRow][column] > 0:
                if columnValues[self.values[iRow][column]]:
                    self.invalidColumns[column] = True
                # Indicate that we've seen this value in this column.
                columnValues[self.values[iRow][column]] = True
        self.columnContents[column] = columnValues

        subMatrixValues = [False for i in range(0, self.matrixSize + 1)]
        thisSubMatrix = self.get_submatrix_for(row, column)
        self.invalidSubMatrices[thisSubMatrix] = False
        # Check for invalid submatrices. Loop through each element in the submatrix to which element[row, column]
        # belongs.
        startingRow, startingColumn = self.get_upper_left_for_submatrix(thisSubMatrix)
        for iRow in range(startingRow, startingRow + self.subMatrixSize):
            for iColumn in range(startingColumn, startingColumn + self.subMatrixSize):
                # If the element has a value and we've already seen this value in this submatrix, indicate an error in
                # this submatrix.
                if self.values[iRow][iColumn] > 0:
                    if subMatrixValues[self.values[iRow][iColumn]]:
                        self.invalidSubMatrices[thisSubMatrix] = True
                    # Indicate that we've seen this value in this submatrix.
                    subMatrixValues[self.values[iRow][iColumn]] = True
        self.subMatrixContents[self.get_submatrix_for(row, column)] = subMatrixValues

    """
    Method to take an input matrix and populate puzzle data structures
    """

    def set_inputs(self, input_matrix):
        if len(input_matrix) != self.matrixSize:
            raise Exception('Input matrix must be %s x %s.' % (self.matrixSize, self.matrixSize))
        else:
            for row in range(0, self.matrixSize):
                if len(input_matrix[row]) != self.matrixSize:
                    raise Exception('Input matrix must be %s x %s.' % (self.matrixSize, self.matrixSize))
                else:
                    for column in range(0, self.matrixSize):
                        i = input_matrix[row][column] # lgtm [py/unused-local-variable]
                        if type(input_matrix[row][column]) is not int:
                            raise Exception('Input error: Non integer input')
                        elif input_matrix[row][column] not in range(0, self.matrixSize + 1):
                            raise Exception('Input error: integer not between 0 and %s, inclusive.' %
                                            self.matrixSize)
                        else:
                            self.values[row][column] = input_matrix[row][column]
            for row in range(0, self.matrixSize):
                for column in range(0, self.matrixSize):
                    self.validate_matrix(row, column)

            if self.is_matrix_valid():
                self.compute_choices()
            else:
                raise Exception('Input error: Invalid input matrix')

    """
    Method that returns if we know the solution to the puzzle
    """

    def is_solution_known(self):
        return self.is_solution_known()

    """
    Method to determine if the matrix is completely filled in
    """

    def is_matrix_complete(self):
        complete = True
        for row in range(0, self.matrixSize):
            for column in range(1, self.matrixSize + 1):
                if self.rowContents[row][column] is False:
                    complete = False
                    break
            if not complete:
                break
        return complete

    """
    Method to solve the matrix recursively starting with the element (row,column). The solution attempts are contained 
    in solutionMatrix. row - Row of element to start solution calculation with column - Column of element to start 
    solution calculation with
    """

    def compute_solution(self):
        self.compute_solution_heavy_lifting()
        if self.is_matrix_complete() and self.is_matrix_valid():
            self.solutionKnown = True
        else:
            raise Exception('Unsolvable matrix')


    """
    This does the heavy lifting and recursion. 
    """

    def compute_solution_heavy_lifting(self):
        if self.is_matrix_complete() and self.is_matrix_valid():
            self.solutionKnown = True
            return
        else:
            currentRow = self.rowOfEmptyElementWithFewestRemainingChoices
            currentColumn = self.columnOfEmptyElementWithFewestRemainingChoices
            if len(self.choicesRemainingForEmptyElement[currentRow][currentColumn]) > 0:
                # copy array
                remainingChoices = list(self.choicesRemainingForEmptyElement[currentRow][currentColumn])
                while len(remainingChoices) > 0 and not self.solutionKnown:
                    nextValueToTry = remainingChoices.pop(0)
                    self.values[currentRow][currentColumn] = nextValueToTry
                    self.validate_matrix(currentRow, currentColumn)
                    self.compute_choices()
                    self.compute_solution_heavy_lifting()
                    if not self.solutionKnown:
                        self.values[currentRow][currentColumn] = 0
                        self.validate_matrix(currentRow, currentColumn)
