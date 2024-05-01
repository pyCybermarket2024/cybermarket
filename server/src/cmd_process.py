"""Accept commands from server.py and output the results to the queue."""
import pandas as pd
from src.model import Merchant, Client, Order, Product
from src.model import InventoryShortage
from src.invitation import create_ivitation, check_ivitation
from src.setting import session, lang
from src.lang import _

lang


def client_create(request_id, connected_address, *args):
    """
    Create a new client with the provided username, email, and password.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        args[0]: The username of new client
        args[1]: The email of new client
        args[2]: The password of new merchant

    Return:
        [reply_message]
    """
    if session.query(Client).filter(Client.username == args[0]).first():
        msg = _("This username is occupied")
        reply = str(request_id) + " 409 Conflict: " + msg
        return [reply]
    else:
        client = Client(username=args[0], email=args[1], password=args[2])
        session.add(client)
        session.commit()
        reply = str(request_id) + " 201 Created"
        return [reply]


def set_client_username(request_id, connected_address, *args):
    """
    Set the username for a logged-in client.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        args[0]: The new username of the client

    Return:
        [reply_message]
    """
    result = session.query(Client).filter(
        Client.connected_address == connected_address).first()
    if result:
        result.set_username(args[0])
        msg = _("Username has been set")
        reply = str(request_id) + " 200 OK: " + msg
        return [reply]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


def set_client_email(request_id, connected_address, *args):
    """
    Set the email for a logged-in client.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        args[0]: The new email of the client

    Return:
        [reply_message]
    """
    result = session.query(Client).filter(
        Client.connected_address == connected_address).first()
    if result:
        result.set_email(args[0])
        msg = _("Email has been set")
        reply = str(request_id) + " 200 OK: " + msg
        return [reply]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


def set_client_password(request_id, connected_address, *args):
    """
    Set a new password for the client if the current password is verified.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        args[0]: The new password.
        args[1]: The current password for verification.

    Return:
        [reply_message]
    """
    result = session.query(Client).filter(
        Client.connected_address == connected_address).first()
    if result:
        if result.verify_password(args[1]):
            result.set_password(args[0], args[1])
            msg = _("New password has been set")
            reply = str(request_id) + " 200 OK: " + msg
            return [reply]
        else:
            msg = _("The password of the user is incorrect")
            reply = str(request_id) + " 403 Forbidden: " + msg
            return [reply]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


def client_login(request_id, connected_address, *args):
    """
    Log in a client if the credentials are correct.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        args[0]: The storename or email of the client
        args[1]: The password of the client

    Return:
        [reply_message]
    """
    result = session.query(Client).filter(
        (Client.username == args[0]) | (Client.email == args[0])
        ).first()
    login_status = session.query(Client.connected_address).filter(
        Client.connected_address == connected_address).first()
    if login_status:
        msg = _("The user has been logged in, please do not log in again")
        reply = str(request_id) + " 400 Bad Request: " + msg
        return [reply]
    elif result:
        if result.verify_password(args[1]):
            result.client_login(args[1], connected_address)
            msg = _("This user is logged in")
            reply = str(request_id) + " 200 OK: " + msg
            return [reply]
        else:
            msg = _("The password of the user is incorrect")
            reply = str(request_id) + " 403 Forbidden: " + msg
            return [reply]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


def client_logout(request_id, connected_address, *args):
    """
    Log out a client if they are currently logged in.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        *args: Variable length argument list: Do not require

    Return:
        [reply_message]
    """
    result = session.query(Client).filter(
        Client.connected_address == connected_address).first()
    if result:
        result.client_logout()
        msg = _("You have successfully logged out")
        reply = str(request_id) + " 200 OK: " + msg
        return [reply]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


def client_add_item(request_id, connected_address, *args):
    """
    Add an item to the client's shopping cart.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        args[0]: The id of the product to add
        args[1]: The quantity of the product to add

    Return:
        [reply_message]
    """
    result = session.query(Client).filter(
        Client.connected_address == connected_address).first()
    product = session.query(Product).filter(
        Product.productId == args[0]).first()
    if int(args[1]) <= 0:
        msg = _("The quantity of added products should be a positive integer")
        reply = str(request_id) + " 400 Bad Request: " + msg
        return [reply]
    elif not product:
        msg = _("The product you are trying to add cannot be found")
        reply = str(request_id) + " 404 Not Found: " + msg
        return [reply]
    elif result:
        result.add_item(args[0], int(args[1]))
        msg = _("This product has been added to the shopping cart")
        reply = str(request_id) + " 200 OK: " + msg
        return [reply]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


def client_remove_item(request_id, connected_address, *args):
    """
    Remove an item from the client's shopping cart.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        args[0]: The id of the product to remove

    Return:
        [reply_message]
    """
    result = session.query(Client).filter(
        Client.connected_address == connected_address).first()
    product = session.query(Order).filter(
            Order.product_id == args[0]
            ).first()
    if not product:
        msg = _("This product is not in your shopping cart")
        reply = str(request_id) + " 404 Not Found: " + msg
        return [reply]
    elif result:
        result.remove_item(args[0])
        msg = _("This product has been removed from the shopping cart")
        reply = str(request_id) + " 200 OK: " + msg
        return [reply]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


def client_get_items(request_id, connected_address, *args):
    """
    Retrieve the list of items in the client's shopping cart.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        *args: Variable length argument list: Do not require

    Return:
        [reply_message, item_dataframe]
        item_dataframe (pd.Dataframe): Dataframe of items in the shopping cart
    """
    result = session.query(Client).filter(
        Client.connected_address == connected_address).first()
    if result:
        msg = _("Obtained order list")
        reply = str(request_id) + " 200 OK: " + msg
        column_labels = [_('storename'), _('productname'),
                         _('price'), _('quantity')]
        df = pd.DataFrame(result.get_items(), columns=column_labels)
        return [reply, df]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


def client_get_price(request_id, connected_address, *args):
    """
    Calculate the total price of the items in the client's shopping cart.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        *args: Variable length argument list: Do not require

    Return:
        [reply_message, total_price]
        total_price: The price all items in the shopping cart
    """
    result = session.query(Client).filter(
        Client.connected_address == connected_address).first()
    if result:
        msg = _("Order price obtained")
        reply = str(request_id) + " 200 OK: " + msg
        return [reply, result.get_price()]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


def client_checkout_item(request_id, connected_address, *args):
    """
    Check out the items in the client's shopping cart.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        *args: Variable length argument list: Do not require

    Return:
        [reply_message]
    """
    result = session.query(Client).filter(
        Client.connected_address == connected_address).first()
    if result:
        try:
            result.checkout_item()
            msg = _("Order has been checked out")
            reply = str(request_id) + " 200 OK: " + msg
            return [reply]
        except InventoryShortage as error:
            msg = _(str(error))
            reply = str(request_id) + " 400 Bad Request: " + msg
            return [reply]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


def list_merchant(request_id, connected_address, *args):
    """
    Retrieve a list of all merchants from the database.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        *args: Variable length argument list: Do not require

    Return:
        [reply_message, merchant_dataframe]
        merchant_dataframe (pd.Dataframe): Dataframe of all merchants
    """
    result = session.query(Merchant).all()
    merchant_list = []
    for merchant in result:
        merchant_list.append([
            merchant.storename,
            merchant.description,
            merchant.email
        ])
    column_labels = [_('storename'), _('description'),
                     _('email')]
    df = pd.DataFrame(merchant_list, columns=column_labels)
    reply = str(request_id) + " 200 OK"
    return [reply, df]


def list_product(request_id, connected_address, *args):
    """
    Retrieve a list of products from merchant by the store name.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        args[0]: Storename of the merchant

    Return:
        [reply_message, product_dataframe]
        product_dataframe (pd.Dataframe): Dataframe of products from merchant
    """
    result = session.query(Merchant).filter(
        Merchant.storename == args[0]).first()
    if result:
        msg = _("Product list has been obtained")
        reply = str(request_id) + " 200 OK: " + msg
        column_labels = [_('product_id'), _('storename'), _('productname'),
                         _('description'), _('price'), _('stock')]
        df = pd.DataFrame(result.get_product_list(), columns=column_labels)
        return [reply, df]
    else:
        msg = _("No store with this name found")
        reply = str(request_id) + " 404 Not Found: " + msg
        return [reply]


def merchant_create_ivitation(
        request_id, connected_address, *args):
    """
    Generate an invitation code for a merchant if they are connected.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        *args: Variable length argument list: Do not require

    Return:
        [reply_message, invitation_code]
        invitation_code (str): Alphanumeric string of length 12.
    """
    result = session.query(Merchant).filter(
        Merchant.connected_address == connected_address).first()
    if result:
        msg = _("Invitation code has been generated")
        reply = str(request_id) + " 200 OK: " + msg
        return [reply, create_ivitation(result.storename)]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


def merchant_create(request_id, connected_address, *args):
    """
    Create a new merchant record if the invitation code is verified.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        args[0]: The storename of new merchant
        args[1]: The description of new merchant
        args[2]: The email of new merchant
        args[3]: The password of new merchant
        args[4]: The storename of the store, who is inviting
        args[5]: The invitation code

    Return:
        [reply_message]
    """
    if check_ivitation(args[4], args[5]):
        if session.query(Merchant).filter(
                Merchant.storename == args[0]).first():
            msg = _("This storename is occupied")
            reply = str(request_id) + " 409 Conflict:  " + msg
            return [reply]
        else:
            merchant = Merchant(
                storename=args[0],
                description=args[1],
                email=args[2],
                password=args[3]
                )
            session.add(merchant)
            session.commit()
            reply = str(request_id) + " 201 Created"
            return [reply]
    else:
        msg = _("Your invitation code cannot be verified.\
 This invitation code may be wrong or has already been used.\
 Please contact other merchants to request the invitation code.")
        reply = str(request_id) + " 406 Not Acceptable: " + msg
        return [reply]


def merchant_login(request_id, connected_address, *args):
    """
    Log in a merchant if the credentials are correct.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        args[0]: The storename or email of the merchant
        args[1]: The password of the merchant

    Return:
        [reply_message]
    """
    result = session.query(Merchant).filter(
        (Merchant.storename == args[0]) | (Merchant.email == args[0])
        ).first()
    login_status = session.query(Merchant.connected_address).filter(
        Merchant.connected_address == connected_address).first()
    if login_status:
        msg = _("The merchant has been logged in, please do not log in again")
        reply = str(request_id) + " 400 Bad Request: " + msg
        return [reply]
    elif result:
        if result.verify_password(args[1]):
            result.merchant_login(args[1], connected_address)
            msg = _("This merchant is logged in")
            reply = str(request_id) + " 200 OK: " + msg
            return [reply]
        else:
            msg = _("The password of the merchant is incorrect")
            reply = str(request_id) + " 403 Forbidden: " + msg
            return [reply]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


def merchant_logout(request_id, connected_address, *args):
    """
    Log out a merchant if they are currently logged in.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        *args: Variable length argument list: Do not require

    Return:
        [reply_message]
    """
    result = session.query(Merchant).filter(
        Merchant.connected_address == connected_address).first()
    if result:
        result.merchant_logout()
        msg = _("You have successfully logged out")
        reply = str(request_id) + " 200 OK: " + msg
        return [reply]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


def set_merchant_storename(request_id, connected_address, *args):
    """
    Set the store name for a logged-in merchant.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        args[0]: The new storename of the merchant

    Return:
        [reply_message]
    """
    result = session.query(Merchant).filter(
        Merchant.connected_address == connected_address).first()
    if result:
        result.set_storename(args[0])
        msg = _("Storename has been set")
        reply = str(request_id) + " 200 OK: " + msg
        return [reply]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


def set_merchant_email(request_id, connected_address, *args):
    """
    Set the email for a logged-in merchant.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        args[0]: The new email of the merchant

    Return:
        [reply_message]
    """
    result = session.query(Merchant).filter(
        Merchant.connected_address == connected_address).first()
    if result:
        result.set_email(args[0])
        msg = _("Email has been set")
        reply = str(request_id) + " 200 OK: " + msg
        return [reply]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


def set_merchant_description(
        request_id, connected_address, *args):
    """
    Set the description for a logged-in merchant.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        args[0]: The new description of the merchant

    Return:
        [reply_message]
    """
    result = session.query(Merchant).filter(
        Merchant.connected_address == connected_address).first()
    if result:
        result.set_description(args[0])
        msg = _("Description has been set")
        reply = str(request_id) + " 200 OK: " + msg
        return [reply]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


def set_merchant_password(request_id, connected_address, *args):
    """
    Set a new password for the merchant if the current password is verified.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        args[0]: The new password.
        args[1]: The current password for verification.

    Return:
        [reply_message]
    """
    result = session.query(Merchant).filter(
        Merchant.connected_address == connected_address).first()
    if result:
        if result.verify_password(args[1]):
            result.set_password(args[0], args[1])
            msg = _("New password has been set")
            reply = str(request_id) + " 200 OK: " + msg
            return [reply]
        else:
            msg = _("The password of the merchant is incorrect")
            reply = str(request_id) + " 403 Forbidden: " + msg
            return [reply]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


def merchant_add_product(request_id, connected_address, *args):
    """
    Add a new product to the merchant's product list.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        args[0]: The name of the new product.
        args[1]: The price of the new product.
        args[2]: The description of the new product.

    Return:
        [reply_message]
    """
    result = session.query(Merchant).filter(
        Merchant.connected_address == connected_address).first()
    if result:
        result.add_product(args[0], args[1], args[2])
        msg = _("This product has been added to the product list")
        reply = str(request_id) + " 200 OK: " + msg
        return [reply]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


def merchant_del_product(request_id, connected_address, *args):
    """
    Delete a product from the merchant's product list.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        args[0]: The productId of the product to be deleted.

    Return:
        [reply_message]
    """
    result = session.query(Merchant).filter(
        Merchant.connected_address == connected_address).first()
    if result:
        result.del_product(args[0])
        msg = _("This product has been deleted from the product list")
        reply = str(request_id) + " 200 OK: " + msg
        return [reply]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


def merchant_restock_product(
        request_id, connected_address, *args):
    """
    Restock a product in the merchant's inventory.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        args[0]: The productId of the product to be restocked.
        args[1]: Quantity of restocking product.

    Return:
        [reply_message]
    """
    result = session.query(Merchant).filter(
        Merchant.connected_address == connected_address).first()
    product = session.query(Product).filter(
        Product.productId == args[0]).first()
    if result:
        if product and product.merchant_id == result.merchantId:
            product.restock(int(args[1]))
            msg = _("This product has been restock")
            reply = str(request_id) + " 200 OK: " + msg
            return [reply]
        else:
            msg = _("You are restocking an item that is not from this store")
            reply = str(request_id) + " 400 Bad Request: " + msg
            return [reply]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


def merchant_get_profit(request_id, connected_address, *args):
    """
    Retrieve the total profit for the merchant.

    Args:
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        *args: Variable length argument list: Do not require

    Return:
        [reply_message, total_profit]
        total_profit (float): This merchant's total profit
    """
    result = session.query(Merchant).filter(
        Merchant.connected_address == connected_address).first()
    if result:
        msg = _("Your total profit has been obtained")
        reply = str(request_id) + " 200 OK: " + msg
        return [reply, result.get_profit()]
    else:
        msg = _("You have not logged in or your login has timed out")
        reply = str(request_id) + " 401 Unauthorized: " + msg
        return [reply]


function_dict = {
    "CLIENT_CREATE": client_create,
    "CLIENT_LOGIN": client_login,
    "CLIENT_LOGOUT": client_logout,
    "SET_CLIENT_USERNAME": set_client_username,
    "SET_CLIENT_EMAIL": set_client_email,
    "SET_CLIENT_PASSWORD": set_client_password,
    "CLIENT_ADD_ITEM": client_add_item,
    "CLIENT_REMOVE_ITEM": client_remove_item,
    "CLIENT_GET_ITEMS": client_get_items,
    "CLIENT_GET_PRICE": client_get_price,
    "CLIENT_CHECKOUT_ITEM": client_checkout_item,
    "LIST_MERCHANT": list_merchant,
    "LIST_PRODUCT": list_product,
    "MERCHANT_CREATE_IVITATION": merchant_create_ivitation,
    "MERCHANT_CREATE": merchant_create,
    "MERCHANT_LOGIN": merchant_login,
    "MERCHANT_LOGOUT": merchant_logout,
    "SET_MERCHANT_STORENAME": set_merchant_storename,
    "SET_MERCHANT_EMAIL": set_merchant_email,
    "SET_MERCHANT_DESCRIPTION": set_merchant_description,
    "SET_MERCHANT_PASSWORD": set_merchant_password,
    "MERCHANT_ADD_PRODUCT": merchant_add_product,
    "MERCHANT_DEL_PRODUCT": merchant_del_product,
    "MERCHANT_RESTOCK_PRODUCT": merchant_restock_product,
    "MERCHANT_GET_PROFIT": merchant_get_profit
}


def cmd_process(cmd, request_id, connected_address, *args):
    """
    Execute the corresponding function from the function dictionary.

    Parameters:
        cmd (str): The command to be processed.
        request_id (str): The unique identifier for the request.
        connected_address (str): The address of the client making the request.
        output (queue): The output queue where the response will be put.
        args: Additional arguments that may be required by the function.

    If the command is found in the function dictionary, the corresponding
    function is called with the provided arguments.
    If the command is not found, a "400 Bad Request" error message is returned.

    Return:
        reply (list): List with prompt information and query results
    """
    func = function_dict.get(cmd)
    if func:
        reply = func(request_id, connected_address, *args)
        return reply
    else:
        msg = _("You are trying to call an undefined method")
        reply = str(request_id) + " 400 Bad Request: " + msg
        return [reply]
