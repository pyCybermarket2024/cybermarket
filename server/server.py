"""
This module provides an asynchronous server for handling client requests.

The server listens on a local port and asynchronously processes requests.
It maintains a connection list and associated message handling queues.

Functions:
    handle_client(reader, writer): Asynchronously handle client connections.
    main(): Start the server and listen for incoming connections.
"""
import asyncio
import pickle
from cmd_process import cmd_process

connect_list = {}


# Run request handler asynchronously
async def handle_client(reader, writer):
    """
    Asynchronously handle client connections.

    This coroutine manages client connections, receives incoming requests,
    and sends responses back to the client.

    Args:
        reader (StreamReader): The stream reader object.
        writer (StreamWriter): The stream writer object.
    """
    connect = "{}:{}".format(*writer.get_extra_info('peername'))
    # Bind the user's pending queue and connection address through a dictionary
    connect_list[connect] = asyncio.Queue()
    print(f"{connect} Connected")
    cmd = ''
    # Create two asynchronous tasks to send and receive
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(connect_list[connect].get())
    # Disconnect when user requests end of service
    while cmd != 'DISCONNECT':
        # If one of the sending and receiving tasks is completed, process first
        requests, _ = await asyncio.wait(
            [send, receive],
            return_when=asyncio.FIRST_COMPLETED)
        for request in requests:
            if request is send:
                send = asyncio.create_task(reader.readline())
                # Decode the request type and request id
                message = request.result().decode().strip()
                args = []
                cmd, request_id, *args = message.split(' ')
                # Pass parameters to the request processing function
                # Wait for processing to complete
                result = cmd_process(cmd, request_id,
                                     connect, *args)
                await connect_list[connect].put(result)
            elif request is receive:
                receive = asyncio.create_task(connect_list[connect].get())
                # Send the results in the queue to be sent to the client
                writer.write(pickle.dumps(request.result()))
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(connect, "DONE")
    del connect_list[connect]
    writer.close()
    await writer.wait_closed()


# Start service(handle_client) on local port 127.0.0.1:22333
async def main():
    """
    Start the server and listen for incoming connections.

    This coroutine sets up the server on a local port,
    starts listening for incoming connections, and handles them
    using the `handle_client` coroutine.
    """
    server = await asyncio.start_server(handle_client, '127.0.0.1', 22333)
    print('Service started')
    async with server:
        await server.serve_forever()

# Run the main program asynchronously
asyncio.run(main())
