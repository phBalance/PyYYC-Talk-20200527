import asyncio

async def client_connected_cb(reader, writer):
  # No more connections allowed.
  socket_server.close()

  msg = b''

  recv_data = await reader.read(1024)

  # Keep reading the connection until there is no more.
  while recv_data:	
    print('partial msg received: {}'.format(recv_data))	        
    msg += recv_data
    recv_data = await reader.read(1024)

  print('full msg received: {}'.format(msg))

  writer.close()
  
  loop.stop()

async def startup():
  port = 8888
  print('Starting up and waiting for input connection on {}'.format(port))

  def factory():
    reader = asyncio.StreamReader(loop=loop)

    protocol = asyncio.StreamReaderProtocol(reader, client_connected_cb, loop=loop)
    
    return protocol

  global socket_server
  socket_server = await loop.create_server(factory,
    host='0.0.0.0',
    port=port,
    reuse_address=True
  )


loop = asyncio.get_event_loop()
loop.create_task(startup())
loop.run_forever()
loop.close()