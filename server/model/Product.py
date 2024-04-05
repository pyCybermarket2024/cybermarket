from sqlalchemy import Column, Integer, String, Float, ForeignKey
from server.config.setting import engine, Base, session


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


# Create the corresponding Tabel in database
Base.metadata.create_all(engine)
