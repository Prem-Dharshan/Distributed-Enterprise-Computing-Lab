import socket
import threading
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger()

clients = {}
lock = threading.Lock()


# Broadcast function to send a message to all clients
def broadcast(message, sender_socket=None):
    with lock:
        for client_socket, username in clients.items():
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode('utf-8'))
                except Exception as e:
                    logger.error(f"Error sending message: {e}")
                    client_socket.close()
                    del clients[client_socket]


# Handle communication with a single client
def handle_client(client_socket, client_address):
    try:
        # Receive and store the username
        username = client_socket.recv(1024).decode('utf-8')
        with lock:
            clients[client_socket] = username
        logger.info(f"{username} connected from {client_address}")
        broadcast(f"{username} has joined the chat!", sender_socket=client_socket)

        # Handle incoming messages
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            full_message = f"{username}: {message}"
            logger.info(full_message)
            broadcast(full_message, sender_socket=client_socket)
    except Exception as e:
        logger.error(f"Error handling client {client_address}: {e}")
    finally:
        # Remove the client on disconnect
        with lock:
            username = clients.pop(client_socket, "Unknown")
        logger.info(f"{username} disconnected.")
        broadcast(f"{username} has left the chat.")
        client_socket.close()


# Main server function
def start_server(host="0.0.0.0", port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    logger.info(f"Server started on {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
