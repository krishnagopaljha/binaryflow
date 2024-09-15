# Binary Flow

`Binary Flow` is a custom Python library for fast and reliable file transfers over a network.It works over `Binary Flow Protocol` and supports transferring files between different devices on the same network using IP addresses and hostnames.

## Features

- **File Transfer**: Simple client-server architecture for transferring files.
- **Network Communication**: Uses TCP/IP for communication across IP-based networks.
- **Binary Encoding**: Transfers any file type, including binary data.
- **Automatic Port Handling**: Server can assign ports automatically or use a fixed port.

## Installation

To install the package in python using pip:

```bash
pip install quicklink
```

## Usage

### FTPServer (Server-side)

The `FTPServer` class is used to host the server and send files to connected clients.

**Methods:**

- `start_server(file_path: str, host: str = '0.0.0.0', port: int = 18367) -> None`  
  Starts the server on the specified IP address and port, and waits for client connections.

  **Parameters:**
  - `file_path` (`str`): Path to the file that will be transferred.
  - `host` (`str`, optional): The IP address to bind the server to (default: `'0.0.0.0'`, which means all interfaces).
  - `port` (`int`, optional): The port number on which the server will listen (default: `18367`).

**Example Usage:**

```python
from ftp import FTPServer

# Path to the file you want to send
file_path = 'example.txt'

# Create an FTPServer instance
server = FTPServer()

# Start the server, bind it to port 18367
server.start_server(file_path)
```

### FTPServer (Client-side)

The `FTPClient` class is used to connect to an FTPServer and receive files.

**Methods**
 - `start_client(server_ip: str, server_port: int = 18367) -> None` Connects to a server using the specified IP and port, then receives and saves the transferred file.

   **Parameters:**

   - server_ip: The IP address of the server.
   - server_port: The port on which the server is listening (default: 18367).

  **Example Usage:**

  ```python
from ftp import FTPClient

# IP address of the server
server_ip = '192.168.1.249'

# Create an FTPClient instance
client = FTPClient()

# Start the client, connect to the server at port 18367
client.start_client(server_ip)
```

## Advanced Use Cases

### Using a Custom Port

You can specify a different port if needed, as long as both the server and client agree on the port.

**Server-side:**

```python
server.start_server(file_path, port=9000)
```

**Client-Side**

```python
client.start_client(server_ip, server_port=9000)
```

### Transferring Large Files
The system supports large file transfers in chunks. Just ensure the file path is valid, and the protocol will handle the rest automatically.


## Common Issues

### Firewall Blocking

Ensure that the firewall on both the server and client machines allows traffic on the specified port. If necessary, configure firewall settings to permit communication through the chosen port.

### IP Configuration

Make sure both devices are on the same network and can communicate via IP when running the server and client on different machines. If using virtual machines, apply a bridge connection to ensure proper network communication between the devices.
