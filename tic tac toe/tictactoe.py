"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    count_x = sum(row.count(X) for row in board)
    count_o = sum(row.count(O) for row in board)

    if count_x <= count_o:
        return X
    else:
        return O


def actions(board):
    possible_actions = set()

    for i in range(3):
        for j in range(3):
            if board[i][j]== EMPTY:
                    possible_actions.add((i,j))
    
    return possible_actions


def result(board, selected_action):
    # Create a deep copy of the board
    new_board = copy.deepcopy(board)
    
    # Extract the row and column from the selected action
    row, col = selected_action
    
    # Check if the selected cell is empty
    if new_board[row][col] != EMPTY:
        raise Exception("Invalid action: Cell is not empty")
    
    # Update the board with the current player's move
    new_board[row][col] = player(board)
    
    return new_board


def winner(board):
    # Check rows
    for row in board:
        if row.count(X) == 3:
            return X
        elif row.count(O) == 3:
            return O

    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j]:
            if board[0][j] == X:
                return X
            elif board[0][j] == O:
                return O

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]:
        if board[1][1] == X:
            return X
        elif board[1][1] == O:
            return O

    return None



def terminal(board):
    if winner(board) is not None or all(all(cell != EMPTY for cell in row)for row in board):
        return True
    else:
        return False


def utility(board):
    # Check if X has won the game
    if winner(board) == X:
        return 1
    # Check if O has won the game
    elif winner(board) == O:
        return -1
    # Game has ended in a tie
    else:
        return 0
    
def min_value(board):
    if terminal(board):
        return utility(board)

    # Set the initial minimum score to positive infinity
    min_score = float('inf')

    for action in actions(board):
        new_board = result(board, action)
        # Recursively call max_value on the new board
        score = max_value(new_board)
        # Update the minimum score if the current score is smaller
        if score < min_score:
            min_score = score

    return min_score

def max_value(board):
    if terminal(board):
        return utility(board)

    # Set the initial maximum score to negative infinity
    max_score = float('-inf')

    for action in actions(board):
        new_board = result(board, action)
        # Recursively call min_value on the new board
        score = min_value(new_board)
        # Update the maximum score if the current score is larger
        if score > max_score:
            max_score = score

    return max_score



def minimax(board):
    # Check if the board is terminal
    if terminal(board):
        return None

    # Determine the current player
    current_player = player(board)

    if current_player == X:
        # If current player is X, maximize the score
        best_score = float('-inf')
        best_move = None
        # Iterate over all possible actions
        for action in actions(board):
            # Generate new board by applying the action
            new_board = result(board, action)
            # Calculate the score by calling min_value on the new board
            score = min_value(new_board)
            # Update best_score and best_move if the score is greater
            if score > best_score:
                best_score = score
                best_move = action
    else:
        # If current player is O, minimize the score
        best_score = float('inf')
        best_move = None
        # Iterate over all possible actions
        for action in actions(board):
            # Generate new board by applying the action
            new_board = result(board, action)
            # Calculate the score by calling max_value on the new board
            score = max_value(new_board)
            # Update best_score and best_move if the score is smaller
            if score < best_score:
                best_score = score
                best_move = action

    # Return the best move for the current player
    return best_move

