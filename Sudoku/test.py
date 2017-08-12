import SudokuSolver
import traceback
import json


def main():
    try:
        good_input = json.loads(
            "[[0,7,0,6,0,9,0,8,0],[4,0,2,0,0,0,0,0,3],[0,0,9,4,1,0,2,5,0],[8,0,0,0,9,0,3,0,5],[0,0,4,8,0,5,6,0,0],"
            "[5,0,1,0,7,0,0,0,9],[0,6,8,0,5,2,4,0,0],[1,0,0,0,0,0,7,0,6],[0,4,0,3,0,1,0,9,0]]")
        bad_input = json.loads(
            "[[1.2,7,1,6,0,9,0,8,0],[4,0,2,0,0,0,0,0,3],[0,0,9,4,1,0,2,5,0],[8,0,0,0,9,0,3,0,5],[0,0,4,8,0,5,6,0,0],"
            "[5,0,1,0,7,0,0,0,9],[0,6,8,0,5,2,4,0,0],[1,0,0,0,0,0,7,0,6],[0,4,0,3,0,1,0,9,0]]")
        puzzle = SudokuSolver.SudokuPuzzle(9)
        print(str(puzzle))
        puzzle.set_inputs(bad_input)
        puzzle.compute_solution()
        print(puzzle.values)

    except Exception as error:
        print(type(error))
        print('Error: ' + str(error))
        traceback.print_exc()

    finally:
        print('finally')


if __name__ == '__main__':
    main()
