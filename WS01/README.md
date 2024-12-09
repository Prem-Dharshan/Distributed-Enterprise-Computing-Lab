To run the complete system that includes the main FTP server (`ftp_server.py`), the two storage servers (`ftp_data_server1.py` and `ftp_data_server2.py`), and the client, follow the sequence below:

### **Step-by-Step Sequence to Run the Servers and Client:**

---

### **1. Set Up the Environment**

Before running the servers and client, ensure you have the `.env` file correctly configured with the appropriate values. This file will contain all the necessary environment variables like FTP server credentials, port numbers, and storage server configurations.

- **Check that `.env` file is in the root of your project directory** and contains correct values for the following:
  - `FTP_USER`, `FTP_PASSWORD`, `FTP_PORT`, `FTP_SERVER_DIR` for the main FTP server.
  - `FTP_SERVER`, `FTP_USER1`, `FTP_PASSWORD1`, `FTP_PORT1` for the first data storage server.
  - `FTP_USER2`, `FTP_PASSWORD2`, `FTP_PORT2` for the second data storage server.

---

### **2. Start the Data Storage Servers**

These servers will handle the storage of file parts. You should start both of them before running the main server.

#### **Run Storage Server 1 (`ftp_data_server1.py`)**

- Navigate to the folder containing `ftp_data_server1.py`.
- Open a terminal and run the following command:
  ```bash
  python ftp_data_server1.py
  ```

This server will listen on the configured port (default `2121`) and store files in the `storage_folder1`.

#### **Run Storage Server 2 (`ftp_data_server2.py`)**

- Navigate to the folder containing `ftp_data_server2.py`.
- Open a terminal and run the following command:
  ```bash
  python ftp_data_server2.py
  ```

This server will listen on the configured port (default `2121`) and store files in the `storage_folder2`.

Both data servers should now be running and waiting for file uploads.

---

### **3. Start the Main FTP Server (`ftp_server.py`)**

The main server handles file uploads, splits files, stores them on the respective storage servers, and retrieves files upon client requests.

- Navigate to the folder containing `ftp_server.py`.
- Open a terminal and run the following command:
  ```bash
  python ftp_server.py
  ```

The main server will start and listen for client connections on the configured port (`2121`). The server will handle the file splitting, distribution to storage servers, and combining files when requested.

---

### **4. Running the Client to Upload/Download Files**

Once the servers are up and running, you can use the client script to upload files to the main FTP server and retrieve them back.

#### **Run the Client for Uploading a File**

- Navigate to the folder containing your client script.
- Open a terminal and run the following command:
  ```bash
  python ftp_client.py
  ```

This will connect to the main FTP server, upload a file (split it into two parts), and store the parts on the two storage servers.

#### **Run the Client for Downloading a File**

To retrieve the file, the client will request the combined file from the main server, which will fetch the parts from the data servers and combine them before sending it back to the client.

To download the file, run the same client script again. The file will be retrieved from both storage servers, combined, and sent back to the client.

---

### **5. Sequence Summary**

1. **Start Data Storage Servers:**
   - Run `python ftp_data_server1.py` in one terminal.
   - Run `python ftp_data_server2.py` in another terminal.

2. **Start the Main FTP Server:**
   - Run `python ftp_server.py` in the main terminal.

3. **Run the Client to Upload Files:**
   - Run `python ftp_client.py` to upload a file.

4. **Run the Client to Download Files:**
   - Run the client script again to retrieve and download the file.

---

### **Notes:**

- **File Paths and Directories:** Ensure the directories where the files will be stored (like `storage_folder1` and `storage_folder2`) exist on the data servers. If not, they will be created dynamically by the data servers.
  
- **Ports and Networking:** Since all servers are running locally, ensure the ports specified in `.env` and the FTP configurations do not conflict with other services.

- **Dependencies:** Ensure you have installed all necessary Python packages like `pyftpdlib` and `python-dotenv`:
  ```bash
  pip install pyftpdlib python-dotenv
  ```

Once you've followed these steps, everything should work as expected. Let me know if you need further clarification!