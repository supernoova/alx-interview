#!/usr/bin/python3
"""N queens solution finder module."""
import sys


def get_input():
    """Validates and retrieves the chessboard size from command line."""
    if len(sys.argv) != 2:
        print("Usage: nqueens N")
        sys.exit(1)
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("N must be a number")
        sys.exit(1)
    if n < 4:
        print("N must be at least 4")
        sys.exit(1)
    return n


def is_attacking(pos0, pos1):
    """Checks if two queens are in an attacking position."""
    if (pos0[0] == pos1[0]) or (pos0[1] == pos1[1]):
        return True
    return abs(pos0[0] - pos1[0]) == abs(pos0[1] - pos1[1])


def build_solution(row, current_solution, solutions, n):
    """Recursively builds solutions for the N queens problem."""
    if row == n:
        solutions.append(current_solution.copy())
        return
    for col in range(n):
        pos = [row, col]
        if all(not is_attacking(pos, queen) for queen in current_solution):
            current_solution.append(pos)
            build_solution(row + 1, current_solution, solutions, n)
            current_solution.pop()


def solve_n_queens(n):
    """Solves the N queens problem for a board of size n."""
    solutions = []
    build_solution(0, [], solutions, n)
    return solutions


n = get_input()
solutions = solve_n_queens(n)
for solution in solutions:
    print(solution)
