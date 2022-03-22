import unittest
from aj_supermarket import Store


class TestAjSupermarket(unittest.TestCase):
    def test_adding_product(self):
        store = Store("Rajesh", "AJ Supermarket")
        store.execute_command("INVENTORY=>1|GoodDay250g|20|10")
        self.assertAlmostEqual(store.get_stock(1), 20)
        store.execute_command("INVENTORY=>2|GoodDay500g|10|20")
        self.assertAlmostEqual(store.get_stock(2), 10)

    def test_stock(self):
        store = Store("Rajesh", "AJ Supermarket")
        store.execute_command("INVENTORY=>1|GoodDay250g|20|10")
        self.assertAlmostEqual(store.execute_command("STOCK=>1"), 20)

    def test_sale(self):
        store = Store("Rajesh", "AJ Supermarket")
        store.execute_command("INVENTORY=>1|GoodDay250g|20|10")
        store.execute_command("INVENTORY=>2|GoodDay500g|10|20")
        order_total = store.execute_command("SALE=>1|2;2|1")
        self.assertAlmostEqual(order_total, 40)

    def test_product_offer(self):
        store = Store("Rajesh", "AJ Supermarket")
        store.execute_command("INVENTORY=>1|GoodDay250g|20|10")
        store.execute_command("INVENTORY=>2|GoodDay500g|10|20")
        store.execute_command("NEW-OFFER=>BuyXMore|1|1|2|10|1")
        order_total = store.execute_command("SALE=>1|4;2|1")
        self.assertAlmostEqual(order_total, 56)

    def test_bill_total_offer(self):
        store = Store("Rajesh", "AJ Supermarket")
        store.execute_command("INVENTORY=>1|GoodDay250g|20|10")
        store.execute_command("INVENTORY=>2|GoodDay500g|10|20")
        store.execute_command("NEW-OFFER=>GreaterThan10Special|1|10|40|2")
        order_total = store.execute_command("SALE=>1|4;2|1")
        self.assertAlmostEqual(order_total, 20)
