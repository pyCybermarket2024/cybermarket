"""Provide Invitation class and methods for creating and using invitations."""
import random
import string
from sqlalchemy import Column, Integer, String
from src.setting import engine, Base, session


class Invitation(Base):
    """
    Store invitation codes linked to merchant's name.

    Attributes:
        id (Column): The primary key of the table.
        merchantname (Column): The name of the merchant associated
        with the invitation code.
        code (Column): The unique invitation code.
    """

    __tablename__ = 'invitation'
    id = Column(Integer, primary_key=True)
    merchantname = Column(String)
    code = Column(String)

    def __repr__(self):
        """
        Represent the Invitation instance as a string.

        Returns:
            str: A string containing the invitation code.
        """
        return f'''
            code: {self.code}
        '''


# Create the corresponding Tabel in database
Base.metadata.create_all(engine)


def generate_random_string():
    """Create a random string with length of 12."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(12))


def create_ivitation(merchantname):
    """
    Create an invitation code for a given merchant and stores in the database.

    Parameters:
        merchantname (str): The name of the merchant for whom the code is
        created.

    Returns:
        str: The generated invitation code.
    """
    code = generate_random_string()
    ivitation = Invitation(merchantname=merchantname, code=code)
    session.add(ivitation)
    session.commit()
    return code


def check_ivitation(merchantname, code):
    """
    Check if an invitation code provided by a merchant exists in the database.

    Parameters:
        merchantname (str): The name of the merchant who provided the code.
        code (str): The invitation code to be verified.

    Returns:
        bool: True if the code is valid and was found, False otherwise.
    """
    result = session.query(Invitation).filter(
        Invitation.merchantname == merchantname,
        Invitation.code == code
        ).first()
    if result:
        session.delete(result)
        session.commit()
        return True
    return False
