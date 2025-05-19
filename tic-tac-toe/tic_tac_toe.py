import random

board = [' ' for _ in range(9)]

# Scores dictionary for Player1, Player2/Bot, and Draws
scores = {'Player 1': 0, 'Player 2/Bot': 0, 'Draws': 0}

def print_board():
    print("\nCurrent Board:")
    for i in range(3):
        row = [board[i*3 + j] for j in range(3)]
        print(f" {row[0]} | {row[1]} | {row[2]} ")
        if i < 2:
            print("---+---+---")
    print()

def check_winner(player):
    win_combos = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    return any(all(board[i] == player for i in combo) for combo in win_combos)

def is_draw():
    return all(cell != ' ' for cell in board)

def player_move(player):
    while True:
        try:
            move = int(input(f"{player}, enter your move (1-9): ")) - 1
            if move < 0 or move > 8:
                print("Invalid move. Choose 1-9.")
            elif board[move] != ' ':
                print("That cell is already taken.")
            else:
                board[move] = 'X' if player == 'Player 1' else 'O'
                break
        except ValueError:
            print("Please enter a valid number.")

def bot_move_easy():
    empty_cells = [i for i, cell in enumerate(board) if cell == ' ']
    move = random.choice(empty_cells)
    board[move] = 'O'

def bot_move_medium():
    # Try to win
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            if check_winner('O'):
                return
            board[i] = ' '
    # Try to block player win
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            if check_winner('X'):
                board[i] = 'O'
                return
            board[i] = ' '
    bot_move_easy()

def bot_move_hard():
    best_score = -float('inf')
    best_move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    board[best_move] = 'O'

def minimax(board_state, is_maximizing):
    if check_winner('O'):
        return 1
    elif check_winner('X'):
        return -1
    elif is_draw():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board_state[i] == ' ':
                board_state[i] = 'O'
                score = minimax(board_state, False)
                board_state[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board_state[i] == ' ':
                board_state[i] = 'X'
                score = minimax(board_state, True)
                board_state[i] = ' '
                best_score = min(score, best_score)
        return best_score

def play_game():
    while True:
        global board
        board = [' ' for _ in range(9)]

        print("Welcome to Tic-Tac-Toe!")
        mode = ''
        while mode not in ['1', '2']:
            print("Choose mode:")
            print("1. Player vs Player")
            print("2. Player vs Bot")
            mode = input("Enter 1 or 2: ").strip()

        bot_mode = ''
        if mode == '2':
            while bot_mode not in ['1', '2', '3']:
                print("Choose Bot difficulty:")
                print("1. Easy")
                print("2. Medium")
                print("3. Hard")
                bot_mode = input("Enter 1, 2, or 3: ").strip()

        current_player = 'Player 1'
        print_board()

        while True:
            if mode == '1':  # Player vs Player
                player_move(current_player)
            else:  # Player vs Bot
                if current_player == 'Player 1':
                    player_move(current_player)
                else:
                    print("Bot is making a move...")
                    if bot_mode == '1':
                        bot_move_easy()
                    elif bot_mode == '2':
                        bot_move_medium()
                    else:
                        bot_move_hard()

            print_board()

            # Check for win or draw
            player_symbol = 'X' if current_player == 'Player 1' else 'O'
            if check_winner(player_symbol):
                print(f"{current_player} wins!")
                scores[current_player] += 1
                break

            if is_draw():
                print("It's a draw!")
                scores['Draws'] += 1
                break

            # Switch turns
            if mode == '1':
                current_player = 'Player 2' if current_player == 'Player 1' else 'Player 1'
            else:
                current_player = 'Player 2/Bot' if current_player == 'Player 1' else 'Player 1'

        print(f"\nScores:\nPlayer 1: {scores['Player 1']}\nPlayer 2/Bot: {scores['Player 2/Bot']}\nDraws: {scores['Draws']}\n")

        play_again = input("Play again? (Y/N): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing! Final scores:")
            print(f"Player 1: {scores['Player 1']} | Player 2/Bot: {scores['Player 2/Bot']} | Draws: {scores['Draws']}")
            break

if __name__ == "__main__":
    play_game()
