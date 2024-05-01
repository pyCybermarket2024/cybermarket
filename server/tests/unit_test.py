from tests import setting_unittest
import unittest
from src import cmd_process
import pandas as pd
from src import invitation

setting_unittest


class TestClientCreate(unittest.TestCase):
    def setUp(cls):
        cmd_process.client_create(
            "8000", "127.0.0.1:33000", "liuhailin",
            "0123liuhailin@gmail.com", "123456"
            )

    def test_0(self):
        result = cmd_process.client_create(
            "0", "127.0.0.1:33001", "qangqi",
            "t390697002@gmail.com", "123456"
            )
        expected_result = ["0 201 Created"]
        self.assertEqual(result, expected_result)

    def test_1(self):
        result = cmd_process.client_create(
            "1", "127.0.0.1:33000", "liuhailin",
            "0123liuhailin@gmail.com", "123456"
            )
        expected_result = ["1 409 Conflict: This username is occupied"]
        self.assertEqual(result, expected_result)


class TestSetClientUsername(unittest.TestCase):
    def setUp(cls):
        cmd_process.client_create(
            "8000", "127.0.0.1:33000", "liuhailin",
            "0123liuhailin@gmail.com", "123456"
            )

    def test_0(self):
        cmd_process.client_login(
            "8000", "127.0.0.1:33000", "liuhailin", "123456"
            )
        result = cmd_process.set_client_username(
            "0", "127.0.0.1:33000", "liu"
            )
        expected_result = ["0 200 OK: Username has been set"]
        self.assertEqual(result, expected_result)

    def test_1(self):
        result = cmd_process.set_client_username(
            "1", "127.0.0.1:33001", "liu"
            )
        expected_result = [
            "1 401 Unauthorized: You have not logged in or your login has \
timed out"
            ]
        self.assertEqual(result, expected_result)


class TestSetClientPassword(unittest.TestCase):
    def setUp(cls):
        cmd_process.client_create(
            "8000", "127.0.0.1:33000", "liuhailin",
            "0123liuhailin@gmail.com", "123456"
            )
        cmd_process.client_login(
            "8000", "127.0.0.1:33000", "liuhailin", "123456"
            )

    def test_0(self):
        result = cmd_process.set_client_password(
            "0", "127.0.0.1:33000", "123", "123456"
            )
        expected_result = ["0 200 OK: New password has been set"]
        self.assertEqual(result, expected_result)

    def test_1(self):
        result = cmd_process.set_client_password(
            "1", "127.0.0.1:33000", "123", "000000"
            )
        expected_result = [
            "1 403 Forbidden: The password of the user is incorrect"
            ]
        self.assertEqual(result, expected_result)


class TestClientLogin(unittest.TestCase):
    def setUp(cls):
        cmd_process.client_create(
            "8000", "127.0.0.1:33000", "liuhailin",
            "0123liuhailin@gmail.com", "123456"
            )

    def test_0(self):
        result = cmd_process.client_login(
            "0", "127.0.0.1:33000", "liuhailin", "123456"
            )
        expected_result = ["0 200 OK: This user is logged in"]
        self.assertEqual(result, expected_result)

    def test_1(self):
        cmd_process.client_login(
            "0", "127.0.0.1:33000", "liuhailin", "123456"
            )
        result = cmd_process.client_login(
            "1", "127.0.0.1:33000", "liuhailin", "123456"
            )
        expected_result = [
            "1 400 Bad Request: The user has been logged in, please do not \
log in again"
            ]
        self.assertEqual(result, expected_result)


class TestClientLogout(unittest.TestCase):
    def setUp(cls):
        cmd_process.client_create(
            "8000", "127.0.0.1:33000", "liuhailin",
            "0123liuhailin@gmail.com", "123456"
            )

    def test_0(self):
        cmd_process.client_login(
            "0", "127.0.0.1:33000", "liuhailin", "123456"
        )
        result = cmd_process.client_logout(
            "1", "127.0.0.1:33000"
        )
        expected_result = ["1 200 OK: You have successfully logged out"]
        self.assertEqual(result, expected_result)

    def test_1(self):
        result = cmd_process.client_logout(
            "2", "127.0.0.1:33000"
        )
        expected_result = [
            "2 401 Unauthorized: You have not logged in or your login has \
timed out"
            ]
        self.assertEqual(result, expected_result)


class TestClientAddItem(unittest.TestCase):
    def setUp(cls):
        cybermarket = cmd_process.Merchant(
            storename="Cybermarket",
            description="Cybermarket official store",
            email="cybermarket@cybermarket.com",
            password="123456"
        )
        cmd_process.session.add(cybermarket)
        cmd_process.session.commit()
        cmd_process.merchant_login(
            "8000", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        cmd_process.merchant_add_product(
            "8001", "127.0.0.1:33000", "router", 100.0, ""
        )
        cmd_process.merchant_add_product(
            "8002", "127.0.0.1:33000", "switch", 200.0, ""
        )
        cmd_process.merchant_logout(
            "8003", "127.0.0.1:33000"
        )
        cmd_process.client_create(
            "8004", "127.0.0.1:33000", "liuhailin",
            "0123liuhailin@gmail.com", "123456"
        )

    def tearDown(self):
        cmd_process.merchant_login(
            "8005", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        cmd_process.merchant_del_product(
            "8006", "127.0.0.1:33000", 1
        )
        cmd_process.merchant_del_product(
            "8007", "127.0.0.1:33000", 2
        )
        cmd_process.merchant_logout(
            "8008", "127.0.0.1:33000"
        )
        result = cmd_process.session.query(cmd_process.Merchant).filter(
            cmd_process.Merchant.storename == "Cybermarket"
        ).first()
        cmd_process.session.delete(result)
        cmd_process.session.commit()

    def test_0(self):
        cmd_process.client_login(
            "0", "127.0.0.1:33000", "liuhailin", "123456"
        )
        result = cmd_process.client_add_item(
            "1", "127.0.0.1:33000", 1, 5
        )
        expected_result = [
            "1 200 OK: This product has been added to the shopping cart"
            ]
        cmd_process.client_remove_item(
            "2", "127.0.0.1:33000", 1
        )
        cmd_process.client_logout(
            "3", "127.0.0.1:33000"
        )
        self.assertEqual(result, expected_result)

    def test_1(self):
        cmd_process.client_login(
            "0", "127.0.0.1:33000", "liuhailin", "123456"
        )
        result = cmd_process.client_add_item(
            "1", "127.0.0.1:33000", 3, 5
        )
        expected_result = [
            "1 404 Not Found: The product you are trying to add cannot be \
found"
            ]
        cmd_process.client_remove_item(
            "2", "127.0.0.1:33000", 1
        )
        cmd_process.client_logout(
            "3", "127.0.0.1:33000"
        )
        self.assertEqual(result, expected_result)


class TestClientRemoveItem(unittest.TestCase):
    def setUp(cls):
        cybermarket = cmd_process.Merchant(
            storename="Cybermarket",
            description="Cybermarket official store",
            email="cybermarket@cybermarket.com",
            password="123456"
        )
        cmd_process.session.add(cybermarket)
        cmd_process.session.commit()
        cmd_process.merchant_login(
            "8000", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        cmd_process.merchant_add_product(
            "8001", "127.0.0.1:33000", "router", 100.0, ""
        )
        cmd_process.merchant_add_product(
            "8002", "127.0.0.1:33000", "switch", 200.0, ""
        )
        cmd_process.merchant_logout(
            "8003", "127.0.0.1:33000"
        )
        cmd_process.client_create(
            "8004", "127.0.0.1:33000", "liuhailin",
            "0123liuhailin@gmail.com", "123456"
        )

    def tearDown(self):
        cmd_process.merchant_login(
            "8005", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        cmd_process.merchant_del_product(
            "8006", "127.0.0.1:33000", 1
        )
        cmd_process.merchant_del_product(
            "8007", "127.0.0.1:33000", 2
        )
        cmd_process.merchant_logout(
            "8008", "127.0.0.1:33000"
        )
        result = cmd_process.session.query(cmd_process.Merchant).filter(
            cmd_process.Merchant.storename == "Cybermarket"
        ).first()
        cmd_process.session.delete(result)
        cmd_process.session.commit()

    def test_0(self):
        cmd_process.client_login(
            "0", "127.0.0.1:33000", "liuhailin", "123456"
        )
        cmd_process.client_add_item(
            "1", "127.0.0.1:33000", 1, 5
        )
        result = cmd_process.client_remove_item(
            "2", "127.0.0.1:33000", 1
        )
        expected_result = [
            "2 200 OK: This product has been removed from the shopping cart"
            ]
        cmd_process.client_logout(
            "3", "127.0.0.1:33000"
        )
        self.assertEqual(result, expected_result)

    def test_1(self):
        cmd_process.client_login(
            "0", "127.0.0.1:33000", "liuhailin", "123456"
        )
        cmd_process.client_add_item(
            "1", "127.0.0.1:33000", 1, 5
        )
        result = cmd_process.client_remove_item(
            "2", "127.0.0.1:33000", 2
        )
        expected_result = [
            "2 404 Not Found: This product is not in your shopping cart"
            ]
        cmd_process.client_remove_item(
            "3", "127.0.0.1:33000", 1
        )
        cmd_process.client_logout(
            "4", "127.0.0.1:33000"
        )
        self.assertEqual(result, expected_result)


class TestClientGetItems(unittest.TestCase):
    def setUp(cls):
        cybermarket = cmd_process.Merchant(
            storename="Cybermarket",
            description="Cybermarket official store",
            email="cybermarket@cybermarket.com",
            password="123456"
        )
        cmd_process.session.add(cybermarket)
        cmd_process.session.commit()
        cmd_process.merchant_login(
            "8000", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        cmd_process.merchant_add_product(
            "8001", "127.0.0.1:33000", "router", 100.0, ""
        )
        cmd_process.merchant_add_product(
            "8002", "127.0.0.1:33000", "switch", 200.0, ""
        )
        cmd_process.merchant_logout(
            "8003", "127.0.0.1:33000"
        )
        cmd_process.client_create(
            "8004", "127.0.0.1:33000", "liuhailin",
            "0123liuhailin@gmail.com", "123456"
        )

    def tearDown(self):
        cmd_process.merchant_login(
            "8005", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        cmd_process.merchant_del_product(
            "8006", "127.0.0.1:33000", 1
        )
        cmd_process.merchant_del_product(
            "8007", "127.0.0.1:33000", 2
        )
        cmd_process.merchant_logout(
            "8008", "127.0.0.1:33000"
        )
        result = cmd_process.session.query(cmd_process.Merchant).filter(
            cmd_process.Merchant.storename == "Cybermarket"
        ).first()
        cmd_process.session.delete(result)
        cmd_process.session.commit()

    def test_0(self):
        cmd_process.client_login(
            "0", "127.0.0.1:33000", "liuhailin", "123456"
        )
        cmd_process.client_add_item(
            "1", "127.0.0.1:33000", 1, 5
        )
        cmd_process.client_add_item(
            "2", "127.0.0.1:33000", 2, 5
        )
        result = cmd_process.client_get_items(
            "3", "127.0.0.1:33000"
        )
        data = {
            'storename': ["Cybermarket", "Cybermarket"],
            'productname': ['router', 'switch'],
            'price': [100.0, 200.0],
            'quantity': [5, 5]
        }
        df = pd.DataFrame(data)
        expected_result = [
            "3 200 OK: Obtained order list", df
            ]
        cmd_process.client_remove_item(
            "4", "127.0.0.1:33000", 1
        )
        cmd_process.client_remove_item(
            "5", "127.0.0.1:33000", 2
        )
        cmd_process.client_logout(
            "6", "127.0.0.1:33000"
        )
        self.assertEqual(
            [result[0], result[1].equals(expected_result[1])],
            [expected_result[0], True]
            )


class TestClientGetPrice(unittest.TestCase):
    def setUp(cls):
        cybermarket = cmd_process.Merchant(
            storename="Cybermarket",
            description="Cybermarket official store",
            email="cybermarket@cybermarket.com",
            password="123456"
        )
        cmd_process.session.add(cybermarket)
        cmd_process.session.commit()
        cmd_process.merchant_login(
            "8000", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        cmd_process.merchant_add_product(
            "8001", "127.0.0.1:33000", "router", 100.0, ""
        )
        cmd_process.merchant_add_product(
            "8002", "127.0.0.1:33000", "switch", 200.0, ""
        )
        cmd_process.merchant_logout(
            "8003", "127.0.0.1:33000"
        )
        cmd_process.client_create(
            "8004", "127.0.0.1:33000", "liuhailin",
            "0123liuhailin@gmail.com", "123456"
        )

    def tearDown(self):
        cmd_process.merchant_login(
            "8005", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        cmd_process.merchant_del_product(
            "8006", "127.0.0.1:33000", 1
        )
        cmd_process.merchant_del_product(
            "8007", "127.0.0.1:33000", 2
        )
        cmd_process.merchant_logout(
            "8008", "127.0.0.1:33000"
        )
        result = cmd_process.session.query(cmd_process.Merchant).filter(
            cmd_process.Merchant.storename == "Cybermarket"
        ).first()
        cmd_process.session.delete(result)
        cmd_process.session.commit()

    def test_0(self):
        cmd_process.client_login(
            "0", "127.0.0.1:33000", "liuhailin", "123456"
        )
        cmd_process.client_add_item(
            "1", "127.0.0.1:33000", 1, 5
        )
        cmd_process.client_add_item(
            "2", "127.0.0.1:33000", 2, 5
        )
        result = cmd_process.client_get_price(
            "3", "127.0.0.1:33000"
        )
        expected_result = [
            "3 200 OK: Order price obtained", 1500.0
            ]
        cmd_process.client_remove_item(
            "4", "127.0.0.1:33000", 1
        )
        cmd_process.client_remove_item(
            "5", "127.0.0.1:33000", 2
        )
        cmd_process.client_logout(
            "6", "127.0.0.1:33000"
        )
        self.assertEqual(result, expected_result)


class TestClientCheckoutItem(unittest.TestCase):
    def setUp(cls):
        cybermarket = cmd_process.Merchant(
            storename="Cybermarket",
            description="Cybermarket official store",
            email="cybermarket@cybermarket.com",
            password="123456"
        )
        cmd_process.session.add(cybermarket)
        cmd_process.session.commit()
        cmd_process.merchant_login(
            "8000", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        cmd_process.merchant_add_product(
            "8001", "127.0.0.1:33000", "router", 100.0, ""
        )
        cmd_process.merchant_restock_product(
            "8002", "127.0.0.1:33000", 1, 5
        )
        cmd_process.merchant_add_product(
            "8003", "127.0.0.1:33000", "switch", 200.0, ""
        )
        cmd_process.merchant_restock_product(
            "8004", "127.0.0.1:33000", 2, 5
        )
        cmd_process.merchant_logout(
            "8005", "127.0.0.1:33000"
        )
        cmd_process.client_create(
            "8006", "127.0.0.1:33000", "liuhailin",
            "0123liuhailin@gmail.com", "123456"
        )

    def tearDown(self):
        cmd_process.merchant_login(
            "8007", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        cmd_process.merchant_del_product(
            "8008", "127.0.0.1:33000", 1
        )
        cmd_process.merchant_del_product(
            "8009", "127.0.0.1:33000", 2
        )
        cmd_process.merchant_logout(
            "8010", "127.0.0.1:33000"
        )
        result = cmd_process.session.query(cmd_process.Merchant).filter(
            cmd_process.Merchant.storename == "Cybermarket"
        ).first()
        cmd_process.session.delete(result)
        cmd_process.session.commit()

    def test_0(self):
        cmd_process.client_login(
            "0", "127.0.0.1:33000", "liuhailin", "123456"
        )
        cmd_process.client_add_item(
            "1", "127.0.0.1:33000", 1, 5
        )
        cmd_process.client_add_item(
            "2", "127.0.0.1:33000", 2, 5
        )
        result = cmd_process.client_checkout_item(
            "3", "127.0.0.1:33000"
        )
        expected_result = [
            "3 200 OK: Order has been checked out"
            ]
        cmd_process.client_remove_item(
            "4", "127.0.0.1:33000", 1
        )
        cmd_process.client_remove_item(
            "5", "127.0.0.1:33000", 2
        )
        cmd_process.client_logout(
            "6", "127.0.0.1:33000"
        )
        self.assertEqual(result, expected_result)

    def test_1(self):
        cmd_process.client_login(
            "0", "127.0.0.1:33000", "liuhailin", "123456"
        )
        cmd_process.client_add_item(
            "1", "127.0.0.1:33000", 1, 10
        )
        cmd_process.client_add_item(
            "2", "127.0.0.1:33000", 2, 10
        )
        result = cmd_process.client_checkout_item(
            "3", "127.0.0.1:33000"
        )
        expected_result = [
            "3 400 Bad Request: Inventory shortage for product router from \
merchant Cybermarket, checkout was not fully executed and this item is still \
in your cart"
            ]
        cmd_process.client_remove_item(
            "4", "127.0.0.1:33000", 1
        )
        cmd_process.client_remove_item(
            "5", "127.0.0.1:33000", 2
        )
        cmd_process.client_logout(
            "6", "127.0.0.1:33000"
        )
        self.assertEqual(result, expected_result)


class TestListMerchant(unittest.TestCase):
    def setUp(cls):
        cybermarket = cmd_process.Merchant(
            storename="Cybermarket",
            description="Cybermarket official store",
            email="cybermarket@cybermarket.com",
            password="123456"
        )
        cmd_process.session.add(cybermarket)
        cmd_process.session.commit()

    def tearDown(self):
        result = cmd_process.session.query(cmd_process.Merchant).filter(
            cmd_process.Merchant.storename == "Cybermarket"
        ).first()
        cmd_process.session.delete(result)
        cmd_process.session.commit()

    def test_0(self):
        result = cmd_process.list_merchant(
            "0", "127.0.0.1:33000"
        )
        data = {
            'storename': ["Cybermarket"],
            'description': ["Cybermarket official store"],
            'email': ["cybermarket@cybermarket.com"]
        }
        df = pd.DataFrame(data)
        expected_result = [
            "0 200 OK", df
            ]
        self.assertEqual(
            [result[0], result[1].equals(expected_result[1])],
            [expected_result[0], True]
            )


class TestListProduct(unittest.TestCase):
    def setUp(cls):
        cybermarket = cmd_process.Merchant(
            storename="Cybermarket",
            description="Cybermarket official store",
            email="cybermarket@cybermarket.com",
            password="123456"
        )
        cmd_process.session.add(cybermarket)
        cmd_process.session.commit()
        cmd_process.merchant_login(
            "8000", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        cmd_process.merchant_add_product(
            "8001", "127.0.0.1:33000", "router", 100.0, ""
        )
        cmd_process.merchant_add_product(
            "8002", "127.0.0.1:33000", "switch", 200.0, ""
        )
        cmd_process.merchant_logout(
            "8003", "127.0.0.1:33000"
        )
        cmd_process.client_create(
            "8004", "127.0.0.1:33000", "liuhailin",
            "0123liuhailin@gmail.com", "123456"
        )

    def tearDown(self):
        cmd_process.merchant_login(
            "8005", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        cmd_process.merchant_del_product(
            "8006", "127.0.0.1:33000", 1
        )
        cmd_process.merchant_del_product(
            "8007", "127.0.0.1:33000", 2
        )
        cmd_process.merchant_logout(
            "8008", "127.0.0.1:33000"
        )
        result = cmd_process.session.query(cmd_process.Merchant).filter(
            cmd_process.Merchant.storename == "Cybermarket"
        ).first()
        cmd_process.session.delete(result)
        cmd_process.session.commit()

    def test_0(self):
        cmd_process.client_login(
            "0", "127.0.0.1:33000", "liuhailin", "123456"
        )
        cmd_process.client_add_item(
            "1", "127.0.0.1:33000", 1, 5
        )
        cmd_process.client_add_item(
            "2", "127.0.0.1:33000", 2, 5
        )
        result = cmd_process.list_product(
            "3", "127.0.0.1:33000", "Cybermarket"
        )
        data = {
            'product_id': [1, 2],
            'storename': ["Cybermarket", "Cybermarket"],
            'productname': ['router', 'switch'],
            'description': ["", ""],
            'price': [100.0, 200.0],
            'stock': [0, 0]
        }
        df = pd.DataFrame(data)
        expected_result = [
            "3 200 OK: Product list has been obtained", df
            ]
        cmd_process.client_remove_item(
            "4", "127.0.0.1:33000", 1
        )
        cmd_process.client_remove_item(
            "5", "127.0.0.1:33000", 2
        )
        cmd_process.client_logout(
            "6", "127.0.0.1:33000"
        )
        self.assertEqual(
            [result[0], result[1].equals(expected_result[1])],
            [expected_result[0], True]
            )


class TestCreateInvitation(unittest.TestCase):
    def setUp(cls):
        cybermarket = cmd_process.Merchant(
            storename="Cybermarket",
            description="Cybermarket official store",
            email="cybermarket@cybermarket.com",
            password="123456"
        )
        cmd_process.session.add(cybermarket)
        cmd_process.session.commit()

    def tearDown(self):
        result = cmd_process.session.query(cmd_process.Merchant).filter(
            cmd_process.Merchant.storename == "Cybermarket"
        ).first()
        cmd_process.session.delete(result)
        cmd_process.session.commit()

    def test_0(self):
        cmd_process.merchant_login(
            "0", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        result = cmd_process.merchant_create_ivitation(
            "1", "127.0.0.1:33000", "Cybermarket"
        )
        expected_result = [
            "1 200 OK: Invitation code has been generated", ""
            ]
        cmd_process.merchant_logout(
            "2", "127.0.0.1:33000"
        )
        code = cmd_process.session.query(invitation.Invitation).filter(
            invitation.Invitation.code == result[1]
        ).first()
        cmd_process.session.delete(code)
        cmd_process.session.commit()
        self.assertEqual(result[0], expected_result[0])


class TestMerchantCreate(unittest.TestCase):
    def setUp(cls):
        cybermarket = cmd_process.Merchant(
            storename="Cybermarket",
            description="Cybermarket official store",
            email="cybermarket@cybermarket.com",
            password="123456"
        )
        cmd_process.session.add(cybermarket)
        cmd_process.session.commit()

    def tearDown(self):
        result = cmd_process.session.query(cmd_process.Merchant).filter(
            cmd_process.Merchant.storename == "Cybermarket"
        ).first()
        cmd_process.session.delete(result)
        cmd_process.session.commit()

    def test_0(self):
        cmd_process.merchant_login(
            "0", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        code = cmd_process.merchant_create_ivitation(
            "1", "127.0.0.1:33000", "Cybermarket"
        )[1]
        cmd_process.merchant_logout(
            "2", "127.0.0.1:33000"
        )
        result = cmd_process.merchant_create(
            "3", "127.0.0.1:33000", "newmerchant", "",
            "newmerchant@cybermarket.com", "123456",
            "Cybermarket", code
        )
        expected_result = ["3 201 Created"]
        code = cmd_process.session.query(invitation.Invitation).filter(
            invitation.Invitation.code == code
        ).first()
        if code:
            cmd_process.session.delete(code)
            cmd_process.session.commit()
        self.assertEqual(result, expected_result)

    def test_1(self):
        cmd_process.merchant_login(
            "0", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        code = cmd_process.merchant_create_ivitation(
            "1", "127.0.0.1:33000", "Cybermarket"
        )[1]
        cmd_process.merchant_logout(
            "2", "127.0.0.1:33000"
        )
        result = cmd_process.merchant_create(
            "3", "127.0.0.1:33000", "newmerchant", "",
            "newmerchant@cybermarket.com", "123456",
            "Cybermarket", "000000000000"
        )
        expected_result = [
            "3 406 Not Acceptable: Your invitation code cannot be verified.\
 This invitation code may be wrong or has already been used.\
 Please contact other merchants to request the invitation code."
            ]
        code = cmd_process.session.query(invitation.Invitation).filter(
            invitation.Invitation.code == code
        ).first()
        if code:
            cmd_process.session.delete(code)
            cmd_process.session.commit()
        self.assertEqual(result, expected_result)


class TestMerchantRestockProduct(unittest.TestCase):
    def setUp(cls):
        cybermarket = cmd_process.Merchant(
            storename="Cybermarket",
            description="Cybermarket official store",
            email="cybermarket@cybermarket.com",
            password="123456"
        )
        cmd_process.session.add(cybermarket)
        cmd_process.session.commit()
        cmd_process.merchant_login(
            "8000", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        cmd_process.merchant_add_product(
            "8001", "127.0.0.1:33000", "router", 100.0, ""
        )
        cmd_process.merchant_add_product(
            "8002", "127.0.0.1:33000", "switch", 200.0, ""
        )
        cmd_process.merchant_logout(
            "8003", "127.0.0.1:33000"
        )

    def tearDown(self):
        cmd_process.merchant_login(
            "8004", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        cmd_process.merchant_del_product(
            "8005", "127.0.0.1:33000", 1
        )
        cmd_process.merchant_del_product(
            "8006", "127.0.0.1:33000", 2
        )
        cmd_process.merchant_logout(
            "8007", "127.0.0.1:33000"
        )
        result = cmd_process.session.query(cmd_process.Merchant).filter(
            cmd_process.Merchant.storename == "Cybermarket"
        ).first()
        cmd_process.session.delete(result)
        cmd_process.session.commit()

    def test_0(self):
        cmd_process.merchant_login(
            "0", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        result = cmd_process.merchant_restock_product(
            "1", "127.0.0.1:33000", 1, 5
        )
        expected_result = [
            "1 200 OK: This product has been restock"
            ]
        cmd_process.merchant_logout(
            "2", "127.0.0.1:33000"
        )
        self.assertEqual(result, expected_result)

    def test_1(self):
        cmd_process.merchant_login(
            "0", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        result = cmd_process.merchant_restock_product(
            "1", "127.0.0.1:33000", 3, 5
        )
        expected_result = [
            "1 400 Bad Request: You are restocking an item that is not from \
this store"
            ]
        cmd_process.merchant_logout(
            "2", "127.0.0.1:33000"
        )
        self.assertEqual(result, expected_result)


class TestMerchantGetProfit(unittest.TestCase):
    def setUp(cls):
        cybermarket = cmd_process.Merchant(
            storename="Cybermarket",
            description="Cybermarket official store",
            email="cybermarket@cybermarket.com",
            password="123456"
        )
        cmd_process.session.add(cybermarket)
        cmd_process.session.commit()
        cmd_process.merchant_login(
            "8000", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        cmd_process.merchant_add_product(
            "8001", "127.0.0.1:33000", "router", 100.0, ""
        )
        cmd_process.merchant_restock_product(
            "8002", "127.0.0.1:33000", 1, 5
        )
        cmd_process.merchant_add_product(
            "8003", "127.0.0.1:33000", "switch", 200.0, ""
        )
        cmd_process.merchant_restock_product(
            "8004", "127.0.0.1:33000", 2, 5
        )
        cmd_process.merchant_logout(
            "8005", "127.0.0.1:33000"
        )
        cmd_process.client_create(
            "8006", "127.0.0.1:33000", "liuhailin",
            "0123liuhailin@gmail.com", "123456"
        )
        cmd_process.client_login(
            "8007", "127.0.0.1:33000", "liuhailin", "123456"
        )
        cmd_process.client_add_item(
            "8008", "127.0.0.1:33000", 1, 5
        )
        cmd_process.client_add_item(
            "8009", "127.0.0.1:33000", 2, 5
        )
        cmd_process.client_checkout_item(
            "8010", "127.0.0.1:33000"
        )
        cmd_process.client_logout(
            "8011", "127.0.0.1:33000"
        )

    def tearDown(self):
        cmd_process.merchant_login(
            "8012", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        cmd_process.merchant_del_product(
            "8013", "127.0.0.1:33000", 1
        )
        cmd_process.merchant_del_product(
            "8014", "127.0.0.1:33000", 2
        )
        cmd_process.merchant_logout(
            "8015", "127.0.0.1:33000"
        )
        result = cmd_process.session.query(cmd_process.Merchant).filter(
            cmd_process.Merchant.storename == "Cybermarket"
        ).first()
        cmd_process.session.delete(result)
        cmd_process.session.commit()

    def test_0(self):
        cmd_process.merchant_login(
            "0", "127.0.0.1:33000", "Cybermarket", "123456"
        )
        result = cmd_process.merchant_get_profit(
            "1", "127.0.0.1:33000", 1
        )
        expected_result = [
            "1 200 OK: Your total profit has been obtained", 1500.0
            ]
        cmd_process.merchant_logout(
            "2", "127.0.0.1:33000"
        )
        self.assertEqual(result, expected_result)
