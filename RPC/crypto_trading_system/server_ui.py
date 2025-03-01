import threading
import streamlit as st
from crypto_trading import RPCServer, CryptoTradingServer

def run_server():
    trading_server = CryptoTradingServer()
    server = RPCServer()
    server.registerInstance(trading_server)
    server.run()

if __name__ == "__main__":
    st.title("Crypto Trading Server Dashboard")
    
    if st.button("Start Server"):
        st.write("Server starting...")
        threading.Thread(target=run_server, daemon=True).start()
        st.success("Server started on port 8080")
    
    st.write("Server controls will be available once implemented with proper UI feedback")
    