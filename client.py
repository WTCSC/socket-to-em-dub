import socket
import threading
from checkers import Checkers

# Function to continuously listen for incoming moves from the server.
def receive_moves(sock, game, my_color):
    while True:
        try:
            # Receive a message from the server (up to 1024 bytes).
            data = sock.recv(1024)
            if not data:
                print("Connection closed by remote.")
                break
            # Decode the received data into a string and remove extra spaces.
            msg = data.decode().strip()
            # Check if the remote player has quit the game.
            if msg.lower() == 'q':
                print("Remote player quit the game.")
                break
            # The message should be a move string: "from_row,from_col to_row,to_col"
            parsed = game.parse_move(msg)
            if parsed:
                from_row, from_col, to_row, to_col = parsed
                # Attempt to apply the move on the local game board.
                if game.move_piece(from_row, from_col, to_row, to_col):
                    game.switch_player()  # Change the turn if move is valid.
                    print("\nRemote move applied:", msg)
                else:
                    print("Remote sent an invalid move:", msg)
            else:
                print("Invalid move format received:", msg)
        except Exception as e:
            print("Error receiving move:", e)
            break
    # Close the socket when finished.
    sock.close()
    exit()

def main():
    # Ask the user for the server IP and port to connect.
    host = input("Enter server IP: ").strip()
    port = int(input("Enter server port: "))
    # Create a TCP socket.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Attempt to connect to the server.
        sock.connect((host, port))
    except Exception as e:
        print("Could not connect to server:", e)
        return

    print("Connected to server at", host, port)

    # Initialize the Checkers game.
    game = Checkers()
    # Set the board to flip so that the client's pieces appear at the bottom.
    game.flip = True
    game.display_board()  # Show the initial board state after connection.

    # Client is assigned blue pieces and waits for the red player's first move.
    my_color = 'b'
    # Start a separate thread to handle receiving moves from the server.
    threading.Thread(target=receive_moves, args=(sock, game, my_color), daemon=True).start()

    # Main loop for sending moves when it's the client's turn.
    while True:
        if game.current_player == my_color:
            # Display the board before taking input to show the latest state.
            game.display_board()
            move = input("Your move (format: from_row,from_col to_row,to_col) or 'q' to quit: ").strip()
            if move.lower() == 'q':
                # Notify the server that the client is quitting.
                sock.sendall("q".encode())
                print("Quitting game.")
                break
            parsed = game.parse_move(move)
            if not parsed:
                print("Invalid move format. Try again.")
                continue
            from_row, from_col, to_row, to_col = parsed
            # Try applying the move to the local game board.
            if game.move_piece(from_row, from_col, to_row, to_col):
                # If move is valid, send it to the server.
                sock.sendall(move.encode())
                # Show the updated board immediately.
                game.display_board()
                game.switch_player()  # Switch turn after a valid move.
            else:
                print("Invalid move. Try again.")

    # Close the socket when the game ends.
    sock.close()

if __name__ == "__main__":
    main()