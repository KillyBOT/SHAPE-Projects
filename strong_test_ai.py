#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Othello Competition Entry

An AI player for Othello. Its name is AlphaGod.

@author: Vincent Liu zl2474
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move

# used to track explored states and their minmax value
minmax_tracker = {}

def compute_utility(board, color):

    dark, light = get_score(board)
    util = dark - light if color == 1 else light - dark

    return util


def switch_color(color):
    return 1 if color == 2 else 2


def alphabeta_min_node(board, color, alpha, beta, level, limit):
    moves = get_possible_moves(board, switch_color(color))
    new_alpha, new_beta = alpha, beta

    if len(moves) == 0 or level >= limit:  # terminal case
        return compute_utility(board, color)

    # order potential states by utility from highest
    options = [play_move(board, switch_color(color), move[0], move[1]) for move in moves]
    options = [(option, compute_utility(option, color)) for option in options]
    options.sort(key=lambda x: x[1])
    options = [option[0] for option in options]

    v = 99**99
    for option in options:
        # take the minmax value from the dict if the state is explored already
        if option in minmax_tracker.keys():
            mmv = minmax_tracker[option]
        else:
            mmv = alphabeta_max_node(option, color, new_alpha, new_beta, level+1, limit)
            minmax_tracker[option] = mmv
        v = min(v, mmv)
        if v <= new_alpha:
            return v
        new_beta = min(new_beta, v)

    return v


def alphabeta_max_node(board, color, alpha, beta, level, limit):
    moves = get_possible_moves(board, color)
    new_alpha, new_beta = alpha, beta

    if len(moves) == 0 or level >= limit:  # terminal case
        return compute_utility(board, color)

    # order potential states by utility from highest
    options = [play_move(board, color, move[0], move[1]) for move in moves]
    options = [(option, compute_utility(option, color)) for option in options]
    options.sort(key=lambda x: x[1], reverse=True)
    options = [option[0] for option in options]

    v = -99**99
    for option in options:
        # take the minmax value from the dict if the state is explored already
        if option in minmax_tracker.keys():
            mmv = minmax_tracker[option]
        else:
            mmv = alphabeta_min_node(option, color, new_alpha, new_beta, level+1, limit)
            minmax_tracker[option] = mmv
        v = max(v, mmv)
        if v >= new_beta:
            return v
        new_alpha = max(new_alpha, v)

    return v


def select_move_alphabeta(board, color):
    values = []
    move_map = {}

    edge = len(board)

    # level-zero edge penalty
    lzero = [(0, 1), (1, 0), (1, 1),
             (edge-1, 1), (edge-2, 0), (edge-2, 1),
             (0, edge-2), (1, edge-1), (1, edge-2),
             (edge-1, edge-2), (edge-2, edge-1), (edge-2, edge-2)]
    if board[0][0] != 0:  # corner taken
        lzero.remove((0, 1))
        lzero.remove((1, 0))
        lzero.remove((1, 1))
    if board[edge-1][0] != 0:
        lzero.remove((edge-2, 0))
        lzero.remove((edge-1, 1))
        lzero.remove((edge-2, 1))
    if board[0][edge-1] != 0:
        lzero.remove((0, edge-2))
        lzero.remove((1, edge-1))
        lzero.remove((1, edge-2))
    if board[edge-1][edge-1] != 0:
        lzero.remove((edge-1, edge-2))
        lzero.remove((edge-2, edge-1))
        lzero.remove((edge-2, edge-2))
    lzero = tuple(lzero)

    # level-one edge benefit
    lone = [(0, x) for x in range(2, edge-2)]
    lone += [(edge-1, x) for x in range(2, edge-2)]
    lone += [(x, 0) for x in range(2, edge-2)]
    lone += [(x, edge-1) for x in range(2, edge-2)]
    lone = tuple(lone)

    # level-two edge benefit
    ltwo = ((0, 0), (0, edge-1), (edge-1, 0), (edge-1, edge-1))

    # order potential states by utility from highest
    moves = get_possible_moves(board, color)
    removed = []
    # take out moves that might let the opponent take the corner
    for move in get_possible_moves(board, color):
        if move in lzero:
            moves.remove(move)
            removed.append(move)
    moves = removed if len(moves) == 0 else moves
    options = [play_move(board, color, move[0], move[1]) for move in moves]
    options = [(option, compute_utility(option, color)) for option in options]

    # mapping state to move
    for i in range(len(options)):
        move_map[options[i][0]] = moves[i]

    options.sort(key=lambda x: x[1], reverse=True)
    options = [option[0] for option in options]

    for option in options:
        val = alphabeta_min_node(option, color, -99**99, 99**99, 0, 4)
        move = move_map[option]
        # give reward/penalty for certain edge situations
        if move in lone:
            val += 3
        elif move in ltwo:
            val += 8
        values.append(val)

    max_option = options[values.index(max(values))]

    # go back and find the move that results in the best option
    best_move = move_map[max_option]

    return best_move


def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("AlphaGod")
    color = int(input())

    while True:
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL":
            print 
        else: 
            board = eval(input())
                    
            # Select the move and send it to the manager
            movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()
