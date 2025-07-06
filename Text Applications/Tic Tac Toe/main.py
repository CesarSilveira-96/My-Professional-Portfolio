import copy


# starting board
game_board = [
    ["   ", "|", "   ", "|", "   "],
    ["---", "|", "---", "|", "---"],
    ["   ", "|", "   ", "|", "   "],
    ["---", "|", "---", "|", "---"],
    ["   ", "|", "   ", "|", "   "]
]

played_positions = []

def clear_screen():
    print("\n" * 50)

def convert_position(row, col):
    row_map = {1: 0, 2: 2, 3: 4}
    col_map = {1: 0, 2: 2, 3: 4}
    return row_map[row], col_map[col]

def print_board():
    for row in game_board:
        print("".join(row))

def minimax(board, is_maximizing):
    # Verificar vitória
    if is_winner_board(board, "O"):
        return 1
    elif is_winner_board(board, "X"):
        return -1
    elif is_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for r in range(0, 5, 2):
            for c in range(0, 5, 2):
                if board[r][c] == "   ":
                    board[r][c] = " O "
                    score = minimax(board, False)
                    board[r][c] = "   "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for r in range(0, 5, 2):
            for c in range(0, 5, 2):
                if board[r][c] == "   ":
                    board[r][c] = " X "
                    score = minimax(board, True)
                    board[r][c] = "   "
                    best_score = min(score, best_score)
        return best_score

def best_ai_move():
    best_score = -float('inf')
    move = None
    for r in range(0, 5, 2):
        for c in range(0, 5, 2):
            if game_board[r][c] == "   ":
                game_board[r][c] = " O "
                score = minimax(game_board, False)
                game_board[r][c] = "   "
                if score > best_score:
                    best_score = score
                    move = (r, c)
    return move

def is_winner(symbol):
    positions = [(r, c) for r in range(0, 5, 2) for c in range(0, 5, 2) if game_board[r][c] == f" {symbol} "]
    win_conditions = [
        # Horizontals
        [(0,0), (0,2), (0,4)],
        [(2,0), (2,2), (2,4)],
        [(4,0), (4,2), (4,4)],
        # Verticals
        [(0,0), (2,0), (4,0)],
        [(0,2), (2,2), (4,2)],
        [(0,4), (2,4), (4,4)],
        # Diagonals
        [(0,0), (2,2), (4,4)],
        [(0,4), (2,2), (4,0)],
    ]
    for condition in win_conditions:
        if all(pos in positions for pos in condition):
            return True
    return False

def is_winner_board(board, symbol):
    positions = [(r, c) for r in range(0, 5, 2) for c in range(0, 5, 2) if board[r][c] == f" {symbol} "]
    win_conditions = [
        [(0,0), (0,2), (0,4)],
        [(2,0), (2,2), (2,4)],
        [(4,0), (4,2), (4,4)],
        [(0,0), (2,0), (4,0)],
        [(0,2), (2,2), (4,2)],
        [(0,4), (2,4), (4,4)],
        [(0,0), (2,2), (4,4)],
        [(0,4), (2,2), (4,0)],
    ]
    for condition in win_conditions:
        if all(pos in positions for pos in condition):
            return True
    return False

def is_full(board):
    return all(board[r][c] != "   " for r in range(0, 5, 2) for c in range(0, 5, 2))

def play_turn(player_symbol):
    while True:
        try:
            row = int(input(f"Player {player_symbol}, choose a line (1, 2 or 3): "))
            col = int(input(f"Player {player_symbol}, choose a column (1, 2 or 3): "))
            if row not in [1,2,3] or col not in [1,2,3]:
                print("Invalid row or column. Try again (numbers only).")
                continue
            board_row, board_col = convert_position(row, col)
            if (board_row, board_col) in played_positions:
                print("That spot is already taken! Try another.")
                continue
            played_positions.append((board_row, board_col))
            game_board[board_row][board_col] = f" {player_symbol} "
            break
        except ValueError:
            print("Invalid entry. Type only numbers from 1 to 3.")

def main():
    vs_ai = input("Do you want to play against the computer? (y/n): ").lower() == "y"
    global game_board, played_positions
    game_board = [
        ["   ", "|", "   ", "|", "   "],
        ["---", "|", "---", "|", "---"],
        ["   ", "|", "   ", "|", "   "],
        ["---", "|", "---", "|", "---"],
        ["   ", "|", "   ", "|", "   "]
    ]
    played_positions = []
    clear_screen()
    print("Welcome to Cesar's Tic tac Toe!\n")
    current_player = "X"
    turns = 0

    while True:
        print_board()
        print("\n")
        if vs_ai and current_player == "O":
            print("Computer is thinking...\n")
            r, c = best_ai_move()
            played_positions.append((r, c))
            game_board[r][c] = " O "
        else:
            play_turn(current_player)
        turns += 1
        clear_screen()

        if is_winner(current_player):
            print_board()
            print(f"Player {current_player} won!!")
            break
        elif turns == 9:
            print_board()
            print("It's a Tie!")
            break

        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    main()
    again = input("Do you want to play again? (y/n): ").lower()
    if again == 'y':
        main()
    else:
        print("Thanks for playing!")