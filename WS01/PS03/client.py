import socket
import logging

logging.basicConfig(filename="game_client.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


def client_program():
    host = input("Enter server IP: ")
    port = int(input("Enter server port: "))

    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    token = client_socket.recv(1024).decode()
    logging.info(f"Connected to the server. Your token is {token}")

    while True:
        board = client_socket.recv(1024).decode()
        print(f"Current board:\n{board}")

        move = input(f"Your turn ({token}). Enter row,column (0-2): ")
        if move.lower() == 'exit':
            client_socket.send('exit'.encode())
            break
        client_socket.send(move.encode())

        status = client_socket.recv(1024).decode()
        print(status)
        logging.info(f"Player made a move: {move} with status: {status}")

        if 'wins' in status or 'draw' in status:
            break

    client_socket.close()


if __name__ == "__main__":
    client_program()
