from typing import Dict, List
from classes.bill_entry import BillEntry
from classes.bill_total_offer_dispatcher import BillTotalOfferDispatcher
from classes.order import Order
from classes.product import Product
from classes.product_offer import ProductOffer
from classes.product_offer_dispatcher import ProductOfferDispatcher
from classes.bill_total_offer import BillTotalOffer

class Store:

    def __init__(self, owner_name: str, shop_name: str):
        self.owner_name = owner_name
        self.shop_name = shop_name

        # A dictionay is used rather than a list to make lookups easier
        self.inventory: Dict[int, Product] = {}  # product_id -> product
        
        self.product_offer_dispatcher:ProductOfferDispatcher=ProductOfferDispatcher()
        self.bill_total_offer_dispatcher:BillTotalOfferDispatcher=BillTotalOfferDispatcher()

    def add_or_update_product(self, query):
        product_id, product_name, quantity, price = query.split("|")
        self.inventory[int(product_id)] = Product(
            int(product_id), product_name, int(quantity), int(price))
        print("Inventory updated")

    def add_offer(self, query):
        offer_name = query.split("|")[0]
        offer_id, product_id, min_quantity, discount_percent = map(
            int, query.split("|")[1:])
        new_offer=ProductOffer(offer_id,offer_name,product_id,min_quantity,discount_percent)
        self.product_offer_dispatcher.add_offer(new_offer)
        print("Offer Added")

    def add_special_offer(self, query):
        offer_id, offer_name, min_total, discount = query.split("|")
        new_offer=BillTotalOffer(int(offer_id), offer_name, int(min_total), int(discount))
        self.bill_total_offer_dispatcher.add_offer(new_offer)
        print("Special Offer Added")

    def get_stock(self, query):
        product_id = int(query)
        requested_product = self.inventory.get(product_id, None)
        if not requested_product:
            raise Exception("The requested product is not found.")
        print("{} - {}".format(requested_product.name, requested_product.quantity))
        return requested_product.quantity

    def make_sale(self, query):
        bill_entries = self.__get_bill_entries(query)
        self.__reduce_stock(bill_entries)
        new_order = Order(bill_entries, self.product_offer_dispatcher,self.bill_total_offer_dispatcher)
        new_order.execute()

    def __reduce_stock(self, bill_entries: List[BillEntry]):
        for e in bill_entries:
            self.inventory[e.product_id].quantity -= e.quantity

    def __display_greetings(self):
        print("\nGood morning, {}".format(self.owner_name))
        print("--- {} is going to sky rocket its sales today! ---".format(self.shop_name))
        print("\n")
        print("Waiting for your commands...")

    def __get_bill_entries(self, query):
        product_ids_and_quantities = query.split(";")
        bill_entries = []
        for e in product_ids_and_quantities:
            product_id, quantity = map(int, e.split("|"))
            product = self.inventory.get(product_id, None)
            if not product:
                raise Exception("Product not found in inventory")
            price = product.price*quantity
            bill_entries.append(BillEntry(
                product_id, product.name, quantity, product.price, "N/A", price))
        return bill_entries

    def start_the_day(self):
        self.__display_greetings()
        store_is_open = True
        while store_is_open:
            try:
                command = input("Enter your command here: \n")
                command_name, query = command.split("=>")

                match command_name:
                    case "EXIT": store_is_open = False

                    case "INVENTORY": self.add_or_update_product(query)

                    case "SALE": self.make_sale(query)

                    case "STOCK": self.get_stock(query)

                    case "NEW-OFFER": self.add_offer(query)

                    case "SPECIAL-OFFER": self.add_special_offer(query)

            except KeyboardInterrupt:
                store_is_open = False
            except Exception as e:
                print(e)

        print("\nGood bye! {}".format(self.owner_name))


if __name__ == "__main__":
    market = Store("Rajesh", "AJ SuperMarket")
    market.start_the_day()
