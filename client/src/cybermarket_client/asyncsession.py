import asyncio
import pickle


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
    msg = []
    while msg != ["exit()"]:
        done, pending = await asyncio.wait([send, receive],
                                           return_when=asyncio.FIRST_COMPLETED)
        for info in done:
            if info is send:
                send = asyncio.create_task(message_queue.get())
                msg = info.result()
                writer.write(pickle.dumps(msg))
                await writer.drain()
            elif info is receive:
                receive = asyncio.create_task(reader.read(4096))
                data = pickle.loads(info.result())
                result_queue.put_nowait(data)
    writer.close()
    await writer.wait_closed()
