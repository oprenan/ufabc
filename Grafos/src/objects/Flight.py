
class Flight():

    def __init__(self, org, dest, date, price, companies, departure, arrival, stops, layovers, duration) -> None:
        self.org = org
        self.dest = dest
        self.date = date
        self.price = price
        self.companies = companies
        self.departure = departure
        self.arrival = arrival
        self.stops = stops
        self.layovers = layovers
        self.duration = duration
    
    def __str__(self) -> str:
        string =  '\nOrg = {org} Dest = {dest} Date = {date} Companies = {companies} Price = {price} Duration = {duration}'.format(
            org = self.org,
            dest = self.dest,
            date = self.date,
            companies = self.companies,
            price = self.price,
            duration = self.duration
        )

        for layover in self.layovers:
            string += layover.__str__()
        
        return string
    
    def export(self):
        return {
            'org': self.org,
            'dest': self.dest,
            'date': self.date,
            'price': self.price,
            'companies': self.companies,
            'departure': self.departure,
            'arrival': self.arrival,
            'stops': self.stops,
            'layovers': [layover.export() for layover in self.layovers],
            'duration': self.duration
        }