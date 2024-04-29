from asyncsession import client_task
import sys
import asyncio
import qasync
from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget, QVBoxLayout, QPushButton,
                             QLineEdit, QLabel, QMessageBox, QFormLayout,QInputDialog)


class LoginWindow(QWidget):
    send_message_counter = 0

    def __init__(self, message_queue, result_queue):
        super().__init__()
        self.initUI()
        self.message_queue = message_queue
        self.result_queue = result_queue
        self.invite_cod = None

    async def run_client(self):
        await self.client_thread.run()

    def initUI(self):
        self.setWindowTitle('Login and Registration')
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout(self)

        tab_widget = QTabWidget(self)
        layout.addWidget(tab_widget)

        merchant_login_tab = QWidget()
        merchant_register_tab = QWidget()
        user_login_tab = QWidget()
        user_register_tab = QWidget()

        tab_widget.addTab(merchant_login_tab, '商家登录')
        tab_widget.addTab(merchant_register_tab, '商家注册')
        tab_widget.addTab(user_login_tab, '用户登录')
        tab_widget.addTab(user_register_tab, '用户注册')

        self.setupMerchantLogin(merchant_login_tab)
        self.setupMerchantRegister(merchant_register_tab)
        self.setupUserLogin(user_login_tab)
        self.setupUserRegister(user_register_tab)

    def setupMerchantLogin(self, tab):
        layout = QFormLayout(tab)
        username = QLineEdit()
        password = QLineEdit()
        password.setEchoMode(QLineEdit.Password)
        login_button = QPushButton('登录')
        login_button.clicked.connect(lambda: self.send_login(
            'merchant', username.text(), password.text()))
        layout.addRow('账号', username)
        layout.addRow('密码', password)
        layout.addRow(login_button)

    def setupMerchantRegister(self, tab):
        layout = QFormLayout(tab)
        username = QLineEdit()
        description_store = QLineEdit()
        email = QLineEdit()
        password = QLineEdit()
        inviter_name = QLineEdit()
        self.invite_cod = QLineEdit()

        password.setEchoMode(QLineEdit.Password)
        register_button = QPushButton('注册')
        register_button.clicked.connect(lambda: self.send_register(
            'merchant', username.text(), description_store.text(), email.text(
            ), password.text(), inviter_name.text(), self.invite_cod.text()))
        regist_code_button = QPushButton('申请邀请码')
        regist_code_button.clicked.connect(lambda: self.creat_register_code())
        layout.addRow('账号', username)
        layout.addRow('店铺介绍', description_store)
        layout.addRow('电子邮箱', email)
        layout.addRow('密码', password)
        layout.addRow('邀请人', inviter_name)
        layout.addRow('邀请码', self.invite_cod)
        layout.addRow(register_button)
        layout.addRow(regist_code_button)

    def setupUserLogin(self, tab):
        layout = QFormLayout(tab)
        username = QLineEdit()
        password = QLineEdit()
        password.setEchoMode(QLineEdit.Password)
        login_button = QPushButton('登录')
        login_button.clicked.connect(
            lambda: self.send_login('user', username.text(), password.text()))
        layout.addRow('账号', username)
        layout.addRow('密码', password)
        layout.addRow(login_button)

    def setupUserRegister(self, tab):
        layout = QFormLayout(tab)
        username = QLineEdit()
        email = QLineEdit()
        password = QLineEdit()
        password.setEchoMode(QLineEdit.Password)
        register_button = QPushButton('注册')
        register_button.clicked.connect(
            lambda: self.send_register('user', username.text(), email.text(),
                                       password.text(), None, None, None))

        layout.addRow('账号', username)
        layout.addRow('电子邮箱', email)
        layout.addRow('密码', password)
        layout.addRow(register_button)

    @qasync.asyncSlot()
    async def creat_register_code(self, block):
        # This should be unique per message
        counter_str = str(self.send_message_counter)
        self.send_message_counter += 1
        message = "MERCHANT_CREATE_IVITATION " + counter_str
        asyncio.create_task(self.message_queue.put(message))
        result = await asyncio.create_task(self.result_queue.get())
        reply = result[0]
        code = result[1]
        print(result)
        if len(result) == 1:
            warning = QMessageBox.Warning(self)
            warning.setWindowTitle('来自服务器的警告')
            warning.setText(reply)
        elif len(result) == 2:
            QMessageBox.question(self, '确认', '已获取邀请码:' + code)

    @qasync.asyncSlot()
    async def send_login(self, role, username, password):
        # This should be unique per message
        counter_str = str(self.send_message_counter)
        self.send_message_counter += 1
        if role == 'user':
            message = "CLIENT_LOGIN {} {} {}".format(counter_str, username,
                                                     password)
        if role == 'merchant':
            message = "MERCHANT_LOGIN {} {} {}".format(counter_str, username,
                                                       password)
        asyncio.create_task(self.message_queue.put(message))
        result = await asyncio.create_task(self.result_queue.get())
        QMessageBox.question(self, '服务器消息', result[0])

    @qasync.asyncSlot()
    async def send_register(self, role, username, description, email, password,
                            inviter_name, invite_code):
        # This should be unique per message
        counter_str = str(self.send_message_counter)
        self.send_message_counter += 1
        if role == 'user':
            message = "CLIENT_CREATE {} {} {} {}".format(
                counter_str, str(username), str(email), str(password))
        if role == 'merchant':
            message = "MERCHANT_CREATE {} {} {} {} {} {} {}".format(
                counter_str, username, str(description), str(email),
                str(password), str(inviter_name), str(invite_code))
        asyncio.create_task(self.message_queue.put(message))
        result = await asyncio.create_task(self.result_queue.get())
        QMessageBox.question(self, '服务器消息', result[0])

    # def handle_received(self, message):
    # Process the received message and update UI accordingly
    # print(f'Received: {message}')

    def closeEvent(self, event):
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
    # loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    finally:
        loop.close()  # 当窗口关闭时关闭事件循环

    sys.exit(app.exec_())
