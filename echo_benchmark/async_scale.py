import asyncio

async def client_connected_cb(reader, writer):
  msg = b''

  recv_data = await reader.read(1024)

  # Echo response
  writer.write(recv_data)

  # print('full msg received: {}'.format(recv_data))


  # # Keep reading the connection until there is no more.
  # while recv_data:	
  #   #print('partial msg received: {}'.format(recv_data))	        
  #   msg += recv_data
  #   writer.write(recv_data)
  #   recv_data = await reader.read(1024)

  # print('full msg received: {}'.format(msg))

  await writer.drain()

  writer.close()

async def startup():
  port = 8888
  #print('Starting up and waiting for input connection on {}'.format(port))

  def factory():
    reader = asyncio.StreamReader(loop=loop)

    protocol = asyncio.StreamReaderProtocol(reader, client_connected_cb, loop=loop)
    
    return protocol

  await loop.create_server(factory,
    host='0.0.0.0',
    port=port,
    reuse_address=True
  )

loop = asyncio.get_event_loop()
loop.create_task(startup())
loop.run_forever()
loop.close()

