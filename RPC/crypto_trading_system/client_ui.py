import streamlit as st

st.set_page_config(page_title="Crypto Trading System", layout="wide")

# The actual pages are defined in the 'pages/' directory
def main():
    st.title("Crypto Trading System")
    st.write("Use the sidebar to navigate between Login and Dashboard.")

if __name__ == "__main__":
    main()
    