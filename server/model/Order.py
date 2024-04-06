from sqlalchemy import Column, Integer, ForeignKey
from server.config.setting import engine, Base, session
from sqlalchemy.orm import relationship


class Order(Base):
    '''
        Order class, corresponds the order product in database
    '''
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
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


# Create the corresponding Tabel in database
Base.metadata.create_all(engine)
