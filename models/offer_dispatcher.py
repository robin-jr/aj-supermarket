from typing import List

from models.offer import Offer
from models.order import Order


class OfferDispatcher:
    def __init__(self):
        self.offers: List[Offer] = []

    def add_offer(self, offer: Offer):
        self.offers.append(offer)

    def apply_offers(self, order: Order):
        raise NotImplementedError()
