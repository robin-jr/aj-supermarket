from typing import List
from models.bill_entry import BillEntry
from models.offer_dispatcher import OfferDispatcher
from models.order import Order
from models.product_offer import ProductOffer


class ProductOfferDispatcher(OfferDispatcher):
    def __init__(self):
        self.offers: List[ProductOffer] = []

    def __get_best_offer_for_a_bill_entry(self, bill_entry: BillEntry):
        product_offers = filter(lambda e: e.product_id==bill_entry.product_id, self.offers)
        best_offer = None
        best_discount=0
        for offer in product_offers:
            if offer.min_quantity <= bill_entry.quantity and best_discount < offer.discount_percent:
                best_discount=offer.discount_percent
                best_offer = offer
        return best_offer

    def __apply_best_offer_for_a_bill_entry(self, bill_entry):
        offer:ProductOffer = self.__get_best_offer_for_a_bill_entry(bill_entry)
        if offer:
            bill_entry.offer_id = offer.id
            bill_entry.net_price -= (bill_entry.net_price* (offer.discount_percent/100))
        return bill_entry
        
    def apply_offers(self, order: Order):
        bill_entries = order.bill_entries
        t=[]
        for e in bill_entries:
            t.append(self.__apply_best_offer_for_a_bill_entry(e))
        order.bill_entries=t
        order.calculate_total()
        return order