# This file is where game logic lives. No input
# or output happens here. The logic in this file
# should be unit-testable.

import random
import pandas as pd
from os.path import exists

class Board:
    def __init__(self):
        self.rows = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

    def __str__(self):
        print_string = ''
        for row in self.rows:
            for item in row:
                if item is None:
                    print_string = print_string + '.'
                else:
                    print_string = print_string + item
            print_string = print_string + '\n'
        return print_string
    
    def get(self, x, y):
        return self.rows[x][y]
    
    def set(self, x, y, value):
        self.rows[x][y] = value

    def get_winner(self):
        winner = None
        # first col
        if self.rows[0][0] == self.rows[1][0] == self.rows[2][0] and self.rows[0][0] != None:
            winner = self.rows[0][0]
            return winner
        # second col
        if self.rows[0][1] == self.rows[1][1] == self.rows[2][1] and self.rows[0][1] != None:
            winner = self.rows[0][1]
            return winner
        # third col
        if self.rows[0][2] == self.rows[1][2] == self.rows[2][2] and self.rows[0][2] != None:
            winner = self.rows[0][2]
            return winner
        # first row
        if self.rows[0][0] == self.rows[0][1] == self.rows[0][2] and self.rows[0][0] != None:
            winner = self.rows[0][0]
            return winner
        # second row
        if self.rows[1][0] == self.rows[1][1] == self.rows[1][2] and self.rows[1][0] != None:
            winner = self.rows[1][1]
            return winner
        # third row
        if self.rows[2][0] == self.rows[2][1] == self.rows[2][2] and self.rows[2][0] != None:
            winner = self.rows[2][0]
            return winner
        # down
        if self.rows[0][0] == self.rows[1][1] == self.rows[2][2] and self.rows[0][0] != None:
            winner = self.rows[0][0]
            return winner
        # up
        if self.rows[0][2] == self.rows[1][1] == self.rows[2][0] and self.rows[0][2] != None:
            winner = self.rows[0][2]
        return winner

    def get_row_size(self):
        return len(self.rows)
    
    def get_col_size(self):
        return len(self.rows[0])
    
    def is_board_filled(self):
        for row in self.rows:
            for item in row:
                if item is None:
                    return False
        return True
class Player:
    def __init__(self, symbol, player_type, player_name):
        self.symbol = symbol
        self.player_type = player_type
        self.player_name = player_name

    def get_symbol(self):
        return self.symbol
    
    def get_type(self):
        return self.player_type

class Human(Player):
    def __init__(self, symbol, name):
        super().__init__(symbol, "Human", name)

    def get_move(self, board):
        while True:
            x = input("Please put down your move, in row: ")
            y = input("Please put down your move, in col: ")
            # check if the input is number
            if x.isnumeric() == False or y.isnumeric() == False:
                print("Please input in numbers")
                continue
            x = int(x)
            y = int(y)
            # check if the input its within the viable range
            if x >= board.get_row_size() or x < 0 or y >= board.get_col_size() or y < 0:
                print("Please input the number within the board size")
                continue
            # check if the input position is placable
            if board.get(int(x), int(y)) is None:
                board.set(int(x), int(y), self.symbol)
                break
            else:
                print("Cannot Place on already used position!")

class Bot(Player):
    def __init__(self, symbol, name):
        super().__init__(symbol, "Bot", name)

    def get_move(self, board):
        while True:
            x = random.randint(0,2)
            y = random.randint(0,2)
            if board.get(int(x), int(y)) is None:
                board.set(int(x), int(y), self.symbol)
                break

class Game:
    def __init__(self, player_x, player_o, games_filename):
        self.board = Board()
        self.player_x = player_x
        self.player_x.set_symbol = 'X'
        self.player_o = player_o
        self.player_o.set_symbol = 'O'
        self.current_player = 'O'
        self.games_filename = games_filename
        if (exists(games_filename)):
            self.games = pd.read_csv(games_filename)
        else:
            self.games = pd.DataFrame(columns=[
                "Game ID",
                "Player 1",
                "Player 2",
                "Winner",
            ])
    
    def next_player(self):
        if self.current_player == 'X':
            self.current_player = 'O'
            return self.player_o
        else:
            self.current_player = 'X'
            return self.player_x
    
    def print_turn(self, player):
        print_string = '\nCurrent Turn: ' + player.get_type() + ' ' + self.current_player
        print(print_string)
        print(self.board)

    def announce_result(self, winner, filled):
        print(self.board)
        if winner is None and filled is True:
            print("\nNo More Spot to place Chess, No Winner is found")
            self.games.loc[len(self.games)] = {
                "Game ID": len(self.games),
                "Player 1": self.player_x.player_name,
                "Player 2": self.player_o.player_name,
                "Winner": "No Winner",
            }
        else:
            print("\nWinner is: ", winner)
            self.games.loc[len(self.games)] = {
                "Game ID": len(self.games),
                "Player 1": self.player_x.player_name,
                "Player 2": self.player_o.player_name,
                "Winner": self.player_x.player_name if winner == self.player_x.symbol else self.player_o.player_name,
            }
        counts = self.games['Winner'].value_counts()
        print(self.player_x.player_name, "'s total wins: ", counts[self.player_x.player_name] if self.player_x.player_name in counts else 0)
        print(self.player_o.player_name, "'s total wins: ", counts[self.player_o.player_name] if self.player_o.player_name in counts else 0)
        print("total draw: ", counts["No Winner"] if "No Winner" in counts else 0)

    def run(self):
        winner = self.board.get_winner()
        filled = self.board.is_board_filled()
        while winner is None and filled is False:
            next_player = self.next_player()
            self.print_turn(next_player)
            next_player.get_move(self.board)
            winner = self.board.get_winner()
            filled = self.board.is_board_filled()
        self.announce_result(winner, filled)
        self.games.to_csv(self.games_filename, index=False)
