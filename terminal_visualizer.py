import time
import os

SUBJECTS = [
    "Data Structures",
    "DBMS",
    "Computer Networks",
    "Operating Systems"
]
N = len(SUBJECTS)


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_board(board, highlight_row=None, highlight_col=None, status=""):
    clear_console()
    print("=================================================================")
    print("      EXAM TIMETABLE SCHEDULER (N-Queens Backtracking Demo)      ")
    print("=================================================================\n")

    # Column headers
    header = f"{'Subject':<20} | " + " | ".join([f"Slot {i+1}" for i in range(N)])
    print(header)
    print("-" * len(header))

    for r in range(N):
        row_str = f"{SUBJECTS[r]:<20} | "
        cells = []
        for c in range(N):
            if r == highlight_row and c == highlight_col:
                cells.append("  ?   ")
            elif board[r] == c:
                cells.append("  [X] ")
            else:
                cells.append("   .  ")
        row_str += " | ".join(cells)
        print(row_str)

    print("-" * len(header))
    print(f"\nStatus: {status}\n")


def is_safe(board, row, col):
    for i in range(row):
        # Same time slot constraint
        if board[i] == col:
            return False, f"Collision with {SUBJECTS[i]} at Slot {col+1}"
        # Diagonal spacing constraint
        if abs(board[i] - col) == abs(i - row):
            return False, f"Diagonal spacing conflict with {SUBJECTS[i]}"
    return True, "Safe assignment"


def animate_backtracking(delay=0.45):
    board = [-1] * N
    solutions = []

    def backtrack(row):
        if row == N:
            solutions.append(board.copy())
            print_board(board, status=f" FOUND VALID CONFLICT-FREE TIMETABLE #{len(solutions)}!")
            time.sleep(delay * 2.5)
            return

        for col in range(N):
            # Probe slot
            print_board(board, highlight_row=row, highlight_col=col,
                        status=f"Trying '{SUBJECTS[row]}' in Slot {col + 1}...")
            time.sleep(delay)

            safe, reason = is_safe(board, row, col)
            if safe:
                board[row] = col
                print_board(board, status=f" Safe! Assigned '{SUBJECTS[row]}' -> Slot {col + 1}. Advancing...")
                time.sleep(delay)
                backtrack(row + 1)

                # Backtrack
                board[row] = -1
                print_board(board, status=f" Backtracking: Clearing '{SUBJECTS[row]}' from Slot {col + 1}...")
                time.sleep(delay)
            else:
                print_board(board, highlight_row=row, highlight_col=col,
                            status=f" Conflict: {reason}. Skipping Slot {col + 1}.")
                time.sleep(delay)

    backtrack(0)
    print(f"\nFinished! Found {len(solutions)} complete schedule(s).")


if __name__ == "__main__":
    animate_backtracking(delay=0.35)
