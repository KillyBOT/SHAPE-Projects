#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMS W4701 Artificial Intelligence - Programming Homework 2

This module contains a simple graphical user interface for Othello. 

This is specifically made for local multiplayer.

@author: Kyle Edwards
"""
from tkinter import *
from tkinter import scrolledtext

from othello_game import OthelloGameManager, AiPlayerInterface, Player, InvalidMoveError, AiTimeoutError
from othello_shared import get_possible_moves, get_score

import sys, os

import socket
import json

port = 5000
host = socket.gethostname()
maxData = 4096

class OthelloGui(object):

    def __init__(self, game_manager, player1, player2):

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind(('',port))

        print("Starting server on port " + str(port))
        print("Looking for player 2...")

        self.serverSocket.listen(2)
        self.conn, self.address = self.serverSocket.accept()
        print("Got connection from " + str(self.address))

        self.game = game_manager
        self.players = [None, player1, player2]
        self.height = self.game.dimension
        self.width = self.game.dimension 

        data = str(self.game.dimension)

        self.conn.send(data.encode())
        self.isGameOver = False

        self.offset = 20
        self.cell_size = 50

        root = Tk()
        root.wm_title("Othello")
        root.lift()
        root.attributes("-topmost", True)
        self.root = root
        self.canvas = Canvas(root,height = self.cell_size * self.height + self.offset*2,width = self.cell_size * self.width + self.offset*2, bg="black")
        self.move_label = Label(root)
        self.score_label = Label(root)
        self.game_label = Label(root)
        self.author_label = Label(root)
        self.restart_button = Button(root)
        self.current_player_canvas = Canvas(root, height = self.cell_size + self.offset*2, width = self.cell_size + self.offset*2, bg="black")
        self.text = scrolledtext.ScrolledText(root, width=70, height=10)
        self.game_label.pack(side="top")
        self.author_label.pack(side="top")
        self.score_label.pack(side="top")
        self.move_label.pack(side="top")
        self.current_player_canvas.pack()
        self.canvas.pack()
        self.text.pack()
        self.restart_button.pack()
        self.draw_board()

    def get_position(self,x,y):
        i = (x -self.offset) // self.cell_size
        j = (y -self.offset) // self.cell_size
        return i,j

    def mouse_pressed(self,event):

        try:
            player = "Dark" if self.game.current_player == 1 else "Light"

            i,j = self.get_position(event.x, event.y)

            hasPlayed = self.game.play(i, j)
            if hasPlayed == False:
                self.log("Cannot play there")
            else:

                self.log("{}: {},{}".format(player, i,j))

            #self.log("Got play! Waiting for player 2...")

            if not get_possible_moves(self.game.board, self.game.current_player):
                self.isGameOver = self.shutdown("Game Over")
            elif isinstance(self.players[self.game.current_player], AiPlayerInterface):
                self.root.unbind("<Button-1>")
                self.root.after(100,lambda: self.ai_move())

            if hasPlayed == True:
                self.draw_board()
                self.root.unbind("<Button-1>")
                toSend = self.game.board
                toSend = json.dumps(toSend)
                self.conn.send(toSend.encode())

                otherHasPlayed = False

                while otherHasPlayed == False:
                    data = self.conn.recv(maxData)
                    decodedData = json.loads(data.decode())
                    otherI = decodedData["row"]
                    otherJ = decodedData["column"]

                    if otherI > self.game.dimension or otherJ > self.game.dimension:
                        self.conn.send('no'.encode())

                    otherHasPlayed = self.game.play(otherI, otherJ)
                    otherHasPlayedData = 'no' if otherHasPlayed == False else 'yes'
                    otherHasPlayedData = 'quit' if self.isGameOver == True else otherHasPlayedData
                    self.conn.send(otherHasPlayedData.encode())

                    self.log("Other played: {}, {}".format(otherI,otherJ))

                self.root.bind("<Button-1>",lambda e: self.mouse_pressed(e))
                self.draw_board()
                self.canvas.mainloop()

        except InvalidMoveError:
            self.log("Invalid move. {},{}".format(i,j))

    def shutdown(self, text):
        self.move_label["text"] = text 
        self.root.unbind("<Button-1>")
        if isinstance(self.players[1], AiPlayerInterface): 
            self.players[1].kill(self.game)
        if isinstance(self.players[2], AiPlayerInterface): 
            self.players[2].kill(self.game)


 
    def ai_move(self):
        player_obj = self.players[self.game.current_player]
        try:
            i,j = player_obj.get_move(self.game)
            player = "Dark" if self.game.current_player == 1 else "Light"
            player = "{} {}".format(player_obj.name, player)
            self.log("{}: {},{}".format(player, i,j))
            self.game.play(i,j)
            self.draw_board()
            if not get_possible_moves(self.game.board, self.game.current_player):
                if get_score(self.game.board)[0] > get_score(self.game.board)[1]:
                    self.shutdown("Dark wins!")
                elif get_score(self.game.board)[0] < get_score(self.game.board)[1]:
                    self.shutdown("White wins!")
                else:
                    self.shutdown("Tie!")
            elif isinstance(self.players[self.game.current_player], AiPlayerInterface):
                self.root.after(1, lambda: self.ai_move())
            else: 
                self.root.bind("<Button-1>",lambda e: self.mouse_pressed(e))        
        except AiTimeoutError:
            self.shutdown("Game Over, {} lost (timeout)".format(player_obj.name))

    def run(self):

        if isinstance(self.players[1], AiPlayerInterface):
            self.root.after(10, lambda: self.ai_move())
        else: 
            self.root.bind("<Button-1>",lambda e: self.mouse_pressed(e))
            
            #self.root.bind("<Button-1>", lambda e: self.mouse_pressed(e))
        self.draw_board()
        self.canvas.mainloop()

        self.log("Other played: " + str(otherI) + ", " + str(otherJ))

    def draw_board(self):
        self.game_label["text"] = "Othello"
        self.game_label["fg"] = "white"
        self.game_label["bg"] = "black"
        self.game_label["font"] = "Helvetica 72 bold"

        self.draw_current_player()
        player = "Player 1: Dark" if self.game.current_player == 1 else "Player 2: Light"
        self.move_label["text"]= player
        self.score_label["text"]= "Dark {} : {} Light".format(*get_score(self.game.board)) 
        self.draw_grid()
        self.draw_disks()

        self.restart_button["text"] = "Restart Game"
        self.restart_button["command"] = self.restart_game

    def log(self, msg, newline = True): 
        self.text.insert("end","{}{}".format(msg, "\n" if newline else ""))
        self.text.see("end")
 
    def draw_grid(self):
        fillColor = "green"
        for i in range(self.height):
            for j in range(self.width):
                self.canvas.create_rectangle(i*self.cell_size + self.offset, j*self.cell_size + self.offset, (i+1)*self.cell_size + self.offset, (j+1)*self.cell_size + self.offset, fill=fillColor)
       
    def draw_disk(self, i,j, color):
        x = i * self.cell_size + self.offset
        y = j * self.cell_size + self.offset
        padding =2 
        self.canvas.create_oval(x+padding, y+padding, x+self.cell_size-padding, y+self.cell_size-padding, fill=color)
        
    def draw_disks(self):
        for i in range(self.height): 
            for j  in range(self.width): 
                if self.game.board[i][j] == 1:
                    self.draw_disk(j, i, "black")
                elif self.game.board[i][j] == 2:
                    self.draw_disk(j, i, "white")

    def draw_current_player(self):
        player = "black" if self.game.current_player == 1 else "white"
        padding = 3
        self.current_player_canvas.create_rectangle(self.offset, self.offset, self.cell_size+self.offset, self.cell_size+self.offset, fill="dark green")
        self.current_player_canvas.create_oval(self.offset+padding, self.offset+padding, self.cell_size + self.offset-padding, self.cell_size + self.offset -padding, fill="black" if self.game.current_player == 1 else "white")

    def restart_game(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

def main():
    
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
    gui = OthelloGui(game, p1, p2) 
    gui.run()

if __name__ == "__main__":
    main()