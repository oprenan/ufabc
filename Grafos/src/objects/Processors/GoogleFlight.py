import re
from src.objects.Flight import Flight
from src.objects.Layover import Layover
import json

class GoogleFlight():
    def __init__(self,content, org, dest, date, lan):
        self.rawContent = content
        self.flights = []
        self.org = org
        self.dest = dest
        self.date = date
        self.configKeys = json.loads(self.readFromFile('src/objects/Processors/GoogleFlight.json'))
        self.processText(self.configKeys['textSearch'][lan])

    def readFromFile(self,filename):
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()

    def processText(self,config):
        flightList = str(self.rawContent).strip('][').split('>, <')
        for flight in flightList:
            price = self.getPrice(flight, config['rPrice'])
            companies = self.getCompanies(flight,config['rCompanies'])
            stops = self.getStops(flight,config['rStops'])
            layovers = self.getLayovers(flight,config['rLayovers'])
            departure,arrival = self.getSummary(flight,config['rSummary'])
            duration = self.getTotalDuration(flight,config['rDuration'])
            layoversList = []

            if layovers is not None:
                for layover in layovers:
                    layoversList.append(Layover(layover, None, None))

            self.flights.append(Flight(
                price = price,
                companies = companies,
                departure = departure,
                arrival = arrival,
                stops = stops,
                layovers = layoversList,
                org = self.org,
                dest = self.dest,
                date = self.date,
                duration = duration
            )) 
    
    def getPrice(self, text, key):
        value = re.findall(key,text)
        if len(value) == 0:
            return None
        return value[0]
    
    def getTotalDuration(self, text, key):
        value = re.findall(key,text)
        if len(value) == 0:
            return None
        return value[0]

    def getCompanies(self, text, key):
        finds = re.findall(key,text)
        if len(finds) == 0:
            return None
        
        indx = None
        aux = 0
        finds = list(finds[0])
        for i, val in enumerate(finds):
            if len(val) > aux:
                indx = i
        return finds[indx]

    def getStops(self, text, key):
        value = re.findall(key,text)
        if len(value) == 0:
            return None
        return re.findall('[0-9]',value[0])[0]
    
    def getSummary(self,text, key):
        overall = re.findall(key['overall'],text)
        
        if len(overall) == 0:
            return None, None
        
        departure = re.findall(key['departure'],overall[0])[0]
        arrival = re.findall(key['arrival'],overall[0])[0]
        if len(departure) != 0:
            if len(arrival) != 0:
                return departure, arrival
            return departure, None
        
        if len(arrival) != 0:
            return None, arrival
        
        return None, None
    
    def getLayovers(self,text, key):
        value = re.findall(key,text)
        if len(value) != 0:
            return re.findall(key,text)[0].split('. ')
        return None
    
    def __str__(self):
        string = ''
        for flight in self.flights:
            string += flight.__str__()
        return string