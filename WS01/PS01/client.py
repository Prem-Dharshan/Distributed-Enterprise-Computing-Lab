import socket
import threading


# Receive messages from the server
def receive_messages(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
    except Exception as e:
        print(f"Error receiving message: {e}")
    finally:
        print("Disconnected from server.")
        client_socket.close()


# Main client function
def start_client(server_host="127.0.0.1", server_port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        username = input("Enter your username: ")

        client_socket.connect((server_host, server_port))
        print(f"Connected to chat server at {server_host}:{server_port}")

        client_socket.send(username.encode('utf-8'))

        thread = threading.Thread(target=receive_messages, args=(client_socket,))
        thread.start()

        while True:
            message = input("Type a message (or 'exit' to leave): ")
            if message.lower() == "exit":
                break
            client_socket.send(message.encode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Connection closed.")


if __name__ == "__main__":
    server_host = input("Enter server IP address: ")
    server_port = int(input("Enter server port: "))
    start_client(server_host, server_port)
