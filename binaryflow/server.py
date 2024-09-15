import socket
import os

class FTPServer:
    def __init__(self, gui_update_callback=None):
        """Initialize the FTP Server."""
        self.server_socket = None
        self.gui_update_callback = gui_update_callback  # To update the GUI

    def send_file(self, client_socket, file_path):
        """Send file metadata and binary data to the client."""
        try:
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            client_socket.sendall(f"{file_name}\n{file_size}".encode('utf-8'))
            client_socket.recv(1024)  # Acknowledgment

            sent_bytes = 0
            with open(file_path, 'rb') as file:
                while chunk := file.read(4096):
                    client_socket.sendall(chunk)
                    sent_bytes += len(chunk)
                    if self.gui_update_callback:
                        self.gui_update_callback(sent_bytes, file_size)  # Update progress bar
            if self.gui_update_callback:
                self.gui_update_callback(file_size, file_size)  # Complete the progress

        except Exception as e:
            if self.gui_update_callback:
                self.gui_update_callback(-1, -1)  # Signal error
            print(f"Error while sending file: {e}")

        finally:
            client_socket.close()

    def start_server(self, file_path):
        """Start the server, bind to a fixed port (18367), and accept client connections."""
        if not os.path.exists(file_path):
            if self.gui_update_callback:
                self.gui_update_callback(-1, -1)
            return None

        try:
            # Create server socket and bind to port 18367
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(('0.0.0.0', 18367))  # Fixed port 18367
            self.server_socket.listen(1)

            if self.gui_update_callback:
                self.gui_update_callback(0, 0, f"Server listening on port 18367")  # Update GUI with server status

            # Listen for a connection
            conn, addr = self.server_socket.accept()
            if self.gui_update_callback:
                self.gui_update_callback(0, 0, f"Connection from {addr}")  # Update GUI with connection info

            # Send the file
            self.send_file(conn, file_path)
            return 18367  # Return the fixed port

        except Exception as e:
            if self.gui_update_callback:
                self.gui_update_callback(-1, -1, f"Error in server: {e}")
            return None

        finally:
            if self.server_socket:
                self.server_socket.close()
                if self.gui_update_callback:
                    self.gui_update_callback(0, 0, f"Server socket closed, port 18367 deactivated.")
