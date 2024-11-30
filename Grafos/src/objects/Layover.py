import re

class Layover():
    def __init__(self, summary, location, duration):
        if summary is None:
            self.location = location
            self.duration = duration
        else:
            self.location = None 
            self.duration = None
            self.processLayover(summary)

    def processLayover(self, summary):
        self.duration = self.getTime(summary)
        self.location = self.getLocation(summary)

    def getTime(self, text):
        value = re.findall('is a ([0-9]* hr [0-9]* min)',text)
        if len(value) == 0:
            return None
        return value[0]

    def getLocation(self, text):
        value = re.findall('at (.* Airport)',text)
        if len(value) == 0:
            return None
        return value[0]

    def __str__(self):
        return '''
    Layover at {} for {} '''.format(self.location, self.duration)

    def export(self):
        return {
            'location': str(self.location).replace('"','\"'),
            'duration': str(self.duration).replace('"','\"')
        }