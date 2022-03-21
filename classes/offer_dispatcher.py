from typing import List

from classes.offer import Offer
from classes.order import Order

class OfferDispatcher:
    def __init__(self):
        self.offers : List[Offer]=[]
    
    def add_offer(self, offer: Offer):
        self.offers.append(offer)
    
    def applyOffers(self,order : Order):
        raise NotImplementedError()