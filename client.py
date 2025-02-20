import socket
import ast
from checkers import Checkers


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = input('Enter server IP: ')
    port = int(input('Enter server port: '))

    try:
        client.connect((server_ip, port))
        print('Connected to server')
        client.recv(1024).decode()
        game = Checkers()
        game.print_board()
        myturn = False 
        print("You're Blue")
        while True:
            if not myturn:
                data = client.recv(1024).decode()
                if not data:
                    print("Server disconnected.")
                    break
                if data == 'quit':
                    print("Server ended the game.")
                    break
                
                start, end = map(ast.literal_eval, data.split())
                game.move_piece(start, end)
                myturn = True
                game.print_board()
            else:
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
                    client.send(f'{start} {end}'.encode())
                    myturn = False
                else:
                    print('Invalid move')
    except ConnectionRefusedError:
        print('Connection refused. Server is not available.')
    finally:
        client.close()

if __name__ == '__main__':
    main()