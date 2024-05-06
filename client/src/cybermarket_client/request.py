import socket
import pickle
import time
from PyQt5.QtWidgets import QMessageBox
from loguru import logger
from threading import Thread as AsyncThread
from settings import TITLE, SERVER_HOST, SERVER_PORT
from ui import CustomMessageBox
from lang import _

def pop_frame(msg):
    """Display a frame with a message.

    Args:
        msg (str): The message to display in the frame.

    Returns:
        None
    """
    msg_box = CustomMessageBox()
    msg_box.setWindowTitle(TITLE)
    msg_box.setText(msg)
    msg_box.addButton(QMessageBox.Yes)
    yes_button = msg_box.button(QMessageBox.Yes)
    yes_button.setText(_('Cancel'))
    msg_box.exec_() 


def request(cmd, *args, **kwargs):
    """Encapsulate a request to the server and handle the response.

    Args:
        cmd (str): The command to send to the server.
        *args: Additional arguments to include in the request.
        **kwargs: Additional keyword arguments:
            - pop_frame (bool): Whether to display a frame with the response message.

    Returns:
        str: The response from the server.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        message = (cmd, str(int(time.time())), *args)
        logger.debug(f'Request parameters: {message}')
        client_socket.sendall(pickle.dumps(message))
        response = pickle.loads(client_socket.recv(2048))
        logger.success(f'Server response: {response}')
        if kwargs.get('pop_frame'):
            pop_frame(response[0])

    except Exception as e:
        logger.error(f'{e}')
        response = f'{e}'

    finally:
        client_socket.close()
    logger.info('-' * 80)
    return response


def _async_request(cmd, *args, pop_frame=False):
    """Make an asynchronous request to the server.

    Args:
        cmd (str): The command to send to the server.
        *args: Additional arguments to include in the request.
        pop_frame (bool): Whether to display a frame with the response message.

    Returns:
        None
    """
    AsyncThread(target=request, args=(cmd, *args), kwargs={'pop_frame': pop_frame}).start()