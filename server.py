import socket
import threading
from checkers import Checkers  # Import the Checkers game logic

# This function handles receiving moves from the remote client.
def receive_moves(conn, game, my_color):
    while True:
        try:
            # Receive data from the connected client.
            data = conn.recv(1024)
            if not data:
                print("Connection closed by remote.")
                break
            msg = data.decode().strip()
            if msg.lower() == 'q':
                print("Remote player quit the game.")
                break
            # Parse incoming move command.
            parsed = game.parse_move(msg)
            if parsed:
                from_row, from_col, to_row, to_col = parsed
                # Attempt to execute the move on the board.
                if game.move_piece(from_row, from_col, to_row, to_col):
                    game.switch_player()  # Change turn after a valid move
                    print("\nRemote move applied:", msg)
                else:
                    print("Remote sent an invalid move:", msg)
            else:
                print("Invalid move format received:", msg)
        except Exception as e:
            print("Error receiving move:", e)
            break
    # Clean up connection on thread exit.
    conn.close()
    exit()

def main():
    # Ask user to supply the port for hosting the game.
    port = int(input("Enter port to host the game on: "))
    # Create a TCP/IP socket.
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(("", port))
    server_sock.listen(1)
    print(f"Hosting game on port {port}, waiting for connection...")
    # Accept a client connection.
    conn, addr = server_sock.accept()
    print("Connection established with", addr)

    game = Checkers()  # Create an instance of the game.
    game.display_board()  # Display initial board state

    # For the server, assign red pieces and allow the first move.
    my_color = 'r'

    # Start a new thread to listen for remote moves.
    threading.Thread(target=receive_moves, args=(conn, game, my_color), daemon=True).start()

    # Main loop to process the local player's moves.
    while True:
        if game.current_player == my_color:
            game.display_board()
            move = input("Your move (format: from_row,from_col to_row,to_col) or 'q' to quit: ").strip()
            if move.lower() == 'q':
                # Inform the remote client that this player is quitting.
                conn.sendall("q".encode())
                print("Quitting game.")
                break
            parsed = game.parse_move(move)
            if not parsed:
                print("Invalid move format. Try again.")
                continue
            from_row, from_col, to_row, to_col = parsed
            # Execute the move locally.
            if game.move_piece(from_row, from_col, to_row, to_col):
                # Transmit the valid move to the remote player.
                conn.sendall(move.encode())
                game.display_board()  # Refresh board view after move
                game.switch_player()  # Change current player
            else:
                print("Invalid move. Try again.")

    # Close the connection and socket after game ends.
    conn.close()
    server_sock.close()

if __name__ == "__main__":
    main()