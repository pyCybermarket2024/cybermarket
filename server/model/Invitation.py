import random
import string
from sqlalchemy import Column, Integer, String
from server.config.setting import engine, Base, session


class Invitation(Base):
    '''
        Invitation class, corresponds the table invitation in database,
        where save all of the invitation codes.
    '''
    __tablename__ = 'invitation'
    merchantname = Column(Integer, primary_key=True)
    code = Column(String)

    # Override the repr, when calling Client item
    def __repr__(self):
        return f'''
            code: {self.code}
        '''


# Create the corresponding Tabel in database
Base.metadata.create_all(engine)


# Create a random string with length of 12
def generate_random_string():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(12))


def create_ivitation(merchantname):
    '''
        merchantname: The name of the merchant to provide the code
        Create an random code in the database
    '''
    code = generate_random_string()
    ivitation = Invitation(merchantname, code)
    session.add(ivitation)
    session.commit()
    return code


def check_ivitation(merchantname, code):
    '''
        merchantname: The name of the merchant who provided the code
        code: Your Code
        Verify that this code is in the database
    '''
    result = session.query(Invitation).filter(
        Invitation.merchantname == merchantname,
        Invitation.code == code
        ).first()
    if result:
        session.delete(result)
        session.commit()
        return True
    return False
