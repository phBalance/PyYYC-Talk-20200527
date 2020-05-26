import socket

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = 8888
sock.bind(('0.0.0.0', port))
sock.listen()

def read_blocking(conn):
  # Blocks and waits for either all or 1024 bytes of data to be received.
  msg = b''
  recv_data = conn.recv(1024)

  # Keep reading the connection until there is no more.
  while recv_data:	
    print('partial msg received: {}'.format(recv_data))	        
    msg += recv_data
    recv_data = conn.recv(1024)

  print('full msg received: {}'.format(msg))


while True:
  # Blocks and waits for a connection.
  print('Starting up and waiting for input connection on {}'.format(port))
  conn, addr = sock.accept()

  read_blocking(conn)

  # Close the connection.
  conn.close()
