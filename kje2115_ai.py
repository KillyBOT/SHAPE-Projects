#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to  
complete and submit. 

@author: Kyle 2115
"""

import random
import sys
import time
import random
#import numpy as np

# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move

max_depth = 3
seen_boards = set()
seen_boards_cost = dict()
seen_boards_max = set()
seen_boards_max_cost = dict()
seen_boards_min = set()
seen_boards_min_cost = dict()

seen_boards_heuristic = set()
seen_boards_heuristic_cost = dict()

volatile_level = 0

def get_score_better(board, mult):
    result = [0,0]
    for i in range(len(board)):
        for j in range(len(board)):
            if board[j][i] == 0:
                lines1 = find_lines(board,i,j,1)
                if lines1: 
                    result[0] += 1 * mult
                lines2 = find_lines(board,i,j,2)
                if lines2:
                    result[1] += 1 * mult
            else:
                result[board[i][j] - 1] += 1
    return result

def get_heuristic(board, color):
    result = 0
    boardLen = len(board)

    scores = get_score(board)

    if scores[color - 2] == 0:
        result += boardLen ** 4
    if scores[color - 1] == 0:
        result -= boardLen ** 4

    result += scores[0] - scores[1]

    result += len(get_possible_moves(board,color)) * boardLen
    result -= len(get_possible_moves(board,1 if color == 2 else 2)) * boardLen

    for x in range(0,boardLen,boardLen-1):
        for y in range(0, boardLen,boardLen-1):
            if board[x][y] == color:
                result += (boardLen * boardLen * boardLen)
            else:
                result -= (boardLen * boardLen * boardLen)

    toSub = (boardLen * boardLen) / 2
    colorSheet = [0,0,0]
    for x in range(0,boardLen,boardLen-2):
        colorSheet[board[1][x]] += toSub
        colorSheet[board[x][1]] += toSub
        colorSheet[board[boardLen-2][x]] += toSub
        colorSheet[board[x][boardLen-2]] += toSub
        colorSheet[board[1][x+1]] += toSub
        colorSheet[board[boardLen - 2][x + 1]] += toSub

    colorSheet = colorSheet[1:]
    result += colorSheet[color - 1] - colorSheet[color - 2]
    return result

"""def get_score_better(board):
    toMat = []
    #sys.stdout.write(str(board))
    for row in board:
        toMat.append(np.array(row))

    toMat = np.array(toMat)
    unique, counts = np.unique(toMat, return_counts = True)
    return (counts[1],counts[2])"""

def compute_utility(board, color):

    mult = 1
    #black, white
    scores = [0]
    scores.extend(list(get_score(board)))
    scores[1] *= mult
    scores[2] *= mult

    if color == 1:
        return scores[1] - scores[2]
    elif color == 2:
        return scores[2] - scores[1]

def switch_color(color):
    return 1 if color == 2 else 2

############ MINIMAX ###############################

def minimax_min_node(board, color, currentColor, depth, maxdepth):
    if depth > maxdepth or len(get_possible_moves(board, color)) <= 0:
        return compute_utility(board, color)
    else:

        childrenNodes = []

        for x in get_possible_moves(board, color):
            if hash(x) not in seen_boards:
                childrenNodes.append(minimax_max_node( play_move(board, currentColor, x[0], x[1]), color, switch_color(currentColor), depth + 1, maxdepth ))
                seen_boards.add(hash(x))
                seen_boards_cost_max[x] = childrenNodes[-1]
            else:
                childrenNodes.append(seen_boards_cost_max[x])

            childrenNodes[-1] += random.randint(-volatile_level,volatile_level)


        return min(childrenNodes)


def minimax_max_node(board, color, currentColor, depth, maxdepth):

    if depth > maxdepth or len(get_possible_moves(board, color)) <= 0:
        return compute_utility(board, color)
    else:

        childrenNodes = []
        for x in get_possible_moves(board, color):
            if hash(x) not in seen_boards:
                childrenNodes.append(minimax_min_node( play_move(board, currentColor, x[0], x[1]), color, switch_color(currentColor), depth + 1, maxdepth ))
                seen_boards.add(hash(x))
                seen_boards_cost_min[x] = childrenNodes[-1]

            else:
                childrenNodes.append(seen_boards_cost_min[x])

            childrenNodes[-1] += random.randint(-volatile_level,volatile_level)

        return max(childrenNodes) 

    
def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """

    moves = {}

    for x in get_possible_moves(board, color):
        if hash(x) not in seen_boards:
            moves[x] = minimax_min_node( play_move(board, color, x[0], x[1]), color, switch_color(color), 1, max_depth)
            seen_boards.add(hash(x))
            seen_boards_cost[x] = moves[x]

        else:
            moves[x] = seen_boards_cost_min[x]

        moves[x] += random.randint(-volatile_level,volatile_level)

    #sys.stderr.write(i, j)
    time.sleep(0.05)
    return max(moves, key=moves.get)
    
############ ALPHA-BETA PRUNING #####################

#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta, depth, maxdepth): 
    if depth > maxdepth or len(get_possible_moves(board, switch_color(color))) <= 0:
        if hash(board) not in seen_boards:
            seen_boards.add(hash(board))
            seen_boards_cost[hash(board)] = compute_utility(board, color)

        return seen_boards_cost[hash(board)]
    else:

        nowBeta = beta
        bestVal = 3000000000
        bestCheck = []

        for x in get_possible_moves(board, switch_color(color)):
            playedBoard = play_move(board, switch_color(color), x[0], x[1])
            if playedBoard not in seen_boards_heuristic:
                seen_boards_heuristic.add(playedBoard)
                seen_boards_heuristic_cost[playedBoard] = get_heuristic(playedBoard, color)
            #toCheck = alphabeta_max_node(playedBoard, color, switch_color(currentColor), alpha, nowBeta, depth + 1, maxdepth )
            bestCheck.append((seen_boards_heuristic_cost[playedBoard],playedBoard))

        bestCheck.sort()

        for x, playedBoard in bestCheck:

            toCheck = 0
            if playedBoard not in seen_boards_max:
                seen_boards_max.add(toCheck)
                seen_boards_max_cost[playedBoard] = alphabeta_max_node(playedBoard, color, alpha, nowBeta, depth + 1, maxdepth )
            
            toCheck = seen_boards_max_cost[playedBoard]
            toCheck += random.randint(-volatile_level,volatile_level)
            if toCheck < bestVal:
                bestVal = toCheck
            if bestVal < nowBeta:
                nowBeta = bestVal
            if alpha >= nowBeta:
                break

        #return min(childrenNodes)
        return bestVal


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta, depth, maxdepth):
    if depth > maxdepth or len(get_possible_moves(board, color)) <= 0:
        if hash(board) not in seen_boards:
            seen_boards.add(hash(board))
            seen_boards_cost[hash(board)] = compute_utility(board, color)

        return seen_boards_cost[hash(board)]
    else:

        nowAlpha = alpha
        bestVal = -3000000000

        bestCheck = []

        for x in get_possible_moves(board, color):
            playedBoard = play_move(board, color, x[0], x[1])
            if playedBoard not in seen_boards_heuristic:
                seen_boards_heuristic.add(playedBoard)
                seen_boards_heuristic_cost[playedBoard] = get_heuristic(playedBoard, color)
            #toCheck = alphabeta_max_node(playedBoard, color, switch_color(currentColor), alpha, nowBeta, depth + 1, maxdepth )
            bestCheck.append((seen_boards_heuristic_cost[playedBoard],playedBoard))

        bestCheck.sort()
        bestCheck.reverse()

        for x, playedBoard in bestCheck:
            #playedBoard = play_move(board, currentColor, x[0], x[1])
            #toCheck = alphabeta_min_node(playedBoard, color, switch_color(currentColor), nowAlpha, beta, depth + 1, maxdepth )
            
            toCheck = 0
            if playedBoard not in seen_boards_min:
                seen_boards_min.add(playedBoard)
                seen_boards_min_cost[playedBoard] = alphabeta_min_node(playedBoard, color, nowAlpha, beta, depth + 1, maxdepth )

            toCheck = seen_boards_min_cost[playedBoard]
            toCheck += random.randint(-volatile_level,volatile_level)
            if toCheck > bestVal:
                bestVal = toCheck
            if bestVal > nowAlpha:
                nowAlpha = bestVal
            if nowAlpha >= beta:
                break

        #return max(childrenNodes) 
        return bestVal


def select_move_alphabeta(board, color): 
    moves = {}

    alpha = -3000000000
    beta = 3000000000

    bestVal = alpha

    bestCheck = []
    boardLen = len(board)

    nextToCorner = [(0,1),
    (1,0),
    (1,1),
    (boardLen-1,1),
    (boardLen-2,0),
    (boardLen-2,1),
    (0,boardLen-2),
    (1,boardLen-2),
    (1,boardLen-1),
    (boardLen-1,boardLen-2),
    (boardLen-2,boardLen-1),
    (boardLen-2,boardLen-2)]

    checkForCorners = False

    nextToCorner = set(nextToCorner)
    possibleMoves = get_possible_moves(board,color)

    if set(possibleMoves).issubset(nextToCorner):
        checkForCorners = True # Only stop if there are no other options

    for x in possibleMoves:
        if x not in nextToCorner or checkForCorners:
            playedBoard = play_move(board, color, x[0], x[1])
            if playedBoard not in seen_boards_heuristic:
                seen_boards_heuristic.add(playedBoard)
                seen_boards_heuristic_cost[playedBoard] = get_heuristic(playedBoard, color)
            #toCheck = alphabeta_max_node(playedBoard, color, switch_color(currentColor), alpha, nowBeta, depth + 1, maxdepth )
            bestCheck.append((seen_boards_heuristic_cost[playedBoard],playedBoard,x))

    bestCheck.sort()
    bestCheck.reverse()

    for n,playedBoard,x in bestCheck:
        
        if playedBoard not in seen_boards_min:
            seen_boards_min.add(playedBoard)
            seen_boards_min_cost[playedBoard] = alphabeta_min_node(playedBoard, color, alpha, beta, 1, max_depth)

        moves[x] = seen_boards_min_cost[playedBoard]
        moves[x] += random.randint(-volatile_level,volatile_level)
        if moves[x] > bestVal:
            bestVal = moves[x]
        if bestVal > alpha:
            alpha = bestVal
        if alpha >= beta:
            return x

    #sys.stderr.write(i, j)
    #time.sleep(0.05)
    return max(moves, key=moves.get)


####################################################
def run_ai():
    name = "Beta Alpha Gamma Omega Epsilon Delta"
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    #print("Minimax AI") # First line is the name of this AI 
    print(name) 
    color = int(input()) # Then we read the color: 1 for dark (goes first), 
                         # 2 for light. 

    while True: # This is the main loop 
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over. 
            print 
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            # Select the move and send it to the manager 
            #movei, movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej)) 

if __name__ == "__main__":
    run_ai()
