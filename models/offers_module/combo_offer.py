from models.offers_module.offer import Offer


class ComboOffer(Offer):
    def __init__(self, id, name, product_ids, discount):
        self.id = id
        self.name = name
        self.product_ids = product_ids
        self.discount = discount
