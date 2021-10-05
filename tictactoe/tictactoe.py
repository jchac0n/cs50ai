"""
Tic Tac Toe Player
"""

import math
import copy
from random import randrange

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
    x_count = 0
    o_count = 0
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
        
    
    return next_player

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
    resulting_board[action[0]][action[1]] = player(board)
    return resulting_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # top row
    if((board[0][0] == X and board[0][1] == X and board[0][2] == X) or (board[0][0] == O and board[0][1] == O and board[0][2] == O)):
        return board[0][0]
        
    # middle row
    if((board[1][0] == X and board[1][1] == X and board[1][2] == X) or (board[1][0] == O and board[1][1] == O and board[1][2] == O)):
        return board[1][0]
        
    # bottom row
    if((board[2][0] == X and board[2][1] == X and board[2][2] == X) or (board[2][0] == O and board[2][1] == O and board[2][2] == O)):
        return board[2][0]
        
    # left column
    if((board[0][0] == X and board[1][0] == X and board[2][0] == X) or (board[0][0] == O and board[1][0] == O and board[2][0] == O)):
        return board[0][0]
        
    # middle column
    if((board[0][1] == X and board[1][1] == X and board[2][1] == X) or (board[0][1] == O and board[1][1] == O and board[2][1] == O)):
        return board[0][1]
        
    # right column
    if((board[0][2] == X and board[1][2] == X and board[2][2] == X) or (board[0][2] == O and board[1][2] == O and board[2][2] == O)):
        return board[0][2]
        
    # forward slash diagonal
    if((board[2][0] == X and board[1][1] == X and board[0][2] == X) or (board[2][0] == O and board[1][1] == O and board[0][2] == O)):
        return board[2][0]
        
    # backward slash diagonal
    if((board[0][0] == X and board[1][1] == X and board[2][2] == X) or (board[0][0] == O and board[1][1] == O and board[2][2] == O)):
        return board[0][0]
        
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if( len(actions(board)) == 0 or winner(board) != None ):
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
    elif(winning_player == O):
        utility_score = -1
    
    return utility_score

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    next_mv = None
    
    if(terminal(board)):
        return next_mv
    
    next_player = player(board)
    moves       = actions(board)

    #if it is the AIs turn and the board is empty
    #let's randomize the first move just to make it
    #more fun
    if(len(moves) == 9):
        first_move = randrange(9)
        temp = 0
        for move in moves:
            if(first_move == temp):
                next_mv = move
                return next_mv
            temp += 1
    
    if(next_player == X):        
        temp = -math.inf
        for move in moves:

            #if i make this move, the resulting board will be played by my
            #oponent who likes to minimize the value. let's find the move
            #that results in the largest value produced by my opponent
            this_move_value = minvalue(result(board,move))
            if(this_move_value > temp):
                temp = this_move_value
                next_mv = move
    
    if(next_player == O):
        temp = math.inf
        for move in moves:
        
            #if i make this move, the resulting board will be played by my
            #oponent who likes to maximize the value. let's find the move
            #that results in the smalleset value produced by my opponent
            this_move_value = maxvalue(result(board,move))
            if(this_move_value < temp):
                temp = this_move_value
                next_mv = move
                
    return next_mv

def minvalue(board):
    
    #the value of the final board is just its utility
    if(terminal(board)):
        return utility(board)
    
    value = math.inf;
    moves = actions(board);
    
    #I'm O, i like to minimize the score. if i make each of
    #my possible moves, what's the lowest score my opponent will
    #produce afterwards
    for move in moves:
        value = min(value, maxvalue(result(board, move)))
        
    return value

def maxvalue(board):
    
    #the value of the final board is just its utility
    if(terminal(board)):
        return utility(board)
    
    value = -math.inf;
    moves = actions(board);
    
    #I'm X, i like to maximize the score. if i make each of
    #my possible moves, what's the highest score my opponent will
    #produce afterwards
    for move in moves:
        value = max(value, minvalue(result(board, move)))
        
    return value    
        