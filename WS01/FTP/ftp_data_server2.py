import ftplib
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def upload_to_server(file_path):
    """Uploads a file to the FTP server."""
    FTP_SERVER = os.getenv('FTP_SERVER')
    FTP_PORT = 2121
    FTP_USER = os.getenv('FTP_USER')
    FTP_PASSWORD = os.getenv('FTP_PASSWORD')

    try:
        logger.info(f"Connecting to FTP server at {FTP_SERVER} on port {FTP_PORT}...")
        ftp = ftplib.FTP()
        ftp.connect(FTP_SERVER, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASSWORD)

        # Ensure the appropriate directory exists
        ftp.cwd('storage_folder2')  # Folder for storage server 2
        file_name = os.path.basename(file_path)

        with open(file_path, 'rb') as file:
            ftp.storbinary(f"STOR {file_name}", file)

        logger.info(f"File part {file_name} uploaded successfully.")

        ftp.quit()
    except Exception as e:
        logger.error(f"Failed to upload file to FTP server: {e}")

def download_from_server(file_path):
    """Downloads the file part from the FTP server."""
    FTP_SERVER = os.getenv('FTP_SERVER')
    FTP_PORT = 2121
    FTP_USER = os.getenv('FTP_USER')
    FTP_PASSWORD = os.getenv('FTP_PASSWORD')

    try:
        logger.info(f"Connecting to FTP server at {FTP_SERVER} on port {FTP_PORT}...")
        ftp = ftplib.FTP()
        ftp.connect(FTP_SERVER, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASSWORD)

        # Ensure the appropriate directory exists
        ftp.cwd('storage_folder2')  # Folder for storage server 2

        file_name = os.path.basename(file_path)
        with open(file_path, 'wb') as file:
            ftp.retrbinary(f"RETR {file_name}", file.write)

        logger.info(f"File part {file_name} downloaded successfully.")

        ftp.quit()
    except Exception as e:
        logger.error(f"Failed to download file part: {e}")
