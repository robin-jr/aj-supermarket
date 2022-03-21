import unittest
from aj_supermarket import Store

class TestAjSupermarket(unittest.TestCase):
    def test_adding_product(self):
        store = Store( "Rajesh","AJ Supermarket")
        store.add_or_update_product(1, "Milk", 10, 20)
        self.assertAlmostEqual(store.get_stock(1), 10)
    
    def test_adding_offer(self):
        store = Store( "Rajesh","AJ Supermarket")
        store.add_or_update_product(1, "Milk", 10, 20)
        store.add_offer(1, "Milk Offer", 1, 5, 10)
        store.make_sale([1], [5])
        
        

        