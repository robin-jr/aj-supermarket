
class BillEntry:
    def __init__(self, product_id, product_name, quantity_purchased, product_price, offer_id, net_price):
        self.product_id = product_id
        self.product_name = product_name
        self.quantity_purchased = quantity_purchased
        self.product_price = product_price
        self.offer_id = offer_id
        self.net_price = net_price