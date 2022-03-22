from models.offers_module.bill_total_offer import BillTotalOffer
from models.offers_module.combo_offer import ComboOffer
from models.offers_module.combo_offer_dispatcher import ComboOfferDispatcher
from models.order import Order
from models.offers_module.product_offer import ProductOffer
from models.offers_module.product_offer_dispatcher import ProductOfferDispatcher
from models.offers_module.bill_total_offer_dispatcher import BillTotalOfferDispatcher


class Offers:
    def __init__(self):
        self.product_offer_dispatcher = ProductOfferDispatcher()
        self.bill_total_offer_dispatcher = BillTotalOfferDispatcher()
        self.combo_offer_dispatcher = ComboOfferDispatcher()

    def __add_product_offer(self, query):
        offer_name = query.split("|")[0]
        offer_id, product_id, min_quantity, discount_percent = map(
            int, query.split("|")[1:])

        new_offer = ProductOffer(offer_id, offer_name,
                                 product_id, min_quantity, discount_percent)
        self.product_offer_dispatcher.add_offer(new_offer)

    def __add_bill_total_offer(self, query):
        offer_name = query.split("|")[0]
        offer_id, min_total, discount = map(int, query.split("|")[1:])

        new_offer = BillTotalOffer(offer_id, offer_name, min_total, discount)
        self.bill_total_offer_dispatcher.add_offer(new_offer)

    def __add_combo_offer(self, query):
        offer_name, offer_id, product_ids, discount = query.split("|")
        product_ids = list(map(int, product_ids.split(",")))
        new_offer = ComboOffer(int(offer_id), offer_name,
                               product_ids, int(discount))
        self.combo_offer_dispatcher.add_offer(new_offer)

    def handle_adding_offer(self, query):
        offer_type = query.split('|')[-1]
        match offer_type:
            case '1':
                self.__add_product_offer(query[:-2])
            case '2':
                self.__add_bill_total_offer(query[:-2])
            case '3':
                self.__add_combo_offer(query[:-2])

    def apply_all_available_offers(self, order: Order):
        order = self.product_offer_dispatcher.apply_offers(order)
        order = self.bill_total_offer_dispatcher.apply_offers(order)
        order = self.combo_offer_dispatcher.apply_offers(order)
        return order
