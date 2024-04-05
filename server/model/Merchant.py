from sqlalchemy import Column, Integer, String
from server.config.setting import engine, Base, session
from sqlalchemy.orm import relationship
from Product import Product


class Merchant(Base):
    '''
        Merchant class, corresponds the table merchant in database
    '''
    __tablename__ = 'merchant'
    merchantId = Column(Integer, primary_key=True)
    storename = Column(String)
    description = Column(String)
    email = Column(String)
    password = Column(String)
    product = relationship("Product", backref="merchant")

    # Override the repr, when calling Client item
    def __repr__(self):
        return f'''
            storename: {self.storename}
            description: {self.description}
            email: {self.email}
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


# Create the corresponding Tabel in database
Base.metadata.create_all(engine)
