from asyncsession import client_task
import sys
import asyncio
import qasync
from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget, QVBoxLayout, QPushButton,
                             QLineEdit, QMessageBox, QFormLayout)


class LoginWindow(QWidget):
    """A class representing the login and registration window."""

    send_message_counter = 0

    def __init__(self, message_queue, result_queue):
        """
        Initializes the LoginWindow.

        Args:
            message_queue (asyncio.Queue): A queue for sending messages.
            result_queue (asyncio.Queue): A queue for receiving results.
        """
        super().__init__()
        self.initUI()
        self.message_queue = message_queue
        self.result_queue = result_queue
        self.invite_code = None

    def initUI(self):
        """Initializes the user interface."""
        self.setWindowTitle('Login and Registration')
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout(self)

        tab_widget = QTabWidget(self)
        layout.addWidget(tab_widget)

        merchant_login_tab = QWidget()
        merchant_register_tab = QWidget()
        user_login_tab = QWidget()
        user_register_tab = QWidget()

        tab_widget.addTab(merchant_login_tab, 'Merchant Login')
        tab_widget.addTab(merchant_register_tab, 'Merchant Register')
        tab_widget.addTab(user_login_tab, 'User Login')
        tab_widget.addTab(user_register_tab, 'User Register')

        self.setupMerchantLogin(merchant_login_tab)
        self.setupMerchantRegister(merchant_register_tab)
        self.setupUserLogin(user_login_tab)
        self.setupUserRegister(user_register_tab)

    def setupMerchantLogin(self, tab):
        """
        Sets up the merchant login tab.

        Args:
            tab (QWidget): The QWidget to set up.
        """
        layout = QFormLayout(tab)
        username = QLineEdit()
        password = QLineEdit()
        password.setEchoMode(QLineEdit.Password)
        login_button = QPushButton('Login')
        login_button.clicked.connect(lambda: self.send_login(
            'merchant', username.text(), password.text()))
        layout.addRow('Username', username)
        layout.addRow('Password', password)
        layout.addRow(login_button)

    def setupMerchantRegister(self, tab):
        """
        Sets up the merchant register tab.

        Args:
            tab (QWidget): The QWidget to set up.
        """
        layout = QFormLayout(tab)
        username = QLineEdit()
        description_store = QLineEdit()
        email = QLineEdit()
        password = QLineEdit()
        inviter_name = QLineEdit()
        self.invite_code = QLineEdit()

        password.setEchoMode(QLineEdit.Password)
        register_button = QPushButton('Register')
        register_button.clicked.connect(lambda: self.send_register(
            'merchant', username.text(), description_store.text(), email.text(),
            password.text(), inviter_name.text(), self.invite_code.text()))
        regist_code_button = QPushButton('Request Invitation Code')
        regist_code_button.clicked.connect(lambda: self.create_register_code())
        layout.addRow('Username', username)
        layout.addRow('Store Description', description_store)
        layout.addRow('Email', email)
        layout.addRow('Password', password)
        layout.addRow('Inviter', inviter_name)
        layout.addRow('Invitation Code', self.invite_code)
        layout.addRow(register_button)
        layout.addRow(regist_code_button)

    def setupUserLogin(self, tab):
        """
        Sets up the user login tab.

        Args:
            tab (QWidget): The QWidget to set up.
        """
        layout = QFormLayout(tab)
        username = QLineEdit()
        password = QLineEdit()
        password.setEchoMode(QLineEdit.Password)
        login_button = QPushButton('Login')
        login_button.clicked.connect(
            lambda: self.send_login('user', username.text(), password.text()))
        layout.addRow('Username', username)
        layout.addRow('Password', password)
        layout.addRow(login_button)

    def setupUserRegister(self, tab):
        """
        Sets up the user register tab.

        Args:
            tab (QWidget): The QWidget to set up.
        """
        layout = QFormLayout(tab)
        username = QLineEdit()
        email = QLineEdit()
        password = QLineEdit()
        password.setEchoMode(QLineEdit.Password)
        register_button = QPushButton('Register')
        register_button.clicked.connect(
            lambda: self.send_register('user', username.text(), None, email.text(),
                                       password.text(), None, None))

        layout.addRow('Username', username)
        layout.addRow('Email', email)
        layout.addRow('Password', password)
        layout.addRow(register_button)

    @qasync.asyncSlot()
    async def create_register_code(self, block):
        """
        Creates a register code.

        Args:
            block: The block to execute.

        Raises:
            Exception: If the result length is invalid.
        """
        counter_str = str(self.send_message_counter)
        self.send_message_counter += 1
        message = f"MERCHANT_CREATE_INVITATION {counter_str}"
        asyncio.create_task(self.message_queue.put(message))
        result = await asyncio.create_task(self.result_queue.get())
        reply = result[0]
        code = result[1]
        if len(result) == 1:
            warning = QMessageBox.Warning(self)
            warning.setWindowTitle('Server Warning')
            warning.setText(reply)
        elif len(result) == 2:
            QMessageBox.question(self, 'Confirmation', f'Invitation Code Obtained: {code}')

    @qasync.asyncSlot()
    async def send_login(self, role, username, password):
        """
        Sends a login request.

        Args:
            role (str): The role of the user.
            username (str): The username.
            password (str): The password.
        """
        counter_str = str(self.send_message_counter)
        self.send_message_counter += 1
        if role == 'user':
            message = ["CLIENT_LOGIN", counter_str,
                       username, password]
        if role == 'merchant':
            message = ["MERCHANT_LOGIN", counter_str, str(username),
                       str(password)]
        asyncio.create_task(self.message_queue.put(message))
        result = await asyncio.create_task(self.result_queue.get())
        QMessageBox.question(self, 'Server Message', result[0])

    @qasync.asyncSlot()
    async def send_register(self, role, username, description, email, password,
                            inviter_name, invite_code):
        """
        Sends a registration request.

        Args:
            role (str): The role of the user.
            username (str): The username.
            description (str): The store description.
            email (str): The email.
            password (str): The password.
            inviter_name (str): The inviter's name.
            invite_code (str): The invitation code.
        """
        counter_str = str(self.send_message_counter)
        self.send_message_counter += 1
        if role == 'user':
            message = ["CLIENT_CREATE", counter_str, str(username),
                       str(email), str(password)]
        if role == 'merchant':
            message = ["MERCHANT_CREATE", counter_str, str(username),
                       str(description), str(email), str(password),
                       str(inviter_name), str(invite_code)]
        asyncio.create_task(self.message_queue.put(message))
        result = await asyncio.create_task(self.result_queue.get())
        QMessageBox.question(self, 'Server Message', result[0])

    def closeEvent(self, event):
        """Handles the close event."""
        self.client_thread.is_running = False
        self.client_thread.quit()
        self.client_thread.wait()
        loop.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    message_queue = asyncio.Queue()
    result_queue = asyncio.Queue()
    loop.create_task(
        client_task('127.0.0.1', 22333, message_queue, result_queue)
    )
    ex = LoginWindow(message_queue, result_queue)
    ex.show()
    try:
        loop.run_forever()
    finally:
        loop.close()  # Close the event loop when the window is closed

    sys.exit(app.exec_())
