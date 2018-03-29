import requests
from info_vuelos import constants
from info_vuelos.Flight import Flight
from bs4 import BeautifulSoup


def getContent(url):
    content = requests.get(url).content
    return BeautifulSoup(content, "html.parser")

def getLocalContent(filename):
    fileHandler = open(filename, encoding="utf8")
    return BeautifulSoup(fileHandler, "html.parser")

def getAirportName(fullname):
    return fullname[: fullname.find("(")].strip()

def getAirportCode(fullname):
    return fullname[fullname.find("(") + 1:fullname.find(")")].strip()

def get_airports(soup):
    airports = []
    origin = soup.find(id="origin_ac")
    resultSet = origin.find_all("option")
    for op in resultSet:
        airports.append([op['value'], getAirportName(op.text)])
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
airportName = airports[0][1]

departures = []
arrivals = []

#soup = getLocalContent(constants.LOCAL_SAMPLE_DEPARTURES)
soup = getDepartures(airportCode)

flightResultsTag = soup.find(id="flightResults")
tables = flightResultsTag.findAll("table")
tableIndex = 0
for table in tables:
    date = clean(table.caption.text.split(",")[-1])
    rows = table.find("tbody").find_all("tr")
    for row in rows:
        if (row["class"][0] == "principal"):
            cells = row.find_all("td")
            time = cells[0].text
            flightNumber = cells[1].a.text.strip()
            url = cells[1].a['href']
            origin = airportName
            originCode = airportCode
            destiny = getAirportName(cells[2].text)
            destinyCode = getAirportCode(cells[2].text)
            company = cells[3].text.strip()
            terminal = cells[4].text
            flight = Flight(date, time, flightNumber, origin, originCode, destiny, destinyCode, company, terminal)
            departures.append(flight)
            print(flight)


