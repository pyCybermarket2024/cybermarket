"""Entrance to the main program."""
import sys
from PyQt5.QtWidgets import QApplication
from .request import _async_request
from .logic import Script

if __name__ == '__main__':
    _async_request('CLIENT_LOGOUT')
    _async_request('MERCHANT_LOGOUT')
    app = QApplication(sys.argv)
    window = Script()
    window.show()
    sys.exit(app.exec_())
