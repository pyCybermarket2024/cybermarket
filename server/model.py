"""Contain classes associated with database tables, and exception classes."""
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from setting import engine, Base, session
from sqlalchemy.orm import relationship


class InventoryShortage(Exception):
    """
    Raise when there is a shortage of inventory that requires items.

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
        """
        Initialize the InventoryShortage exception with a message.

        Args:
            message (str): A description of the shortage situation.
        """
        super().__init__()
        self.message = message

    def __str__(self):
        """
        Return the string representation of the InventoryShortage exception.

        Returns:
            str: The message describing the inventory shortage.
        """
        return self.message


class Client(Base):
    """
    Client class, corresponds to the 'client' table in the database.

    Contains fields such as client ID, username, email, password,
    connected address, etc.

    Associated with the Order class through a relationship.

    Provides methods for getting and setting usernames, emails, passwords,
    as well as methods for login, logout, adding products, removing products,
    retrieving product lists, calculating prices, and checking out.
    """

    __tablename__ = 'client'
    clientId = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String)
    password = Column(String)
    connected_address = Column(String, default=None)
    order = relationship("Order", backref="client")

    def __repr__(self):
        """Return a string representation of the client."""
        return f'''
            username: {self.username}
            email: {self.email}
        '''

    def get_username(self):
        """Return the username of the client."""
        return self.username

    def set_username(self, new_username):
        """
        Set a new username for the client.

        Args:
            new_username (str): The new username to be set for the client.
        """
        self.username = new_username
        session.commit()

    def get_email(self):
        """Return the email of the client."""
        return self.email

    def set_email(self, new_email):
        """
        Set a new email for the client.

        Args:
            new_email (str): The new email to be set for the client.
        """
        self.email = new_email
        session.commit()

    def verify_password(self, password):
        """
        Verify the provided password against the client's stored password.

        Parameters:
            password (str): The password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return self.password == password

    def set_password(self, new_password, old_password):
        """
        Set a new password for the client after verifying the old password.

        Parameters:
            new_password (str): The new password to set.
            old_password (str): The current password for verification.

        Returns:
            bool: True if the password was successfully changed,
            False otherwise.
        """
        if self.password == old_password:
            self.password = new_password
            session.commit()
            return True
        return False

    def client_login(self, password, connected_address):
        """
        Log the client in by setting connected address, verifying the password.

        Parameters:
            password (str): The client's password for verification.
            connected_address (str): The address to set as connected.
        """
        if self.verify_password(password):
            self.connected_address = connected_address
            session.commit()

    def client_logout(self):
        """Log the client out by clearing their connected address."""
        self.connected_address = None
        session.commit()

    def add_item(self, product_id, quantity):
        """
        Add or increase quantity of product to the order.

        Parameters:
            product_id (int): The ID of the product to add.
            quantity (int): The quantity of the product to add.
        """
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
        """
        Remove a product from the client's order.

        Parameters:
            product_id (int): The ID of the product to remove.
        """
        result = session.query(Order).filter(
            Order.client_id == self.clientId,
            Order.product_id == product_id
            ).first()
        session.delete(result)
        session.commit()

    def get_items(self):
        """
        Retrieve all items in the client's basket.

        Returns:
            list: A list of tuples containing store name, product name, price,
            and quantity of each item.
        """
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
        """
        Calculate the total price of all items in the client's basket.

        Returns:
            float: The total price of the items.
        """
        sum_price = 0
        item_list = self.get_items()
        for item in item_list:
            sum_price += item[2]*item[3]
        return sum_price

    def checkout_item(self):
        """Check out all items in the client's basket, finalizing the order."""
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
    """
    Order class, corresponds to the 'order' table in the database.

    Contain fields such as order ID, client ID, product ID, quantity, etc.

    Associate with the Product class through a relationship.

    Provide methods for setting and getting quantities,
    as well as a method for checking out the current item.
    """

    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.clientId'))
    product_id = Column(Integer, ForeignKey('product.productId'))
    quantity = Column(Integer)
    product = relationship("Product")

    def set_quantity(self, new_quantity):
        """
        Set quantity for the order.

        Args:
            new_quantity (int): The quantity to be set for the order.
        """
        self.quantity = new_quantity
        session.commit()

    def get_quantity(self):
        """Get quantity for the order."""
        return self.quantity

    def checkout(self):
        """Check out the current item, by the purchase method to purchase."""
        self.product.purchase(self.quantity)


class Product(Base):
    """
    Product class, corresponds to the 'product' table in the database.

    Contain fields such as product ID, product name, price, stock,
    description, merchant ID, etc.

    Provide methods for getting and setting product names, prices,
    descriptions, as well as methods for restocking and purchasing.
    """

    __tablename__ = 'product'
    productId = Column(Integer, primary_key=True)
    productname = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    description = Column(String)
    merchant_id = Column(Integer, ForeignKey('merchant.merchantId'))

    def __repr__(self):
        """
        Represent the Product instance as a string.

        Returns:
            str: A string representation of the product with its ID,
            store name, product name, description, price, and stock.
        """
        return f'''
            product_id: {self.productId}
            storename: {self.merchant.storename}
            productname: {self.productname}
            description: {self.description}
            price: {self.price}
            stock: {self.stock}
        '''

    def get_productname(self):
        """Get the name of the product."""
        return self.productname

    def set_productname(self, new_productname):
        """
        Set a new name for the product.

        Args:
            new_productname (str): The new name to be set for the product.
        """
        self.productname = new_productname
        session.commit()

    def get_price(self):
        """
        Get the price of the product.

        Returns:
            float: The price of the product.
        """
        return self.price

    def set_price(self, new_price):
        """
        Set a new price for the product.

        Args:
            new_price (float): The new price to be set for the product.
        """
        self.price = new_price
        session.commit()

    def get_description(self):
        """
        Get the description of the product.

        Returns:
            str: The description of the product.
        """
        return self.description

    def set_description(self, new_description):
        """
        Set a new description for the product.

        Args:
            new_description (str): The new description to be set for the
            product.
        """
        self.description = new_description
        session.commit()

    def restock(self, quantity):
        """
        Restock the product.

        Parameters:
            quantity (int): The quantity to be added to the stock.
        """
        self.stock += quantity
        session.commit()

    def purchase(self, quantity):
        """
        Process the purchase, reduce the stock and increase the profit.

        Parameters:
            quantity (int): The quantity of the product to be purchased.
        """
        self.stock -= quantity
        self.merchant.profit += self.price*quantity
        session.commit()


class Merchant(Base):
    """
    Merchant class, corresponds to the 'merchant' table in the database.

    Contain fields such as merchant ID, store name, description, email,
    password, connected address, profit, etc.

    Associate with the Product class through a relationship.

    Provide methods for getting and setting store names, descriptions, emails,
    passwords, as well as methods for login, logout, retrieving product lists,
    adding products, and deleting products.
    """

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
        """
        Represent the Merchant instance as a string.

        Returns:
            str: A string containing the store name, description, and email.
        """
        return f'''
            storename: {self.storename}
            description: {self.description}
            email: {self.email}
        '''

    def get_storename(self):
        """
        Get the store name of the merchant.

        Returns:
            str: The store name.
        """
        return self.storename

    def set_storename(self, new_storename):
        """
        Set a new store name for the merchant.

        Args:
            new_storename (str): The new store name to be set.

        """
        self.storename = new_storename
        session.commit()

    def get_description(self):
        """
        Get the description of the merchant's store.

        Returns:
            str: The store description.
        """
        return self.description

    def set_description(self, new_description):
        """
        Set a new description for the merchant's store.

        Args:
            new_description (str): The new description to be set.

        """
        self.description = new_description
        session.commit()

    def get_email(self):
        """
        Get the email of the merchant.

        Returns:
            str: The merchant's email.
        """
        return self.email

    def set_email(self, new_email):
        """
        Set a new email for the merchant.

        Args:
            new_email (str): The new email to be set.

        """
        self.email = new_email
        session.commit()

    def get_profit(self):
        """
        Get the current profit of the merchant.

        Returns:
            float: The current profit.
        """
        return self.profit

    def verify_password(self, password):
        """
        Verify the provided password against the merchant's stored password.

        Parameters:
            password (str): The password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return self.password == password

    def set_password(self, new_password, old_password):
        """
        Set a new password for the merchant after verifying the old password.

        Parameters:
            new_password (str): The new password to set.
            old_password (str): The current password for verification.

        Returns:
            bool: True if the password was successfully changed,
            False otherwise.
        """
        if self.password == old_password:
            self.password = new_password
            session.commit()
            return True
        return False

    def merchant_login(self, password, connect):
        """
        Log the merchant in by connected address and verifying their password.

        Parameters:
            password (str): The merchant's password for verification.
            connected_address (str): The address to set as connected.
        """
        if self.verify_password(password):
            self.connected_address = connect
            session.commit()

    def merchant_logout(self):
        """Log the merchant out by clearing their connected address."""
        self.connected_address = None
        session.commit()

    def get_product_list(self):
        """
        Retrieve a list of products associated with this merchant.

        Returns:
            list: A list of Product objects.
        """
        return self.product

    def add_product(self, productname, price, description):
        """
        Create a new product in the 'product' table.

        Parameters:
            productname (str): The name of the new product.
            price (float): The price of the new product.
            description (str): The description of the new product.
        """
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
        """
        Delete a product by its ID from the 'product' table.

        Parameters:
            product_id (int): The ID of the product to delete.
        """
        result = session.query(Product).filter(Product.productId == id).first()
        session.delete(result)
        session.commit()


# Create the corresponding Tabel in database
Base.metadata.create_all(engine)
session.close()
