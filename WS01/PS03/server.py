import socket
import threading
import logging

logging.basicConfig(filename="game_server.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_turn = 'X'  # Player 'X' starts the game
        self.winner = None  # No winner initially

    def display_board(self):
        return f'''
        {self.board[0]} | {self.board[1]} | {self.board[2]}
        ---+---+---
        {self.board[3]} | {self.board[4]} | {self.board[5]}
        ---+---+---
        {self.board[6]} | {self.board[7]} | {self.board[8]}
        '''

    def make_move(self, position, player):
        if self.board[position] == ' ' and player == self.current_turn:
            self.board[position] = player
            if self.check_winner(player):
                self.winner = player
            elif ' ' not in self.board:
                self.winner = 'D'  # Draw
            else:
                self.current_turn = 'O' if player == 'X' else 'X'
            return True
        return False

    def check_winner(self, player):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning_combinations:
            if all(self.board[i] == player for i in combo):
                return True
        return False


def handle_session(player1_socket, player2_socket, session_id):
    logging.info(f"Session {session_id} started. Waiting for players.")

    game = TicTacToe()
    player1_socket.send("You are Player 1 (X). Waiting for Player 2.".encode())
    player2_socket.send("You are Player 2 (O). Player 1 will start.".encode())

    while game.winner is None:
        # Player 1's turn
        player1_socket.send(f"Your turn! Current board:\n{game.display_board()}".encode())
        move = player1_socket.recv(1024).decode()
        if move.lower() == 'exit':
            break
        row, col = map(int, move.split(','))
        if game.make_move(row * 3 + col, 'X'):
            logging.info(f"Player 1 made a move: {move} on session {session_id}")
        else:
            player1_socket.send("Invalid move. Try again.".encode())
            continue

        # Check if Player 1 won or if it was a draw
        if game.winner == 'X':
            player1_socket.send("You win!".encode())
            player2_socket.send("Player 1 wins!".encode())
            break
        elif game.winner == 'D':
            player1_socket.send("It's a draw!".encode())
            player2_socket.send("It's a draw!".encode())
            break

        # Player 2's turn
        player2_socket.send(f"Your turn! Current board:\n{game.display_board()}".encode())
        move = player2_socket.recv(1024).decode()
        if move.lower() == 'exit':
            break
        row, col = map(int, move.split(','))
        if game.make_move(row * 3 + col, 'O'):
            logging.info(f"Player 2 made a move: {move} on session {session_id}")
        else:
            player2_socket.send("Invalid move. Try again.".encode())
            continue

        # Check if Player 2 won or if it was a draw
        if game.winner == 'O':
            player2_socket.send("You win!".encode())
            player1_socket.send("Player 2 wins!".encode())
            break
        elif game.winner == 'D':
            player1_socket.send("It's a draw!".encode())
            player2_socket.send("It's a draw!".encode())
            break

    player1_socket.close()
    player2_socket.close()
    logging.info(f"Session {session_id} ended.")


# Main server function
def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    session_id = 1

    logging.info(f"Server started on {host}:{port}")

    try:
        while True:
            logging.info("Waiting for players to connect...")
            player1_socket, player1_address = server_socket.accept()
            logging.info(f"Player 1 connected from {player1_address}")
            player1_socket.send("Welcome to Tic-Tac-Toe! Waiting for Player 2.".encode())

            player2_socket, player2_address = server_socket.accept()
            logging.info(f"Player 2 connected from {player2_address}")
            player2_socket.send("Welcome to Tic-Tac-Toe! Player 1 has connected.".encode())

            logging.info(f"Starting session {session_id}")
            threading.Thread(target=handle_session, args=(player1_socket, player2_socket, session_id)).start()
            session_id += 1

    except KeyboardInterrupt:
        logging.info("Server shutting down.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    host = input("Enter server IP (default 127.0.0.1): ") or '127.0.0.1'
    port = int(input("Enter server port (default 5000): ") or 5000)
    start_server(host, port)
