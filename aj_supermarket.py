from typing import Dict, List
from models.bill_entry import BillEntry
from models.offers_module.offers import Offers
from models.order import Order
from models.product import Product


class Store:
    def __init__(self, owner_name: str, shop_name: str):
        self.owner_name = owner_name
        self.shop_name = shop_name

        # A dictionay is used rather than a list to make lookups easier
        self.inventory: Dict[int, Product] = {}  # product_id -> product
        self.offers: Offers = Offers()

    def __add_or_update_product(self, query):
        product_id, product_name, quantity, price = query.split("|")
        self.inventory[int(product_id)] = Product(
            int(product_id), product_name, int(quantity), int(price))
        print("Inventory updated")

    def get_stock(self, query):
        product_id = int(query)
        requested_product = self.inventory.get(product_id, None)
        if not requested_product:
            raise Exception("The requested product is not found.")
        print(requested_product)
        return requested_product.quantity

    def __make_sale(self, query):
        bill_entries = self.__get_bill_entries(query)
        self.__reduce_stock(bill_entries)
        order = Order(bill_entries)
        order = self.offers.apply_all_available_offers(order)
        print(order)
        return order.total

    def __add_offer(self, query):
        self.offers.handle_adding_offer(query)
        print("Offer Added")

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

    def execute_command(self, command):
        command_name, query = command.split("=>")

        match command_name:
            case "INVENTORY": self.__add_or_update_product(query)

            case "SALE": return self.__make_sale(query)

            case "STOCK": return self.get_stock(query)

            case "NEW-OFFER": self.__add_offer(query)

    def start_the_day(self):
        self.__display_greetings()
        store_is_open = True
        while store_is_open:
            try:
                command = input("\nEnter your command here: ")
                self.execute_command(command)

            # when ctrl+c is pressed
            except KeyboardInterrupt:
                store_is_open = False
            except Exception as e:
                print("Error: ", e)

        print("\nGood bye! {}".format(self.owner_name))


if __name__ == "__main__":
    market = Store("Rajesh", "AJ SuperMarket")
    market.start_the_day()
