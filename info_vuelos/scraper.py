import constants
import crawler

infovuelosUrl =  constants.LOCAL_URL

def get_airports(soup):
    airports = []
    origin = soup.find(id="origin_ac")
    resultSet = origin.find_all("option")
    for op in resultSet:
        airports.append([op['value'], op.text.strip()])
    airports.pop(0)
    return airports

def getDeparturesUrl(urlBase, airportCode):
    return urlBase + constants.DEPARTURES + airportCode

def getArrivalsUrl(urlBase, airportCode):
    return urlBase + constants.ARRIVALS + airportCode

def get_flights(url):
    return


soup = crawler.getLocalContent(infovuelosUrl)
airports = get_airports(soup)
print(airports)