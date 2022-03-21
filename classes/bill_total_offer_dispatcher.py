from typing import List
from classes.bill_total_offer import BillTotalOffer
from classes.offer_dispatcher import OfferDispatcher
from classes.order import Order

class BillTotalOfferDispatcher(OfferDispatcher):
    def __init__(self):
        self.offers : List[BillTotalOffer] = []
    
    def __get_special_discount(self,total: int):
        special_discount=0
        for e in self.offers:
            if e.min_total<=total and e.discount>special_discount:
                special_discount=e.discount
        return special_discount

    def applyOffers(self, order : Order):
        order.special_discount = self.__get_special_discount(order.total)
        return order.special_discount