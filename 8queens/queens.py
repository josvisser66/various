#!/usr/bin/env python3

import copy

# Place n queens on an nxn chess board so that they don't
# attack each other.

# Board cells
# ' ' = Free, no queen there, it is not under attack.
# 'Q' = There is a queen there.
# '*' = This cell is under attack from a queen.

# Starting at (r, c), fill out the diagonal identified by (dr, dc)
# (a single step) with starts, signifying that these cells are
# under attack.
def diagonal(board, r0, c0, dr, dc):
  n = len(board) # Assuming nxn board.
  c = c0 + dc
  r = r0 + dr

  while r >= 0 and r < n and c >= 0 and c < n:
    assert board[r][c] != 'Q'
    board[r][c] = '*'
    c += dc
    r += dr


# Place a queen at (r, c)
def place(board, r, c):
  assert board[r][c] == ' '
  n = len(board) # Assuming nxn
  board[r][c] = 'Q'

  # Fill out the horizontal and vertical as being under attack.
  for i in range(0, n):
    if i != c:
      board[r][i] = '*'
    if i != r:
      board[i][c] = '*'

  # Fill out the diagonals.
  diagonal(board, r, c, -1, -1)
  diagonal(board, r, c, -1, 1)
  diagonal(board, r, c, 1, 1)
  diagonal(board, r, c, 1, -1)


# Prints the board.
def print_board(board):
  for line in board:
    for cell in line:
      print(cell, end='')
    print()


# Recursive function for placing a queen. Returns
# the board if a queen was successfully placed, or None
# if there is no way to place a queen.
def greedy(board, num_queens):
  n = len(board) # Assuming nxn

  if num_queens == n:
    return board # We have placed n queens!
  

  # Try to place a queen in row num_queens. Try all
  # the columns in that row.
  for c in range(0, n):
    # If this column is empty (no queen yet, and not
    # under attack).
    if board[num_queens][c] == ' ':
      # Makes a deep copy of the board.
      new_board = copy.deepcopy(board)
      # And places a queen in this column, marking all appropriate
      # cells as under attack.
      place(new_board, num_queens, c)
      # Now recursively try to place a queen on the next row.
      even_newer_board = greedy(new_board, num_queens + 1)
      # If that succeeded, we got a solution that we can
      # return.
      if even_newer_board:
        return even_newer_board
      # If that failed, we will try to next column.

  # If we got here that means that there was no column where
  # we could place a queen, and hence we return None.
  return None


# Solve the n queens problem.
def queens(n):
  # Creates the board, all spaces.
  board = [[' '] * n for i in range(0, n)]
  # Recursively solve the placement problem.
  board = greedy(board, 0)
  # Prints the solution.
  if board is None:
    print('No solution found')
  else:
    print_board(board)


def main():
  # Solves the n queens problem and prints the board.
  queens(8)


if __name__ == '__main__':
  main()
