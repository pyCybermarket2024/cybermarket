from model import Merchant, Client, Order, Product
from setting import session


async def user_create(request_id, connected_address, output, *args):
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
    result = session.query(Client).filter(Client.username == args[0]).first()
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
    result = session.query(Client).filter(
        Client.connected_address == connected_address).first()
    if result:
        result.checkout_item()
        msg = "Order has been checked out"
        repeat = str(request_id) + " 200 OK: " + msg
        await output.put([repeat])
    else:
        msg = "You have not logged in or your login has timed out"
        repeat = str(request_id) + " 401 Unauthorized: " + msg
        await output.put([repeat])


async def list_merchant(request_id, connected_address, output, *args):
    result = session.query(Merchant).all()
    repeat = str(request_id) + " 200 OK"
    await output.put([repeat, result])


async def list_product(request_id, connected_address, output, *args):
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


function_dict = {
    "USER_CREATE": user_create,
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
}


async def cmd_process(cmd, request_id, connected_address, output, *args):
    func = function_dict.get(cmd)
    if func:
        await func(request_id, connected_address, output, *args)
    else:
        msg = "The method you are trying to call is not defined by the server"
        await output.put(str(request_id) + " 400 Bad Request: " + msg)
