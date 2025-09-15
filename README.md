TreeDrive - File Sharing Server

TreeDrive is a client–server file-sharing system built in Python using raw TCP sockets.
It supports user authentication, file upload/download, deletion, and server-side metadata tracking.
Additionally, it includes a test driver to measure latency and throughput under increasing client loads.

🚀 Features

User Authentication – Clients must log in with a username before issuing commands.

File Operations

PUSH <filename> – Upload a file to the server.

GET <filename> – Download a file from the server.

DELETE <filename> – Remove a file (only by the owner).

LIST – View files on the server with owner, size, and timestamp.

Metadata Tracking – Server stores file info (username, filename, size, timestamp) in metadata.txt.

Persistence – Uploaded files are stored in the server_files/ directory.

Performance Testing – test_driver.py can spawn multiple clients, simulate concurrent downloads, and report latency/throughput.

📂 Project Structure

server.py – Multi-client TCP server handling file operations and metadata

server

.

client.py – Interactive client program supporting commands like PUSH, GET, LIST, DELETE, ls, cd, and QUIT

client

.

test_driver.py – Automated benchmarking tool to test system performance with varying client loads

test_driver

.

server_files/ – Directory where uploaded files are stored.

metadata.txt – Tracks file ownership, size, and timestamps.

⚙️ Installation & Usage
1. Clone the repository
git clone https://github.com/yourusername/TreeDrive-FileSharing.git
cd TreeDrive-FileSharing

2. Start the server
python3 server.py


The server listens on port 8042 by default.

3. Start a client
python3 client.py <username> <server-hostname>


Example:

python3 client.py alice 127.0.0.1

4. Available Client Commands
LOGIN <username>   # handled automatically at startup
PUSH <filename>    # upload file to server
GET <filename>     # download file from server
LIST               # list all server files
DELETE <filename>  # delete owned file
QUIT               # disconnect
ls                 # list local files
cd <directory>     # change local directory

5. Run Performance Tests
python3 test_driver.py <server-hostname>
