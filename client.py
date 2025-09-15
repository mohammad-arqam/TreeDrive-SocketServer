import os
import socket
import sys

port = 8042
#Collect username and hostname from the user
try:
    username = sys.argv[1]
    host = sys.argv[2]

except:
    print("ERROR: Please run using the following format *python3 filename.py username hostname* ")
    sys.exit(1)

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print(f"Connected to the {hostname} at port {port}")
except socket.error as e:
    print(f"CLIENT: Error creating a socket{e}")
    sys.exit(1)


# connect to the server
try:
    client_socket.connect((host, port))
    #print(f"Connected to the {hostname} at port {port}")
except socket.error as e:
    print(f"Error connecting to server: {e}")
    sys.exit(1)

# Send the LOGIN command to the server
client_socket.sendall(f"LOGIN {username}\n".encode("utf-8"))

try:
    # Receive the server's response
    response_bytes = client_socket.recv(1024)
    response = response_bytes.decode("utf-8").strip()
    print("Server response:", response)

    # Check if the response indicates a successful login
    if response.upper() == "LOGIN SUCCESSFUL":
        print("You are now authenticated.")

        while True:
            print(f"Available commands (e.g., PUSH <filename>, LIST, GET <filename>, DELETE <filename>, ls, cd, QUIT): \n")
            print("Enter command: ")
            commands = sys.stdin.readline().strip()
            if not commands:
                break


            # PUSH
            if commands.upper().startswith("PUSH "):
                try:
                     x, filename = commands.split(" ", 1)  # extract file name from command

                     if not filename:  # user doesn't use the correct command format.
                        print(f"Invalid format error: following format must me followed (PUSH <filename>).\n")
                        continue

                     if not os.path.exists(filename):  # file does not exist on local host
                         print(f"ERROR: File '{filename} does not exist.\n")
                     elif os.path.exists(filename):  # file exists
                         client_socket.sendall(f"PUSH {filename}\n".encode("utf-8"))  # send the push command to the server
                         server_response= client_socket.recv(1024).decode("utf-8").strip()  # get response from the server

                         if server_response.startswith("Uploading"):  # if server is ready to accept the file
                             print(f"Sending file '{filename}' to the server...")
                             # send the file
                             with open(filename,"rb") as send_file:
                                data = send_file.read(4096)
                                while data:
                                    client_socket.sendall(data)
                                    data = send_file.read(4096)
                             client_socket.sendall(b"EOF")  # marker
                            # check if file was uploaded
                             server_response= client_socket.recv(1024).decode("utf-8").strip()
                             if server_response.startswith("ERROR: "):
                                 print(f"Error occured while uploading the file.\n")
                             else:
                                 print(f"File '{filename}' was uploaded successfully")
                         else:
                             print(server_response)
                except Exception:
                    print("Error pushing the file.")

            # LIST
            elif commands.upper().startswith("LIST"):
                client_socket.sendall("LIST ".encode("utf-8"))
                response = client_socket.recv(1024).decode("utf-8").strip()
                #check if their exist any files on the serer
                if response.strip() == "Ready":  # files exist on server
                    response = client_socket.recv(4096).decode("utf-8")
                    list = response.strip().split("\n")
                    # list all the files
                    for entry in list:
                        filename, size_MB, username, timestamp = entry.split(", ")
                        print(f"{filename} - {size_MB} - Uploaded by {username} on {timestamp}\n")
                elif response == "No files exist on the server.":
                    print(f"{response}\n")
                    continue
                else:
                    print(f"Error creating list")
            #GET
            elif commands.upper().startswith("GET "):
                try:
                     x, filename = commands.split(" ", 1)  # extract file name from command

                     if not filename:  # user doesn't use the correct command format.
                        print(f"Invalid format error: following format must me followed (GET <filename>).\n")
                        continue
                     
                     client_socket.sendall(f"GET {filename}\n".encode("utf-8"))

                     # Receive server response 
                     server_response = client_socket.recv(1024).decode("utf-8").strip()

                     if server_response.startswith("ERROR:"):  # error getting the file
                         print(server_response)
                         continue
                     elif server_response == "Available":
                         
                         with open(filename, "wb") as file:
                            while True:  #receive data
                                data = client_socket.recv(4096)
                                if not data:
                                    break  # no more data
                                if data.endswith(b"EOF"):
                                    file.write(data[:-3])  # Remove EOF
                                    break
                                else:
                                    file.write(data)  # Copy the received data

                         print(f"File '{filename}' downloaded.")
                except Exception:
                    print("Error getting the file.")
            #DELETE
            elif commands.upper().startswith("DELETE "):
                try:
                     x, filename = commands.split(" ", 1)  # extract file name from command

                     if not filename:  # user doesn't use the correct command format.
                        print(f"Invalid format error: following format must me followed (DELETE <filename>).\n")
                        continue
                     
                     client_socket.sendall(f"DELETE {filename}\n".encode("utf-8"))
                     print(client_socket.recv(1024).decode("utf-8").strip())
                except Exception:
                    print("Error deleting the file.")
            #QUIT
            elif commands.upper() == "QUIT":
                client_socket.sendall("QUIT".encode("utf-8"))
                print(client_socket.recv(1024).decode("utf-8").strip())
                break  # break loop
            #cd
            elif commands.upper().startswith("CD"):
                try:
                    x, name = commands.split(" ", 1)
                    os.chdir(name)
                    print(f"Directory changed to '{name}.\n")
                except Exception as e:
                    print(f"Error changing directory\n")
            #ls
            elif commands.upper().startswith("LS"):
                try:
                    list = os.listdir()

                    if not list:  # no files available
                        print("Current directory is empty.\n")
                    else:
                    #print the files
                        for file in list:
                            print(file)

                except Exception as e:
                    print(f"Error listing files on local directory")
            #Invalid commands
            else:
                print(f"ERROR: Invalid command\n")
                continue                           

    else:
        print("Authentication failed. Please check your credentials.")
except Exception as e:
    print(f"An error occurred while receiving the server's response: {e}")


client_socket.close()
sys.exit(0)


