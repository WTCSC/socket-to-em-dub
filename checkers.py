from colorama import Fore, Back, init, Style
from random import choice



class Board():
    def __init__(self):
        self.size = 8
        self.pieces = ['X', 'O', '♔', ' ']
        self.board = [[' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X'],
                      ['X', ' ', 'X', ' ', 'X', ' ', 'X', ' '],
                      [' ', 'X', ' ', 'X', ' ', 'X', ' ', 'X'],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                      ['O', ' ', 'O', ' ', 'O', ' ', 'O', ' '],
                      [' ', 'O', ' ', 'O', ' ', 'O', ' ', 'O'],
                      ['O', ' ', 'O', ' ', 'O', ' ', 'O', ' ']] 

    def print_board(self):
        horzwall = '+---+---+---+---+---+---+---+---+'
        vertwall = '|'
        for row in self.board:
            print(Back.WHITE + Fore.BLACK + horzwall, end='')
            print(Style.RESET_ALL)
            for piece in row:
                print(Back.WHITE + Fore.BLACK + vertwall, end=' ')
                if piece == 'X':
                    print(Back.WHITE + Fore.RED + 'O', end=' ')
                elif piece == 'O':
                    print(Back.WHITE + Fore.BLUE + 'O', end=' ')
                else:
                    print(Back.WHITE + Fore.BLACK + piece, end=' ')
            print(Back.WHITE + Fore.BLACK + vertwall, end='')
            print(Style.RESET_ALL)
        print(Back.WHITE + Fore.BLACK + horzwall, end='')
        print(Style.RESET_ALL)

board = Board()
board.print_board()