import requests
import constants
from bs4 import BeautifulSoup

def getContent(url):
    content = requests.get(url).content
    return BeautifulSoup(content, "html.parser")

def getLocalContent(filename):
    fileHandler = open(filename, encoding="utf8")
    return BeautifulSoup(fileHandler, "html.parser")

def get_airports(soup):
    airports = []
    origin = soup.find(id="origin_ac")
    resultSet = origin.find_all("option")
    for op in resultSet:
        airports.append([op['value'], op.text.strip()])
    airports.pop(0)
    return airports

def getDepartures(airportCode):
    return getContent(constants.AENA_INFOVUELOS_URL + constants.DEPARTURES + airportCode)

def getArrivals(airportCode):
    return getContent(constants.AENA_INFOVUELOS_URL + constants.ARRIVALS + airportCode)

def getDetails(flightURL):
    return getContent(constants.AENA_BASE_URL + flightURL)

def clean(rawText):
    return rawText.replace("\n", "").strip()

#soup = getLocalContent(constants.LOCAL_INFOVUELOS_URL)
soup = getContent(constants.AENA_INFOVUELOS_URL)
airports = get_airports(soup)
airportCode = airports[0][0]

#soup = getLocalContent(constants.LOCAL_SAMPLE_DEPARTURES)
soup = getDepartures(airportCode)

flightResultsTag = soup.find(id="flightResults")
tables = flightResultsTag.findAll("table")
tableIndex = 0
for table in tables:
    date = clean(table.caption.text.split(",")[-1])
    rows = table.find("tbody").find_all("tr")
    for row in rows:
        time = clean(row.td.text)
        flightNumber = clean(row.a.text)
        url = clean(row.a['href'])
        print('{} {} {} {}'.format(date, time, flightNumber, url))


