# ANSI escape codes
RED = '\033[38;2;228;8;10m'
BLUE = '\033[94m'
LIGHT_BROWN_BG = '\033[48;2;209;159;109m'  # Light brown squares
DARK_BROWN_BG = '\033[48;2;101;67;33m'    # Dark brown squares
RESET = '\033[0m'


class Checkers():
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

    def move_piece(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = ' '

    def check_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = self.board[start_row][start_col]
    
        # Check if move is diagonal
        if abs(end_col - start_col) != abs(end_row - start_row):
            return False
        
        # Check direction based on piece
        if piece == 'X' and end_row <= start_row:  # X moves down
            return False
        if piece == 'O' and end_row >= start_row:  # O moves up 
            return False
        
        # Check distance
        distance = abs(end_row - start_row)
        if distance > 2 or distance == 0:
            return False
        
        # Handle jumps
        if distance == 2:
            # Calculate position of jumped piece
            jumped_row = (start_row + end_row) // 2
            jumped_col = (start_col + end_col) // 2
            jumped_piece = self.board[jumped_row][jumped_col]
        
            # Must jump opponent's piece
            if (piece == 'X' and jumped_piece != 'O') or \
            (piece == 'O' and jumped_piece != 'X'):
                return False
            
        return True
    
 ''':)'''  
