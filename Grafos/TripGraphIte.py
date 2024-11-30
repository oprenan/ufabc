class GraphItem:
    def __init__(self, place, destiny, price, date):
        self.place = place
        self.destiny = destiny
        self.price = price
        self.date = date
    
    def return_weight(self):
        return self.price