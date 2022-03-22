from typing import List
from models.bill_entry import BillEntry


class Order:
    def __init__(self, bill_entries: List[BillEntry]):
        self.bill_entries = bill_entries
        self.special_discount = 0
        self.total = 0

    def calculate_total(self):
        total = 0
        for e in self.bill_entries:
            total += e.net_price
        total -= self.special_discount
        self.total = total
    
    def set_total(self, total):
        self.total = total

    def __str__(self):
        print("== Bill ==")
        for bill_entry in self.bill_entries:
            print("{} - {} - {} - {} - {} - {}".format(bill_entry.product_id, bill_entry.product_name,
                  bill_entry.quantity, bill_entry.product_price, bill_entry.offer_id, bill_entry.net_price))

        print("Special discount: {}".format(self.special_discount))
        print("== Total ==")
        print(self.total)
        print("============")
        return ""
