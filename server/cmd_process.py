from model import Merchant, Client, Order, Product
from model import InventoryShortage
from invitation import create_ivitation, check_ivitation
from setting import session


async def client_create(request_id, connected_address, output, *args):
    """
    Creates a new client with the provided username, email, and password.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list:
            args[0]: The username of new client
            args[1]: The email of new client
            args[2]: The password of new merchant

    Reply:
        [reply_message]
    """
    if session.query(Client).filter(Client.username == args[0]).first():
        msg = "This username is occupied"
        repeat = str(request_id) + " 409 Conflict:  " + msg
        await output.put([repeat])
    else:
        client = Client(username=args[0], email=args[1], password=args[2])
        session.add(client)
        session.commit()
        repeat = str(request_id) + " 201 Created"
        await output.put([repeat])


async def set_client_username(request_id, connected_address, output, *args):
    """
    Sets the username for a logged-in client.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list:
            args[0]: The new username of the client

    Reply:
        [reply_message]
    """
    result = session.query(Client).filter(
        Client.connected_address == connected_address).first()
    if result:
        result.set_username(args[0])
        msg = "Username has been set"
        repeat = str(request_id) + " 200 OK: " + msg
        await output.put([repeat])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def set_client_email(request_id, connected_address, output, *args):
    """
    Sets the email for a logged-in client.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list:
            args[0]: The new email of the client

    Reply:
        [reply_message]
    """
    result = session.query(Client).filter(
        Client.connected_address == connected_address).first()
    if result:
        result.set_email(args[0])
        msg = "Email has been set"
        repeat = str(request_id) + " 200 OK: " + msg
        await output.put([repeat])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def set_client_password(request_id, connected_address, output, *args):
    """
    Sets a new password for the client if the current password is verified.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list:
            args[0]: The new password.
            args[1]: The current password for verification.

    Reply:
        [reply_message]
    """
    result = session.query(Client).filter(
        Client.connected_address == connected_address).first()
    if result:
        if result.verify_password(args[1]):
            result.set_password(args[0], args[1])
            msg = "New password has been set"
            repeat = str(request_id) + " 200 OK: " + msg
            await output.put([repeat])
        else:
            msg = "The password of the user is incorrect"
            repeat = str(request_id) + " 403 Forbidden: " + msg
            await output.put([repeat])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def client_login(request_id, connected_address, output, *args):
    """
    Logs in a client if the credentials are correct and the client
    is not already logged in.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list:
            args[0]: The storename or email of the client
            args[1]: The password of the client

    Reply:
        [reply_message]
    """
    result = session.query(Client).filter(
        (Client.username == args[0]) | (Client.email == args[0])
        ).first()
    login_status = session.query(Client.connected_address).filter(
        Client.connected_address == connected_address).first()
    if login_status:
        msg = "The user has been logged in, please do not log in again"
        repeat = str(request_id) + " 400 Bad Request: " + msg
        await output.put([repeat])
    elif result:
        if result.verify_password(args[1]):
            result.client_login(args[1], connected_address)
            msg = "This user is logged in"
            repeat = str(request_id) + " 200 OK: " + msg
            await output.put([repeat])
        else:
            msg = "The password of the user is incorrect"
            repeat = str(request_id) + " 403 Forbidden: " + msg
            await output.put([repeat])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def client_logout(request_id, connected_address, output, *args):
    """
    Logs out a client if they are currently logged in.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list: This function
        do not require additional parameters

    Reply:
        [reply_message]
    """
    result = session.query(Client).filter(
        Client.connected_address == connected_address).first()
    if result:
        result.client_logout()
        msg = "You have successfully logged out"
        repeat = str(request_id) + " 200 OK: " + msg
        await output.put([repeat])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def client_add_item(request_id, connected_address, output, *args):
    """
    Adds an item to the client's shopping cart.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list:
            args[0]: The id of the product to add
            args[1]: The quantity of the product to add

    Reply:
        [reply_message]
    """
    result = session.query(Client).filter(
        Client.connected_address == connected_address).first()
    product = session.query(Product).filter(
        Product.productId == args[0]).first()
    if int(args[1]) <= 0:
        msg = "The quantity of added products should be a positive integer"
        repeat = str(request_id) + " 400 Bad Request: " + msg
        await output.put([repeat])
    elif not product:
        msg = "The product you are trying to add cannot be found"
        repeat = str(request_id) + " 404 Not Found: " + msg
        await output.put([repeat])
    elif result:
        result.add_item(args[0], int(args[1]))
        msg = "This product has been added to the shopping cart"
        repeat = str(request_id) + " 200 OK: " + msg
        await output.put([repeat])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def client_remove_item(request_id, connected_address, output, *args):
    """
    Removes an item from the client's shopping cart.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list:
            args[0]: The id of the product to remove

    Reply:
        [reply_message]
    """
    result = session.query(Client).filter(
        Client.connected_address == connected_address).first()
    product = session.query(Order).filter(
            Order.product_id == args[0]
            ).first()
    if not product:
        msg = "This product is not in your shopping cart"
        repeat = str(request_id) + " 404 Not Found: " + msg
        await output.put([repeat])
    elif result:
        result.remove_item(args[0])
        msg = "This product has been removed from the shopping cart"
        repeat = str(request_id) + " 200 OK: " + msg
        await output.put([repeat])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def client_get_items(request_id, connected_address, output, *args):
    """
    Retrieves the list of items in the client's shopping cart.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list: This function
        do not require additional parameters

    Reply:
        [reply_message, item_list]
        item_list: A list of all items in the shopping cart
    """
    result = session.query(Client).filter(
        Client.connected_address == connected_address).first()
    if result:
        msg = "Obtained order list"
        repeat = str(request_id) + " 200 OK: " + msg
        await output.put([repeat, result.get_items()])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def client_get_price(request_id, connected_address, output, *args):
    """
    Calculates the total price of the items in the client's shopping cart.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list: This function
        do not require additional parameters

    Reply:
        [reply_message, total_price]
        total_price: The price all items in the shopping cart
    """
    result = session.query(Client).filter(
        Client.connected_address == connected_address).first()
    if result:
        msg = "Order price obtained"
        repeat = str(request_id) + " 200 OK: " + msg
        await output.put([repeat, result.get_price()])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def client_checkout_item(request_id, connected_address, output, *args):
    """
    Checks out the items in the client's shopping cart.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list: This function
        do not require additional parameters

    Reply:
        [reply_message]
    """
    result = session.query(Client).filter(
        Client.connected_address == connected_address).first()
    if result:
        try:
            result.checkout_item()
            msg = "Order has been checked out"
            repeat = str(request_id) + " 200 OK: " + msg
            await output.put([repeat])
        except InventoryShortage as error:
            msg = str(error)
            repeat = str(request_id) + " 400 Bad Request: " + msg
            await output.put([repeat])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def list_merchant(request_id, connected_address, output, *args):
    """
    Retrieves a list of all merchants from the database.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list: This function
        do not require additional parameters

    Reply:
        [reply_message, merchant_list]
        merchant_list: list of all merchants
    """
    result = session.query(Merchant).all()
    repeat = str(request_id) + " 200 OK"
    await output.put([repeat, result])


async def list_product(request_id, connected_address, output, *args):
    """
    Retrieves a list of products from a specific merchant identified
    by the store name.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list:
            args[0]: Storename of the merchant

    Reply:
        [reply_message, product_list]
        product_list: A list of all products from the merchant
    """
    result = session.query(Merchant).filter(
        Merchant.storename == args[0]).first()
    if result:
        msg = "Product list has been obtained"
        repeat = str(request_id) + " 200 OK: " + msg
        await output.put([repeat, result.get_product_list()])
    else:
        msg = "No store with this name found"
        repeat = str(request_id) + " 404 Not Found: " + msg
        await output.put([repeat])


async def merchant_create_ivitation(
        request_id, connected_address, output, *args):
    """
    Generates an invitation code for a merchant if they are connected.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list: This function
        do not require additional parameters

    Reply:
        [reply_message, invitation_code]
        invitation_code (str): Alphanumeric string of length 12.
    """
    result = session.query(Merchant).filter(
        Merchant.connected_address == connected_address).first()
    if result:
        msg = "Invitation code has been generated"
        repeat = str(request_id) + " 200 OK: " + msg
        await output.put([repeat, create_ivitation(result.storename)])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def merchant_create(request_id, connected_address, output, *args):
    """
    Creates a new merchant record if the invitation code is verified
    and the store name is not occupied.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list:
            args[0]: The storename of new merchant
            args[1]: The description of new merchant
            args[2]: The email of new merchant
            args[3]: The password of new merchant
            args[4]: The storename of the store, who is inviting
            args[5]: The invitation code

    Reply:
        [reply_message]
    """
    if check_ivitation(args[4], args[5]):
        if session.query(Merchant).filter(
                Merchant.storename == args[0]).first():
            msg = "This storename is occupied"
            repeat = str(request_id) + " 409 Conflict:  " + msg
            await output.put([repeat])
        else:
            merchant = Merchant(
                storename=args[0],
                description=args[1],
                email=args[2],
                password=args[3]
                )
            session.add(merchant)
            session.commit()
            repeat = str(request_id) + " 201 Created"
            await output.put([repeat])
    else:
        msg = "Your invitation code cannot be verified."
        + " This invitation code may be wrong or has already been used."
        + " Please contact other merchants to request the invitation code."
        repeat = str(request_id) + " 406 Not Acceptable:  " + msg
        await output.put([repeat])


async def merchant_login(request_id, connected_address, output, *args):
    """
    Logs in a merchant if the credentials are correct and the merchant
    is not already logged in.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list:
            args[0]: The storename or email of the merchant
            args[1]: The password of the merchant

    Reply:
        [reply_message]
    """
    result = session.query(Merchant).filter(
        (Merchant.storename == args[0]) | (Merchant.email == args[0])
        ).first()
    login_status = session.query(Merchant.connected_address).filter(
        Merchant.connected_address == connected_address).first()
    if login_status:
        msg = "The merchant has been logged in, please do not log in again"
        repeat = str(request_id) + " 400 Bad Request: " + msg
        await output.put([repeat])
    elif result:
        if result.verify_password(args[1]):
            result.merchant_login(args[1], connected_address)
            msg = "This merchant is logged in"
            repeat = str(request_id) + " 200 OK: " + msg
            await output.put([repeat])
        else:
            msg = "The password of the merchant is incorrect"
            repeat = str(request_id) + " 403 Forbidden: " + msg
            await output.put([repeat])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def merchant_logout(request_id, connected_address, output, *args):
    """
    Logs out a merchant if they are currently logged in.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list: This function
        do not require additional parameters

    Reply:
        [reply_message]
    """
    result = session.query(Merchant).filter(
        Merchant.connected_address == connected_address).first()
    if result:
        result.merchant_logout()
        msg = "You have successfully logged out"
        repeat = str(request_id) + " 200 OK: " + msg
        await output.put([repeat])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def set_merchant_storename(request_id, connected_address, output, *args):
    """
    Sets the store name for a logged-in merchant.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list:
            args[0]: The new storename of the merchant

    Reply:
        [reply_message]
    """
    result = session.query(Merchant).filter(
        Merchant.connected_address == connected_address).first()
    if result:
        result.set_storename(args[0])
        msg = "Storename has been set"
        repeat = str(request_id) + " 200 OK: " + msg
        await output.put([repeat])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def set_merchant_email(request_id, connected_address, output, *args):
    """
    Sets the email for a logged-in merchant.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list:
            args[0]: The new email of the merchant

    Reply:
        [reply_message]
    """
    result = session.query(Merchant).filter(
        Merchant.connected_address == connected_address).first()
    if result:
        result.set_email(args[0])
        msg = "Email has been set"
        repeat = str(request_id) + " 200 OK: " + msg
        await output.put([repeat])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def set_merchant_description(
        request_id, connected_address, output, *args):
    """
    Sets the description for a logged-in merchant.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list:
            args[0]: The new description of the merchant

    Reply:
        [reply_message]
    """
    result = session.query(Merchant).filter(
        Merchant.connected_address == connected_address).first()
    if result:
        result.set_description(args[0])
        msg = "Description has been set"
        repeat = str(request_id) + " 200 OK: " + msg
        await output.put([repeat])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def set_merchant_password(request_id, connected_address, output, *args):
    """
    Sets a new password for the merchant if the current password is verified.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list:
            args[0]: The new password.
            args[1]: The current password for verification.

    Reply:
        [reply_message]
    """
    result = session.query(Merchant).filter(
        Merchant.connected_address == connected_address).first()
    if result:
        if result.verify_password(args[1]):
            result.set_password(args[0], args[1])
            msg = "New password has been set"
            repeat = str(request_id) + " 200 OK: " + msg
            await output.put([repeat])
        else:
            msg = "The password of the merchant is incorrect"
            repeat = str(request_id) + " 403 Forbidden: " + msg
            await output.put([repeat])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def merchant_add_product(request_id, connected_address, output, *args):
    """
    Adds a new product to the merchant's product list.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list:
            args[0]: The name of the new product.
            args[1]: The price of the new product.
            args[2]: The description of the new product.

    Reply:
        [reply_message]
    """
    result = session.query(Merchant).filter(
        Merchant.connected_address == connected_address).first()
    if result:
        result.add_product(args[0], args[1], args[2])
        msg = "This product has been added to the product list"
        repeat = str(request_id) + " 200 OK: " + msg
        await output.put([repeat])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def merchant_del_product(request_id, connected_address, output, *args):
    """
    Deletes a product from the merchant's product list.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list:
            args[0]: The productId of the product to be deleted.

    Reply:
        [reply_message]
    """
    result = session.query(Merchant).filter(
        Merchant.connected_address == connected_address).first()
    if result:
        result.del_product(args[0])
        msg = "This product has been deleted from the product list"
        repeat = str(request_id) + " 200 OK: " + msg
        await output.put([repeat])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def merchant_restock_product(
        request_id, connected_address, output, *args):
    """
    Restocks a product in the merchant's inventory.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list:
            args[0]: The productId of the product to be restocked.
            args[1]: Quantity of restocking product.

    Reply:
        [reply_message]
    """
    result = session.query(Merchant).filter(
        Merchant.connected_address == connected_address).first()
    product = session.query(Product).filter(
        Product.productId == args[0]).first()
    if result:
        if product.merchant_id == result.merchantId:
            product.restock(int(args[1]))
            msg = "This product has been restock"
            repeat = str(request_id) + " 200 OK: " + msg
            await output.put([repeat])
        else:
            msg = "You are trying to restock an item that is not from"
            + "this store"
            repeat = str(request_id) + " 400 Bad Request: " + msg
            await output.put([repeat])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def merchant_get_profit(request_id, connected_address, output, *args):
    """
    Retrieves the total profit for the merchant.

    Args:
        request_id (str), connected_address (str), output (asyncio.Queue):
        Read the document of function cmd_process.cmd_process().
        *args: Variable length argument list: This function
        do not require additional parameters

    Reply:
        [reply_message, total_profit]
        total_profit (float): This merchant's total profit
    """
    result = session.query(Merchant).filter(
        Merchant.connected_address == connected_address).first()
    if result:
        msg = "Your total profit has been obtained"
        repeat = str(request_id) + " 200 OK: " + msg
        await output.put([repeat, result.get_profit()])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


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


async def cmd_process(cmd, request_id, connected_address, output, *args):
    """
    Process a command by executing the corresponding function from the
    function dictionary.

    Parameters:
    - cmd (str): The command to be processed.
    - request_id (str): The unique identifier for the request.
    - connected_address (str): The address of the client making the request.
    - output (queue): The output queue where the response will be put.
    - args: Additional arguments that may be required by the function.

    If the command is found in the function dictionary, the corresponding
    function is called with the provided arguments.
    If the command is not found, a "400 Bad Request" error message is returned.

    Returns:
    None
    """
    func = function_dict.get(cmd)
    if func:
        await func(request_id, connected_address, output, *args)
    else:
        msg = "The method you are trying to call is not defined by the server"
        await output.put(str(request_id) + " 400 Bad Request: " + msg)
