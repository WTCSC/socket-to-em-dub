import colorama
import os
colorama.init()

class Checkers:
    # Define color codes for red, blue, and reset
    RED = "\033[31m"
    BLUE = "\033[34m"
    RESET = "\033[0m"

    def __init__(self):
        # Initialize the game board and set the current player
        self.board = self.init_board()
        self.current_player = 'r'
        self.flip = False

    def init_board(self):
        # Create an 8x8 board and place initial pieces
        board = [[' ' for _ in range(8)] for _ in range(8)]

        # Place blue pieces
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    board[i][j] = 'b'

        # Place red pieces
        for i in range(5, 8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    board[i][j] = 'r'
        return board

    def color_piece(self, piece):
        # Return the colored piece based on its type
        if piece == 'r' or piece == 'R':
            return f"{self.RED}{piece}{self.RESET}"
        elif piece == 'b' or piece == 'B':
            return f"{self.BLUE}{piece}{self.RESET}"
        return piece

    def display_board(self):
        # Clear the console and display the board
        os.system('cls' if os.name == 'nt' else 'clear')
        print("   " + " ".join(str(j) for j in range(8)))
        print("  +" + "-+" * 8)

        # Display each row of the board
        rows = list(reversed(range(8))) if self.flip else list(range(8))
        for i in rows:
            colored_row = [self.color_piece(cell) for cell in self.board[i]]
            row_display = f"{i} |" + "|".join(colored_row) + "|"
            print(row_display)
            print("  +" + "-+" * 8)

    def switch_player(self):
        # Switch the current player
        self.current_player = 'b' if self.current_player == 'r' else 'r'

    def parse_move(self, move_str):
        # Parse the move input string and return the positions
        try:
            parts = move_str.strip().split()
            if len(parts) != 2:
                return None
            from_pos = parts[0].split(',')
            to_pos = parts[1].split(',')
            if len(from_pos) != 2 or len(to_pos) != 2:
                return None
            from_row, from_col = int(from_pos[0]), int(from_pos[1])
            to_row, to_col = int(to_pos[0]), int(to_pos[1])
            return from_row, from_col, to_row, to_col
        except ValueError:
            return None

    def is_within_bounds(self, row, col):
        # Check if the position is within the board bounds
        return 0 <= row < 8 and 0 <= col < 8

    def valid_move(self, from_row, from_col, to_row, to_col):
        # Validate the move based on the game rules
        if not (self.is_within_bounds(from_row, from_col) and self.is_within_bounds(to_row, to_col)):
            return False, "Move out of board bounds."
        
        piece = self.board[from_row][from_col]
        if piece == ' ' or piece.lower() != self.current_player:
            return False, "You must move your own piece."
        
        if self.board[to_row][to_col] != ' ':
            return False, "Destination square is not empty."

        row_diff = to_row - from_row
        col_diff = to_col - from_col
        abs_row_diff = abs(row_diff)
        abs_col_diff = abs(col_diff)
        is_king = piece.isupper()

        # Check for normal move
        if abs_row_diff == 1 and abs_col_diff == 1:
            if not is_king:
                if self.current_player == 'r' and row_diff != -1:
                    return False, "Red pieces must move up (to lower row indices)."
                if self.current_player == 'b' and row_diff != 1:
                    return False, "Blue pieces must move down (to higher row indices)."
            return True, ""

        # Check for capture move
        elif abs_row_diff == 2 and abs_col_diff == 2:
            mid_row = from_row + row_diff // 2
            mid_col = from_col + col_diff // 2
            jumped_piece = self.board[mid_row][mid_col]
            if jumped_piece == ' ' or jumped_piece.lower() == self.current_player:
                return False, "No opponent piece to capture."
            if not is_king:
                if self.current_player == 'r' and row_diff != -2:
                    return False, "Red pieces must capture upward."
                if self.current_player == 'b' and row_diff != 2:
                    return False, "Blue pieces must capture downward."
            return True, ""
        else:
            return False, "Invalid move distance."

    def move_piece(self, from_row, from_col, to_row, to_col):
        # Move the piece on the board if the move is valid
        valid, message = self.valid_move(from_row, from_col, to_row, to_col)
        if not valid:
            print("Invalid move:", message)
            return False

        row_diff = to_row - from_row

        # Handle capture move
        if abs(row_diff) == 2:
            mid_row = from_row + row_diff // 2
            mid_col = from_col + (to_col - from_col) // 2
            self.board[mid_row][mid_col] = ' '

        # Move the piece
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = ' '

        # Promote to king if reaching the opposite end
        piece = self.board[to_row][to_col]
        if piece.lower() == 'r' and to_row == 0:
            self.board[to_row][to_col] = 'R'
        if piece.lower() == 'b' and to_row == 7:
            self.board[to_row][to_col] = 'B'

        return True

    def check_winner(self):
        # Check if there is a winner
        red_exists = any(cell.lower() == 'r' for row in self.board for cell in row if cell != ' ')
        blue_exists = any(cell.lower() == 'b' for row in self.board for cell in row if cell != ' ')
        if not red_exists:
            return 'b'
        if not blue_exists:
            return 'r'
        return None

    def run(self):
        # Main game loop
        print("Welcome to Command Line Checkers!")
        while True:
            self.display_board()
            winner = self.check_winner()
            if winner:
                print(f"Player '{winner}' wins!")
                break

            print(f"Player '{self.current_player}' turn.")
            move_input = input("Enter your move (format: from_row,from_col to_row,to_col) or 'q' to quit: ").strip()
            if move_input.lower() == 'q':
                print("Exiting game.")
                break

            parsed_move = self.parse_move(move_input)
            if not parsed_move:
                print("Invalid move format. Please try again.")
                continue

            from_row, from_col, to_row, to_col = parsed_move
            if self.move_piece(from_row, from_col, to_row, to_col):
                self.switch_player()

if __name__ == "__main__":
    game = Checkers()
    game.run()