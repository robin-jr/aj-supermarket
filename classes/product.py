class Product:
    def __init__(self, id, name, quantity, price):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price
    
    def __str__(self):
        return "{} - {}".format(self.name, self.quantity)