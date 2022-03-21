from typing import Dict, List


class Store:
    class Product:
        def __init__(self, id, name, quantity, price):
            self.id = id
            self.name = name
            self.quantity = quantity
            self.price = price

    class Offer:
        def __init__(self, id, name, product_id, min_quantity, discount_percent):
            self.id = id
            self.name = name
            self.product_id = product_id
            self.min_quantity = min_quantity
            self.discount_percent = discount_percent

    class BillEntry:
        def __init__(self, product_id, product_name, quantity_purchased, product_price, offer_id, net_price):
            self.product_id = product_id
            self.product_name = product_name
            self.quantity_purchased = quantity_purchased
            self.product_price = product_price
            self.offer_id = offer_id
            self.net_price = net_price

    def __init__(self, owner_name: str, shop_name: str):
        # A dictionay is used rather than a list to make lookups easier
        self.owner_name = owner_name
        self.shop_name = shop_name
        self.inventory: Dict[int, Store.Product] = {}  # product_id -> product
        self.offers: Dict[int, List[Store.Offer]] = {}  # product_id -> offer[]

    def add_or_update_product(self, product_id, product_name, quantity, price):
        self.inventory[product_id] = self.Product(
            product_id, product_name, quantity, price)
        print("Inventory updated")

    def add_offer(self, offer_id, offer_name, product_id, min_quantity, discount_percent):
        self.offers[product_id] = self.offers.get(offer_id, [])
        self.offers[product_id].append(self.Offer(
            offer_id, offer_name, product_id, min_quantity, discount_percent))
        print("Offer Added")

    def get_stock(self, product_id):
        requested_product = self.inventory.get(product_id, None)
        if not requested_product:
            print("The requested product is not found.")
        else:
            print("{} - {}".format(requested_product.name,
                  requested_product.quantity))

    def make_sale(self, product_ids: List[int], quantity_purchased: List[int]):
        if not self.__check_availability(product_ids, quantity_purchased):
            return None
        self.__reduce_stock(product_ids, quantity_purchased)

        bill_entries = self.__generate_bill(product_ids, quantity_purchased)
        for bill_entry in bill_entries:
            bill_entry = self.__apply_offer(bill_entry)
        self.__display_bill(bill_entries)
        
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


    def __calculate_price_with_discount(self, price, discount_percent):
        return round(price - (price * discount_percent / 100), 2)

    def __get_best_offer(self, bill_entry: BillEntry):
        offers = self.offers.get(bill_entry.product_id, [])
        if not offers:
            return None
        best_offer = None
        current_best_price = bill_entry.product_price * bill_entry.quantity_purchased
        for offer in offers:
            if offer.min_quantity <= bill_entry.quantity_purchased and self.__calculate_price_with_discount(bill_entry.product_price*bill_entry.quantity_purchased, offer.discount_percent) < current_best_price:
                current_best_price = offer.discount_percent
                best_offer = offer
        return best_offer

    def __apply_offer(self, bill_entry: BillEntry):
        offer = self.__get_best_offer(bill_entry)

        if not offer:
            bill_entry.net_price = bill_entry.quantity_purchased * bill_entry.product_price
            bill_entry.offer_id = "N/A"
        else:
            bill_entry.net_price = self.__calculate_price_with_discount(
                bill_entry.product_price*bill_entry.quantity_purchased, offer.discount_percent)
            bill_entry.offer_id = offer.id

        return bill_entry

    def __generate_bill(self, product_ids: List[int], quantity_purchased: List[int]):
        bill_entries: List[Store.BillEntry] = []
        for product_id, quantity in zip(product_ids, quantity_purchased):
            bill_entry = self.BillEntry(
                product_id, self.inventory[product_id].name, quantity, self.inventory[product_id].price, None, None)
            bill_entries.append(bill_entry)
        return bill_entries

    def __display_bill(self, bill_entries: List[BillEntry]):
        print("== Bill ==")
        total = 0
        for bill_entry in bill_entries:
            total += bill_entry.net_price
            print("{} - {} - {} - {} - {} - {}".format(bill_entry.product_id, bill_entry.product_name,
                  bill_entry.quantity_purchased, bill_entry.product_price, bill_entry.offer_id, bill_entry.net_price))
        print("== Total ==")
        print(total)
        print("============")
    
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
                else:
                    print("Unknown command. Please try again.")
            except KeyboardInterrupt:
                store_is_open = False
            except:
                print("Unknown command. Please try again.")

        print("\nGood bye! {}".format(self.owner_name))


if __name__ == "__main__":
    market = Store("Rajesh", "AJ SuperMarket")
    market.start_the_day()
