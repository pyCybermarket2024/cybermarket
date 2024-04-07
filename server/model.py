from sqlalchemy import Column, Integer, String, Float, ForeignKey
from setting import engine, Base, session
from sqlalchemy.orm import relationship


class Client(Base):
    '''
        Client class, corresponds the table client in database
    '''
    __tablename__ = 'client'
    clientId = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String)
    password = Column(String)
    connected_address = Column(String, default=None)
    order = relationship("Order", backref="client")

    # Override the repr, when calling Client item
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
        return self.password == password

    def set_password(self, new_password, old_password):
        if self.password == old_password:
            self.password = new_password
            session.commit()
            return True
        return False

    def client_login(self, password, connect):
        if self.verify_password(password):
            self.connected_address = connect
            session.commit()

    def client_logout(self):
        self.connected_address = None
        session.commit()

    def add_item(self, product_id, quantity):
        new_item = Order(
            client_id=self.clientId,
            quantity=quantity,
            product_id=product_id
            )
        session.add(new_item)
        session.commit()

    def remove_item(self, product_id):
        result = session.query(Order).filter(
            Order.product_id == product_id
            ).first()
        session.delete(result)
        session.commit()

    def get_item(self):
        '''
            return all items in the basket
        '''
        result = session.query(
            Order.product.merchant.storename,
            Order.product.productname,
            Order.product.price,
            Order.quantity
            ).filter(
            Order.client_id == self.clientId
            )
        return result

    def get_price(self):
        '''
            calculate the sum price of all all items in the basket
        '''
        sum_price = 0
        item_list = self.get_item()
        for item in item_list:
            sum_price += item[2]*item[3]
        return sum_price

    def checkout_item(self):
        '''
            checkout all items in the basket
        '''
        for item in self.order:
            item.checkout()


class Order(Base):
    '''
        Order class, corresponds the order product in database
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
            To checkout the current item
        '''
        self.product.purchase(self.quantity)


class Product(Base):
    '''
        Product class, corresponds the table product in database
    '''
    __tablename__ = 'product'
    productId = Column(Integer, primary_key=True)
    productname = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    description = Column(String)
    merchant_id = Column(Integer, ForeignKey('merchant.merchantId'))

    # Override the repr, when calling Client item
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
        self.stock += quantity
        session.commit()

    def purchase(self, quantity):
        self.stock -= quantity
        self.merchant.profit += self.price*quantity
        session.commit()


class Merchant(Base):
    '''
        Merchant class, corresponds the table merchant in database
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

    # Override the repr, when calling Client item
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
        return self.password == password

    def set_password(self, new_password, old_password):
        if self.password == old_password:
            self.password = new_password
            session.commit()
            return True
        return False

    def merchant_login(self, password, connect):
        if self.verify_password(password):
            self.connected_address = connect
            session.commit()

    def merchant_logout(self):
        self.connected_address = None
        session.commit()

    def get_product_list(self):
        '''
            return a list of products of this merchant
        '''
        return self.product

    def add_product(self, productname, price, description):
        '''
            create a new product in table product
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
            delete a product by its id in table product
        '''
        result = session.query(Product).filter(Product.productId == id).first()
        session.delete(result)
        session.commit()


Base.metadata.create_all(engine)
session.close()
# Create the corresponding Tabel in database
