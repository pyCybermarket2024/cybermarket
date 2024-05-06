"""This script is the main entry point for creating a fully functional marketplace interface. It is called by the main function and imports various UI files, static resources, and backend request functions to facilitate the creation of the marketplace interface."""
import os
from lang import _
BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, 'static')
LOGO_PATH = os.path.join(STATIC_DIR, 'logo.png')

USER_LOGIN = os.path.join(STATIC_DIR, 'user_login.ui')
user_register = os.path.join(STATIC_DIR, 'user_register.ui')
user_shopping_cart = os.path.join(STATIC_DIR, 'user_shopping_cart.ui')
user_update = os.path.join(STATIC_DIR, 'user_update.ui')

MERCHANT_LOGIN = os.path.join(STATIC_DIR, 'merchant_login.ui')
merchant_register = os.path.join(STATIC_DIR, 'merchant_register.ui')
merchant_index_ui = os.path.join(STATIC_DIR, 'merchant_index.ui')

index = os.path.join(STATIC_DIR, 'index.ui')

TITLE = _('Cybermarket')
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 22333
