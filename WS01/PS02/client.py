import socket
import logging

# Configure logging
logging.basicConfig(filename="client.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


def connect_to_server(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))
        logging.info(f"Connected to server at {server_ip}:{server_port}")
    except Exception as e:
        logging.error(f"Connection failed: {e}")
        return None
    return client_socket


def client_program():
    server_ip = input("Enter main server IP: ")
    server_port = int(input("Enter main server port: "))

    client_socket = connect_to_server(server_ip, server_port)
    if not client_socket:
        return

    while True:
        action = input("Do you want to upload or download a file? (upload/download): ").lower()

        if action == "upload":
            file_path = input("Enter the path of the file to upload: ")
            logging.info(f"Uploading file: {file_path}")
            try:
                with open(file_path, 'rb') as file:
                    client_socket.sendall(file.read())
                logging.info("File uploaded successfully.")
            except Exception as e:
                logging.error(f"File upload failed: {e}")

        elif action == "download":
            file_name = input("Enter the name of the file to download: ")
            logging.info(f"Downloading file: {file_name}")
            try:
                client_socket.sendall(file_name.encode())
                with open(file_name, 'wb') as file:
                    file_data = client_socket.recv(1024)
                    file.write(file_data)
                logging.info("File downloaded successfully.")
            except Exception as e:
                logging.error(f"File download failed: {e}")

        elif action == "exit":
            client_socket.sendall(b"exit")
            logging.info("Exiting client program.")
            break


if __name__ == "__main__":
    client_program()
