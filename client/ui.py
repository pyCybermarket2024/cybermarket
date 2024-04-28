from ast import Await
from asyncio import events
from lib2to3.pgen2.token import AWAIT
from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget, QVBoxLayout, QPushButton, 
                             QLineEdit, QLabel, QMessageBox, QFormLayout)
from PyQt5.QtCore import pyqtSlot
from asyncsession import client_task
import sys
import asyncio
import qasync 
class LoginWindow(QWidget):
    send_message_counter=0

    def __init__(self, message_queue, result_queue):
        super().__init__()
       # self.client_thread = AsyncSession("127.0.0.1", 22333)
        #self.client_thread.get_reply.connect(self.handle_received)
        self.initUI()
        self.message_queue = message_queue
        self.result_queue = result_queue
        #coro=self.client_thread.run()#创建事件

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
        login_button.clicked.connect(lambda: self.send_login('merchant', username.text(), password.text()))
        layout.addRow('账号', username)
        layout.addRow('密码', password)
        layout.addRow(login_button)

    def setupMerchantRegister(self, tab):
        layout = QFormLayout(tab)
        username = QLineEdit()
        password = QLineEdit()
        password.setEchoMode(QLineEdit.Password)
        register_button = QPushButton('注册')
        register_button.clicked.connect(lambda: self.send_register('merchant', username.text(), password.text(), None))
        layout.addRow('账号', username)
        layout.addRow('密码', password)
        layout.addRow(register_button)

    def setupUserLogin(self, tab):
        layout = QFormLayout(tab)
        username = QLineEdit()
        password = QLineEdit()
        password.setEchoMode(QLineEdit.Password)
        login_button = QPushButton('登录')
        login_button.clicked.connect(lambda: self.send_login('user', username.text(), password.text()))
        layout.addRow('账号', username)
        layout.addRow('密码', password)
        layout.addRow(login_button)

    def setupUserRegister(self, tab):
        layout = QFormLayout(tab)
        username = QLineEdit()
        password = QLineEdit()
        password.setEchoMode(QLineEdit.Password)
        register_button = QPushButton('注册')
        register_button.clicked.connect(lambda: self.send_register('user', username.text(), password.text(), None))
        layout.addRow('账号', username)
        layout.addRow('密码', password)
        layout.addRow(register_button)

    @qasync.asyncSlot()
    async def send_login(self, role, username, password):
        counter_str = str(self.send_message_counter)  # This should be unique per message
        self.send_message_counter+=1
        if role == 'user':
            msg = "CLIENT_LOGIN " + counter_str + " " + username + " " + password
        if role == 'merchant':
            msg = "MERCHANT_LOGIN " + counter_str + " " + username + " " + password
        asyncio.create_task(self.message_queue.put(msg))
        result = await asyncio.create_task(self.result_queue.get())
        QMessageBox.question(self, '服务器消息', result)


    def send_register(self, role, username, password, invite_code):
        if invite_code:
            message = f'REGISTER {role} {username} {password} {invite_code}'
        else:
            message = f'REGISTER {role} {username} {password}'
        self.client_thread.send_message(message)

    #def handle_received(self, message):
    #    # Process the received message and update UI accordingly
    #    print(f'Received: {message}')

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
    loop.create_task(client_task('127.0.0.1', 22333, message_queue, result_queue))
    ex = LoginWindow(message_queue,result_queue)
    ex.show()
    #loop = asyncio.get_event_loop()
    try:
       loop.run_forever()
    finally:
        loop.close()  # 当窗口关闭时关闭事件循环

    sys.exit(app.exec_())