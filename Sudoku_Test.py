import Sudoku
import unittest
import Sudoku_Errors

class TestRender(unittest.TestCase):

    def test_empty_render(self):
        for i in [1, 4, 9, 16]:
            board = [['0' for _ in range(i)] for j in range(i)]
            result = Sudoku.render(board)
            expected = "-"*(((len(str(i))+1)*i)+1) + "\n"+ (("|" +"_"*len(str(i)))*i + "|\n")*i + "-"*(((len(str(i))+1)*i)+1)
            self.assertEqual(result, expected, "expected rendered board: \n{}\n, instead got: \n{}".format(
                expected, result
            ))

    def test_incomplete_render_4x4(self):
        board = [['0', '0', '3', '4'],
                 ['0', '3', '0', '1'],
                 ['3', '4', '0', '0'],
                 ['0', '1', '0', '3']]
        result = Sudoku.render(board)
        expected = "---------\n" +\
                   "|_|_|3|4|\n" +\
                   "|_|3|_|1|\n" +\
                   "|3|4|_|_|\n" +\
                   "|_|1|_|3|\n" +\
                   "---------" 
        self.assertEqual(result, expected, "expected incomplete 4x4 rendered board")


    def test_incomplete_render_9x9(self):
        board = [['9', '7', '0', '0', '0', '0', '0', '0', '0'],
                 ['4', '0', '0', '8', '0', '0', '0', '0', '0'],
                 ['0', '0', '0', '0', '4', '0', '7', '0', '0'],
                 ['0', '0', '0', '0', '9', '0', '6', '0', '0'], 
                 ['0', '0', '0', '2', '0', '0', '0', '3', '0'],
                 ['0', '0', '0', '0', '0', '1', '0', '0', '8'],
                 ['0', '4', '0', '0', '6', '0', '9', '0', '0'],
                 ['0', '0', '5', '0', '0', '0', '0', '0', '0'],
                 ['0', '0', '0', '0', '0', '3', '0', '0', '1']]
        result = Sudoku.render(board)
        expected = "-------------------\n"+\
                   "|9|7|_|_|_|_|_|_|_|\n"+\
                   "|4|_|_|8|_|_|_|_|_|\n"+\
                   "|_|_|_|_|4|_|7|_|_|\n"+\
                   "|_|_|_|_|9|_|6|_|_|\n"+\
                   "|_|_|_|2|_|_|_|3|_|\n"+\
                   "|_|_|_|_|_|1|_|_|8|\n"+\
                   "|_|4|_|_|6|_|9|_|_|\n"+\
                   "|_|_|5|_|_|_|_|_|_|\n"+\
                   "|_|_|_|_|_|3|_|_|1|\n"+\
                   "-------------------" 
        self.assertEqual(result, expected, "expected an incomplete 9x9 rendered board")


    def test_solved_render_1x1(self):
        board = [['1']]
        result = Sudoku.render(board)
        expected = "---\n" +\
                   "|1|\n" +\
                   "---" 
        self.assertEqual(result, expected, "expected a solved 1x1 rendered board")


    def test_solved_render_4x4(self):
        board = [['1', '2', '3', '4'],
                 ['4', '3', '2', '1'],
                 ['3', '4', '1', '2'],
                 ['2', '1', '4', '3']]
        result = Sudoku.render(board)
        expected = "---------\n" +\
                   "|1|2|3|4|\n" +\
                   "|4|3|2|1|\n" +\
                   "|3|4|1|2|\n" +\
                   "|2|1|4|3|\n" +\
                   "---------" 
        self.assertEqual(result, expected, "expected a solved 4x4 rendered board")



class Test_Sudoku_Constructor(unittest.TestCase):

    def test_empty_valid_puzzle(self):
        for side_length in [1, 4, 9]:
            puzzle = "0 "*(side_length**2)

            expected = [['0' for j in range(side_length)] for _ in range(side_length)]
            result = Sudoku.Sudoku(puzzle)

            self.assertEqual(result.get_puzzle(), expected,
            "expected length {} puzzle of all 0's, instead created \n{}".format(side_length, 
                Sudoku.render(result.get_puzzle())))


    def test_solved_valid_puzzle_1x1(self):
        puzzle = "1"
        expected = [['1']]
        result = Sudoku.Sudoku(puzzle)

        self.assertEqual(result.get_puzzle(), expected,
        "expected solved length 1 puzzle, instead created \n{}".format(Sudoku.render(result.get_puzzle())))
            

    def test_solved_valid_puzzle_4x4(self):
        puzzle = "1 2 3 4 4 3 2 1 3 4 1 2 2 1 4 3"
        expected = [['1', '2', '3', '4'],
                    ['4', '3', '2', '1'],
                    ['3', '4', '1', '2'],
                    ['2', '1', '4', '3']] 
        result = Sudoku.Sudoku(puzzle)

        self.assertEqual(result.get_puzzle(), expected,
        "expected solved length 4 puzzle, instead created \n{}".format(Sudoku.render(result.get_puzzle())))


    def test_invalid_puzzle_1(self):
        invalid_puzzles = [
            "1 0", 
            "-1",
            "2 1 1 2",
            "1 2 3 4 4 3 2 3 3 4 1 2 2 1 4 3",
            "1 2 3 4 4 3 2 1 3 4 1 2 2 1 4 5",
            "1 2 3 4 4 3 2 1 3 4 1 2 2 1 4 3 0 0 0"]

        for invalid in invalid_puzzles:
            try:
                result = Sudoku.Sudoku(invalid)
                print("expected InvalidPuzzleError for invalid puzzle input {},".format(invalid) +
                "instead got :\n{}".format(Sudoku.render(result.get_puzzle())))
                self.assertTrue(False)
            except Sudoku_Errors.InvalidPuzzleException:
                pass



class Test_Sudoku_Valid_Square(unittest.TestCase):

    def check_square_valid_value(self, board, rows, cols, vals, is_valid=True):
        puzzle = Sudoku.Sudoku(board)
        render = Sudoku.render(puzzle.get_puzzle())

        for ind in range(len(rows)):
            row, col, value = rows[ind], cols[ind], vals[ind]
            result = puzzle.valid_square(row, col, value)

            if is_valid:
                self.assertTrue(result, "expected True for valid value {} for square: ".format(value) +
                "({}, {}) for rendered board:\n{}".format(row, col, render)) 
            else:
               self.assertFalse(result, "expected False for invalid value {} for square: ".format(value) +
                "({}, {}) for rendered board:\n{}".format(row, col, render))  


    def test_valid_square_1x1(self):
        board = "0"
        valid_rows = [0]
        valid_cols = [0]
        valid_vals = [1]
        invalid_rows = [0, 0, 1, 1, 0, 2, 1]
        invalid_cols = [0, 1, 0, 1, 1, 1, 90]
        invalid_vals = [2, 1, 1, -1, 3, 0, 1]
        
        self.check_square_valid_value(board, valid_rows, valid_cols, valid_vals)
        self.check_square_valid_value(board, invalid_rows, invalid_cols, invalid_vals, False)


    def test_valid_square_4x4(self):
        board = '0 0 3 4 ' +\
                '0 3 0 1 ' +\
                '3 4 0 0 ' +\
                '0 1 0 3'

        valid_rows = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]
        valid_cols = [0, 0, 1, 0, 0, 2, 2, 2, 3, 0, 2, 2]
        valid_vals = [1, 2, 2, 2, 4, 2, 1, 2, 2, 2, 2, 4]
        invalid_rows = [0, 0, 1, 1, 2, 2, 3, 3, 5]
        invalid_cols = [1, 3, 2, 1, 0, 3, 0, 1, 4]
        invalid_vals = [3, 4, 4, 2, 1, 3, 5, 0, 1]
       
        self.check_square_valid_value(board, valid_rows, valid_cols, valid_vals)
        self.check_square_valid_value(board, invalid_rows, invalid_cols, invalid_vals, False)


    def test_valid_square_9x9(self):
        board = "9 7 0 0 0 0 0 0 0 " + \
                "4 0 0 8 0 0 0 0 0 " + \
                "0 0 0 0 4 0 7 0 0 " + \
                "0 0 0 0 9 0 6 0 0 " + \
                "0 0 0 2 0 0 0 3 0 " + \
                "0 0 0 0 0 1 0 0 8 " + \
                "0 4 0 0 6 0 9 0 0 " + \
                "0 0 5 0 0 0 0 0 0 " + \
                "0 0 0 0 0 3 0 0 1"
  
        valid_rows = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8]
        valid_cols = [2, 5, 7, 7, 1, 2, 4, 8, 0, 0, 8, 3, 2, 1, 5, 7, 8, 4, 5, 1, 3, 4, 6, 0, 7, 3, 2, 5, 1, 6, 8, 3, 3, 4, 2, 7]
        valid_vals = [1, 5, 4, 8, 1, 6, 0, 3, 6, 1, 5, 1, 8, 2, 7, 1, 5, 0, 4, 1, 3, 3, 2, 7, 0, 5, 3, 8, 1, 4, 6, 9, 5, 2, 8, 4]
        invalid_rows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -1, 8]
        invalid_cols = [3, 0, 2, 8, 5, 1, 1, 6, 7, 4, 16, 9]
        invalid_vals = [-7, 0, 7, 10, 3, 8, 4, 1, 3, 0, 5, 4]

        self.check_square_valid_value(board, valid_rows, valid_cols, valid_vals)
        self.check_square_valid_value(board, invalid_rows, invalid_cols, invalid_vals, False)



class Test_Sudoku_Solve(unittest.TestCase):

    def check_puzzle_solved(self, board, solution_expected=None):
        puzzle = Sudoku.Sudoku(board) 
        is_solved = puzzle.solve_sudoku()
        is_solved_check = puzzle.is_solved()
        solution_result = puzzle.get_puzzle()

        self.assertTrue(is_solved, "expected True for solvable puzzle \n{}".format(
            Sudoku.render(Sudoku.Sudoku(board).get_puzzle())
        ))
        self.assertTrue(is_solved_check, "expected correct solved puzzle, instead got \n{}".format(
            Sudoku.render(solution_result)
        ))

        if solution_expected:
            self.assertEqual(solution_result, solution_expected, "expected correct and only solution"+\
            " for puzzle. Expected \n{}\n but instead got \n{}".format(
                Sudoku.render(solution_expected), Sudoku.render(solution_result)
            ))


    def test_solve_empty(self):
        for sl in [1, 4, 9]:
            board = "0 "*(sl**2)
            self.check_puzzle_solved(board)


    def test_solve_incomplete_4x4(self):
        board = '4 0 3 2 ' +\
                '0 3 0 1 ' +\
                '3 2 0 0 ' +\
                '0 4 0 3'
        solution_expected = [['4', '1', '3', '2'], 
                             ['2', '3', '4', '1'], 
                             ['3', '2', '1', '4'], 
                             ['1', '4', '2', '3']]
        self.check_puzzle_solved(board, solution_expected)


    def test_solve_incomplete_9x9_1(self):
        board = '9 6 0 0 0 8 3 7 0 ' +\
                '0 2 0 4 0 3 9 0 1 ' +\
                '0 3 4 0 1 0 0 0 6 ' +\
                '6 0 0 0 0 0 7 0 0 ' +\
                '0 5 9 0 0 0 6 1 0 ' +\
                '0 0 7 0 0 0 0 0 5 ' +\
                '1 0 0 0 2 0 4 3 0 ' +\
                '5 0 3 9 0 4 0 6 0 ' +\
                '0 9 2 1 0 0 0 5 7'
        solution_expected_board = '9 6 1 2 5 8 3 7 4 ' +\
                                  '7 2 5 4 6 3 9 8 1 ' +\
                                  '8 3 4 7 1 9 5 2 6 ' +\
                                  '6 1 8 5 9 2 7 4 3 ' +\
                                  '2 5 9 3 4 7 6 1 8 ' +\
                                  '3 4 7 6 8 1 2 9 5 ' +\
                                  '1 7 6 8 2 5 4 3 9 ' +\
                                  '5 8 3 9 7 4 1 6 2 ' +\
                                  '4 9 2 1 3 6 8 5 7'
        solution_expected = Sudoku.Sudoku(solution_expected_board).get_puzzle()
        self.check_puzzle_solved(board, solution_expected)


    def test_solve_incomplete_9x9_2(self):
        board = '0 0 0 6 0 0 4 0 0 ' +\
                '7 0 0 0 0 3 6 0 0 ' +\
                '0 0 0 0 9 1 0 8 0 ' +\
                '0 0 0 0 0 0 0 0 0 ' +\
                '0 5 0 1 8 0 0 0 3 ' +\
                '0 0 0 3 0 6 0 4 5 ' +\
                '0 4 0 2 0 0 0 6 0 ' +\
                '9 0 3 0 0 0 0 0 0 ' +\
                '0 2 0 0 0 0 1 0 0'
        solution_expected_board = '5 8 1 6 7 2 4 3 9 ' +\
                                  '7 9 2 8 4 3 6 5 1 ' +\
                                  '3 6 4 5 9 1 7 8 2 ' +\
                                  '4 3 8 9 5 7 2 1 6 ' +\
                                  '2 5 6 1 8 4 9 7 3 ' +\
                                  '1 7 9 3 2 6 8 4 5 ' +\
                                  '8 4 5 2 1 9 3 6 7 ' +\
                                  '9 1 3 7 6 8 5 2 4 ' +\
                                  '6 2 7 4 3 5 1 9 8'
        solution_expected = Sudoku.Sudoku(solution_expected_board).get_puzzle()
        self.check_puzzle_solved(board, solution_expected)


    def test_solve_solved_1x1(self):
        board = "1"
        self.check_puzzle_solved(board)


    def test_solve_solved_4x4(self):
        board = '4 1 3 2 ' +\
                '2 3 4 1 ' +\
                '3 2 1 4 ' +\
                '1 4 2 3'  
        solution_expected = [['4', '1', '3', '2'], 
                             ['2', '3', '4', '1'], 
                             ['3', '2', '1', '4'], 
                             ['1', '4', '2', '3']]
        self.check_puzzle_solved(board, solution_expected)



class Test_Sudoku_Insert(unittest.TestCase):

    def test_insert(self):
        for sl in [1,4,9,16]:
            puzzle = Sudoku.Sudoku("0 "*(sl**2))

            for row in range(sl):
                for col in range(sl):
                    for value in range(0, sl+1):
                        self.assertTrue(puzzle.insert(row, col, value), 
                        "expected True for insert on puzzle \n{}\n with valid inputs: ({}, {}, {})".format(
                            Sudoku.render(puzzle.get_puzzle()), row, col, value
                        ))
                        if value != 0:
                            self.assertFalse(puzzle.insert(row, col, int(value*row/(col+1)) + 1), 
                            "expected False for insert on puzzle \n{}\n with invalid inputs: ({}, {}, {})".format(
                                Sudoku.render(puzzle.get_puzzle()), row, col, int(value*row/(col+1)) + 1
                            ))
                        puzzle.insert(row, col, 0)

            invalid_inputs = [[-1, 3, 1], [4, 10, -2], [-2,-1,-1], [0,0,sl*2]]
            for row, col, value in invalid_inputs:
                self.assertFalse(puzzle.insert(row, col, value),
                        "expected False for insert on puzzle \n{}\n with invalid inputs: ({}, {}, {})".format(
                            Sudoku.render(puzzle.get_puzzle()), row, col, value
                        ))


class Test_Sudoku_One_Solution(unittest.TestCase):

    def check_puzzle_one_sol(self, board, puzzle, is_solvable=False, is_one=False):
        if is_one:
            self.assertTrue(puzzle.is_one_sol(), 
                "expected True for is_one_solution on puzzle \n{}\n".format(Sudoku.render(puzzle.get_puzzle())))
        if is_solvable:
            self.assertTrue(puzzle.is_solvable(), 
                "expected True for is_solvable on puzzle \n{}\n".format(Sudoku.render(puzzle.get_puzzle())))
        if not is_one:
            self.assertFalse(puzzle.is_one_sol(), 
                "expected False for is_one_solution on puzzle \n{}\n".format(Sudoku.render(puzzle.get_puzzle()))) 
        if not is_solvable:
            self.assertFalse(puzzle.is_solvable(), 
                "expected False for is_solvable on puzzle \n{}\n".format(Sudoku.render(puzzle.get_puzzle()))) 

        self.assertEqual(puzzle.get_puzzle(), Sudoku.Sudoku(board).get_puzzle(),
            "expected puzzle to be not be mutated after is_one_sol and is_solvable calls. Expected \n{}\n, instead got \n{}\n".format(
                Sudoku.render(Sudoku.Sudoku(board).get_puzzle()), Sudoku.render(puzzle.get_puzzle())))


    def test_one_sol_empty(self):
        for sl in [1, 4, 9]:
            board = "0 "*(sl**2)
            puzzle = Sudoku.Sudoku(board)
            if sl == 1:
                self.check_puzzle_one_sol(board, puzzle, True, True)
            else:
                self.check_puzzle_one_sol(board, puzzle, True, False)

    def test_one_sol_4x4(self):
        board = '4 0 3 2 ' +\
                '0 3 0 1 ' +\
                '3 2 0 0 ' +\
                '0 4 0 3'
        puzzle = Sudoku.Sudoku(board)
        self.check_puzzle_one_sol(board, puzzle, True, True)

    def test_mult_sol_4x4(self):
        board = '1 2 0 0 ' +\
                '3 4 0 0 ' +\
                '0 0 0 0 ' +\
                '0 0 0 0'
        puzzle = Sudoku.Sudoku(board)
        self.check_puzzle_one_sol(board, puzzle, True, False)

    def test_no_sol_4x4(self):
        board = '0 0 3 0 ' +\
                '1 2 0 0 ' +\
                '0 4 2 3 ' +\
                '0 1 0 0'
        puzzle = Sudoku.Sudoku(board)
        self.check_puzzle_one_sol(board, puzzle, False, False)

    def test_one_sol_9x9(self):
        board = '9 6 0 0 0 8 3 7 0 ' +\
                '0 2 0 4 0 3 9 0 1 ' +\
                '0 3 4 0 1 0 0 0 6 ' +\
                '6 0 0 0 0 0 7 0 0 ' +\
                '0 5 9 0 0 0 6 1 0 ' +\
                '0 0 7 0 0 0 0 0 5 ' +\
                '1 0 0 0 2 0 4 3 0 ' +\
                '5 0 3 9 0 4 0 6 0 ' +\
                '0 9 2 1 0 0 0 5 7'
        puzzle = Sudoku.Sudoku(board)
        self.check_puzzle_one_sol(board, puzzle, True, True)

    def test_no_sol_9x9(self):
        board = '9 6 0 0 0 8 3 7 0 ' +\
                '0 2 0 4 0 3 9 0 1 ' +\
                '0 3 4 0 1 0 0 0 6 ' +\
                '6 0 0 0 0 0 7 0 0 ' +\
                '0 5 9 0 0 0 6 1 0 ' +\
                '0 0 7 0 0 2 0 0 5 ' +\
                '1 8 0 0 2 0 4 3 0 ' +\
                '5 0 3 9 0 4 0 6 0 ' +\
                '0 9 2 1 0 0 0 5 7'
        puzzle = Sudoku.Sudoku(board)
        self.check_puzzle_one_sol(board, puzzle, False, False) 

class Test_Create_Sudoku_Random(unittest.TestCase):

    def test_random_insertion_and_deletion(self):
        for sl in [1, 4, 9, 16]:
            creation = Sudoku.Create_Sudoku(sl)
            board = "0 "*(sl**2)
            puzzle = Sudoku.Sudoku(board)

            avail = [i for i in range(sl**2)] 
            deletions = []

            result = creation.random_insertion(puzzle, sl, avail, deletions)

            self.assertTrue(result <= sl, 
                "expected up to sl random insertions in empty Sudoku puzzle, instead got puzzle \n{}\n".format(Sudoku.render(puzzle.get_puzzle())))
            copy = puzzle.get_puzzle()
            for row in range(sl):
                for col in range(sl):
                    prev_value = copy[row][col]
                    puzzle.insert(row, col, 0)
                    self.assertTrue(puzzle.valid_square(row, col, int(prev_value)), 
                        "expected each value inserted to be valid, instead incorrect value {} at ({},{}) in puzzle \n{}".format(
                            prev_value, row, col, Sudoku.render(puzzle.get_puzzle())
                        ))
                    puzzle.insert(row, col, int(prev_value))

            self.assertEqual(creation.random_deletion(puzzle, sl, avail, deletions), result, 
                "expected all previous insertions to be deleted, leaving an empty puzzle. Instead got \n{}\n".format(Sudoku.render(puzzle.get_puzzle())))
            self.assertEqual(puzzle.get_puzzle(), Sudoku.Sudoku(board).get_puzzle(), "expected empty puzzle after deleting all insertions")

class Test_Sudoku_Create(unittest.TestCase):

    def check_one_sol_and_size(self, puzzle, sl):
        self.assertEqual(len(puzzle.get_puzzle()), sl, "expected {} rows in puzzle, instead got puzzle \n{}\n".format(
            sl, Sudoku.render(puzzle.get_puzzle())
        ))
        for i in range(sl):
            self.assertEqual(len(puzzle.get_puzzle()[i]), sl, "expected {} columns in puzzle, instead got puzzle \n{}\n".format(
                sl, Sudoku.render(puzzle.get_puzzle())
            ))
        self.assertTrue(puzzle.is_one_sol(), "expected created puzzle to have one solution, instead got puzzle \n{}\n".format(
            Sudoku.render(puzzle.get_puzzle())
        ))


    def test_create_1x1(self):
        puzzle = Sudoku.Create_Sudoku(1).create()
        self.check_one_sol_and_size(puzzle, 1)

    def test_create_4x4(self):
        for _ in range(5):
            puzzle = Sudoku.Create_Sudoku(4).create()
            self.check_one_sol_and_size(puzzle, 4)

    def test_create_9x9(self):
        puzzle = Sudoku.Create_Sudoku(9).create()
        self.check_one_sol_and_size(puzzle, 9)


if __name__ == '__main__':
    unittest.main(verbosity=2)
