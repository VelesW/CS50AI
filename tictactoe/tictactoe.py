"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None
FIELD_AMOUNT = 9
INFINITY = 1e309

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # If the board is empty. Then is X's turn
    if board == initial_state():
        return X
    x = 0
    o = 0
    for row in board:
        x += row.count(X)
        o += row.count(O)

    # If the board is full the game is over
    if x + o == FIELD_AMOUNT:
        return
    # Check player turn
    if x == o:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set = set()

    for row_index, row in enumerate(board):
        for column_index, item in enumerate(row):
            if item == EMPTY:
                actions_set.add((row_index, column_index))
    return actions_set

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    player_turn = player(board) # Get the current player turn

    new_board = deepcopy(board) # Create a copy of the board
    i, j = action  # Unpack tuple

    if i not in range(3) or j not in range(3): # Check if the move is valid
        raise Exception("Invalid move")

    if board[i][j] is not EMPTY: # Check if the move is valid
        raise Exception("Invalid move")
    else:
        new_board[i][j] = player_turn 
    
    return new_board 


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for player in (X, O):
        # check vertical
            for row in board:
                if row == [player] * 3:
                    return player

        # check horizontal
            for i in range(3):
                column = [board[x][i] for x in range(3)]
                if column == [player] * 3:
                    return player
        
        # check diagonal
            if [board[i][i] for i in range(0, 3)] == [player] * 3:
                return player

            elif [board[i][~i] for i in range(0, 3)] == [player] * 3:
                return player
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # game is over if there is a winner
    if winner(board) is not EMPTY:
        return True

    # moves are still available
    for row in board:
        if EMPTY in row:
            return False

    # game is over if there is no winner and no moves available
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    state = winner(board)
    if state == X:
        return 1
    elif state == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    if player(board) == X:
        # Current player is X
        current_result = (EMPTY, -INFINITY)
        for action in actions(board):
            score_value = minimax_value(result(board, action), False) # Get the score of the move
            # If the move is a winning move, return it
            if score_value == 1:
                return action
            # Check if the current move is better than the previous one    
            if score_value > current_result[1]:
                current_result = (action, score_value)

        return current_result[0] 
                
        
    # Current player is O
    current_result = (EMPTY, INFINITY)
    for action in actions(board):
        score_value = minimax_value(result(board, action), True)
        if score_value == -1:
            return action
        if score_value < current_result[1]:
            current_result = (action, score_value)

    return current_result[0]

def minimax_value(board, player):
    """
    Recursive function that returns the optimal move for the board
    """
    if terminal(board):
        return utility(board)

    if player:
        current_value = -INFINITY
        for action in actions(board):
            result_board = result(board, action)
            current_value = max(current_value, minimax_value(result_board, False))

        return current_value

    current_value = INFINITY
    for action in actions(board):
        result_board = result(board, action)
        current_value = min(current_value, minimax_value(result_board, True))

    return current_value