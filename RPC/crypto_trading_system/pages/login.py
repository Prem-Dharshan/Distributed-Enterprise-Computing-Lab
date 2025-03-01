import streamlit as st
import json
import socket

SIZE = 1024

class RPCClient:
    def __init__(self, host='localhost', port=8080):
        self.address = (host, port)
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.address)

    def disconnect(self):
        if self.sock:
            self.sock.close()

    def call(self, method, *args):
        if not self.sock:
            self.connect()
        self.sock.sendall(json.dumps((method, args, {})).encode())
        response = self.sock.recv(SIZE).decode()
        return json.loads(response)

def login_page():
    st.title("Login")
    client = RPCClient()

    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.client_id = None
        st.session_state.state = None
        st.session_state.coins = None
        st.session_state.client = client

    if not st.session_state.logged_in:
        client_id = st.text_input("Client ID")
        name = st.text_input("Name")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            try:
                response = client.call("login", client_id, name, password)
                if response["status"] == "error":
                    raise ValueError(response["message"])
                st.session_state.state = response["data"]

                # Preload coins during login
                coins_response = client.call("get_all_coins")
                if coins_response["status"] == "error":
                    raise ValueError(coins_response["message"])
                st.session_state.coins = coins_response["data"]

                st.session_state.logged_in = True
                st.session_state.client_id = client_id
                st.success("Logged in successfully! Navigate to Dashboard.")
            except Exception as e:
                st.error(f"Login failed: {e}")
    else:
        st.info("Already logged in. Go to Dashboard to start trading.")

if __name__ == "__main__":
    login_page()
    