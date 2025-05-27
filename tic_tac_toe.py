# tic_tac_toe.py

def create_board():
    return [' ' for _ in range(9)]

def print_board(board):
    print()
    for i in range(3):
        row = board[i*3:(i+1)*3]
        print(' | '.join(row))
        if i < 2:
            print('--+---+--')

def player_move(board, symbol):
    while True:
        move = input(f"Player {symbol}, enter your move (0-8): ")
        if move.isdigit():
            move = int(move)
            if 0 <= move <= 8:
                if board[move] == ' ':
                    board[move] = symbol
                    break
                else:
                    print("Cell already filled. Choose another.")
            else:
                print("Number out of range. Enter 0-8.")
        else:
            print("Please enter a number only.")

def check_winner(board, symbol):
    win_positions = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for pos in win_positions:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] == symbol:
            return True
    return False

def is_draw(board):
    return ' ' not in board

def play_game():
    board = create_board()
    current_symbol = 'X'

    while True:
        print_board(board)
        player_move(board, current_symbol)

        if check_winner(board, current_symbol):
            print_board(board)
            print(f"Player {current_symbol} wins!")
            break

        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_symbol = 'O' if current_symbol == 'X' else 'X'

if __name__ == "__main__":
    play_game()

