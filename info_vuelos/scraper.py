import requests
import constants
import crawler
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
    return crawler.getContent(constants.AENA_INFOVUELOS_URL + constants.DEPARTURES + airportCode)

def getArrivals(airportCode):
    return crawler.getContent(constants.AENA_INFOVUELOS_URL + constants.ARRIVALS + airportCode)

soup = BeautifulSoup(crawler.getLocalContent(constants.LOCAL_INFOVUELOS_URL), "html.parser")
airports = get_airports(soup)
code = airports[0][0]

soup = BeautifulSoup(crawler.getLocalContent(constants.LOCAL_SAMPLE_DEPARTURES), "html.parser")

flightResultsTag = soup.find(id="flightResults")
tables = flightResultsTag.findAll("table")
tableIndex = 0
for table in tables:
    when = table.caption.text.split(",")[-1]
    print(when)
    rows = table.find("tbody").find_all("tr")
    for row in rows:
        flightNumer = row.a.text
        print(flightNumer)


