from sqlalchemy import Column, Integer, String
from server.config.setting import engine, Base, session


class Client(Base):
    '''
        Client class, corresponds the table client in database
    '''
    __tablename__ = 'client'
    clientId = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

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


# Create the corresponding Tabel in database
Base.metadata.create_all(engine)
