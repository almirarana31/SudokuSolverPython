# Sudoku Solver Python
Sudoku Solver Backtracking Development (From Recursive to Iterative)

**User Manual: Using The Sudoku Solver**

**Description:** This is a Sudoku Solver that requires a minimum of 17 clues. If there is a valid unique solution, the solver will provide it and show the execution time and estimated space used. The solver is capable of receiving input for an unsolved board and clearing the board. Follow these steps to ensure a smooth experience with the solver.
When you first start up the solver, it should look like this:
!(https://github.com/almirarana31/SudokuSolverPython/blob/main/initial state.png?raw=true)

**To Enter a Sudoku Puzzle**

**Inputting Numbers:**
- Click on any cell in the grid to select it.
- Type a single digit (1-9) to input the number into the cell.
- The solver only allows digits from 1-9. Any number or letter outside this will be cleared automatically or seen as an invalid input.
- The solver requires at least 17 clues (pre-filled numbers) to guarantee solvability and a unique solution. The solver will display an error message if the puzzle is not filled correctly.
- Ensure the grid has no duplicate numbers in each row, column, or subgrid, or the solver will reject the input.

**Navigating the Grid**
- Use the arrow keys on your keyboard to move between cells quickly or click each cell individually.

**Solving the Puzzle**

**Starting the Solver**
- Once the puzzle has been inputted, click the green “Solve” button located below the grid.
- After the button has been pressed, the solver will use advanced algorithms to finish the puzzle in real time.
- If the puzzle is solvable, the solution will appear in the grid and previously filled cells will be highlighted for clarity. 
- If the puzzle has no solution, a message will pop up stating there is no solution.

**Clearing the Board**

**Resetting the Grid**
- Click the red “Clear Board” button to erase all entries and reset the grid and the statistics to its initial state.
- This should be used when you would like to start over and input a new puzzle.
