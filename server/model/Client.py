from sqlalchemy import Column, Integer, String
from server.config.setting import engine, Base, session
from sqlalchemy.orm import relationship
from Order import Order


class Client(Base):
    '''
        Client class, corresponds the table client in database
    '''
    __tablename__ = 'client'
    clientId = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
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


# Create the corresponding Tabel in database
Base.metadata.create_all(engine)
