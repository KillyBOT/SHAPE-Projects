#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMS W4701 Artificial Intelligence - Programming Homework 2

This module contains a simple graphical user interface for Othello. 

@author: Daniel Bauer 
"""
from tkinter import *
from tkinter import scrolledtext

import socket, json

import sys, os

port = 5000
host = "209.2.224.12"
maxData = 4096


class OthelloGui(object):

    def __init__(self):

        self.clientSocket = socket.socket()
        self.clientSocket.connect((host,port))

        data = self.clientSocket.recv(maxData).decode()
        print(data)

        self.dimension = int(data)

        #self.players = [None, player1, player2]
        self.height = self.dimension
        self.width = self.dimension 
        
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

        self.board = self.create_initial_board()
        self.draw_board()

        self.log("Connected!")


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

    def get_position(self,x,y):
        i = (x -self.offset) // self.cell_size
        j = (y -self.offset) // self.cell_size
        return i,j

    def mouse_pressed(self,event):

        #self.draw_board()

        hasPlayed = False

        #print(self.board)

        player = "Light"
        i,j = self.get_position(event.x, event.y)
        #print(i, j)
        #self.log("{}: {},{}".format(player, i,j))
        data = json.dumps({'row' : int(i), 'column' : int(j)})
        self.clientSocket.send(data.encode())

        canGo = self.clientSocket.recv(maxData).decode()

        if canGo == 'yes':
            hasPlayed = True
        elif canGo == 'no':
            self.log("Cannot play there")

        if hasPlayed == True:
            board = self.clientSocket.recv(maxData)

            board = json.loads(board.decode())

            self.board = board

        if not get_possible_moves(self.board, 2):
            self.shutdown("Game Over")
            self.clientSocket.close()

        #self.root.bind("<Button-1>",lambda e: self.mouse_pressed(e))  
        self.draw_board()
        self.canvas.mainloop()


    def shutdown(self, text):
        self.move_label["text"] = text 
        self.root.unbind("<Button-1>")
        #if isinstance(self.players[1], AiPlayerInterface): 
        #    self.players[1].kill(self.game)
        #if isinstance(self.players[2], AiPlayerInterface): 
        #    self.players[2].kill(self.game)
 
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

        board = self.clientSocket.recv(maxData)

        board = json.loads(board.decode())

        self.board = board

        self.root.bind("<Button-1>",lambda e: self.mouse_pressed(e))   

        self.draw_board()
        self.canvas.mainloop()

    def draw_board(self):

        self.game_label["text"] = "Othello"
        self.game_label["fg"] = "white"
        self.game_label["bg"] = "black"
        self.game_label["font"] = "Helvetica 72 bold"

        self.draw_current_player()
        player = "Player 2: Light"
        self.move_label["text"]= player

        self.score_label["text"]= "Dark {} : {} Light".format(*get_score(self.board)) 
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
                if self.board[i][j] == 1:
                    self.draw_disk(j, i, "black")
                elif self.board[i][j] == 2:
                    self.draw_disk(j, i, "white")

    def draw_current_player(self):
        player = "white"
        padding = 3
        self.current_player_canvas.create_rectangle(self.offset, self.offset, self.cell_size+self.offset, self.cell_size+self.offset, fill="dark green")
        self.current_player_canvas.create_oval(self.offset+padding, self.offset+padding, self.cell_size + self.offset-padding, self.cell_size + self.offset -padding, fill="white")

    def restart_game(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

#These are the functions used in othello_shared, but I wanted to make the client able to run on its own

def get_score(board):
    p1_count = 0
    p2_count = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 1:
                p1_count += 1
            elif board[i][j] == 2:
                p2_count += 1
    return p1_count, p2_count

def get_possible_moves(board, player):
    """
    Return a list of all possible (column,row) tuples that player can play on
    the current board. 
    """
    result = []
    for i in range(len(board)):
        for j in range(len(board)):
            if board[j][i] == 0:
                lines = find_lines(board,i,j,player)
                if lines: 
                    result.append((i,j))
    return result
def find_lines(board, i, j, player):
    """
    Find all the uninterupted lines of stones that would be captured if player
    plays column i and row j. 
    """
    lines = []
    for xdir, ydir in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], 
                       [-1, 0], [-1, 1]]:
        u = i
        v = j
        line = []

        u += xdir
        v += ydir
        found = False
        while u >= 0 and u < len(board) and v >= 0 and v < len(board):
            if board[v][u] == 0:
                break
            elif board[v][u] == player:
                found = True
                break
            else: 
               line.append((u,v))
            u += xdir
            v += ydir
        if found and line: 
            lines.append(line)
    return lines


def main():
    gui = OthelloGui()
    gui.run()

if __name__ == "__main__":
    main()