# cybermarket_server

The server of a online cybermarket.

## Statement of solved problem

**Module goals:** Build a module to accept binary messages from cybermarket_client, parse the messages and perform add, delete, modify and query operations in the database based on parameters.

**Client functions**:
  - **Create an account**:
    - Provide username, email, and password to create a new client.
  - **Account login or logout**:
    - Log in using username or email and password and log out
  - **Modify Personal Information**:
    - Username, email, and password are allowed to be modified
  - **Add or remove products**:
    - Allow customers to add or remove items from their shopping cart
  - **List order items**:
    - Users can view the items in their shopping cart
  - **Get total price**:
    - The user can get the total price of the items in the shopping cart
  - **Checkout order**:
    - Users can check out items in their shopping cart

**Merchant functions**:
  - **Create invitation code**:
    - Merchants can generate invitation codes to invite new merchants to join
  - **Create an account**:
    - Provide storename, description, email, password, and the invitation information to create a new merchant.
  - **Account login or logout**:
    - Log in using storename or email and password and log out
  - **Modify Personal Information**:
    - Storename, description, email, and password are allowed to be modified
  - **Put on or off the shelf**:
    - Merchants should be able to put products on or off the shelves
  - **Product restock**: 
    - Merchants should be able to restock products on shelves
  - **Get profit**:
    - Merchants should be able to capture their profits

**Common functions**:
  - **List Merchant**:
    - Allows to get a list of merchants without logging in
  - **List Product**:
    - Allows to obtain the product list of a specified merchant without logging in

## Description of proposed solution tools
| Depends        | Description |
|---|---|
| Pandas          | A tool for data analysis and manipulation. |
| SQLAlchemy      | A tool for interfacing between Python and databases. |

## Database ERD diagram
![ERD diagram](./ERD_diagram.png)
