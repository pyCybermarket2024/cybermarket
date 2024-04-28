import asyncio
from PyQt5.QtCore import pyqtSlot,QThread
import qasync 
async def client_task(addr, port, message_queue, result_queue):
    """
    Asynchronous client task for handling sending and receiving messages
    over a network connection.

    This coroutine establishes a connection to the given address and port,
    then enters a loop where it waits for either a message to send or data
    to receive. It sends messages from the message_queue and puts received
    data into the result_queue.

    Args:
        addr (str): The IP address or hostname of the server to connect to.
        port (str): The port number of the server to connect to.
        message_queue (asyncio.Queue): A queue for outgoing messages.
        result_queue (asyncio.Queue): A queue for incoming messages.

    """
    reader, writer = await asyncio.open_connection(addr, int(port))
    print(f"Connected to {addr}:{port}")

    # Get a message from the main process
    send = asyncio.create_task(message_queue.get())
    receive = asyncio.create_task(reader.read(4096))
    loop=asyncio.get_event_loop()
    msg = ""
    while msg.strip() != "exit()":
        done, pending = await asyncio.wait(
            [send, receive],
            return_when=asyncio.FIRST_COMPLETED
            )
        for info in done:
            if info is send:
                send = asyncio.create_task(message_queue.get())
                msg = info.result()
                msg += '\n'
                writer.write(msg.encode())
                await writer.drain()
            elif info is receive:
                receive = asyncio.create_task(reader.read(4096))
                data = info.result().decode().strip()
                result_queue.put_nowait(data)
    writer.close()
    await writer.wait_closed()


#class AsyncSession():
#    """
#    A class that encapsulates an asynchronous session with a server.

#    This class manages a connection to a server and provides methods
#    to send and receive messages asynchronously.

#    Attributes:
#        address (str): The IP address or hostname of the server.
#        port (int): The port number of the server.
#        send (asyncio.Queue): A queue for outgoing messages.
#        receive (asyncio.Queue): A queue for incoming messages.
#        task (asyncio.Task): The running task for the client connection.

#    Methods:
#        push(message: str): Sends a message to the server.
#        pull(): Receives a message from the server.
#        get_reply(message: str): Sends a message and waits for the reply.
#    """
        
#    def __init__(self, address, port):
#        """
#        Initializes a new AsyncSession instance.

#        Args:
#            address (str): The IP address or hostname of the server to connect.
#            port (int): The port number of the server to connect to.
#        """
#        self.address = address
#        self.port = port
#        self.send = asyncio.Queue()
#        self.receive = asyncio.Queue()
#        self.loop = asyncio.new_event_loop()
#        self.task = asyncio.create_task(
#            client_task(self.address, self.port, self.send, self.receive)
#            )
#        self.loop = asyncio.get_running_loop()
#    async def push(self, message):
#        """
#        Sends a message to the server.

#        Args:
#            message (str): The message to send.
#        """
#        await self.send.put(message)

#    async def pull(self):
#        """
#        Receives a message from the server.

#        Returns:
#            str: The received message.
#        """
#        result = await self.receive.get()
#        return result

#    async def get_reply(self, message):
#        """
#        Sends a message to the server and waits for the reply.

#        Args:
#            message (str): The message to send.

#        Returns:
#            str: The reply from the server.
#        """
#        await self.push(message)
#        result = await self.pull()
#        return result
