from typing import List
from classes.bill_entry import BillEntry

class Order:
    def __init__(self, bill_entries: List[BillEntry],product_offer_dispatcher,bill_total_offer_dispatcher):
        self.bill_entries= bill_entries
        self.product_offer_dispatcher= product_offer_dispatcher
        self.bill_total_offer_dispatcher= bill_total_offer_dispatcher
        
        self.special_discount=0
        self.total=0
    
    def execute(self):
        self.product_offer_dispatcher.applyOffers(self)
        self.__calculate_total()
        self.bill_total_offer_dispatcher.applyOffers(self)
        self.__calculate_total()
        self.__display_bill(self.bill_entries)

    def __calculate_total(self):
        total=0
        for e in self.bill_entries:
            total+=e.net_price
        total-=self.special_discount
        self.total=total
    
    def __display_bill(self, bill_entries: List[BillEntry]):
        print("== Bill ==")
        for bill_entry in bill_entries:
            print("{} - {} - {} - {} - {} - {}".format(bill_entry.product_id, bill_entry.product_name,
                  bill_entry.quantity, bill_entry.product_price, bill_entry.offer_id, bill_entry.net_price))
            
        print("Special discount: {}".format(self.special_discount))
        print("== Total ==")
        print(self.total)
        print("============")
        return self.total
