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
    """
    Returns player who has the next turn on a board.
    """
    next_player = None
    # count number of Xs and Os in the board game
    for row in board:
        for box in row:
            if(box == X):
                x_count += 1
            if(box == O):
                o_count += 1

    # since X goes first, any time num(X) == num(O)
    # it is Xs turn, otherwise O goes next
    if(x_count == o_count):
        next_player = X
    else:
        next_player = O
        
    
    return next_player;


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for row in range(len(board)):
        for column in range(len(board[0])):
            if(board[row][column] == EMPTY):
                actions.add((row,column))
                
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Desired action not valid")
    
    resulting_board = copy.deepcopy(board)
    resulting_board[action(0)][action(1)] = player(board)
    return resulting_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # top row
    if((board[0][0] == X and board[0][1] == X and board[0][2] == X) or (board[0][0] == O and board[0][1] == O and board[0][2] == O))
        return board[0][0]
        
    # middle row
    if((board[1][0] == X and board[1][1] == X and board[1][2] == X) or (board[1][0] == O and board[1][1] == O and board[1][2] == O))
        return board[1][0]
        
    # bottom row
    if((board[2][0] == X and board[2][1] == X and board[2][2] == X) or (board[2][0] == O and board[2][1] == O and board[2][2] == O))
        return board[2][0]
        
    # left column
    if((board[0][0] == X and board[1][0] == X and board[2][0] == X) or (board[0][0] == O and board[1][0] == O and board[2][0] == O))
        return board[0][0]
        
    # middle column
    if((board[0][1] == X and board[1][1] == X and board[2][1] == X) or (board[0][1] == O and board[1][1] == O and board[2][1] == O))
        return board[0][1]
        
    # right column
    if((board[0][2] == X and board[1][2] == X and board[2][2] == X) or (board[0][2] == O and board[1][2] == O and board[2][2] == O))
        return board[0][2]
        
    # forward slash diagonal
    if((board[2][0] == X and board[1][1] == X and board[0][2] == X) or (board[2][0] == O and board[1][1] == O and board[0][2] == O))
        return board[2][0]
        
    # backward slash diagonal
    if((board[0][0] == X and board[1][1] == X and board[2][2] == X) or (board[0][0] == O and board[1][1] == O and board[2][2] == O))
        return board[0][0]
        
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if( len(actions(board)) == 0 or winner(board) != None )
        return True
        
    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    utility_score  = 0
    winning_player = winner(board)
    if(winning_player == X):
        utility_score = 1
    else if(winning_layer == O):
        utility_score = -1
    
    return utility_score


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
