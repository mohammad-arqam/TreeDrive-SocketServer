TreeDrive - File Sharing System
===============================

Overview:
---------
TreeDrive is a file-sharing system that allows users to upload, list, download, and delete files from a central server. The system uses TCP sockets and supports multiple clients.

--------------------------
How to Start the Server:
--------------------------
1. Open a terminal on the server machine.
2. Navigate to the folder containing server.py.
3. Run:
   python3 server.py

- The server listens on port 8042 by default.
- Uploaded files are stored in the 'server_files' directory.

--------------------------
How to Start the Client:
--------------------------
1. Open a terminal on the client machine.
2. Navigate to the folder containing client.py.
3. Run:
   python3 client.py <username> <server_ip>

   Example:
   python3 client.py test 192.168.2.70

-------------------------------
How to Interact with the System:
-------------------------------
Once connected, the client will display a prompt for commands. The following commands are supported:

- PUSH <filename>     : Upload a file to the server
- GET <filename>      : Download a file from the server
- LIST                : Show all files currently on the server
- DELETE <filename>   : Remove a file from the server
- QUIT                : Disconnect from the server

Commands are case-insensitive. Make sure the file you reference exists in the client's directory when using PUSH.

----------------------------------
Bonus Features / Extra Functionality:
----------------------------------
- Includes a stress-testing script (test_driver.py) to measure latency and throughput with increasing clients.
- Implements the bonus functionality (ls,cd)