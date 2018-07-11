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

# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move

def compute_utility(board, color):
    black = 0
    white = 0

    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == 1:
                black += 1
                
                if row == 0 and column == 0:
                    black += 2
                elif row == len(board)-1 and column == 0:
                    black += 2
                elif row == 0 and column == len(board[row])-1:
                    black += 2
                elif row == len(board)-1 and column == len(board[row])-1:
                    black += 2

                elif row == 1 and column == 1:
                    black -= 1
                elif row == len(board)-2 and column == 1:
                    black -= 1
                elif row == 1 and column == len(board[row])-2:
                    black -= 1
                elif row == len(board)-2 and column == len(board[row])-2:
                    black -= 1

                elif row == 0 and column == 1:
                    black -= 1
                elif row == 1 and column == 0:
                    black -= 1
                elif row == len(board)-2 and column == 0:
                    black -= 1
                elif row == len(board) - 1 and column == 1:
                    black -= 1
                elif row == 0 and column == len(board[row])-1:
                    black -=1
                elif row == 1 and column == len(board[row])-2:
                    black -= 1
                elif row == len(board) - 1 and column == len(board[row])-2:
                    black -= 1
                elif row == len(board) - 2 and column == len(board[row])-1:
                    black -= 1
            

            elif board[row][column] == 2:
                white += 1
                
                if row == 0 and column == 0:
                    white += 2
                elif row == len(board) and column == 0:
                    white += 2
                elif row == 0 and column == len(board[row]):
                    white += 2
                elif row == len(board) and column == len(board[row]):
                    white += 2

                if row == 1 and column == 1:
                    white -= 1
                elif row == len(board)-2 and column == 1:
                    white -= 1
                elif row == 1 and column == len(board[row])-2:
                    white -= 1
                elif row == len(board)-2 and column== len(board[row])-2:
                    white -= 1

                elif row == 0 and column == 1:
                    white -= 1
                elif row == 1 and column == 0:
                    white -= 1
                elif row == len(board)-2 and column == 0:
                    white -= 1
                elif row == len(board) - 1 and column == 1:
                    white -= 1
                elif row == 0 and column == len(board[row])-1:
                    white -=1
                elif row == 1 and column == len(board[row])-2:
                    white -= 1
                elif row == len(board) - 1 and column == len(board[row])-2:
                    white -= 1
                elif row == len(board) - 2 and column == len(board[row])-1:
                    white -= 1
                    
    if color == 1:
        return black - white
    elif color == 2:
        return white - black

############ MINIMAX ###############################

def minimax_min_node(board, color, depth, maxdepth):
    if len(get_possible_moves(board, color)) <= 0 or depth > maxdepth:
        return compute_utility(board, color)

    childrenNodes = []

    for x in get_possible_moves(board, color):
        childrenNodes.append(minimax_max_node( play_move(board, color, x[0], x[1]), color, depth + 1, maxdepth ))

    return min(childrenNodes)


def minimax_max_node(board, color, depth, maxdepth):

    if len(get_possible_moves(board, color)) <= 0 or depth > maxdepth:
        return compute_utility(board, color)

    childrenNodes = []
    for x in get_possible_moves(board, color):
        childrenNodes.append(minimax_min_node( play_move(board, color, x[0], x[1]), color, depth + 1, maxdepth ))

    return max(childrenNodes) 

    
def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """

    moves = {}

    for x in get_possible_moves(board, color):
        moves[x] = minimax_max_node( play_move(board, color, x[0], x[1]), color, 0, 3)


    #sys.stderr.write(i, j)
    time.sleep(0.05)
    return max(moves, key=moves.get)
    
############ ALPHA-BETA PRUNING #####################

#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta): 
    return None


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta):
    return None


def select_move_alphabeta(board, color): 
    return 0,0 


####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Minimax AI") # First line is the name of this AI  
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
            movei, movej = select_move_minimax(board, color)
            #movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej)) 


if __name__ == "__main__":
    run_ai()
