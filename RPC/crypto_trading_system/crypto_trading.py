import json
import socket
import inspect
import threading
import logging
from datetime import datetime
import os
from threading import Lock

SIZE = 1024

# Configure logging
logging.basicConfig(
    filename='crypto_trading.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CryptoCoin:
    def __init__(self, name, abbr, description, market_cap, trading_volume, opening_price):
        self.name = name
        self.abbr = abbr
        self.description = description
        self.market_cap = market_cap
        self.trading_volume = trading_volume
        self.price = opening_price
        self.timestamp = datetime.now().isoformat()

class ClientState:
    def __init__(self, client_id, name, purchase_power):
        self.client_id = client_id
        self.name = name
        self.purchase_power = purchase_power
        self.coins = {}  # {coin_abbr: {'quantity': qty, 'purchase_price': price, 'timestamp': time}}

class CryptoTradingServer:
    def __init__(self):
        self.coins = {}
        self.clients = {}
        self.lock = Lock()
        self.state_file = "client_states.json"
        self.load_states()

    def add_coin(self, name, abbr, description, market_cap, trading_volume, opening_price):
        with self.lock:
            if abbr in self.coins:
                raise Exception(f"Coin {abbr} already exists")
            coin = CryptoCoin(name, abbr, description, market_cap, trading_volume, opening_price)
            self.coins[abbr] = coin
            logging.info(f"Added new coin: {abbr}")
            return True

    def remove_coin(self, abbr):
        with self.lock:
            if abbr not in self.coins:
                raise Exception(f"Coin {abbr} not found")
            del self.coins[abbr]
            logging.info(f"Removed coin: {abbr}")
            return True

    def edit_coin(self, abbr, price):
        with self.lock:
            if abbr not in self.coins:
                raise Exception(f"Coin {abbr} not found")
            self.coins[abbr].price = price
            self.coins[abbr].timestamp = datetime.now().isoformat()
            logging.info(f"Updated price for {abbr} to {price}")
            return True

    def login(self, client_id, name, password):
        if password != "password123":  # Simple demo password
            raise Exception("Invalid credentials")
        with self.lock:
            if client_id not in self.clients:
                self.clients[client_id] = ClientState(client_id, name, 10000.0)
            logging.info(f"Client {client_id} logged in")
            return self.get_client_state(client_id)

    def buy_coin(self, client_id, abbr, quantity):
        with self.lock:
            if client_id not in self.clients:
                raise Exception("Client not logged in")
            if abbr not in self.coins:
                raise Exception("Coin not found")
            total_cost = self.coins[abbr].price * quantity
            client = self.clients[client_id]
            if client.purchase_power < total_cost:
                raise Exception("Insufficient funds")
            client.purchase_power -= total_cost
            if abbr in client.coins:
                client.coins[abbr]['quantity'] += quantity
            else:
                client.coins[abbr] = {
                    'quantity': quantity,
                    'purchase_price': self.coins[abbr].price,
                    'timestamp': datetime.now().isoformat()
                }
            logging.info(f"Client {client_id} bought {quantity} of {abbr}")
            return self.get_client_state(client_id)

    def sell_coin(self, client_id, abbr, quantity):
        with self.lock:
            if client_id not in self.clients:
                raise Exception("Client not logged in")
            if abbr not in self.coins:
                raise Exception("Coin not found")
            if abbr not in self.clients[client_id].coins:
                raise Exception("Client doesn't own this coin")
            client = self.clients[client_id]
            if client.coins[abbr]['quantity'] < quantity:
                raise Exception("Insufficient coin quantity")
            revenue = self.coins[abbr].price * quantity
            client.purchase_power += revenue
            client.coins[abbr]['quantity'] -= quantity
            if client.coins[abbr]['quantity'] == 0:
                del client.coins[abbr]
            logging.info(f"Client {client_id} sold {quantity} of {abbr}")
            return self.get_client_state(client_id)

    def get_client_state(self, client_id):
        with self.lock:
            if client_id not in self.clients:
                raise Exception("Client not found")
            client = self.clients[client_id]
            return {
                'client_id': client.client_id,
                'name': client.name,
                'purchase_power': client.purchase_power,
                'coins': client.coins
            }

    def get_all_coins(self):
        with self.lock:
            return {abbr: {
                'name': coin.name,
                'price': coin.price,
                'market_cap': coin.market_cap,
                'trading_volume': coin.trading_volume
            } for abbr, coin in self.coins.items()}

    def save_states(self):
        with self.lock:
            states = {cid: {
                'client_id': c.client_id,
                'name': c.name,
                'purchase_power': c.purchase_power,
                'coins': c.coins
            } for cid, c in self.clients.items()}
            with open(self.state_file, 'w') as f:
                json.dump(states, f)
            logging.info("Client states saved")
            return True

    def load_states(self):
        with self.lock:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    states = json.load(f)
                    for cid, state in states.items():
                        client = ClientState(state['client_id'], state['name'], state['purchase_power'])
                        client.coins = state['coins']
                        self.clients[cid] = client
                logging.info("Client states loaded")

class RPCServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.address = (host, port)
        self._methods = {}

    def registerInstance(self, instance):
        for func_name, func in inspect.getmembers(instance, predicate=inspect.ismethod):
            if not func_name.startswith('__'):
                self._methods[func_name] = func

    def __handle__(self, client, address):
        logging.info(f"Handling requests from {address}")
        while True:
            try:
                data = json.loads(client.recv(SIZE).decode())
                func_name, args, kwargs = data
                try:
                    result = self._methods[func_name](*args, **kwargs)
                    response = {"status": "success", "data": result}
                except Exception as e:
                    response = {"status": "error", "message": str(e)}
                client.sendall(json.dumps(response).encode())
            except Exception as e:
                logging.error(f"Connection error with {address}: {e}")
                break
        client.close()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(self.address)
            sock.listen()
            logging.info(f"Server running at {self.address}")
            while True:
                client, address = sock.accept()
                threading.Thread(target=self.__handle__, args=(client, address)).start()
                