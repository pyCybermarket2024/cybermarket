from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QMessageBox, QDesktopWidget, QHeaderView, QTableView, QWidget, \
    QHBoxLayout, QPushButton, QStyledItemDelegate, QVBoxLayout, QLineEdit, QDialogButtonBox, QDialog, QLabel
from PyQt5.uic import loadUi

from settings import LOGO_PATH, TITLE, USER_LOGIN, MERCHANT_LOGIN, user_register, merchant_register, index, \
    user_shopping_cart, user_update, merchant_index_ui


class CustomMessageBox(QMessageBox):
    '''Custom message box with window icon.'''

    def event(self, e):
        '''Override event handler to set window icon.'''
        result = super().event(e)
        if e.type() == 99:
            self.setWindowIcon(QIcon(LOGO_PATH))
        return result


class ThreeFieldsDialog(QDialog):
    '''Dialog window with three input fields.'''
    valuesEntered = pyqtSignal(str, str, str)

    def __init__(self, parent=None):
        '''Initialize the dialog window.

        Args:
            parent: Parent widget (default: None).
        '''
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        '''Initialize the UI components of the dialog window.'''
        layout = QVBoxLayout()
        label_a = QLabel("Product name:")
        label_b = QLabel("Amount:")
        label_c = QLabel("Description:")
        self.input_a = QLineEdit()
        self.input_b = QLineEdit()
        self.input_c = QLineEdit()
        self.input_a.setStyleSheet('QLineEdit { border-radius: 3px; border: 0.5px solid #CCCCCC;}')
        self.input_b.setStyleSheet('QLineEdit { border-radius: 3px; border: 0.5px solid #CCCCCC;}')
        self.input_c.setStyleSheet('QLineEdit { border-radius: 3px; border: 0.5px solid #CCCCCC;}')
        self.input_a.setFixedHeight(30)
        self.input_b.setFixedHeight(30)
        self.input_c.setFixedHeight(30)

        layout.addWidget(label_a)
        layout.addWidget(self.input_a)
        layout.addWidget(label_b)
        layout.addWidget(self.input_b)
        layout.addWidget(label_c)
        layout.addWidget(self.input_c)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)

        self.setLayout(layout)
        self.setWindowTitle('Add products')
        self.setFixedWidth(300)

    def accept(self):
        '''Handle the accept button click event.'''
        value_a = self.input_a.text()
        value_b = self.input_b.text()
        value_c = self.input_c.text()

        self.valuesEntered.emit(value_a, value_b, value_c)

        super().accept()

    def reject(self):
        '''Handle the reject button click event.'''
        print("Operation canceled.")
        super().reject()



class UpdatemerchantThreeFieldsDialog(QDialog):
    '''Dialog window for updating merchant information with four input fields.'''
    valuesEntered = pyqtSignal(str, str, str, str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()


        label_a = QLabel("Username:")
        label_b = QLabel("Password:")
        label_c = QLabel("Email:")
        label_d = QLabel("Description:")

        self.input_a = QLineEdit()
        self.input_b = QLineEdit()
        self.input_c = QLineEdit()
        self.input_d = QLineEdit()

        self.input_a.setStyleSheet('QLineEdit { border-radius: 3px; border: 0.5px solid #CCCCCC;}')
        self.input_b.setStyleSheet('QLineEdit { border-radius: 3px; border: 0.5px solid #CCCCCC;}')
        self.input_c.setStyleSheet('QLineEdit { border-radius: 3px; border: 0.5px solid #CCCCCC;}')
        self.input_d.setStyleSheet('QLineEdit { border-radius: 3px; border: 0.5px solid #CCCCCC;}')
        self.input_a.setFixedHeight(30)
        self.input_b.setFixedHeight(30)
        self.input_c.setFixedHeight(30)
        self.input_d.setFixedHeight(30)

        layout.addWidget(label_a)
        layout.addWidget(self.input_a)
        layout.addWidget(label_b)
        layout.addWidget(self.input_b)
        layout.addWidget(label_c)
        layout.addWidget(self.input_c)
        layout.addWidget(label_d)
        layout.addWidget(self.input_d)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)

        self.setLayout(layout)
        self.setWindowTitle('Update Information')

        self.setFixedWidth(300)

    def accept(self):
        '''Handle the accept button click event.'''
        value_a = self.input_a.text()
        value_b = self.input_b.text()
        value_c = self.input_c.text()
        value_d = self.input_d.text()

        self.valuesEntered.emit(value_a, value_b, value_c, value_d)

        super().accept()

    def reject(self):
        '''Handle the reject button click event.'''
        print("Operation canceled.")
        super().reject()


class UserWindow(QMainWindow):
    '''Main window for the application.'''

    def __init__(self):
        super().__init__()
        self.init_page()
        self.index_model()
        self.user_shopping_cart_models()
        self.merchant_index_models()


    def init_page(self):
        '''Load all UI pages and set up initial page.'''
        self.setWindowTitle(TITLE)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setWindowIcon(QIcon(LOGO_PATH))

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.user_login = self.load_ui(USER_LOGIN)
        self.user_register = self.load_ui(user_register)
        self.user_shopping_cart = self.load_ui(user_shopping_cart)
        self.user_update = self.load_ui(user_update)

        self.merchant_login = self.load_ui(MERCHANT_LOGIN)
        self.merchant_register = self.load_ui(merchant_register)
        self.merchant_shouye = self.load_ui(merchant_index_ui)

        self.index = self.load_ui(index)

        self.switch_to_user_login()
        self.login_or_register()


    def user_shopping_cart_models(self):
        '''Set up index data model.'''
        self.user_shopping_cart_model = QStandardItemModel()
        self.user_shopping_cart_model.setHorizontalHeaderLabels(['ProductId', 'Store Name', 'Product Name', 'Price', 'quantity', 'operate'])
        self.user_shopping_cart.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.user_shopping_cart.tableView.verticalHeader().setVisible(False)
        self.user_shopping_cart.tableView.setModel(self.user_shopping_cart_model)
        self.user_shopping_cart.tableView.setEditTriggers(QTableView.NoEditTriggers)
        self.index.tableView_2.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)
        self.index.tableView_2.setColumnWidth(4, 60)

    def index_model(self):
        '''Set up index data model.'''
        self.merchant_model = QStandardItemModel()
        self.merchant_model.setHorizontalHeaderLabels(['Store Name', ])
        self.index.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.index.tableView.verticalHeader().setVisible(False)
        self.index.tableView.setModel(self.merchant_model)
        self.index.tableView.setEditTriggers(QTableView.NoEditTriggers)

        self.shangpin_model = QStandardItemModel()
        self.shangpin_model.setHorizontalHeaderLabels(['id', 'Name', 'Price', 'quantity', 'description', 'Whether to purchase more'])
        self.index.tableView_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.index.tableView_2.verticalHeader().setVisible(False)
        self.index.tableView_2.setModel(self.shangpin_model)
        self.index.tableView_2.setEditTriggers(QTableView.NoEditTriggers)
        self.index.tableView_2.horizontalHeader().setSectionResizeMode(5, QHeaderView.Fixed)
        self.index.tableView_2.setColumnWidth(5, 60)

    def merchant_index_models(self):
        '''Set up merchant index data model.'''
        self.merchant_shouye_model = QStandardItemModel()
        self.merchant_shouye_model.setHorizontalHeaderLabels(['productId', 'Merchant name', 'Product name', 'Description', 'Price', 'Quantity', 'Replenishment', 'Delete'])
        self.merchant_shouye.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.merchant_shouye.tableView.verticalHeader().setVisible(False)
        self.merchant_shouye.tableView.setModel(self.merchant_shouye_model)
        self.merchant_shouye.tableView.setEditTriggers(QTableView.NoEditTriggers)

        self.merchant_shouye.tableView.horizontalHeader().setSectionResizeMode(6, QHeaderView.Fixed)
        self.merchant_shouye.tableView.setColumnWidth(6, 50)
        self.merchant_shouye.tableView.horizontalHeader().setSectionResizeMode(7, QHeaderView.Fixed)
        self.merchant_shouye.tableView.setColumnWidth(7, 50)


    def login_or_register(self):
        '''Bind events for login and registration pages.'''
        self.user_login.pushButton_2.clicked.connect(self.switch_to_merchant_login)
        self.user_login.pushButton_3.clicked.connect(self.switch_to_user_register)
        self.user_register.pushButton_2.clicked.connect(self.switch_to_merchant_login)
        self.user_register.pushButton_3.clicked.connect(self.switch_to_user_login)
        self.merchant_login.pushButton_2.clicked.connect(self.switch_to_user_login)
        self.merchant_login.pushButton_3.clicked.connect(self.switch_to_merchant_register)
        self.merchant_register.pushButton_2.clicked.connect(self.switch_to_user_login)
        self.merchant_register.pushButton_3.clicked.connect(self.switch_to_merchant_login)
        self.user_shopping_cart.pushButton_2.clicked.connect(self.switch_to_user_update)
        self.index.pushButton_2.clicked.connect(self.switch_to_user_update)

    def switch_to_merchant_shouye(self):
        '''Switch to the merchant homepage.'''
        self.stacked_widget.setCurrentWidget(self.merchant_shouye)
        self.setFixedSize(self.merchant_shouye.size())
        self.center()

    def switch_to_user_update(self):
        '''Switch to the user update page.'''
        self.stacked_widget.setCurrentWidget(self.user_update)
        self.setFixedSize(self.user_update.size())
        self.center()

    def switch_to_user_shopping_cart(self):
        '''Switch to the user shopping cart page.'''
        self.stacked_widget.setCurrentWidget(self.user_shopping_cart)
        self.setFixedSize(self.user_shopping_cart.size())
        self.center()

    def switch_to_index(self):
        '''Switch to the index page.'''
        self.stacked_widget.setCurrentWidget(self.index)
        self.setFixedSize(self.index.size())
        self.center()

    def switch_to_user_login(self):
        '''Switch to the user login page.'''
        self.stacked_widget.setCurrentWidget(self.user_login)
        self.setFixedSize(self.user_login.size())
        self.center()

    def switch_to_user_register(self):
        '''Switch to the user registration page.'''
        self.stacked_widget.setCurrentWidget(self.user_register)
        self.setFixedSize(self.user_register.size())
        self.center()

    def switch_to_merchant_login(self):
        '''Switch to the merchant login page.'''
        self.stacked_widget.setCurrentWidget(self.merchant_login)
        self.setFixedSize(self.merchant_login.size())
        self.center()

    def switch_to_merchant_register(self):
        '''Switch to the merchant registration page.'''
        self.stacked_widget.setCurrentWidget(self.merchant_register)
        self.setFixedSize(self.merchant_register.size())
        self.center()

    def pop_frame(self, msg):
        '''Display a message box.

        Args:
            msg (str): The message to display.
        '''
        msgBox = CustomMessageBox()
        msgBox.setWindowTitle(TITLE)
        msgBox.setText(msg)
        msgBox.addButton(QMessageBox.Yes)
        yes_button = msgBox.button(QMessageBox.Yes)
        yes_button.setText('Cancel')
        msgBox.exec_()

    def load_ui(self, path):
        '''Load a UI file.

        Args:
            path (str): The path to the UI file.
        Returns:
            QWidget: The loaded UI widget.
        '''
        ui = loadUi(path)
        self.stacked_widget.addWidget(ui)
        return ui

    def center(self):
        '''Center the window on the screen.'''
        screen = QDesktopWidget().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)

