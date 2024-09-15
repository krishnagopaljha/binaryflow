import tkinter as tk
from tkinter import filedialog, ttk
from ftp import FTPServer, FTPClient
import threading

def update_gui_progress(sent_bytes, total_bytes, status_message=None):
    """Update the progress bar and status message in the GUI."""
    if sent_bytes == -1 and total_bytes == -1:
        status_label.config(text="Error during file transfer.")
        progress_var.set(0)
    elif sent_bytes == total_bytes:
        status_label.config(text="File transfer completed successfully.")
        progress_var.set(100)
    elif status_message:
        status_label.config(text=status_message)
    else:
        progress_percentage = (sent_bytes / total_bytes) * 100
        progress_var.set(progress_percentage)
        status_label.config(text=f"Transferred {sent_bytes} of {total_bytes} bytes")

def start_server():
    file_path = filedialog.askopenfilename(title="Select a File to Send")
    if not file_path:
        status_label.config(text="No file selected!")
        return

    try:
        # Initialize and start the server
        server = FTPServer(gui_update_callback=update_gui_progress)
        def run_server():
            assigned_port = server.start_server(file_path)
            if assigned_port:
                port_label.config(text=f"Server running on port {assigned_port}")
        
        # Run the server on a separate thread to keep the GUI responsive
        server_thread = threading.Thread(target=run_server)
        server_thread.start()
        status_label.config(text="Server started, waiting for client.")
    except Exception as e:
        status_label.config(text=f"Failed to start server: {str(e)}")

def start_client():
    server_ip = ip_entry.get()

    if not server_ip:
        status_label.config(text="IP address must be provided!")
        return

    try:
        client = FTPClient(gui_update_callback=update_gui_progress)
        client_thread = threading.Thread(target=client.start_client, args=(server_ip, 18367))
        client_thread.start()
        status_label.config(text=f"Client connected to {server_ip}:18367")
    except Exception as e:
        status_label.config(text=f"Failed to connect to server: {str(e)}")

# Close the app
def close_app():
    root.quit()

# Create the main window
root = tk.Tk()
root.title("FTP - Fast Transmission Protocol")
root.geometry("450x350")

# Set styles and fonts for modern look
root.configure(bg='#f2f2f2')
root.option_add('*Font', 'Arial 12')
root.option_add('*Button.Font', 'Arial 10 bold')

# IP Entry
ip_label = tk.Label(root, text="Server IP Address:", bg='#f2f2f2')
ip_label.pack(pady=10)
ip_entry = tk.Entry(root, width=30)
ip_entry.pack(pady=5)

# Port Label (Fixed Port)
port_label = tk.Label(root, text="Port: 18367 (Fixed)", bg='#f2f2f2')
port_label.pack(pady=10)

# Status Label
status_label = tk.Label(root, text="Status: Not connected", bg='#f2f2f2', fg='#333333')
status_label.pack(pady=10)

# Progress Bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=20, padx=20, fill='x')

# Buttons to start server and client
button_frame = tk.Frame(root, bg='#f2f2f2')
button_frame.pack(pady=20)

server_button = tk.Button(button_frame, text="Start Server", command=start_server, bg='#4CAF50', fg='white', width=15)
server_button.grid(row=0, column=0, padx=10)

client_button = tk.Button(button_frame, text="Start Client", command=start_client, bg='#2196F3', fg='white', width=15)
client_button.grid(row=0, column=1, padx=10)

# Exit button
exit_button = tk.Button(root, text="Exit", command=close_app, bg='#FF5252', fg='white', width=15)
exit_button.pack(pady=20)

# Run the Tkinter main loop
root.mainloop()
