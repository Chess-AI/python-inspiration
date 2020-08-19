import chess
import random
import time
from IPython.display import display, HTML, clear_output
from string import ascii_lowercase
import numpy as np
import sys

sys.setrecursionlimit(80000)

def reverse_points_array(score_array):
    return np.flip(score_array,axis=0)

global board
board = chess.Board()
points_array = np.zeros((8,8)) # currently a dummy variable with no real meaning
depth = 3
pawnEvalWhite = [
         [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
         [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
         [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
         [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
         [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
         [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
         [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
         [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
     ]
pawnEvalBlack = reverse_points_array(pawnEvalWhite)

knightEval = [
         [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
         [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
         [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
         [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
         [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
         [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
         [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
         [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
     ]
bishopEvalWhite = [
     [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
     [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
     [ -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
     [ -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
     [ -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
     [ -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
     [ -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
     [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
 ]

bishopEvalBlack=reverse_points_array(bishopEvalWhite)

rookEvalWhite = [
     [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
     [0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
     [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
     [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
     [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
     [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
     [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
     [0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
 ]
rookEvalBlack = reverse_points_array(rookEvalWhite)

evalQueen = [
     [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
     [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
     [ -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
     [ -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
     [  0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
     [ -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
     [ -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
     [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
 ]

kingEvalWhite = [
     [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
     [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
     [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
     [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
     [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
     [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
     [  2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0 ],
     [  2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0 ]
 ]

kingEvalBlack = reverse_points_array(kingEvalWhite)

def getPieceValue(piece, x, y):
    if (piece == 'P'):
        return 10 + pawnEvalWhite[y][x]
    elif (piece == 'p'):
        return (10 + pawnEvalBlack[y][x])*(-1)
    elif (piece == 'R'):
        return 50 + rookEvalWhite[y][x]
    elif (piece == 'r'):
        return (50 + rookEvalBlack[y][x])*(-1)
    elif (piece == 'n' or piece =='N'):
        if (piece == 'N'):
            return 30 + knightEval[y][x]
        else:
            return (30 + knightEval[y][x])*(-1)
    elif (piece == 'B'):
        return 30 + bishopEvalWhite[y][x]
    elif (piece == 'b'):
        return (30 + bishopEvalBlack[y][x])*(-1)
    elif (piece == 'Q' or piece == 'q'):
        if (piece == 'Q'):
            return 90 + evalQueen[y][x]
        else:
            return (90 + evalQueen[y][x])*(-1)
    elif (piece == 'K'):
        return 900 + kingEvalWhite[y][x]
    elif (piece == 'k'):
        return (900 + kingEvalBlack[y][x])*(-1)
    else:
        return 0

def miniMax(curr_depth, isMax):
    global board
    every_legal_move_possible = list(board.legal_moves)
    best_val_for_maximizing_player = -9999
    best_val_for_minimizing_player = 9999
    if (curr_depth == 0):
        return evaluate_board()
    if (isMax):
        for currMove in every_legal_move_possible:
            board.push_uci(currMove.uci())
            best_val_for_maximizing_player = max(miniMax(curr_depth - 1, not(isMax)),best_val_for_maximizing_player)
            board.pop()
        return best_val_for_maximizing_player
    else:
        for currMove in every_legal_move_possible:
            board.push_uci(currMove.uci())
            best_val_for_minimizing_player = min(miniMax(curr_depth - 1, not(isMax)),best_val_for_minimizing_player)
            board.pop()
        return best_val_for_minimizing_player

def miniMaxTreeBuilder():
    global board
    isMax = True
    board = chess.Board(board.fen())
    every_legal_move_possible = list(board.legal_moves)
    # print(every_legal_move_possible)
    bestVal = -9999
    bestMove : Any
    for currMove in every_legal_move_possible:
        uci = currMove.uci()
        board.push(currMove)
        currVal = miniMax(depth - 1, not(isMax))
        # print(uci +':'+str(currVal))
        board.pop()
        if (currVal > bestVal):
            # print("entered")
            bestVal = currVal
            bestMove = currMove
    return bestMove





# This is a useful function to reverse the score arrays to be used for evaluation of board score


# Currently, this function only prints out the kind of chess piece at every position on the board
def evaluate_board():
    global board
    currScore = 0
    for (index,c) in enumerate(ascii_lowercase):
        if (c<='h'):
            for num in range(0,8):
                c = c.capitalize()
                points_array[index][num] = index
                chess_square = str(c)+str(num+1)
                piece = ''
                script = 'board.piece_at(chess.'+chess_square+')'
                piece = str(eval(script))
                # print(piece)
                piece_score = getPieceValue(piece,index,num)
                # print(piece_score)
                currScore = currScore + piece_score
        else:
            #print(currScore)
            return currScore

def random_player():
    move = miniMaxTreeBuilder()
    # move = random.choice(list(board.legal_moves))
    return move.uci()

def who(player):
    return "White" if player == chess.WHITE else "Black"

def display_board(board, use_svg):
    if use_svg:
        return board._repr_svg_()
    else:
        return "<pre>" + str(board) + "</pre>"

def play_game(player1, player2, visual="svg", pause=0.1):
    """
    playerN1, player2: functions that takes board, return uci move
    visual: "simple" | "svg" | None
    """
    use_svg = (visual == "svg")
    global board
    try:
        while not board.is_game_over(claim_draw=True):
            if board.turn == chess.WHITE:
                uci = player1()
                board.push_uci(uci)
            else:
                uci = player2()
                board.push_uci(uci)
            name = who(board.turn)
            board_stop = display_board(board, use_svg)
            html = "<b>Move %s %s, Play '%s':</b><br/>%s" % (
                       len(board.move_stack), name, uci, board_stop)
            if visual is not None:
                if visual == "svg":
                    clear_output(wait=True)
                display(HTML(html))
                if visual == "svg":
                    time.sleep(pause)
    except KeyboardInterrupt:
        msg = "Game interrupted!"
        return (None, msg, board)
    result = None
    if board.is_checkmate():
        msg = "checkmate: " + who(not board.turn) + " wins!"
        result = not board.turn
    elif board.is_stalemate():
        msg = "draw: stalemate"
    elif board.is_fivefold_repetition():
        msg = "draw: 5-fold repetition"
    elif board.is_insufficient_material():
        msg = "draw: insufficient material"
    elif board.can_claim_draw():
        msg = "draw: claim"
    if visual is not None:
        print(msg)
    return (result, msg, board)

def human_player():
    global board
    display(board)
    uci = get_move("%s's move [q to quit]> " % who(board.turn))
    legal_uci_moves = [move.uci() for move in board.legal_moves]
    while uci not in legal_uci_moves:
        print("Legal moves: " + (",".join(sorted(legal_uci_moves))))
        uci = get_move("%s's move[q to quit]> " % who(board.turn))
    return uci
def get_move(prompt):
    uci = input(prompt)
    if uci and uci[0] == "q":
        raise KeyboardInterrupt()
    try:
        chess.Move.from_uci(uci)
    except:
        uci = None
    return uci

#print(points_array)
#miniMaxTreeBuilder()
play_game(human_player, random_player)