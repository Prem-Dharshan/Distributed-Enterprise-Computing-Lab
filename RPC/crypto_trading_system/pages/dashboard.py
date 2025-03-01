import streamlit as st
from datetime import datetime

@st.cache_data
def get_cached_coins(coins):
    return coins

def dashboard_page():
    st.title("Trading Dashboard")

    # Check if logged in
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.error("Please log in first.")
        st.stop()

    client = st.session_state.client
    coins = get_cached_coins(st.session_state.coins)

    # Sidebar for navigation
    st.sidebar.title("Operations")
    operation = st.sidebar.radio(
        "Select Operation",
        ["View Market", "Buy/Sell", "Portfolio", "Manage Coins"]
    )

    # Main content based on selected operation
    if operation == "View Market":
        st.subheader("Available Coins")
        for abbr, details in coins.items():
            st.write(f"{details['name']} ({abbr}): ${details['price']} - Market Cap: ${details['market_cap']}")

    elif operation == "Buy/Sell":
        st.subheader(f"Welcome, {st.session_state.state.get('name', 'User')}")
        purchase_power = float(st.session_state.state.get('purchase_power', 0))
        st.write(f"Purchase Power: ${purchase_power:.2f}")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Buy Coins")
            buy_coin = st.selectbox("Coin to buy", list(coins.keys()), key="buy_select")
            buy_qty = st.number_input("Quantity to buy", min_value=0.01, step=0.01, key="buy_qty")
            if st.button("Buy"):
                try:
                    response = client.call("buy_coin", st.session_state.client_id, buy_coin, buy_qty)
                    if response["status"] == "error":
                        raise ValueError(response["message"])
                    st.session_state.state = response["data"]
                    coins_response = client.call("get_all_coins")
                    if coins_response["status"] == "success":
                        st.session_state.coins = coins_response["data"]
                    st.success("Purchase successful!")
                except Exception as e:
                    st.error(f"Buy failed: {e}")

        with col2:
            st.subheader("Sell Coins")
            owned_coins = list(st.session_state.state.get('coins', {}).keys())
            if owned_coins:
                sell_coin = st.selectbox("Coin to sell", owned_coins, key="sell_select")
                sell_qty = st.number_input("Quantity to sell", min_value=0.01, step=0.01, key="sell_qty")
                if st.button("Sell"):
                    try:
                        response = client.call("sell_coin", st.session_state.client_id, sell_coin, sell_qty)
                        if response["status"] == "error":
                            raise ValueError(response["message"])
                        st.session_state.state = response["data"]
                        coins_response = client.call("get_all_coins")
                        if coins_response["status"] == "success":
                            st.session_state.coins = coins_response["data"]
                        st.success("Sale successful!")
                    except Exception as e:
                        st.error(f"Sell failed: {e}")
            else:
                st.write("No coins owned yet")

    elif operation == "Portfolio":
        st.subheader("Your Portfolio")
        coins_dict = st.session_state.state.get('coins', {})
        if coins_dict:
            for abbr, details in coins_dict.items():
                st.write(f"{abbr}: {details['quantity']} @ ${details['purchase_price']} "
                        f"(Bought: {details['timestamp']})")
        else:
            st.write("Portfolio is empty")

    elif operation == "Manage Coins":
        st.subheader("Manage Coins")
        action = st.selectbox("Action", ["Add Coin", "Remove Coin", "Edit Coin Price"])
        
        if action == "Add Coin":
            name = st.text_input("Coin Name")
            abbr = st.text_input("Abbreviation")
            desc = st.text_input("Description")
            market_cap = st.number_input("Market Cap", min_value=0.0)
            volume = st.number_input("Trading Volume", min_value=0.0)
            price = st.number_input("Opening Price", min_value=0.0)
            if st.button("Add"):
                try:
                    response = client.call("add_coin", name, abbr, desc, market_cap, volume, price)
                    if response["status"] == "error":
                        raise ValueError(response["message"])
                    coins_response = client.call("get_all_coins")
                    if coins_response["status"] == "success":
                        st.session_state.coins = coins_response["data"]
                    st.success("Coin added successfully!")
                except Exception as e:
                    st.error(f"Add failed: {e}")

        elif action == "Remove Coin":
            remove_coin = st.selectbox("Coin to remove", list(coins.keys()))
            if st.button("Remove"):
                try:
                    response = client.call("remove_coin", remove_coin)
                    if response["status"] == "error":
                        raise ValueError(response["message"])
                    coins_response = client.call("get_all_coins")
                    if coins_response["status"] == "success":
                        st.session_state.coins = coins_response["data"]
                    st.success("Coin removed successfully!")
                except Exception as e:
                    st.error(f"Remove failed: {e}")

        elif action == "Edit Coin Price":
            edit_coin = st.selectbox("Coin to edit", list(coins.keys()))
            new_price = st.number_input("New Price", min_value=0.0)
            if st.button("Update"):
                try:
                    response = client.call("edit_coin", edit_coin, new_price)
                    if response["status"] == "error":
                        raise ValueError(response["message"])
                    coins_response = client.call("get_all_coins")
                    if coins_response["status"] == "success":
                        st.session_state.coins = coins_response["data"]
                    st.success("Price updated successfully!")
                except Exception as e:
                    st.error(f"Update failed: {e}")

    # Logout button in sidebar
    if st.sidebar.button("Logout"):
        try:
            response = client.call("save_states")
            if response["status"] == "error":
                raise ValueError(response["message"])
            client.disconnect()
            st.session_state.logged_in = False
            st.session_state.coins = None
            st.session_state.state = None
            st.session_state.client_id = None
            st.success("Logged out successfully!")
        except Exception as e:
            st.error(f"Logout failed: {e}")

if __name__ == "__main__":
    dashboard_page()
    