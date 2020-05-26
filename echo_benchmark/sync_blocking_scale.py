import socket
import threading
import _thread

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = 8888
sock.bind(('0.0.0.0', port))
sock.listen()

threadId = 0

threading.stack_size(64*1024)

class EchoThread(threading.Thread):
  def __init__(self, threadName, conn):
    threading.Thread.__init__(self)

    self.threadName = threadName
    self.msg = b''
    self.conn = conn

  def run(self):
    # print('{}: conn is {}'.format(self.threadName, self.conn))
    #print('{} starting'.format(self.threadName))

    try:
      # Blocks and waits for either all or 1024 bytes of data to be received.
      recv_data = self.conn.recv(1024)

      # Echo response
      self.conn.send(recv_data)
    except socket.error as err:
      print('{} socket error: {}'.format(self.threadName, err))
      print('{}: conn is {}'.format(self.threadName, self.conn))

    finally:
      # Close the connection.
      self.conn.close()

while True:
  # Blocks and waits for a connection.
  #print('Main thread: starting up and waiting for input connection on {}'.format(port))
  conn, addr = sock.accept()

  threadId += 1
  threadName = 'Thread {}'.format(threadId)
  # print('{}: giving conn: {}'.format(threadName, conn))
  EchoThread(threadName, conn).start()

sock.close()