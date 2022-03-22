from typing import List
from models.bill_total_offer import BillTotalOffer
from models.offer_dispatcher import OfferDispatcher
from models.order import Order


class BillTotalOfferDispatcher(OfferDispatcher):
    def __init__(self):
        self.offers: List[BillTotalOffer] = []

    def __get_special_discount(self, total: int):
        special_discount = 0
        for e in self.offers:
            if e.min_total <= total and e.discount > special_discount:
                special_discount = e.discount
        return special_discount

    def apply_offers(self, order: Order):
        order.special_discount = self.__get_special_discount(order.total)
        order.calculate_total()
        return order
