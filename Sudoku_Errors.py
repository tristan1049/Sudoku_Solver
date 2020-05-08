class SudokuException(Exception):
    """
    A base class for errors that occur specific to working with 
    the sudoku puzzle abstract data type
    """
    pass


class InvalidPuzzleException(SudokuException):
    """
    Exception raised for the existence of invalid sudoku puzzles

    Attributes:
        expression -- input expression for which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


"""
A Success!!!!!
-------------------
|_|_|5|_|7|8|_|_|_|
|_|_|7|_|_|6|3|2|4|
|_|_|_|_|_|_|_|_|8|
|8|_|_|_|_|_|6|_|_|
|_|_|_|_|9|3|5|_|_|
|_|6|_|_|_|5|1|4|_|
|_|_|_|3|6|_|_|_|_|
|_|_|8|_|1|2|_|_|5|
|_|1|3|_|8|_|_|_|_|
-------------------
"""