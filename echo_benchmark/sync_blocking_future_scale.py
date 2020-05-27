import concurrent.futures
import socket
import threading

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = 8888
sock.bind(('0.0.0.0', port))
sock.listen()

def read_blocking(conn, exec_number):
  # print('{}: read_blocking invoked'.format(exec_number))
  try:
    # Blocks and waits for either all or 1024 bytes of data to be received.
    recv_data = conn.recv(1024)

    # Echo response
    conn.send(recv_data)
  except socket.error as err:
    print('{}: socket error: {}'.format(exec_number, err))

  finally:
    # Close the connection.
    # print('{}: shutting connection'.format(exec_number))
    conn.close()


# NOTE: 1000 was chosen to be able to make this comparable to sync_blocking_scale.py when
# running the benchmark which supports the largest number of simultaneous connections: 1000.
with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
  exec_num = 0

  while True:
    # Blocks and waits for a connection.
    #print('Main thread: starting up and waiting for input connection on {}'.format(port))
    conn, addr = sock.accept()

    exec_num += 1
    executor.submit(read_blocking, conn, exec_num)