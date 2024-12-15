import socket
import threading
import os
import logging
import subprocess
import sys

# Configure logging
logging.basicConfig(filename="main_server.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


# Start a storage server
def start_storage_server(port):
    try:
        storage_server = subprocess.Popen([sys.executable, "storage_server.py", str(port)])
        logging.info(f"Started storage server on port {port}")
        return storage_server
    except Exception as e:
        logging.error(f"Error starting storage server on port {port}: {e}")


# Stop a storage server
def stop_storage_server(storage_server):
    try:
        storage_server.terminate()
        storage_server.wait()
        logging.info("Storage server stopped successfully.")
    except Exception as e:
        logging.error(f"Error stopping storage server: {e}")


# Main server to handle connections
def handle_client_connection(client_socket):
    try:
        # Handle communication with the client
        logging.info("Connected to client")
        client_socket.sendall("Welcome to the file storage system!".encode())
        while True:
            data = client_socket.recv(1024)
            if data:
                logging.info(f"Received from client: {data.decode()}")
                client_socket.sendall("Data received!".encode())
            else:
                break
    except Exception as e:
        logging.error(f"Error handling client: {e}")
    finally:
        client_socket.close()


def start_main_server(host, port, storage_server_count):
    try:
        # Create server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        logging.info(f"Main server started on {host}:{port}")

        # Start storage servers
        storage_servers = []
        for i in range(storage_server_count):
            storage_server = start_storage_server(5001 + i)
            storage_servers.append(storage_server)

        while True:
            client_socket, _ = server_socket.accept()
            logging.info("New connection established.")
            threading.Thread(target=handle_client_connection, args=(client_socket,)).start()

    except Exception as e:
        logging.error(f"Server error: {e}")
    finally:
        logging.info("Shutting down main server.")


if __name__ == "__main__":
    # Ask for user input to configure the server
    host = input("Enter the server IP (e.g., 127.0.0.1): ")
    port = int(input("Enter the server port: "))
    storage_server_count = int(input("Enter the number of storage servers: "))

    start_main_server(host, port, storage_server_count)
