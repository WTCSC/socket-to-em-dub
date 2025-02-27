import socket
import threading
from checkers import Checkers  # Import the Checkers game logic

# This function continuously receives moves from the remote player.
def receive_moves(conn, game, my_color):
    while True:
        try:
            # Receive data from the connection (max 1024 bytes)
            data = conn.recv(1024)
            if not data:
                print("Connection closed by remote.")
                break
            msg = data.decode().strip()
            if msg.lower() == 'q':
                print("Remote player quit the game.")
                break
            # Parse the move received from the peer.
            parsed = game.parse_move(msg)
            if parsed:
                from_row, from_col, to_row, to_col = parsed
                # Attempt to perform the move on the local game board.
                if game.move_piece(from_row, from_col, to_row, to_col):
                    game.switch_player()  # Switch turns
                    print("\nRemote move applied:", msg)
                else:
                    print("Remote sent an invalid move:", msg)
            else:
                print("Invalid move format received:", msg)
        except Exception as e:
            print("Error receiving move:", e)
            break
    # Clean up connection on exit.
    conn.close()
    exit()

def main():
    # Ask user which port to host the game on.
    port = int(input("Enter port to host the game on: "))
    # Create a socket for the server.
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(("", port))
    server_sock.listen(1)
    print(f"Hosting game on port {port}, waiting for connection...")
    # Accept a connection from a remote client.
    conn, addr = server_sock.accept()
    print("Connection established with", addr)

    game = Checkers()  # Initialize the game
    game.display_board()  # Display the initial board configuration

    # The server (this client file) uses red pieces and goes first.
    my_color = 'r'

    # Start a thread to handle receiving moves from the remote player.
    threading.Thread(target=receive_moves, args=(conn, game, my_color), daemon=True).start()

    # Main loop to allow local moves as long as it's the player's turn.
    while True:
        if game.current_player == my_color:
            game.display_board()
            move = input("Your move (format: from_row,from_col to_row,to_col) or 'q' to quit: ").strip()
            if move.lower() == 'q':
                # Notify remote that the player is quitting.
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
                # Send the valid move to the peer.
                conn.sendall(move.encode())
                game.display_board()  # Refresh board view
                game.switch_player()  # Switch turns after successful move
            else:
                print("Invalid move. Try again.")

    # Close connections and shutdown server.
    conn.close()
    server_sock.close()

if __name__ == "__main__":
    main()