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


def play_game(game, player1, player2):

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
                toSend += ('\nHost played: '+ str(i) + ' ' +str(j))
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
    play_game(game, p1, p2)