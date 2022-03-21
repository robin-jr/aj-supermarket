
class BillTotalOffer:
    def __init__(self, id, name,min_total, discount):
        self.id = id
        self.name = name
        self.min_total = min_total
        self.discount = discount
    
    def __str__(self):
        return "{} {} {} {}".format(self.id, self.name, self.min_total, self.discount)