# Sudoku Solver Python
Sudoku Solver Backtracking Development (From Recursive to Iterative)

**User Manual: Using The Sudoku Solver**

**Description:** This is a Sudoku Solver that requires a minimum of 17 clues. If there is a valid unique solution, the solver will provide it and show the execution time and estimated space used. The solver is capable of receiving input for an unsolved board and clearing the board. Follow these steps to ensure a smooth experience with the solver.
When you first start up the solver, it should look like this:

![initial state](https://github.com/user-attachments/assets/bf9e246f-dd26-4608-8365-7e78bafbc229)

**To Enter a Sudoku Puzzle**

**Inputting Numbers:**
- Click on any cell in the grid to select it.
- Type a single digit (1-9) to input the number into the cell.
- The solver only allows digits from 1-9. Any number or letter outside this will be cleared automatically or seen as an invalid input.

  ![error message 3](https://github.com/user-attachments/assets/83dd3186-2562-43f3-b7a4-9ae14a251203)

- The solver requires at least 17 clues (pre-filled numbers) to guarantee solvability and a unique solution. The solver will display an error message if the puzzle is not filled correctly.
  
  ![error message 1](https://github.com/user-attachments/assets/1a368d86-ae8a-4cbf-b805-cc13de4d0cde)
  
- Ensure the grid has no duplicate numbers in each row, column, or subgrid, or the solver will reject the input.
  
![error message 2](https://github.com/user-attachments/assets/08e02851-1451-47d3-a799-d3628631523a)


**Navigating the Grid**
- Use the arrow keys on your keyboard to move between cells quickly or click each cell individually.

**Solving the Puzzle**

**Starting the Solver**
- Once the puzzle has been inputted, click the green “Solve” button located below the grid.
  
![solve button](https://github.com/user-attachments/assets/679e83ba-f99f-4b76-af57-ea903c375517)

- After the button has been pressed, the solver will use advanced algorithms to finish the puzzle in real time.
- If the puzzle is solvable, the solution will appear in the grid and previously filled cells will be highlighted for clarity.
  
  ![solved board](https://github.com/user-attachments/assets/b2a7e572-5666-4c59-9d1d-d4c408414a63)
  
- If the puzzle has no solution, a message will pop up stating there is no solution.
  
![error message 4](https://github.com/user-attachments/assets/4d190d8e-31ce-4c43-8b86-622040ca56b4)


**Clearing the Board**

**Resetting the Grid**
- Click the red “Clear Board” button to erase all entries and reset the grid and the statistics to its initial state.
  
  ![clear button](https://github.com/user-attachments/assets/adb02ad7-68ac-4bdd-8cf1-b337ad571e41)

- This should be used when you would like to start over and input a new puzzle.
