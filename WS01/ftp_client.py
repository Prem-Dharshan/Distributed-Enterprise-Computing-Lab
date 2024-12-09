import os
import ftplib
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration for FTP client
HOSTNAME = os.getenv('FTP_SERVER')
FTP_PORT = 2121
USERNAME = os.getenv('FTP_USER')
PASSWORD = os.getenv('FTP_PASSWORD')

# Define file path
FTP_DIRECTORY = os.getenv('FTP_SERVER_DIR')  # The directory from .env
FILE_TO_UPLOAD = os.path.join(FTP_DIRECTORY, "dummy_file.txt")

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure file exists or create it with dummy content
if not os.path.exists(FILE_TO_UPLOAD):
    logger.info(f"Creating dummy file: {FILE_TO_UPLOAD}")
    with open(FILE_TO_UPLOAD, "w") as f:
        f.write("This is a dummy file for FTP transfer.\n")
else:
    logger.info(f"Using existing file: {FILE_TO_UPLOAD}")

try:
    logger.info(f"Connecting to FTP server at {HOSTNAME} on port {FTP_PORT}...")
    ftp_server = ftplib.FTP()
    ftp_server.connect(HOSTNAME, FTP_PORT)  # Connect to the FTP server at the right address and port
    ftp_server.login(USERNAME, PASSWORD)  # Corrected login method
    ftp_server.encoding = "utf-8"
    logger.info(f"Connected to FTP server: {ftp_server.getwelcome()}")

    # Upload the file
    logger.info(f"Uploading file: {FILE_TO_UPLOAD}...")
    with open(FILE_TO_UPLOAD, "rb") as file:
        ftp_server.storbinary(f"STOR {os.path.basename(FILE_TO_UPLOAD)}", file)

    # List files on the server
    logger.info("Directory listing on the server:")
    ftp_server.dir()

    ftp_server.quit()
    logger.info("FTP session closed.")

except Exception as e:
    logger.error(f"An error occurred: {e}")
