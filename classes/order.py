from typing import List
from classes.bill_entry import BillEntry

class Order:
    def __init__(self, bill_entries: List[BillEntry],product_offer_dispatcher,special_offers):
        self.bill_entries= bill_entries
        self.product_offer_dispatcher= product_offer_dispatcher
        self.special_offers= special_offers
    
    def execute(self):
        self.product_offer_dispatcher.applyOffers(self)
        self.__display_bill(self.bill_entries)

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
                  bill_entry.quantity, bill_entry.product_price, bill_entry.offer_id, bill_entry.net_price))
            
        special_discount=self.__get_special_discount(total)
        total-=special_discount
        print("Special discount: {}".format(special_discount))
        print("== Total ==")
        print(total)
        print("============")
        return total
