# Sudoku Solver using CSP (Constraint Satisfaction Problem)

A Python implementation of a Sudoku solver that models the puzzle as a **Constraint Satisfaction Problem (CSP)** and solves it using **backtracking search**.

---

## Table of Contents

- [Overview](#overview)
- [What is a CSP?](#what-is-a-csp)
- [How Sudoku Maps to a CSP](#how-sudoku-maps-to-a-csp)
- [Algorithm](#algorithm)
- [Project Structure](#project-structure)
- [Code Walkthrough](#code-walkthrough)
- [How to Run](#how-to-run)
- [Example Output](#example-output)
- [Complexity](#complexity)
- [Possible Improvements](#possible-improvements)

---

## Overview

Sudoku is a 9x9 grid puzzle where some cells start filled in and the rest must be completed so that every row, column, and 3x3 box contains the digits 1–9 exactly once.

This project solves that puzzle by treating it as a CSP and searching for a valid assignment of numbers to empty cells using backtracking.

---

## What is a CSP?

A Constraint Satisfaction Problem is formally defined by three components:

1. **Variables** — the things that need values assigned
2. **Domains** — the set of possible values each variable can take
3. **Constraints** — rules restricting which combinations of values are allowed

Solving a CSP means finding an assignment of values to all variables such that every constraint is satisfied.

---

## How Sudoku Maps to a CSP

| CSP Concept | Sudoku Equivalent |
|---|---|
| Variables | The 81 cells of the grid (specifically, the empty ones) |
| Domain | `{1, 2, 3, 4, 5, 6, 7, 8, 9}` for each empty cell |
| Constraints | No repeated digit in any row, column, or 3x3 box |

| CSP Concept | Code |
|---|---|
| Select unassigned variable | `find_empty(grid)` |
| Domain of the variable | `range(1, 10)` |
| Constraint check | `is_valid(grid, row, col, num)` |
| Assign value | `grid[row][col] = num` |
| Recursive search | `solve(grid)` calling itself |
| Backtrack on failure | `grid[row][col] = 0` |

---

## Algorithm

The solver uses **backtracking search**, the standard general-purpose algorithm for solving CSPs:

1. Find the next empty (unassigned) cell.
2. If there are no empty cells left, the puzzle is solved — return success.
3. Otherwise, try each value `1–9` in that cell.
4. For each value, check whether it violates the row, column, or box constraint.
5. If the value is valid, place it and recursively try to solve the rest of the grid.
6. If the recursive call succeeds, propagate success back up.
7. If it fails (leads to a dead end later), undo the placement (**backtrack**) and try the next value.
8. If no value from 1–9 works for this cell, return failure so the previous cell can try a different value.

This is a **depth-first search** through the space of possible assignments, pruned at each step by the constraint check — a value is only tried if it doesn't immediately violate a rule.

---

## Project Structure

The solver is broken into four small functions, each responsible for one part of the CSP:

- **`is_valid(grid, row, col, num)`** — the constraint checker. Verifies that placing `num` at `(row, col)` doesn't break the row, column, or box rule.
- **`find_empty(grid)`** — variable selection. Scans the grid and returns the coordinates of the next unassigned cell, or `None` if the grid is full.
- **`solve(grid)`** — the backtracking search itself. Recursively assigns values to empty cells, backtracking on failure.
- **`print_grid(grid)`** — formats and displays the grid in a readable Sudoku layout with box separators.

---

## Code Walkthrough

### 1. Grid representation

The board is a list of 9 lists (rows), each containing 9 integers. `0` represents an empty cell — it is a placeholder, not a valid Sudoku digit (Sudoku only ever uses 1–9).

```python
grid[row][col]  # value at a given cell, both indices range 0–8
```

### 2. Constraint check — `is_valid`

Checks all three Sudoku rules for a candidate number at a given position:

- **Row check** — scans across `grid[row][0..8]`
- **Column check** — scans down `grid[0..8][col]`
- **Box check** — finds the top-left corner of the relevant 3x3 box using integer division (`(row // 3) * 3`, `(col // 3) * 3`), then scans all 9 cells in that box

If the number is found in any of the three, the placement is invalid.

### 3. Finding the next variable — `find_empty`

Scans row by row, column by column, and returns the coordinates of the first cell equal to `0`. Returns `None` once no empty cells remain — this is how the algorithm knows the puzzle is complete.

### 4. Backtracking search — `solve`

Ties everything together: finds an empty cell, tries each candidate value, checks validity, assigns and recurses on success, undoes the assignment (`grid[row][col] = 0`) on failure before trying the next candidate.

The undo step is essential — `is_valid` always reads the grid's *current* state, so any value left in place incorrectly restricts later constraint checks in the same row, column, or box.

### 5. Display — `print_grid`

Prints the grid with `|` separators between box columns and `-` separator lines between box rows, so the output resembles an actual Sudoku grid rather than a flat list.

---

## How to Run

1. Save the code as `sudoku_solver.py`.
2. Edit the `grid` variable at the top with your own puzzle (`0` for empty cells).
3. Run:

```bash
python sudoku_solver.py
```

If a solution exists, the completed grid is printed. Otherwise, `"No solution exists"` is printed.

---

## Example Output

```
5 3 4 | 6 7 8 | 9 1 2
6 7 2 | 1 9 5 | 3 4 8
1 9 8 | 3 4 2 | 5 6 7
- - - - - - - - - - - -
8 5 9 | 7 6 1 | 4 2 3
4 2 6 | 8 5 3 | 7 9 1
7 1 3 | 9 2 4 | 8 5 6
- - - - - - - - - - - -
9 6 1 | 5 3 7 | 2 8 4
2 8 7 | 4 1 9 | 6 3 5
3 4 5 | 2 8 6 | 1 7 9
```

---

## Complexity

- **Worst-case time complexity:** O(9^m), where `m` is the number of empty cells — in the worst case, the algorithm tries up to 9 values for each empty cell before backtracking.
- **Space complexity:** O(m) for the recursion stack, where `m` is the number of empty cells (depth of recursion equals number of cells assigned so far).

In practice, the constraint check prunes the search space heavily, so real puzzles solve far faster than the theoretical worst case.

---

## Possible Improvements

Plain backtracking is the baseline CSP-solving approach. It can be made significantly faster with standard CSP techniques:

- **Forward checking** — after each assignment, immediately eliminate that value from the domains of related cells (same row/column/box), catching dead ends earlier instead of discovering them deep in the recursion.
- **Constraint propagation (e.g. AC-3)** — proactively enforce arc consistency across all cells before and during search, shrinking domains further.
- **Minimum Remaining Values (MRV) heuristic** — instead of always picking the first empty cell found, pick the empty cell with the fewest remaining valid candidates, which tends to fail faster and prune the search tree more effectively.
- **Degree heuristic** — as a tie-breaker for MRV, prefer the cell that constrains the most other unassigned cells.
