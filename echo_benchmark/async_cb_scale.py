# Performance is much improved over the streamer version.
# Abstractions seem to be costly in Python.
import asyncio

class EchoProtocol(asyncio.Protocol):
  def connection_made(self, transport):
    # print('connection made {}'.format(transport))
    self.transport = transport

  def connection_lost(self, reason):
    # print('connection closed {}'.format(reason))
    self.transport = None

  def data_received(self, data):
    # print('received {}'.format(data))
    self.transport.write(data)
    self.transport.close()
    self.transport = None

async def startup():
  port = 8888
  await loop.create_server(EchoProtocol,
    host='0.0.0.0',
    port=port,
    reuse_address=True
  )

loop = asyncio.get_event_loop()
loop.create_task(startup())
loop.run_forever()
loop.close()