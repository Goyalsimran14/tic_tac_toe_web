from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for sessions

board = [' ' for _ in range(9)]
current_turn = 'X'

win_positions = [
    [0,1,2], [3,4,5], [6,7,8],
    [0,3,6], [1,4,7], [2,5,8],
    [0,4,8], [2,4,6]
]

def check_winner(symbol):
    for pos in win_positions:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] == symbol:
            return True
    return False

def is_draw():
    return ' ' not in board

def ai_move():
    # Simple AI: win/block/first empty
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            if check_winner('O'):
                return
            board[i] = ' '
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            if check_winner('X'):
                board[i] = 'O'
                return
            board[i] = ' '
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            return

@app.route('/')
def index():
    # Initialize scores in session if not present
    if 'score_x' not in session:
        session['score_x'] = 0
    if 'score_o' not in session:
        session['score_o'] = 0
    if 'score_draw' not in session:
        session['score_draw'] = 0

    return render_template('index.html', board=board, turn=current_turn,
                           score_x=session['score_x'],
                           score_o=session['score_o'],
                           score_draw=session['score_draw'])

@app.route('/move/<int:cell>')
def move(cell):
    global current_turn, board

    if board[cell] == ' ' and current_turn == 'X':
        board[cell] = 'X'

        if check_winner('X'):
            session['score_x'] = session.get('score_x', 0) + 1
            winner = 'X'
            return render_template('index.html', board=board, winner=winner,
                                   score_x=session['score_x'],
                                   score_o=session['score_o'],
                                   score_draw=session['score_draw'])

        elif is_draw():
            session['score_draw'] = session.get('score_draw', 0) + 1
            return render_template('index.html', board=board, draw=True,
                                   score_x=session['score_x'],
                                   score_o=session['score_o'],
                                   score_draw=session['score_draw'])

        ai_move()

        if check_winner('O'):
            session['score_o'] = session.get('score_o', 0) + 1
            winner = 'O'
            return render_template('index.html', board=board, winner=winner,
                                   score_x=session['score_x'],
                                   score_o=session['score_o'],
                                   score_draw=session['score_draw'])

        elif is_draw():
            session['score_draw'] = session.get('score_draw', 0) + 1
            return render_template('index.html', board=board, draw=True,
                                   score_x=session['score_x'],
                                   score_o=session['score_o'],
                                   score_draw=session['score_draw'])

    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    global board, current_turn
    board = [' ' for _ in range(9)]
    current_turn = 'X'
    # Reset scores as well if you want:
    # session['score_x'] = 0
    # session['score_o'] = 0
    # session['score_draw'] = 0
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
