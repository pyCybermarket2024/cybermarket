"""Initialize the Script class."""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QColor
from PyQt5.QtWidgets import QInputDialog, QLineEdit
from .request import request, _async_request
from .ui import UserWindow, ThreeFieldsDialog, UpdatemerchantThreeFieldsDialog
from threading import Thread as _async
from .lang import _


class Script(UserWindow):
    """The Script class."""

    def __init__(self):
        """Initialize the Script class."""
        self.product_data, self.user_shopping_cart_data = [], []
        self.merchant_username = ''
        self.merchant_index_data = []

        super(Script, self).__init__()
        # User register
        self.user_register.pushButton.clicked.connect(self.user_register_task)
        # User login
        self.user_login.pushButton.clicked.connect(self.user_login_task)

        self.merchant_register.pushButton.clicked.connect(
            self.merchant_register_task
            )  # Merchant register
        self.merchant_login.pushButton.clicked.connect(
            self.merchant_login_task
            )  # Merchant login

        self.index.tableView.clicked.connect(
            self.handle_cell_clicked
            )  # Home page merchant cell clicked event
        self.index.tableView_2.clicked.connect(
            self.handle_cell_clicked_2
            )  # Clicking the add to cart button

        self.index.pushButton_3.clicked.connect(
            self.login_out
            )  # Log out
        self.index.pushButton.clicked.connect(
            self.user_shopping_cart_task
            )  # Clicking the shopping cart button to load data

        self.user_shopping_cart.pushButton_4.clicked.connect(
            self.index_task
            )  # User shopping cart back to home page to load data
        self.user_shopping_cart.pushButton_3.clicked.connect(
            self.login_out
            )  # Log out
        self.user_shopping_cart.tableView.clicked.connect(
            self.user_shopping_cart_handle_cell_clicked
            )  # User shopping cart cell clicked event
        self.user_shopping_cart.pushButton_5.clicked.connect(
            self.checkout_item_order
            )  # Checkout

        self.user_update.pushButton.clicked.connect(
            self.user_update_call
            )  # Update user information
        self.user_update.pushButton_2.clicked.connect(
            self.ritorno
            )  # Return to the home page

        self.merchant_shouye.tableView.clicked.connect(
            self.rimborso_o_cancellazione
            )  # Replenishment or deletion
        self.merchant_shouye.pushButton_5.clicked.connect(
            self.create_product
            )  # Create product
        self.merchant_shouye.pushButton_4.clicked.connect(
            self.codice_invito
            )  # Create invitation code
        self.merchant_shouye.pushButton_3.clicked.connect(
            self.login_out
            )  # Log out
        self.merchant_shouye.pushButton_2.clicked.connect(
            self.update_merchant_info
            )  # Update merchant information

    def ritorno(self):
        """Return to the home page from the user update page."""
        self.switch_to_index()
        self.index_merchant_get_data()

    def user_update_call(self):
        """Update user information."""
        self.pop_frame('update success')

    def login_out(self):
        """Log out the user."""
        self.switch_to_user_login()
        _async_request(request('CLIENT_LOGOUT'))

    def index_task(self):
        """Load data when navigating from the shopping cart to home page."""
        self.switch_to_index()

    def checkout_item_order(self):
        """Checkout items in the user's shopping cart."""
        self.pop_frame(request('CLIENT_CHECKOUT_ITEM')[0])
        self.user_shopping_cart_get_data()

    def index_merchant_get_data(self):
        """Retrieve data for the merchant's home page."""
        self.merchant_model.removeRows(0, self.merchant_model.rowCount())
        queryset = [[i.tolist()[0], ] for i in request(
            'LIST_MERCHANT'
            )[1].values]
        for row_index, row_data in enumerate(queryset):
            for col_index, col_data in enumerate(row_data):
                item = QStandardItem(str(col_data))
                item.setTextAlignment(Qt.AlignLeft)
                self.merchant_model.setItem(row_index, col_index, item)

    def user_shopping_cart_get_data(self):
        """Retrieve data for the user's shopping cart."""
        self.user_shopping_cart_model.removeRows(
            0, self.user_shopping_cart_model.rowCount()
            )
        queryset = [i.tolist() for i in request('CLIENT_GET_ITEMS')[1].values]
        queryset = list(map(
            lambda i: [
                i[4], i[0], i[1], i[2], f'{i[3]:.2f}', 'Delete'
                ], queryset
            ))
        self.user_shopping_cart_data = queryset

        for row_index, row_data in enumerate(queryset):
            for col_index, col_data in enumerate(row_data):
                item = QStandardItem(str(col_data))
                item.setTextAlignment(Qt.AlignCenter)
                self.user_shopping_cart_model.setItem(
                    row_index, col_index, item
                    )
                if col_index == 5:
                    item.setForeground(QColor(Qt.red))
        self.user_shopping_cart.label.setText(
            _('Total amount:') + "{}:.2f".format(
                request("CLIENT_GET_PRICE")[1]
                )
                )

    def user_shopping_cart_task(self):
        """Navigate to the user's shopping cart."""
        self.switch_to_user_shopping_cart()
        self.user_shopping_cart_get_data()

    def user_shopping_cart_handle_cell_clicked(self, index):
        """Handle cell click events in the user's shopping cart."""
        row, col = index.row(), index.column()
        if col == 5:
            product_id = self.user_shopping_cart_data[row][0]
            request('CLIENT_REMOVE_ITEM', product_id)
            self.user_shopping_cart_get_data()

    def handle_cell_clicked_2(self, index):
        """Handle click events on the 'Add to cart' button."""
        row, col = index.row(), index.column()
        if col == 5:
            product_id = self.product_data[row][0]
            text, okPressed = QInputDialog.getText(
                self, _("Add to cart"), _("Please enter the quantity:"),
                QLineEdit.Normal, ""
                )
            if okPressed and text != '':
                request('CLIENT_ADD_ITEM', product_id, text)

    def handle_cell_clicked(self, index):
        """Handle cell click events on the home page."""
        value = index.data(Qt.DisplayRole)
        queryset = [i.tolist() for i in request(
            'LIST_PRODUCT', value)[1].values]
        queryset = list(map(lambda i: [
            i[0], i[2], f'{i[4]:.2f}', i[5], i[3],
            _('Add to cart')], queryset))
        self.product_data = queryset
        for row_index, row_data in enumerate(queryset):
            for col_index, col_data in enumerate(row_data):
                item = QStandardItem(str(col_data))
                item.setTextAlignment(Qt.AlignCenter)
                if col_index == 5:
                    item.setForeground(QColor(Qt.blue))
                self.product_model.setItem(row_index, col_index, item)

    def user_register_task(self):
        """Process user registration."""
        username = self.user_register.lineEdit.text()
        password = self.user_register.lineEdit_2.text()
        email = self.user_register.lineEdit_3.text()
        response = request('CLIENT_CREATE', username, email, password)[0]
        self.pop_frame(response)

    def user_login_task(self):
        """Process user login."""
        username = self.user_login.lineEdit.text()
        password = self.user_login.lineEdit_2.text()
        response = request('CLIENT_LOGIN', username, password)[0]
        if '200' in response:
            self.switch_to_index()
            self.index_merchant_get_data()
        else:
            self.pop_frame(response)

    def merchant_register_task(self):
        """Process merchant registration."""
        username = self.merchant_register.lineEdit.text()
        description = self.merchant_register.lineEdit_2.text()
        email = self.merchant_register.lineEdit_3.text()
        password = self.merchant_register.lineEdit_4.text()
        yaoqingren = self.merchant_register.lineEdit_5.text()
        invitation_code = self.merchant_register.lineEdit_6.text()
        response = request(
            'MERCHANT_CREATE', username, description, email, password,
            yaoqingren, invitation_code
            )[0]
        self.pop_frame(response)

    def merchant_login_task(self):
        """Process merchant login."""
        username = self.merchant_login.lineEdit.text()
        password = self.merchant_login.lineEdit_2.text()
        response = request('MERCHANT_LOGIN', username, password)[0]
        if '200' in response:
            self.merchant_username = username
            self.switch_to_merchant_shouye()
            self.merchant_index_get_data()
        else:
            self.pop_frame(response)

    def merchant_index_get_data(self):
        """Retrieve data for the merchant's home page."""
        self.merchant_shouye_model.removeRows(
            0, self.merchant_shouye_model.rowCount()
            )
        queryset = [i.tolist() for i in request(
            'LIST_PRODUCT', self.merchant_username
            )[1].values]
        queryset = list(map(lambda i: [
            i[0], i[1], i[2], i[3], f'{i[4]:.2f}',
            i[5], 'Replenishment', 'Delete'
            ], queryset))
        self.merchant_index_data = queryset

        for row_index, row_data in enumerate(queryset):
            for col_index, col_data in enumerate(row_data):
                item = QStandardItem(str(col_data))
                item.setTextAlignment(Qt.AlignCenter)
                self.merchant_shouye_model.setItem(row_index, col_index, item)
                if col_index == 6:
                    item.setForeground(QColor(Qt.blue))
                elif col_index == 7:
                    item.setForeground(QColor(Qt.red))
        self.merchant_shouye.label.setText(
            'Total profit: ' + '{}:.2f'.format(
                request("MERCHANT_GET_PROFIT")[1]
                )
            )

    def rimborso_o_cancellazione(self, index):
        """Process replenishment or deletion actions."""
        row, col = index.row(), index.column()
        if col == 6:
            product_id = self.merchant_index_data[row][0]
            text, okPressed = QInputDialog.getText(
                self, _("Replenishment"),
                _("Please enter the replenishment quantity:"),
                QLineEdit.Normal, ""
                )
            if okPressed and text != '':
                request('MERCHANT_RESTOCK_PRODUCT', product_id, text)
                self.merchant_index_get_data()

        elif col == 7:
            product_id = self.merchant_index_data[row][0]
            request('MERCHANT_DEL_PRODUCT', product_id)
            self.merchant_index_get_data()

    def create_product(self):
        """Create a new product."""
        dialog = ThreeFieldsDialog(self)
        dialog.valuesEntered.connect(self.__create_product)
        dialog.exec_()

    def __create_product(self, value_a, value_b, value_c):
        """Create a new product.

        Args:
            value_a (str): Product ID.
            value_b (str): Product name.
            value_c (str): Product price.

        Returns:
            None.

        Raises:
            None.
        """
        request('MERCHANT_ADD_PRODUCT', value_a, value_b, value_c)
        _async(target=self.merchant_index_get_data()).start()

    def codice_invito(self):
        """Generate an invitation code for the merchant."""
        response = request('MERCHANT_CREATE_IVITATION')[1]
        self.pop_frame(_('Your invitation code is:') + response)

    def update_merchant_info(self):
        """Update merchant information."""
        dialog = UpdatemerchantThreeFieldsDialog(self)
        dialog.valuesEntered.connect(self.__update_merchant_info)
        dialog.exec_()

    def __update_merchant_info(self, value_a, value_b, value_c, value_d):
        """Update merchant information.

        Args:
            value_a (str): Store name.
            value_b (str): Password.
            value_c (str): Email.
            value_d (str): Description.

        Returns:
            None.

        Raises:
            None.
        """
        request('SET_MERCHANT_STORENAME', value_a)
        request('SET_MERCHANT_PASSWORD', value_b, value_b)
        request('SET_MERCHANT_EMAIL', value_c)
        request('SET_MERCHANT_DESCRIPTION', value_d)
        self.pop_frame('200 OK')
