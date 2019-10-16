

class Sudoku():
    """An updated version of the sudoku code 09/22/19"""
    
    def __init__(self, puzzle):
        """Takes in a string representation of the sudoku puzzle and stores it as
        one list of numbers, row by row (list = puzzle[row1:] + puzzle[row1:row2 + ...]])
        """
        self.puzzle = [int(i) for i in puzzle.split(' ')]   #Split string by spaces into single list




    def valid_square(self, square, value):
        """Takes in the index of a square and returns a boolean of whether that
        value is valid for the square given, assumes valid input
        O(1)
        """
        row = square // 9                           #Find the row and column that square is in
        col = square % 9
        
        for i in range(9):                      
            if self.puzzle[row*9 + i] == value:     #Check each square in row for same value
                return False
            if self.puzzle[col + i*9] == value:     #Check each square in col for same value
                return False
            
            #check each square in box for same value, a little more complex index-wise, but it works
            if self.puzzle[(3*(row//3)+(i//3))*9 + (col//3)*3+(i%3)] == value: 
                return False
    
        return True
    
    
    
    
    def solve_sudoku(self, square=0):
        """Upon this call, will recurse through the sudoku puzzle and attempt
        to solve, returning a solved solution. The parameter square is the
        current index in the puzzle"""
        if square == 81:                                #Hit end of the puzzle, meaning solved
            return self.puzzle
        if self.puzzle[square] != 0:                    #If value in square, move to next
            return self.solve_sudoku(square + 1)
        
        
        for value in range(1, 10):                      #Try each number in square    
                
            if self.valid_square(square, value):        #Place into puzzle only if it is valid
                self.puzzle[square] = value
                solved = self.solve_sudoku(square + 1)       #Recurse and move index to next square
                
                if solved != None:                           #If solved, return it
                    return solved
                
        self.puzzle[square] = 0                     #If not solved, replace value with 0
        
    

    def render(self):
        """
        Prints the board as a visual representation of the sudoku puzzle
        Return: None
        """
        print('--'*9+'-')                               #The top of the board
            
        for i in range(9):                              #Create a print statement for each line
            line = '|' 
            
            for j in range(9):                          #For each number in line, add to print line 
                space = str(self.puzzle[9*i + j])       
                
                if space == '0':                        #If spot is a zero, replace for visuals with '_'
                    space = '_'
                    
                line += space + '|'                     #Add number to print line with a separator '|'

            print(line)                                 #Print the rendered line
            
        print('--'*9+'-')                               #Print the bottom of the board
            
        
