from tkinter import *
from tkinter import scrolledtext

from othello_game import OthelloGameManager, AiPlayerInterface, Player, InvalidMoveError, AiTimeoutError
from othello_shared import get_possible_moves, get_score
from othello_gui import *

import socket
import json

port = 5000
host = socket.gethostname()
maxData = 4096

def main():

	clientSocket = socket.socket()
	clientSocket.connect((host,port))

	while True:

		board = clientSocket.recv(maxData)

		board = json.loads(board.decode())

		print(str(board))

		hasPlayed = False

		while hasPlayed == False:

			i = input("Type row: ")
			j = input("Type column: ")

			data = json.dumps({'row' : int(i), 'column' : int(j)})
			clientSocket.send(data.encode())

			canGo = clientSocket.recv(maxData).decode()
			#print(canGo)

			if canGo == 'yes':
				hasPlayed = True



	clientSocket.close()

if __name__ == "__main__":
	main()