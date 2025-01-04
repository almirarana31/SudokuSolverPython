import tkinter as tk
from tkinter import messagebox
import random
import time
import sys


def is_valid(grid, row, col, num):
    # check if placing number is valid
    global operations
    for x in range(9):
        operations += 1
        if grid[row][x] == num or grid[x][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            operations += 1
            if grid[i][j] == num:
                return False
    return True


def has_duplicates(grid):
    # checking for duplicates in rows, columns, subgrids
    for i in range(9):
        row_seen = set()
        col_seen = set()
        for j in range(9):
            if grid[i][j] != 0:
                if grid[i][j] in row_seen:
                    return True
                row_seen.add(grid[i][j])
            if grid[j][i] != 0:
                if grid[j][i] in col_seen:
                    return True
                col_seen.add(grid[j][i])
    for start_row in range(0, 9, 3):
        for start_col in range(0, 9, 3):
            subgrid_seen = set()
            for i in range(start_row, start_row + 3):
                for j in range(start_col, start_col + 3):
                    if grid[i][j] != 0:
                        if grid[i][j] in subgrid_seen:
                            return True
                        subgrid_seen.add(grid[i][j])
    return False


operations = 0  # counts recursive calls and validation checks
max_recursion_depth = 0  # tracks the maximum recursion depth
current_recursion_depth = 0 # tracks current depth

def initialize_possibilities(grid):
    # initialize possibilities for each cell based on rules
    possibilities = {}
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                possibilities[(row, col)] = {num for num in range(1, 10) if is_valid(grid, row, col, num)}
            else:
                possibilities[(row, col)] = set()  # filled cells have no possibilities
    return possibilities


def update_possibilities(grid, possibilities, row, col, num):
    # update possibilities
    for x in range(9):
        possibilities.get((row, x), set()).discard(num)  # row
        possibilities.get((x, col), set()).discard(num)  # column

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            possibilities.get((i, j), set()).discard(num)


def solve_sudoku(grid):
    """Solve the Sudoku puzzle using optimized backtracking with constraint propagation."""
    global operations, max_recursion_depth, current_recursion_depth
    possibilities = initialize_possibilities(grid)

    def backtrack(possibilities):
        global operations, max_recursion_depth, current_recursion_depth
        # increment recursion
        current_recursion_depth += 1
        max_recursion_depth = max(max_recursion_depth, current_recursion_depth)

        if all(grid[row][col] != 0 for row in range(9) for col in range(9)):
            current_recursion_depth -= 1 # backtracking recursion
            return True  # puzzle is solved

        # select minimum possibilities
        row, col = min((cell for cell in possibilities if grid[cell[0]][cell[1]] == 0),
                       key=lambda cell: len(possibilities[cell]),
                       default=(None, None))

        if row is None:  # no more cells to solve
            current_recursion_depth -= 1  # backtracking recursion before returning
            return True

        for num in sorted(possibilities[(row, col)]):  # try possible values
            if is_valid(grid, row, col, num):
                grid[row][col] = num  # place number
                operations += 1
                # backup possibilities and update
                backup = {key: set(values) for key, values in possibilities.items()}
                update_possibilities(grid, possibilities, row, col, num)

                if backtrack(possibilities):
                    current_recursion_depth -= 1  # backtracking recursion before returning
                    return True  # puzzle solved
                # backtrack
                grid[row][col] = 0
                possibilities = backup  # restore possibilities

        current_recursion_depth -= 1  # backtrack recursion depth before returning
        return False  # no solution found

    return backtrack(possibilities)


def solve_sudoku_gui():
    # solve sudoku and update GUI
    global operations, max_recursion_depth, current_recursion_depth

    # reset counters
    operations = 0
    max_recursion_depth = 0
    current_recursion_depth = 0

    # read the filled grid
    grid_copy = []
    filled_cells = 0
    for i in range(9):
        row = []
        for j in range(9):
            val = entries[i][j].get().strip()
            if val == "":
                row.append(0)
            else:
                try:
                    num = int(val)
                    if num < 1 or num > 9:
                        raise ValueError("Number out of range.")
                    row.append(num)
                    filled_cells += 1
                except ValueError:
                    messagebox.showerror(
                        "Invalid Input",
                        f"Invalid input at row {i + 1}, column {j + 1}. Only digits 1-9 are allowed.",
                    )
                    return
        grid_copy.append(row)

    # check for minimum 17 clues
    if filled_cells < 17:
        messagebox.showerror("Error", "The board must have at least 17 clues to be solvable.")
        return

    # check for duplicates
    if has_duplicates(grid_copy):
        messagebox.showerror("Error", "The grid contains duplicates and cannot be solved.")
        return

    # start the solving process
    start_time = time.time()
    if solve_sudoku(grid_copy):  # solve using backtracking
        end_time = time.time()

        # update the GUI with the solved grid
        for i in range(9):
            for j in range(9):
                entries[i][j].config(state="normal")
                entries[i][j].delete(0, tk.END)
                entries[i][j].insert(0, str(grid_copy[i][j]))
                entries[i][j].config(state="disabled", bg="#DFF2FF")

        # calculate statistics
        time_taken = end_time - start_time
        space_complexity = sys.getsizeof(grid_copy) + max_recursion_depth * sys.getsizeof(grid_copy[0])

        # display statistics
        display_statistics(operations, time_taken, filled_cells, 81 - filled_cells, space_complexity)
    else:
        messagebox.showerror("Error", "No solution exists for this puzzle!")


def display_statistics(operations, time_taken, hints, empty_cells, space_complexity):
    # display statistics such as num operations, time taken, etc.
    stats_label.config(
        text=(
            f"Operations: {operations}\n"
            f"Time Taken: {time_taken:.6f} seconds\n"
            f"Number of Hints: {hints}\n"
            f"Empty Cells: {empty_cells}\n"
            f"Space Complexity: {space_complexity} bytes\n"
            f"Max Recursion Depth: {max_recursion_depth}"
        )
    )


def clear_board():
    # clear the board
    for i in range(9):
        for j in range(9):
            entries[i][j].config(state="normal")
            entries[i][j].delete(0, tk.END)
            entries[i][j].insert(0, "")
            entries[i][j].config(state="normal", bg="white")
    stats_label.config(text="")


def restrict_input(event):
    # restrict input to single digits and replace any invalid input
    widget = event.widget
    if not widget.get().isdigit() or len(widget.get()) > 1:
        widget.delete(0, tk.END)  # Clear the cell
    if event.char.isdigit() and 1 <= int(event.char) <= 9:
        widget.delete(0, tk.END)  # Replace any existing input
        widget.insert(0, event.char)


def navigate(event):
    # keyboard navigation
    global current_row, current_col
    if event.keysym == "Up":
        current_row = (current_row - 1) % 9
    elif event.keysym == "Down":
        current_row = (current_row + 1) % 9
    elif event.keysym == "Left":
        current_col = (current_col - 1) % 9
    elif event.keysym == "Right":
        current_col = (current_col + 1) % 9
    entries[current_row][current_col].focus_set()


# GUI
root = tk.Tk()
root.title("Sudoku Solver")
root.geometry("650x760")
root.resizable(False, False)

title_label = tk.Label(root, text="Sudoku Solver", font=("Helvetica", 18, "bold"), bg="#FFDEE9", pady=10)
title_label.pack(fill="x")

frame = tk.Frame(root, bg="#FFDEE9")
frame.pack()

entries = [[None for _ in range(9)] for _ in range(9)]

for grid_row in range(3):
    for grid_col in range(3):
        subgrid_frame = tk.Frame(
            frame,
            bg="#FFDEE9",
            highlightbackground="black",
            highlightthickness=2,
            padx=1,
            pady=1,
        )
        subgrid_frame.grid(row=grid_row, column=grid_col, padx=1, pady=1)

        for i in range(3):
            for j in range(3):
                row = grid_row * 3 + i
                col = grid_col * 3 + j
                entry = tk.Entry(
                    subgrid_frame,
                    width=2,
                    font=("Helvetica", 14),
                    justify="center",
                    bg="white",
                )
                entry.grid(row=i, column=j, padx=1, pady=1, ipadx=5, ipady=5)
                entry.bind("<KeyRelease>", restrict_input)  # restrict input to single digits
                entries[row][col] = entry

button_frame = tk.Frame(root, bg="#FFDEE9")
button_frame.pack(pady=20)

solve_button = tk.Button(
    button_frame,
    text="Solve",
    font=("Helvetica", 14),
    bg="#A5FFAA",
    width=20,
    command=solve_sudoku_gui,
)
solve_button.pack(pady=5)

clear_button = tk.Button(
    button_frame,
    text="Clear Board",
    font=("Helvetica", 14),
    bg="#FFD580",
    width=20,
    command=clear_board,
)
clear_button.pack(pady=5)

stats_label = tk.Label(
    root, text="", font=("Helvetica", 12), bg="#FFDEE9", pady=5, justify="left"
)
stats_label.pack(fill="x")

root.configure(bg="#FFDEE9")
frame.configure(bg="#FFDEE9")

current_row, current_col = 0, 0
entries[current_row][current_col].focus_set()
root.bind("<Up>", navigate)
root.bind("<Down>", navigate)
root.bind("<Left>", navigate)
root.bind("<Right>", navigate)

root.mainloop()
