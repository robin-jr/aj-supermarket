from typing import List
from models.offers_module.combo_offer import ComboOffer
from models.offers_module.offer_dispatcher import OfferDispatcher
from models.order import Order


class ComboOfferDispatcher(OfferDispatcher):
    def __init__(self):
        self.offers: List[ComboOffer] = []

    def __order_has_product_ids(self, order: Order, product_ids):
        ordered_ids = []
        for e in order.bill_entries:
            ordered_ids.append(e.product_id)
        for e in product_ids:
            if e not in ordered_ids:
                return False
        return True

    def apply_offers(self, order: Order):
        for e in self.offers:
            if self.__order_has_product_ids(order, e.product_ids):
                order.combo_discount = e.discount
                order.total -= e.discount
                break
        return order
