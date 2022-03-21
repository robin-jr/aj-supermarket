from typing import Dict, List

from classes.product import Product
from classes.bill_entry import BillEntry
from classes.offer import Offer
from classes.bill_total_offer import BillTotalOffer
from classes.order import Order


class Store:

    def __init__(self, owner_name: str, shop_name: str):
        # A dictionay is used rather than a list to make lookups easier
        self.owner_name = owner_name
        self.shop_name = shop_name
        self.inventory: Dict[int, Product] = {}  # product_id -> product
        self.offers: Dict[int, List[Offer]] = {}  # product_id -> offer[]
        self.special_offers: List[BillTotalOffer] = []

    def add_or_update_product(self, product_id, product_name, quantity, price):
        self.inventory[product_id] = Product(
            product_id, product_name, quantity, price)
        print("Inventory updated")

    def add_offer(self, offer_id, offer_name, product_id, min_quantity, discount_percent):
        self.offers[product_id] = self.offers.get(offer_id, [])
        self.offers[product_id].append(Offer(
            offer_id, offer_name, product_id, min_quantity, discount_percent))
        print("Offer Added")

    def add_special_offer(self, offer_id, offer_name, min_total, discount):
        self.special_offers.append(BillTotalOffer(
            offer_id, offer_name, min_total, discount))
        print("Special Offer Added")

    def get_stock(self, product_id):
        requested_product = self.inventory.get(product_id, None)
        if not requested_product:
            print("The requested product is not found.")
        else:
            print("{} - {}".format(requested_product.name,
                  requested_product.quantity))
        return requested_product.quantity


    def make_sale(self, bill_entries: List[BillEntry]):
        self.__reduce_stock(bill_entries)
        new_order = Order(bill_entries, self.offers, self.special_offers)
        new_order.execute()

    def __reduce_stock(self, bill_entries: List[BillEntry]):
        for e in bill_entries:
            self.inventory[e.product_id].quantity -= e.quantity

    def start_the_day(self):
        print("\nGood morning, {}".format(self.owner_name))
        print("--- {} is going to sky rocket its sales today! ---".format(self.shop_name))
        print("\n")
        print("Waiting for your commands...")

        store_is_open = True
        while store_is_open:
            try:
                command = input("Enter your command here: \n")
                command_name, query = command.split("=>")
                if command_name == "EXIT":
                    store_is_open = False
                    break
                elif command_name == "INVENTORY":
                    product_id, product_name, quantity, price_per_quantity = query.split(
                        "|")
                    self.add_or_update_product(
                        int(product_id), product_name, int(quantity), int(price_per_quantity))
                elif command_name == "SALE":
                    product_ids_and_quantities = query.split(";")
                    bill_entries=[]
                    for e in product_ids_and_quantities:
                        product_id, quantity = map(int,e.split("|"))
                        product = self.inventory.get(product_id,None)
                        if not product:
                            print("product not found")
                            return
                        gross_price = product.price*quantity
                        bill_entries.append(BillEntry(product_id, product.name,quantity,product.price,"N/A",gross_price))
                    self.make_sale(bill_entries)
                elif command_name == "STOCK":
                    self.get_stock(int(product_id))
                elif command_name == "NEW-OFFER":
                    offer_name, offer_id, product_id, min_quantity, discount_percent = query.split(
                        "|")
                    self.add_offer(
                        int(offer_id), offer_name, int(product_id), int(min_quantity), int(discount_percent))
                elif command_name == "SPECIAL-OFFER":
                    offer_id, offer_name, min_total, discount = query.split(
                        "|")
                    self.add_special_offer(
                        int(offer_id), offer_name, int(min_total), int(discount))
                else:
                    print("Unknown command. Please try again.")
            except KeyboardInterrupt:
                store_is_open = False
            except Exception as e:
                print("Unknown command. Please try again.", e)

        print("\nGood bye! {}".format(self.owner_name))


if __name__ == "__main__":
    market = Store("Rajesh", "AJ SuperMarket")
    market.start_the_day()
