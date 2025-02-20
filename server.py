import socket
import ast
from checkers import Checkers

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Ensure valid port input
    while True:
        try:
            port = int(input('Enter port: '))
            break
        except ValueError:
            print("Invalid port. Enter a number.")

    server.bind(('', port))
    server.listen(1)
    game = Checkers()
    
    print('Waiting for connection...')
    conn, addr = server.accept()
    print(f'Connected to {addr}')
    
    conn.send("ready".encode())
    game.print_board()
    
    myturn = True
    try:
        while True:
            if myturn:
                move = input('Enter move (start_x,start_y end_x,end_y): ').split()
                if len(move) != 2:
                    print("Invalid format. Enter two coordinates.")
                    continue
                
                try:
                    start = tuple(map(int, move[0].split(',')))
                    end = tuple(map(int, move[1].split(',')))
                except ValueError:
                    print("Invalid input. Use numbers separated by commas.")
                    continue

                if game.check_move(start, end):
                    game.move_piece(start, end)
                    conn.send(f'{start} {end}'.encode())
                    myturn = False
                else:
                    print('Invalid move')
            else:
                data = conn.recv(1024).decode()
                if not data:
                    print("Client disconnected.")
                    break
                if data == 'quit':
                    print("Client ended the game.")
                    break
                
                try:
                    start, end = map(ast.literal_eval, data.split())
                    game.move_piece(start, end)
                    myturn = True
                except (ValueError, SyntaxError):
                    print("Received invalid move data.")
                    break

            game.print_board()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        conn.close()
        server.close()

if __name__ == '__main__':
    main()
