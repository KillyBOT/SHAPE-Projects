#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMS W4701 Artificial Intelligence - Programming Homework 2

This module contains the main Othello game which maintains the board, score, and 
players.  

@author: Daniel Bauer 
"""
import sys
import subprocess
from threading import Timer
from othello_shared import find_lines, get_possible_moves, play_move, get_score

import json
import socket
import numpy as np

port = 5000
host = socket.gethostname()
maxData = 4096

class InvalidMoveError(RuntimeError):
    pass


class AiTimeoutError(RuntimeError):
    pass

class Player(object):
    def __init__(self, color, name="Human"):
        self.name = name
        self.color = color

    def get_move(self, manager):
        pass  

    def __str__(self):
        return str(self.color)

class AiPlayerInterface(Player):

    TIMEOUT = 10

    def __init__(self, filename, color):
        self.color = color
        self.process = subprocess.Popen(['python3',filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        name = self.process.stdout.readline().decode("ASCII").strip()
        self.name = name
        self.process.stdin.write((str(color)+"\n").encode("ASCII"))
        self.process.stdin.flush()

    def timeout(self): 
        sys.stderr.write("{} timed out.".format(self.name))
        self.process.kill() 
        self.timed_out = True

    def get_move(self, manager):
        white_score, dark_score = get_score(manager.board)
        self.process.stdin.write("SCORE {} {}\n".format(white_score, dark_score).encode("ASCII"))
        self.process.stdin.flush()
        self.process.stdin.write("{}\n".format(str(manager.board)).encode("ASCII"))
        self.process.stdin.flush()

        timer = Timer(AiPlayerInterface.TIMEOUT, lambda: self.timeout())
        self.timed_out = False
        timer.start()

        # Wait for the AI call
        move_s = self.process.stdout.readline().decode("ASCII") 

        if self.timed_out:  
            raise AiTimeoutError
        timer.cancel()
        i_s, j_s = move_s.strip().split()
        i = int(i_s)
        j = int(j_s)
        return i,j 
    
    def kill(self,manager):
        white_score, dark_score = get_score(manager.board)
        self.process.stdin.write("FINAL {} {}\n".format(white_score, dark_score).encode("ASCII"))
        self.process.kill() 

class OthelloGameManager(object):

    def __init__(self, dimension = 6):

        self.dimension = dimension
        self.board = self.create_initial_board()
        self.current_player = 1
            
    def create_initial_board(self):
        board = []
        for i in range(self.dimension): 
            row = []
            for j in range(self.dimension):
                row.append(0)
            board.append(row) 

        i = self.dimension // 2 -1
        j = self.dimension // 2 -1
        board[i][j] = 2
        board[i+1][j+1] = 2
        board[i+1][j] = 1
        board[i][j+1] = 1
        final = []
        for row in board: 
            final.append(tuple(row))
        return board

    def print_board(self):

        boardString = "  "

        for column in range(len(self.board)):
            boardString += (str(column) + " ")

        boardString += '\n'
        for row in range(len(self.board)): 
            boardString += (str(row) + " ")
            boardString += (" ".join([str(x) for x in self.board[row]]))
            boardString += '\n'

        return boardString
       
            
    def play(self, i,j):
        if self.board[j][i] != 0:
           #raise InvalidMoveError("Occupied square.")
           print("Occupied square")
           return False
        lines = find_lines(self.board, i,j, self.current_player)
        if not lines:  
           #raise InvalidMoveError("Invalid Move.")
           print("Invalid move.")
           return False
        else:
     
            self.board = play_move(self.board, self.current_player, i, j) 
            self.current_player = 1 if self.current_player == 2 else 2
            """matrix = []
            #sys.stdout.write(str(board))
            for row in self.board:
                matrix.append(np.array(row))

            matrix = np.array(matrix)
            unique, counts = np.unique(matrix, return_counts = True)
            print(counts[1],counts[2])"""
            return True

    def get_possible_moves(self):
        return get_possible_moves(self.board, self.current_player)

    def play_game_multiplayer(game, player1, player2):

        players = [None, player1, player2]

        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverSocket.bind((host,port))

        serverSocket.listen(2)
        conn, address = serverSocket.accept()
        print("Got connection from " + str(address))

        while True: 
            player_obj = players[game.current_player]
            possible_moves = game.get_possible_moves() 

            if not possible_moves: 
                p1score, p2score = get_score(game.board)
                print("FINAL: {} (dark) {}:{} {} (light)".format(player1.name, p1score, p2score, player2.name))
                player1.kill(game)
                player2.kill(game)
                serverSocket.close()
                break 
            else: 

                color = "dark" if game.current_player == 1 else "light"
                try: 
                    print(game.print_board())

                    hasPlayed = False

                    while hasPlayed == False:
                        i = int(input("Type row: "))
                        j = int(input("Type column: "))
                        #i, j = player_obj.get_move(game)
                        hasPlayed = game.play(i,j)

                    print("{} ({}) plays {},{}".format(player_obj.name, color, i,j))

                    toSend = game.print_board()
                    #toSend = ("Other played: " + str(i) + " " + str(j))
                    toSend = json.dumps(toSend)
                    conn.send(toSend.encode())

                    otherHasPlayed = False

                    while otherHasPlayed == False:
                        data = conn.recv(maxData)
                        decodedData = json.loads(data.decode())
                        otherI = decodedData["row"]
                        otherJ = decodedData["column"]
                        otherHasPlayed = game.play(otherI, otherJ)
                        otherHasPlayedData = 'no' if otherHasPlayed == False else 'yes'
                        conn.send(otherHasPlayedData.encode())

                    print("Other played: ", otherI, otherJ)

                except AiTimeoutError:
                    print("{} ({}) timed out!".format(player_obj.name, color))
                    print("FINAL: {} (dark) {}:{} {} (light)".format(player_obj.name, p1score, p2score, player2.name))
                    player1.kill(game)
                    player2.kill(game)
                    serverSocket.close()
                    break


         
        

if __name__ == "__main__":

    if len(sys.argv) == 4:
        game = OthelloGameManager(dimension=int(sys.argv[1]))
        p1 = AiPlayerInterface(sys.argv[2],1)
        p2 = AiPlayerInterface(sys.argv[3],2)
    elif len(sys.argv) == 3:
        game = OthelloGameManager(dimension=int(sys.argv[1]))
        p1 = Player(1)
        p2 = AiPlayerInterface(sys.argv[2],2)
    elif len(sys.argv) == 2: 
        p1 = Player(1)
        p2 = Player(2)
        game = OthelloGameManager(dimension=int(sys.argv[1]))
    else:
        p1 = Player(1)
        p2 = Player(2)
        game = OthelloGameManager(dimension=8)
    #gameManager = OthelloGameManager(game, p1, p2) 
    game.play_game(game, p1, p2)