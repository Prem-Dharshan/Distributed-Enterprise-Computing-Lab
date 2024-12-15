import os
import logging
import hashlib
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from dotenv import load_dotenv
from ftp_data_server1 import upload_to_server as upload1
from ftp_data_server2 import upload_to_server as upload2
from ftp_data_server1 import download_from_server as download1
from ftp_data_server2 import download_from_server as download2

# Load environment variables from .env file
load_dotenv()

# Configuration for FTP server
FTP_PORT = os.getenv('FTP_PORT')
FTP_USER = os.getenv('FTP_USER')
FTP_PASSWORD = os.getenv('FTP_PASSWORD')
FTP_DIRECTORY = os.getenv('FTP_SERVER_DIR')

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def split_file(file_path):
    """Splits a file into two parts and returns the paths to the parts."""
    part1_path = file_path + ".part1"
    part2_path = file_path + ".part2"
    
    # Open the original file and split it into two parts
    with open(file_path, 'rb') as file:
        data = file.read()
        midpoint = len(data) // 2
        part1_data = data[:midpoint]
        part2_data = data[midpoint:]
        
        # Write the two parts to separate files
        with open(part1_path, 'wb') as part1:
            part1.write(part1_data)
        
        with open(part2_path, 'wb') as part2:
            part2.write(part2_data)
    
    return part1_path, part2_path

def store_file_parts(part1_path, part2_path):
    """Stores the two file parts on the respective FTP storage servers."""
    # Store part 1 on the first data server
    logger.info(f"Storing part 1 in server 1: {part1_path}")
    upload1(part1_path)
    
    # Store part 2 on the second data server
    logger.info(f"Storing part 2 in server 2: {part2_path}")
    upload2(part2_path)

def retrieve_and_combine_file(file_name):
    """Retrieve the file parts from two storage servers and combine them."""
    part1_path = f"./storage_folder/{file_name}.part1"
    part2_path = f"./storage_folder/{file_name}.part2"

    # Retrieve part 1
    download1(part1_path)

    # Retrieve part 2
    download2(part2_path)

    # Combine the parts
    combined_file_path = f"./{file_name}"
    with open(combined_file_path, 'wb') as combined_file:
        with open(part1_path, 'rb') as part1:
            combined_file.write(part1.read())
        with open(part2_path, 'rb') as part2:
            combined_file.write(part2.read())

    logger.info(f"File {file_name} combined and ready to send back to client.")
    return combined_file_path

def main():
    # Ensure the directory exists
    if not os.path.exists(FTP_DIRECTORY):
        logger.info(f"Creating FTP directory: {FTP_DIRECTORY}")
        os.makedirs(FTP_DIRECTORY)
    else:
        logger.info(f"Using existing FTP directory: {FTP_DIRECTORY}")
    
    # Set up authorizer
    authorizer = DummyAuthorizer()
    authorizer.add_user(FTP_USER, FTP_PASSWORD, FTP_DIRECTORY, perm='elradfmw')

    # Set up handler and attach authorizer
    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = "pyftpdlib FTP server ready."

    # Create and start the server
    address = ('0.0.0.0', int(FTP_PORT))  # Bind to the specified IP and port
    server = FTPServer(address, handler)
    server.max_cons = 256
    server.max_cons_per_ip = 5

    logger.info(f"FTP server running on port {FTP_PORT}...")

    # Start the server and listen for client uploads
    server.serve_forever()

if __name__ == '__main__':
    main()
