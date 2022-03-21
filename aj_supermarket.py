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
    
    def add_special_offer(self,offer_id, offer_name,min_total,discount):
        self.special_offers.append(BillTotalOffer(offer_id,offer_name,min_total,discount))
        print("Special Offer Added")

    def get_stock(self, product_id):
        requested_product = self.inventory.get(product_id, None)
        if not requested_product:
            print("The requested product is not found.")
        else:
            print("{} - {}".format(requested_product.name,
                  requested_product.quantity))
        return requested_product.quantity

    
    def __generate_bill(self, product_ids: List[int], quantity_purchased: List[int]):
        bill_entries: List[BillEntry] = []
        for product_id, quantity in zip(product_ids, quantity_purchased):
            bill_entry = BillEntry(
                product_id, self.inventory[product_id].name, quantity, self.inventory[product_id].price, None, None)
            bill_entries.append(bill_entry)
        return bill_entries

    def make_sale(self, product_ids: List[int], quantity_purchased: List[int]):
        if not self.__check_availability(product_ids, quantity_purchased):
            return None
        self.__reduce_stock(product_ids, quantity_purchased)
        

        bill_entries = self.__generate_bill(product_ids, quantity_purchased)
        new_order = Order(bill_entries,self.offers,self.special_offers)
        new_order.execute()

    # Utility Methods start --------------------------------
    def __check_availability(self, product_ids: List[int], quantity_purchased: List[int]):
        for product_id, quantity in zip(product_ids, quantity_purchased):
            if product_id not in self.inventory:
                print(
                    "The product id {} is not found in the inventory.".format(product_id))
                return False
            elif self.inventory[product_id].quantity < quantity:
                print("The inventory does not have the required quantity for product {}".format(
                    self.inventory[product_id].name))
                return False
        return True

    def __reduce_stock(self, product_ids: List[int], quantity_purchased: List[int]):
        for product_id, quantity in zip(product_ids, quantity_purchased):
            self.inventory[product_id].quantity -= quantity


    

    # Utility methods end ----------------------------------

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
                    product_id = int(product_id)
                    quantity = int(quantity)
                    price_per_quantity = int(price_per_quantity)
                    self.add_or_update_product(
                        product_id, product_name, quantity, price_per_quantity)
                elif command_name == "SALE":
                    product_ids_and_quantities = query.split(";")
                    product_ids = []
                    quantities = []
                    for e in product_ids_and_quantities:
                        product_ids.append(int(e.split("|")[0]))
                        quantities.append(int(e.split("|")[1]))
                    self.make_sale(product_ids, quantities)
                elif command_name == "STOCK":
                    product_id = int(query)
                    self.get_stock(product_id)
                elif command_name == "NEW-OFFER":
                    offer_name, offer_id, product_id, min_quantity, discount_percent = query.split(
                        "|")
                    offer_id = int(offer_id)
                    product_id = int(product_id)
                    min_quantity = int(min_quantity)
                    discount_percent = int(discount_percent)
                    self.add_offer(
                        offer_id, offer_name, product_id, min_quantity, discount_percent)
                elif command_name=="SPECIAL-OFFER":
                    offer_id,offer_name,min_total,discount=query.split("|")
                    self.add_special_offer(int(offer_id),offer_name,int(min_total),int(discount))
                else:
                    print("Unknown command. Please try again.")
            except KeyboardInterrupt:
                store_is_open = False
            except Exception as e:
                print("Unknown command. Please try again.",e)

        print("\nGood bye! {}".format(self.owner_name))


if __name__ == "__main__":
    market = Store("Rajesh", "AJ SuperMarket")
    market.start_the_day()
