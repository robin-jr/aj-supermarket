from models.offer import Offer


class BillTotalOffer(Offer):
    def __init__(self, id, name, min_total, discount):
        self.id = id
        self.name = name
        self.min_total = min_total
        self.discount = discount
