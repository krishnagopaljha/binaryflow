import socket
import os

class FTPClient:
    def __init__(self, gui_update_callback=None):
        self.gui_update_callback = gui_update_callback  # Callback to update the GUI

    def receive_file(self, client_socket):
        """Receive file metadata and binary data from the server."""
        try:
            # Receive file name and size
            file_metadata = client_socket.recv(1024).decode('utf-8')
            file_name, file_size = file_metadata.split('\n')
            file_size = int(file_size)
            
            # Send acknowledgment to the server
            client_socket.sendall(b"ACK")

            # Start receiving the file
            received_bytes = 0
            with open(file_name, 'wb') as file:
                while received_bytes < file_size:
                    chunk = client_socket.recv(4096)
                    if not chunk:
                        break
                    file.write(chunk)
                    received_bytes += len(chunk)
                    
                    if self.gui_update_callback:
                        self.gui_update_callback(received_bytes, file_size)  # Update progress bar on GUI

            if self.gui_update_callback:
                self.gui_update_callback(file_size, file_size)  # File transfer complete

        except Exception as e:
            if self.gui_update_callback:
                self.gui_update_callback(-1, -1)  # Signal error
            print(f"Error while receiving file: {e}")

        finally:
            client_socket.close()

    def start_client(self, server_ip, server_port):
        """Start the client, connect to the server, and receive the file."""
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, server_port))
            if self.gui_update_callback:
                self.gui_update_callback(0, 0, f"Connected to {server_ip}:{server_port}")

            self.receive_file(client_socket)

        except Exception as e:
            if self.gui_update_callback:
                self.gui_update_callback(-1, -1, f"Error in client: {e}")

        finally:
            client_socket.close()
