#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 16:03:22 2019

@author: tristanculp
"""
import math
import time
import random
import Sudoku_Errors


def render(board):
    """Returns a string of the board as a visual representation of the 
    sudoku puzzle. Can only handle Sudoku boards with 9x9 dimensions.
    
    board : A nxn list of lists representing a sudoku board
    Return: A string representing the rendered board"""
    #The top of the board render, which gives enough space for each square based on max square value
    spot_length = len(str(len(board)))
    rv = '-'*((spot_length+1)*len(board))+'-\n'      

    #Create a print statement for each line
    for i in range(len(board)):                     
        line = '|' 

        #For each number in line, add to print line 
        for j in range(len(board[i])):                 
            spot = str(board[i][j])      
            #If spot is a zero, replace for visuals with '_' 
            if spot == '0':       
                spot = '_'*spot_length
            #Add number to print line with a separator '|'
            line += ' '*(spot_length-len(spot)) + spot + '|'  

        #Print the rendered line
        rv += line + '\n'              

    #Print the bottom of the board
    rv += '-'*((spot_length+1)*len(board))+'-'                     
    return rv



class Sudoku():
    """
    RI: len(puzzle) must be a fourth squared integer (81 = 3^4, 16 = 2^4), sl must be
    the square root of the puz, and bs must be the square root of sl

    AF(puzzle, sl, bs): A Sudoku puzzle with side length sl and block size bs, with 
    each consecutive row being puzzle[i], for 0 <= i < sl.

    Safety From Rep Exposure: No references to mutable inputs are kept, and no 
    references to fields are returned.
    """

    def __init__(self, puzzle):
        """Takes in a string representation of the sudoku puzzle and allows for 
        sudoku operations on it"""
        # Split the given string input and find the side length and block size of the puzzle
        puz = [int(i) for i in puzzle.split(' ') if i]
        self.sl = int(math.sqrt(len(puz)))                          
        self.bs = int(math.sqrt(self.sl))

        # If side length squared not the same length as total puzzle, or if side lengths
        # not a square length, raise error
        if not (self.sl**2 == len(puz)) or not (self.bs**2 == self.sl):
            raise Sudoku_Errors.InvalidPuzzleException(puzzle, "Puzzle side lengths not a perfect square")

        # For each value in the puzzle, if not in correct range, raise error
        for ind in range(len(puz)):
            row = ind // self.sl
            col = ind % self.sl
            if not (0 <= puz[ind] <= self.sl):
                raise Sudoku_Errors.InvalidPuzzleException(puzzle,
            "Puzzle value at ({}, {}) is out of range in puzzle \n{}".format(row, col, puzzle))

        # Split string by spaces into single list
        self.puzzle = [[j for j in puz[(i*self.sl):(i*self.sl)+self.sl]] for i in range(self.sl)]

        # For each value in the puzzle, check that it is a valid value for that square
        for row in range(self.sl):
            for col in range(self.sl):
                # This temporary replacing of each value with 0 is a trick so that
                # the valid_square method can be used on every square
                val = self.puzzle[row][col]
                self.puzzle[row][col] = 0

                if not self.valid_square(row, col, val):
                    # If not a valid puzzle, reset self.puzzle and raise error
                    self.puzzle = None
                    raise Sudoku_Errors.InvalidPuzzleException(puzzle,
                    "Puzzle value at ({}, {}) is incorrect in puzzle \n{}".format(row, col, puzzle))

                # If value is valid, replace that square with prior value that was input
                self.puzzle[row][col] = val


    def get_puzzle(self):
        """Returns a copy of the sudoku puzzle for this instance as a list of lists of strings"""
        return [[str(self.puzzle[i][j]) for j in range(len(self.puzzle[0]))] for i in range(len(self.puzzle))]


    def valid_square(self, row, col, value):
        """Takes in the row and column indices of a square in a sudoku puzzle and returns a 
        boolean of whether the given value is valid to be input for the square given
        
        row: An integer 
        col: Another integer
        value: The integer value to set the puzzle square value, indexed by 
            row and col

        return: Boolean of whether the value is valid for the square of the
        puzzle indexed by row and col"""
        # Check that the row and col are valid puzzle indices
        if not ((0 <= row < self.sl) and (0 <= col < self.sl)):
            return False

        # Check that the square input is empty
        if self.puzzle[row][col] != 0:
            return False
            
        # Check that the value input is a valid puzzle value
        if not (1 <= value <= self.sl):
            if self.puzzle[row][col] == 0 and value == 0:
                return True
            return False
        
        # Check each row, column and block for same number
        for i in range(self.sl):                      
            if self.puzzle[row][i] == value:     # Check each square in row for same value
                return False
            if self.puzzle[i][col] == value:     # Check each square in col for same value
                return False
            
            # Check each square in box for same value, a little more complex index-wise
            r = self.bs*(row//self.bs) + (i//self.bs) 
            c = self.bs*(col//self.bs) + (i%self.bs) 
            if self.puzzle[r][c] == value:
                return False
    
        return True
    

    def is_solved(self):
        """Determines if the puzzle is solved.
        return: A boolean of whether the puzzle object is solved"""
        # Iterate through each square of the puzzle
        for row in range(self.sl):
            for col in range(self.sl):
                val = self.puzzle[row][col]

                # If any square value is blank (0), not solved, return False
                if val == 0:
                    return False

                # Trick to keep DRY code: replace each value temporarily with a
                # 0, and use valid_square method with original value to determine
                # if every square is valid
                self.puzzle[row][col] = 0
                valid = self.valid_square(row, col, val)
                self.puzzle[row][col] = val
                    
                # If not a valid value for square, return False
                if not valid:
                    return False
        return True


    def is_solvable(self, row=0, col=0):
        """Determines if the puzzle can be solved.
        return: A boolean of whether the puzzle object can solved"""
        if row == self.sl-1 and col == self.sl:      
            return True

        # If column is the side length, mvoe indices to next row
        if col == self.sl:
            return self.is_solvable(row+1, 0)

        # If square has a value already, move to next column
        if self.puzzle[row][col] != 0:                                 
            return self.is_solvable(row, col + 1)

        # If empty square, try each value in that square
        for value in range(1, self.sl+1):                
            # If a valid value, recurse with that value and attempt to solve    
            if self.valid_square(row, col, value):                      
                self.puzzle[row][col] = value
                solved = self.is_solvable(row, col + 1)       
                self.puzzle[row][col] = 0

                # If value solves puzzle, return solved
                if solved:
                    return solved

        return False    


    def solve_sudoku(self, row=0, col=0):
        """Upon this call, will recurse through the sudoku puzzle and attempt
        to solve, returning a boolean of whether it was solved, None otherwise.
        This method modifies the puzzle object itself, keeping it the same if 
        unsolvable, and filling each square with a valid value if solvable.
    
        row = An integer
        col = Another integer

        return: A boolean of whether the puzzle was solved or not"""
        # If end of puzzle is hit, the puzzle is solved, return True
        if row == self.sl-1 and col == self.sl:      
            return True
        
        # If column is the side length, mvoe indices to next row
        if col == self.sl:
            return self.solve_sudoku(row+1, 0)

        # If square has a value already, move to next column
        if self.puzzle[row][col] != 0:                                 
            return self.solve_sudoku(row, col + 1)

        # If empty square, try each value in that square
        for value in range(1, self.sl+1):                
            # If a valid value, recurse with that value and attempt to solve      
            if self.valid_square(row, col, value):                      
                self.puzzle[row][col] = value
                solved = self.solve_sudoku(row, col + 1)               

                # If value solves puzzle, return solved
                if solved:                                    
                    return solved

                # If not solved, replace value with 0 for next iteration
                self.puzzle[row][col] = 0

        return False                               
        

    def insert(self, row, col, value):
        """Attempt to insert an integer value into the Sudoku puzzle 
        object at row and col, and returns a boolean of whether the 
        operation was successful. Can be used with value 0 to remove
        a value from a square. 

        row = An integer
        col = Another integer
        value = Another integer
        
        return: A boolean of whether the insert was successful"""
        if self.valid_square(row, col, value) or value == 0:
            self.puzzle[row][col] = value
            return True
        return False


    def is_one_sol(self, row=0, col=0, sols=None):
        """Attempts to solve the solve the Sudoku object puzzle, 
        without mutating the Sudoku object, and returns a boolean
        of whether there is exactly one solution to the puzzle
        
        return: A boolean of whether the Sudoku puzzle has exactly
        one solution"""
        # For testing reasons, initialize with None
        if sols == None:
            sols = []

        # Uses an aliased list to maintain variance of number of solutions 
        # found across all recursive calls, and returns when more than 1 is found
        if len(sols) > 1:
            return False

        # If end of puzzle is hit, the puzzle is solved, return True
        if row == self.sl-1 and col == self.sl:      
            sols.append(True)
            return
        
        # If column is the side length, mvoe indices to next row
        if col == self.sl:
            return self.is_one_sol(row+1, 0, sols)

        # If square has a value already, move to next column
        if self.puzzle[row][col] != 0:                                 
            return self.is_one_sol(row, col+1, sols)

        # If empty square, try each value in that square
        for value in range(1, self.sl+1):                
            # If a valid value, recurse with that value and attempt to solve      
            if self.valid_square(row, col, value):                      
                self.puzzle[row][col] = value
                self.is_one_sol(row, col+1, sols) 
                self.puzzle[row][col] = 0

                if len(sols) > 1:
                    return False

        # If exhausted all possibilities, return if only one solution found thus far
        return len(sols) == 1



class Create_Sudoku():

    def __init__(self, sl):
        """Takes in an integer side length and allows for the 
        creation of pseudorandom puzzles"""
        if int(math.sqrt(sl))**2 != sl:
            raise Sudoku_Errors.InvalidPuzzleException(sl, "Invalid Sudoku puzzle side length, must be a square integer")

        self.sl = sl
        self.bs = int(math.sqrt(sl))


    def random_insertion(self, puzzle, num_squares, avail, deleted):
        """Given a Sudoku object puzzle, randomly inserts a valid value into
        Sudoku puzzle, at an available index in avail.

        return: An integer of the number of squares that were successfully 
        inserted"""
        rv = 0
        for _ in range(min(num_squares, len(avail))):
            # Initialize possible values for random square, and choose row and column of square
            vals = [i for i in range(self.sl+1) if i != 0]
            ind = random.choice(avail)
            row = ind // self.sl
            col = ind % self.sl

            # Attempt to put random value into random square
            while len(vals):
                val = random.choice(vals)
                if puzzle.valid_square(row, col, val):
                    puzzle.insert(row, col, val)
                    avail.remove(ind)
                    deleted.append(ind)
                    rv += 1
                    break
                vals.remove(val)
        
        # Return the amount of successful insertions
        return rv


    def random_deletion(self, puzzle, num_squares, avail, deleted):
        """Given a Sudoku object puzzle, randomly deletes values from
        Sudoku puzzle, at available indices in deleted

        return: An integer of the number of squares that were successfully 
        deleted"""
        rv = 0
        for _ in range(min(num_squares, len(deleted))):
            if deleted == []:
                return rv

            # Choose row and column of square to delete
            ind = random.choice(deleted)
            avail.append(ind)
            deleted.remove(ind)
            row = ind // self.sl
            col = ind % self.sl
            puzzle.insert(row, col, 0)
            rv += 1
        
        # Return the amount of successful deletions
        return rv


    def create(self, show=False):
        """Returns a pseudorandom puzzle as a Sudoku object"""
        # First create empty Sudoku object, and set of indices of empty squares
        puzzle = Sudoku("0 "*(self.sl**2))
        indices = [i for i in range(self.sl**2)]
        deleted = []

        # First add pseudorandom squares into puzzle, try 1/2 of total squares
        num_squares_to_add = (self.sl**2) // 2
        self.random_insertion(puzzle, num_squares_to_add, indices, deleted)

        # Repeat steps of deleting/inserting until one solution puzzle created
        while True:
            if show:
                print(render(puzzle.get_puzzle()))
            # Now check if one solution exists, and return Sudoku object if it does
            s = time.time()
            if puzzle.is_one_sol():
                return puzzle
            t = time.time()

            # If solving takes too much time, "revamp" process by deleting and inserting 
            # multiple squares
            if t-s > 0.5:
                dels, ins = 1, 0
                while dels > ins:
                    dels = self.random_deletion(puzzle, self.sl*2, indices, deleted)
                    ins = self.random_insertion(puzzle, self.sl*10, indices, deleted) 

            # If not one solution exists and it's solvable, more than one solution exists
            elif puzzle.is_solvable():
                dels, ins = 1, 0
                while dels > ins:
                    dels = self.random_deletion(puzzle, self.sl*2, indices, deleted)
                    ins = self.random_insertion(puzzle, self.sl*10, indices, deleted)

            # Else, there are no solutions, so must delete a square
            else:
                self.random_deletion(puzzle, 1, indices, deleted)

        return puzzle


if __name__ == "__main__":
    # An example of creating a pseudorandom 9x9 Sudoku puzzle
    s = Create_Sudoku(9).create(True)
    puz = render(s.get_puzzle())
    print(puz)
