from random import choice

# ANSI escape codes
RED = '\033[38;2;;21;21m'
BLUE = '\033[94m'
LIGHT_BROWN_BG = '\033[48;2;209;159;109m'  # Light brown squares
DARK_BROWN_BG = '\033[48;2;101;67;33m'    # Dark brown squares
RESET = '\033[0m'

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
        for row_idx, row in enumerate(self.board):
            print(f'{horzwall}{RESET}')
            print(f'{vertwall}', end='')  # Left wall without background
            for col_idx, piece in enumerate(row):
                # Determine background color based on position
                bg = DARK_BROWN_BG if (row_idx + col_idx) % 2 else LIGHT_BROWN_BG
                if piece == 'X':
                    print(f'{bg} {RED}●{RESET}{bg} ', end='')
                elif piece == 'O':
                    print(f'{bg} {BLUE}●{RESET}{bg} ', end='')
                else:
                    print(f'{bg}   ', end='')
                print(f'{RESET}{vertwall}', end='')  # Right wall without background
            print()  # New line
        print(f'{horzwall}{RESET}')

board = Board()
board.print_board()