#https://www.agoda.com/pt-br/search?city=2002&checkIn=2025-03-17&los=6&rooms=1&adults=2&children=0&locale=en-gb&ckuid=f67cf26b-f655-40b3-8524-dca691cf56b9&prid=0&currency=USD&correlationId=a148f8bf-2773-41d3-836a-21898a600757&analyticsSessionId=-6518406440201971329&pageTypeId=5&realLanguageId=16&languageId=1&origin=BR&stateCode=SP&cid=1844104&userId=f67cf26b-f655-40b3-8524-dca691cf56b9&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=7&currencyCode=USD&htmlLanguage=en-gb&cttp=4&isRealUser=False&mode=production&cdnDomain=agoda.net&checkOut=2025-03-23&priceCur=BRL&textToSearch=Barcelona&travellerType=1&familyMode=off&ds=Y8L4NgAzHw57SDYS&productType=-1

class Hotel():

    def __init__(self, name, price, url, address, score) -> None:
        self.name = name
        self.price = price
        self.url = url
        self.address = address
        self.score = score
    
    def __str__(self) -> str:
        return 'Name:{}\nPrice:{}\nURL:{}\nScore:{}'.format(
            self.name
            ,self.price
            ,self.url
            ,self.score
        )
    
    def export(self) -> str:
        return {
            'name': self.name,
            'price': self.price,
            'url': self.url,
            'address': self.address,
            'score': self.score
        }