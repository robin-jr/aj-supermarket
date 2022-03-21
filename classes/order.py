from typing import List
from classes.bill_entry import BillEntry
from classes.bill_total_offer import BillTotalOffer
from classes.offer import Offer


class Order:
    def __init__(self, bill_entries: List[BillEntry],offers: List[Offer],special_offers: List[BillTotalOffer]):
        self.bill_entries= bill_entries
        self.offers= offers
        self.special_offers= special_offers
    
    def execute(self):
        for bill_entry in self.bill_entries:
            bill_entry = self.__apply_offer(bill_entry)
        self.__display_bill(self.bill_entries)

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
    

    def __get_special_discount(self,total: int):
        special_discount=0
        for e in self.special_offers:
            if e.min_total<=total and e.discount>special_discount:
                special_discount=e.discount
        return special_discount
    
    def __display_bill(self, bill_entries: List[BillEntry]):
        print("== Bill ==")
        total = 0
        for bill_entry in bill_entries:
            total += bill_entry.net_price
            print("{} - {} - {} - {} - {} - {}".format(bill_entry.product_id, bill_entry.product_name,
                  bill_entry.quantity_purchased, bill_entry.product_price, bill_entry.offer_id, bill_entry.net_price))
            
        special_discount=self.__get_special_discount(total)
        total-=special_discount
        print("Special discount: {}".format(special_discount))
        print("== Total ==")
        print(total)
        print("============")
        return total

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