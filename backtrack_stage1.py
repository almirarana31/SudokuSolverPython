import tkinter as tk
from tkinter import messagebox
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
    # checking for duplicates
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
current_recursion_depth = 0

def solve_sudoku(grid):
    # recursive solver
    global operations, max_recursion_depth, current_recursion_depth

    current_recursion_depth += 1
    max_recursion_depth = max(max_recursion_depth, current_recursion_depth)

    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:  # find empty cell
                for num in range(1, 10):  # try numbers 1-9
                    if is_valid(grid, row, col, num):  # check if valid
                        grid[row][col] = num
                        operations += 1  # count operation
                        if solve_sudoku(grid):  # recursive call
                            current_recursion_depth -= 1
                            return True
                        grid[row][col] = 0  # backtracking
                current_recursion_depth -= 1
                return False  # if no solution
    current_recursion_depth -= 1
    return True

def solve_sudoku_gui():
    # solve sudoku and update GUI
    global operations, max_recursion_depth, current_recursion_depth

    # reset counters
    operations = 0
    max_recursion_depth = 0
    current_recursion_depth = 0

    # read the user-filled grid
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
            f"Space Complexity: {space_complexity} bytes"
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

frame = tk.Frame(root)
frame.pack()

entries = [[None for _ in range(9)] for _ in range(9)]
for i in range(9):
    for j in range(9):
        entry = tk.Entry(frame, width=2, font=("Helvetica", 14), justify="center", bg="white")
        entry.grid(row=i, column=j, padx=5, pady=5, ipadx=5, ipady=5)
        entry.bind("<KeyRelease>", restrict_input)
        entries[i][j] = entry

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
