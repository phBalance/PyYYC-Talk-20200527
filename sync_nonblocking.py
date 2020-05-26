import sys
import socket
import errno
import types
from time import sleep

msg = b''

def service_nonblocking(conn):
  global msg

  try:
    recv_data = conn.recv(1024)

  except IOError as e:
    if(e.errno == errno.EWOULDBLOCK):
      print('nothing to read')

  except socket.timeout as e:
    err = e.args[0]
    # this next if/else is a bit redundant, but illustrates how the
    # timeout exception is setup
    if err == 'timed out':
      sleep(1)
      print('recv timed out, retry later')
    else:
      print(e)
      sys.exit(1)

  except socket.error as e:
    # Something else happened, handle error, exit, etc.
    print(e)
    sys.exit(1)

  else:
    if len(recv_data) == 0:
      print('orderly shutdown on server end full message is {}'.format(msg))
      sys.exit(0)
    else:
      print('partial msg received: {}'.format(recv_data))
      msg = msg + recv_data


sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = 8888
sock.bind(('0.0.0.0', port))
sock.listen()

# Blocks and waits for a connection.
print('Starting up and waiting for input connection on {}'.format(port))
conn, addr = sock.accept()
conn.setblocking(False)

while True:
  sleep(1)
  service_nonblocking(conn)