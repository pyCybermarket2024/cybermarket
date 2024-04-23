from sqlalchemy import Column, Integer, String, Float, ForeignKey
from setting import engine, Base, session
from sqlalchemy.orm import relationship


class InventoryShortage(Exception):
    """
    The `InventoryShortage` class is a custom exception class that inherits
    from the built-in `Exception` class in Python. It is designed to be raised
    when there is a shortage of inventory in a system that requires a specific
    quantity of items.

    Attributes:
        message (str): A string describing the shortage situation.

    Methods:
        __init__(self, message):
            The constructor for the `InventoryShortage` class.
            It takes a single argument, `message`, which is a string
            that describes the shortage situation. This message is then stored
            in the instance attribute `message`.

        __str__(self):
            The string representation method for the `InventoryShortage` class.
            It returns the `message` attribute, allowing the exception
            to be printed directly or converted to a string,
            which will display the message describing the inventory shortage.

    """
    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message


class Client(Base):
    '''
    Client class, corresponds to the 'client' table in the database.

    Contains fields such as client ID, username, email, password,
    connected address, etc.

    Associated with the Order class through a relationship.

    Provides methods for getting and setting usernames, emails, passwords,
    as well as methods for login, logout, adding products, removing products,
    retrieving product lists, calculating prices, and checking out.
    '''
    __tablename__ = 'client'
    clientId = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String)
    password = Column(String)
    connected_address = Column(String, default=None)
    order = relationship("Order", backref="client")

    def __repr__(self):
        return f'''
            username: {self.username}
            email: {self.email}
        '''

    def get_username(self):
        return self.username

    def set_username(self, new_username):
        self.username = new_username
        session.commit()

    def get_email(self):
        return self.email

    def set_email(self, new_email):
        self.email = new_email
        session.commit()

    def verify_password(self, password):
        '''
        Verifies the provided password against the client's stored password.

        Parameters:
            password (str): The password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        '''
        return self.password == password

    def set_password(self, new_password, old_password):
        '''
        Sets a new password for the client after verifying the old password.

        Parameters:
            new_password (str): The new password to set.
            old_password (str): The current password for verification.

        Returns:
            bool: True if the password was successfully changed,
            False otherwise.
        '''
        if self.password == old_password:
            self.password = new_password
            session.commit()
            return True
        return False

    def client_login(self, password, connected_address):
        '''
        Logs the client in by setting their connected address,
        after verifying their password.

        Parameters:
            password (str): The client's password for verification.
            connected_address (str): The address to set as connected.
        '''
        if self.verify_password(password):
            self.connected_address = connected_address
            session.commit()

    def client_logout(self):
        '''
        Logs the client out by clearing their connected address.
        '''
        self.connected_address = None
        session.commit()

    def add_item(self, product_id, quantity):
        '''
        Adds a specified quantity of a product to the client's order.
        If the product is already in the order, increases the quantity.

        Parameters:
            product_id (int): The ID of the product to add.
            quantity (int): The quantity of the product to add.
        '''
        result = session.query(Order).filter(
            Order.client_id == self.clientId,
            Order.product_id == product_id
            ).first()
        if result:
            result.quantity += quantity
            session.commit()
        else:
            new_item = Order(
                client_id=self.clientId,
                quantity=quantity,
                product_id=product_id
                )
            session.add(new_item)
            session.commit()

    def remove_item(self, product_id):
        '''
        Removes a product from the client's order.

        Parameters:
            product_id (int): The ID of the product to remove.
        '''
        result = session.query(Order).filter(
            Order.client_id == self.clientId,
            Order.product_id == product_id
            ).first()
        session.delete(result)
        session.commit()

    def get_items(self):
        '''
        Retrieves all items in the client's basket.

        Returns:
            list: A list of tuples containing store name, product name, price,
            and quantity of each item.
        '''
        result = session.query(
            Merchant.storename,
            Product.productname,
            Product.price,
            Order.quantity
            ).join(
                Product, Order.product_id == Product.productId
            ).join(
                Merchant, Product.merchant_id == Merchant.merchantId
            ).filter(
                Order.client_id == self.clientId
            ).all()
        return result

    def get_price(self):
        '''
        Calculates the total price of all items in the client's basket.
        Returns:
            float: The total price of the items.
        '''
        sum_price = 0
        item_list = self.get_items()
        for item in item_list:
            sum_price += item[2]*item[3]
        return sum_price

    def checkout_item(self):
        '''
        Checks out all items in the client's basket, finalizing the order.
        '''
        for item in self.order:
            if item.quantity < item.product.stock:
                item.checkout()
                session.delete(item)
                session.commit()
            else:
                raise InventoryShortage(
                    "Inventory shortage for product "
                    + "{} from merchant {},".format(
                        item.product.productname,
                        item.product.merchant.storename
                        )
                    + " checkout was not fully executed "
                    + "and this item is still in your cart")


class Order(Base):
    '''
    Order class, corresponds to the 'order' table in the database.

    Contains fields such as order ID, client ID, product ID, quantity, etc.

    Associated with the Product class through a relationship.

    Provides methods for setting and getting quantities,
    as well as a method for checking out the current item.
    '''
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.clientId'))
    product_id = Column(Integer, ForeignKey('product.productId'))
    quantity = Column(Integer)
    product = relationship("Product")

    def set_quantity(self, new_quantity):
        self.quantity = new_quantity
        session.commit()

    def get_quantity(self):
        return self.quantity

    def checkout(self):
        '''
        Checks out the current item, calling the purchase method of
        the Product class to proceed with the purchase.
        '''
        self.product.purchase(self.quantity)


class Product(Base):
    '''
    Product class, corresponds to the 'product' table in the database.

    Contains fields such as product ID, product name, price, stock,
    description, merchant ID, etc.

    Provides methods for getting and setting product names, prices,
    descriptions, as well as methods for restocking and purchasing.
    '''
    __tablename__ = 'product'
    productId = Column(Integer, primary_key=True)
    productname = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    description = Column(String)
    merchant_id = Column(Integer, ForeignKey('merchant.merchantId'))

    def __repr__(self):
        return f'''
            productname: {self.productname}
            price: {self.price}
            stock: {self.stock}
            description: {self.description}
        '''

    def get_productname(self):
        return self.productname

    def set_productname(self, new_productname):
        self.productname = new_productname
        session.commit()

    def get_price(self):
        return self.price

    def set_price(self, new_price):
        self.price = new_price
        session.commit()

    def get_description(self):
        return self.description

    def set_description(self, new_description):
        self.price = new_description
        session.commit()

    def restock(self, quantity):
        '''
        Restocks the product by adding the specified quantity to the current
        stock.

        Parameters:
            quantity (int): The quantity to be added to the stock.
        '''
        self.stock += quantity
        session.commit()

    def purchase(self, quantity):
        '''
        Processes the purchase of the specified quantity of the product,
        reducing the stock and increasing the merchant's profit accordingly.

        Parameters:
            quantity (int): The quantity of the product to be purchased.
        '''
        self.stock -= quantity
        self.merchant.profit += self.price*quantity
        session.commit()


class Merchant(Base):
    '''
    Merchant class, corresponds to the 'merchant' table in the database.

    Contains fields such as merchant ID, store name, description, email,
    password, connected address, profit, etc.

    Associated with the Product class through a relationship.

    Provides methods for getting and setting store names, descriptions, emails,
    passwords, as well as methods for login, logout, retrieving product lists,
    adding products, and deleting products.
    '''
    __tablename__ = 'merchant'
    merchantId = Column(Integer, primary_key=True)
    storename = Column(String, unique=True)
    description = Column(String)
    email = Column(String)
    password = Column(String)
    connected_address = Column(String, default=None)
    profit = Column(Float, default=0.0)
    product = relationship("Product", backref="merchant")

    def __repr__(self):
        return f'''
            storename: {self.storename}
            description: {self.description}
            email: {self.email}
            profit: {self.profit}
        '''

    def get_storename(self):
        return self.storename

    def set_storename(self, new_storename):
        self.storename = new_storename
        session.commit()

    def get_description(self):
        return self.storename

    def set_description(self, new_storename):
        self.storename = new_storename
        session.commit()

    def get_email(self):
        return self.email

    def set_email(self, new_email):
        self.email = new_email
        session.commit()

    def verify_password(self, password):
        '''
        Verifies the provided password against the merchant's stored password.

        Parameters:
            password (str): The password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        '''
        return self.password == password

    def set_password(self, new_password, old_password):
        '''
        Sets a new password for the merchant after verifying the old password.

        Parameters:
            new_password (str): The new password to set.
            old_password (str): The current password for verification.

        Returns:
            bool: True if the password was successfully changed,
            False otherwise.
        '''
        if self.password == old_password:
            self.password = new_password
            session.commit()
            return True
        return False

    def merchant_login(self, password, connect):
        '''
        Logs the merchant in by setting their connected address,
        after verifying their password.

        Parameters:
            password (str): The merchant's password for verification.
            connected_address (str): The address to set as connected.
        '''
        if self.verify_password(password):
            self.connected_address = connect
            session.commit()

    def merchant_logout(self):
        '''
        Logs the merchant out by clearing their connected address.
        '''
        self.connected_address = None
        session.commit()

    def get_product_list(self):
        '''
        Retrieves a list of products associated with this merchant.

        Returns:
            list: A list of Product objects.
        '''
        return self.product

    def add_product(self, productname, price, description):
        '''
        Creates a new product in the 'product' table.

        Parameters:
            productname (str): The name of the new product.
            price (float): The price of the new product.
            description (str): The description of the new product.
        '''
        new_product = Product(
            productname=productname,
            price=price,
            stock=0,
            description=description,
            merchant_id=self.merchantId
            )
        session.add(new_product)
        session.commit()

    def del_product(self, id):
        '''
        Deletes a product by its ID from the 'product' table.

        Parameters:
            product_id (int): The ID of the product to delete.
        '''
        result = session.query(Product).filter(Product.productId == id).first()
        session.delete(result)
        session.commit()


# Create the corresponding Tabel in database
Base.metadata.create_all(engine)
session.close()
