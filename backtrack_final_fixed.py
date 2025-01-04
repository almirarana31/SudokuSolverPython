import tkinter as tk
from tkinter import messagebox
import time
import sys

def initialize_possibilities_bitmask(grid):
    # initialize possibilities with bitmasking
    possibilities = {}
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                possibilities[(row, col)] = (1 << 9) - 1
            else:
                possibilities[(row, col)] = 0
    return possibilities

def update_possibilities_bitmask(possibilities, row, col, num, action="remove"):
    # update possibilities with bitmasking
    mask = ~(1 << (num - 1)) # mask to translate number to bitmask
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)

    for x in range(9):
        if action == "remove":
            possibilities[(row, x)] &= mask # remove from row
            possibilities[(x, col)] &= mask # remove from column
        elif action == "restore":
            possibilities[(row, x)] |= (1 << (num - 1)) # restore to row
            possibilities[(x, col)] |= (1 << (num - 1)) # restore to column

    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if action == "remove":
                possibilities[(i, j)] &= mask # remove from subgrid
            elif action == "restore":
                possibilities[(i, j)] |= (1 << (num - 1))  # restore to subgrid

def solve_sudoku_iterative(grid):
    # solver using iteration
    possibilities = initialize_possibilities_bitmask(grid)
    stack = []
    operations = 0

    # update grid from the initial state
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                stack.append((row, col, possibilities[(row, col)]))

    while stack:
        row, col, bitmask = stack.pop()

        if grid[row][col] != 0:  # cell thats already filled
            continue

        found_valid_number = False
        for num in range(1, 10):
            if bitmask & (1 << (num - 1)):  # check if number is valid
                grid[row][col] = num
                operations += 1
                update_possibilities_bitmask(possibilities, row, col, num, action="remove")
                # add the next empty cell
                next_cell_found = False
                for next_row in range(9):
                    for next_col in range(9):
                        if grid[next_row][next_col] == 0:
                            stack.append((next_row, next_col, possibilities[(next_row, next_col)]))
                            next_cell_found = True
                            break
                    if next_cell_found:
                        break

                found_valid_number = True
                break

        if not found_valid_number:
            grid[row][col] = 0 # backtrack
            if num > 0:  # only restore if actually tried a number
                update_possibilities_bitmask(possibilities, row, col, num, action="restore")

    return all(grid[row][col] != 0 for row in range(9) for col in range(9)), possibilities, operations

def solve_sudoku_gui():
    # solve sudoku and update GUI
    grid_copy = []
    original_grid = []
    filled_cells = 0

    for i in range(9):
        row = []
        original_row = []
        for j in range(9):
            val = entries[i][j].get().strip()
            if val == "":
                row.append(0)
                original_row.append(0)
            else:
                try:
                    num = int(val)
                    if num < 1 or num > 9:
                        messagebox.showerror(
                            "Invalid Input",
                            f"Invalid input at row {i + 1}, column {j + 1}. Only digits 1-9 are allowed."
                        )
                        return
                    row.append(num)
                    original_row.append(num)
                    filled_cells += 1
                except ValueError:
                    messagebox.showerror(
                        "Invalid Input",
                        f"Invalid input at row {i + 1}, column {j + 1}. Only digits 1-9 are allowed."
                    )
                    return
        grid_copy.append(row)
        original_grid.append(original_row)

    # check for minimum 17 clues
    if filled_cells < 17:
        messagebox.showerror(
            "Insufficient Clues",
            "The puzzle must have at least 17 clues to guarantee a unique solution."
        )
        return

    # check for duplicates
    if has_duplicates(grid_copy):
        messagebox.showerror(
            "Invalid Grid",
            "The grid contains duplicate numbers in a row, column, or subgrid."
        )
        return

    # start the solving process
    start_time = time.time()
    solved, possibilities, operations = solve_sudoku_iterative(grid_copy)
    end_time = time.time()

    if solved:
        # update the GUI with the solved grid
        for i in range(9):
            for j in range(9):
                entries[i][j].config(state="normal")
                entries[i][j].delete(0, tk.END)
                entries[i][j].insert(0, str(grid_copy[i][j]))
                entries[i][j].config(state="readonly")

        highlight_original_cells(entries, original_grid)

        time_taken = end_time - start_time
        space_complexity = sys.getsizeof(grid_copy) + sys.getsizeof(possibilities)
        display_statistics(operations, time_taken, filled_cells, 81 - filled_cells, space_complexity)
    else:
        messagebox.showerror("No Solution", "This puzzle has no valid solution!")

def clear_board():
    # clear board reset stats
    for i in range(9):
        for j in range(9):
            entries[i][j].config(state="normal")
            entries[i][j].delete(0, tk.END)
            entries[i][j].config(bg="white")
            entries[i][j].config(readonlybackground="white")
    stats_label.config(text="")

def restrict_input(event):
   # restrict input
    widget = event.widget
    if event.char.isdigit():
        if not (1 <= int(event.char) <= 9):
            widget.delete(0, tk.END)
            return "break"
        widget.delete(0, tk.END)
        widget.insert(0, event.char)
        return "break"
    elif event.char:  # if there are non-digit characters
        widget.delete(0, tk.END)
        return "break"

def navigate(event):
    # handle keyboard navigation
    current = event.widget

    current_info = current.grid_info()
    subgrid_info = current.master.grid_info()

    global_row = subgrid_info['row'] * 3 + current_info['row']
    global_col = subgrid_info['column'] * 3 + current_info['column']

    if event.keysym == 'Up':
        next_row = (global_row - 1) % 9
        next_col = global_col
    elif event.keysym == 'Down':
        next_row = (global_row + 1) % 9
        next_col = global_col
    elif event.keysym == 'Left':
        next_row = global_row
        next_col = (global_col - 1) % 9
    elif event.keysym == 'Right':
        next_row = global_row
        next_col = (global_col + 1) % 9
    else:
        return

    entries[next_row][next_col].focus_set()

def has_duplicates(grid):
    # check rows and columns for duplicates
    for i in range(9):
        row_seen = set()
        col_seen = set()
        for j in range(9):
            # check for duplicates in the row
            if grid[i][j] != 0:
                if grid[i][j] in row_seen:
                    return True
                row_seen.add(grid[i][j])
            # check for duplicates in the column
            if grid[j][i] != 0:
                if grid[j][i] in col_seen:
                    return True
                col_seen.add(grid[j][i])

    # check subgrids for duplicates
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

def display_statistics(operations, time_taken, hints, empty_cells, space_complexity):
    # display solving statistics
    stats_label.config(
        text=(
            f"Operations: {operations}\n"
            f"Time Taken: {time_taken:.6f} seconds\n"
            f"Number of Hints: {hints}\n"
            f"Empty Cells: {empty_cells}\n"
            f"Space Complexity: {space_complexity} bytes"
        )
    )

def highlight_original_cells(entries, original_grid):
    # highlight solved cells for clarity
    for i in range(9):
        for j in range(9):
            if original_grid[i][j] != 0:
                entries[i][j].config(bg="#FFFFFF")
                entries[i][j].config(readonlybackground="#FFFFFF")
            else:
                entries[i][j].config(bg="#DFF2FF")  # light blue for solved cells
                entries[i][j].config(readonlybackground="#DFF2FF")

# GUI setup
root = tk.Tk()
root.title("Sudoku Solver")
root.geometry("650x760")
root.resizable(False, False)

title_label = tk.Label(
    root,
    text="Sudoku Solver",
    font=("Helvetica", 18, "bold"),
    bg="#FFDEE9",
    pady=10
)
title_label.pack(fill="x")

main_frame = tk.Frame(
    root,
    bg="#FFF3D4",
    padx=4,
    pady=4,
    relief="raised",
    bd=2
)
main_frame.pack(padx=10, pady=10)

entries = [[None for _ in range(9)] for _ in range(9)]

for box_i in range(3):
    for box_j in range(3):
        box_frame = tk.Frame(
            main_frame,
            bg="#FFF3D4",
            padx=1,
            pady=1,
            bd=1
        )
        box_frame.grid(row=box_i, column=box_j, padx=1, pady=1)

        for i in range(3):
            for j in range(3):
                global_i = box_i * 3 + i
                global_j = box_j * 3 + j
                entry = tk.Entry(
                    box_frame,
                    width=2,
                    font=("Helvetica", 14),
                    justify="center",
                    bg="white"
                )
                entry.grid(row=i, column=j, padx=1, pady=1, ipadx=5, ipady=5)
                entry.bind("<KeyPress>", restrict_input)
                entry.bind("<Up>", navigate)
                entry.bind("<Down>", navigate)
                entry.bind("<Left>", navigate)
                entry.bind("<Right>", navigate)
                entries[global_i][global_j] = entry

button_frame = tk.Frame(root, bg="#FFDEE9")
button_frame.pack(pady=20)

solve_button = tk.Button(
    button_frame,
    text="Solve",
    font=("Helvetica", 14),
    bg="#A5FFAA",
    width=20,
    command=solve_sudoku_gui
)
solve_button.pack(pady=5)

clear_button = tk.Button(
    button_frame,
    text="Clear Board",
    font=("Helvetica", 14),
    bg="#F88379",
    width=20,
    command=clear_board
)
clear_button.pack(pady=5)

stats_label = tk.Label(
    root,
    text="",
    font=("Helvetica", 12),
    bg="#FFDEE9",
    pady=5,
    justify="left"
)
stats_label.pack(fill="x")

root.configure(bg="#FFDEE9")

root.mainloop()
