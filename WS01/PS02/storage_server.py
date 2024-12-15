import socket
import threading
import logging
import os
import sys

# Configure logging
logging.basicConfig(filename="storage_server.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Handle client requests to store or retrieve files
def handle_client_connection(client_socket):
    try:
        logging.info("Storage server connected to client.")
        client_socket.sendall("Storage server ready.".encode())
        while True:
            data = client_socket.recv(1024)
            if data:
                logging.info(f"Received request: {data.decode()}")
                client_socket.sendall("File operation complete.".encode())
            else:
                break
    except Exception as e:
        logging.error(f"Error in storage server: {e}")
    finally:
        client_socket.close()

def start_storage_server(port):
    try:
        # Create storage server socket
        storage_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        storage_server_socket.bind(('127.0.0.1', port))
        storage_server_socket.listen(5)
        logging.info(f"Storage server listening on port {port}.")

        while True:
            client_socket, _ = storage_server_socket.accept()
            logging.info("New connection from storage client.")
            threading.Thread(target=handle_client_connection, args=(client_socket,)).start()

    except Exception as e:
        logging.error(f"Error in storage server: {e}")
    finally:
        logging.info("Storage server stopped.")

if __name__ == "__main__":
    port = int(sys.argv[1])
    start_storage_server(port)
