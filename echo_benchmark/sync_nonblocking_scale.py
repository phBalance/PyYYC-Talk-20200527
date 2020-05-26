import sys
import socket
import selectors
import types

def accept_nonblocking(sock):
    conn, addr = sock.accept()
    # print('accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, msg_in=b'')
    events = selectors.EVENT_READ
    sel.register(conn, events, data=data)    

def service_nonblocking(key, mask):
    conn = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = conn.recv(1024)
        if recv_data:
            # print('partial msg received: {}'.format(recv_data))
            data.msg_in += recv_data
            conn.send(recv_data)

        sel.unregister(conn)
        conn.close()

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = 8888
sock.bind(('0.0.0.0', port))
sock.listen()

sock.setblocking(False)

sel = selectors.DefaultSelector()
sel.register(sock, selectors.EVENT_READ, data=None)

#print('Starting up and waiting for input connection on {}'.format(port))

while True:
    #print('waiting on select forever')
    events = sel.select(timeout=None)
    # print('select has returned: {}'.format(events))

    for key, mask in events:
        if key.data is None:
            accept_nonblocking(key.fileobj)
        else:
            service_nonblocking(key, mask)
