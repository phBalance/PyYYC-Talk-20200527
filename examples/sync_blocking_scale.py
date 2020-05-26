import socket
import threading

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = 8888
sock.bind(('0.0.0.0', port))
sock.listen()

threadId = 0

class ReadThread(threading.Thread):
  def __init__(self, threadName, conn):
    threading.Thread.__init__(self)

    self.threadName = threadName
    self.msg = b''
    self.conn = conn

  def run(self):
    print('{} starting'.format(self.threadName))

    # Blocks and waits for either all or 1024 bytes of data to be received.
    recv_data = self.conn.recv(1024)

    # Keep reading the connection until there is no more.
    while recv_data:
      print('{} partial msg received: {}'.format(self.threadName, recv_data))        
      self.msg += recv_data
      recv_data = self.conn.recv(1024)

    print('{} full msg received: {}'.format(self.threadName, self.msg))

    # Close the connection.
    self.conn.close()

while True:
  # Blocks and waits for a connection.
  print('Main thread: starting up and waiting for input connection on {}'.format(port))
  conn, addr = sock.accept()

  threadId += 1
  threadName = 'Thread {}'.format(threadId)
  ReadThread(threadName, conn).start()

