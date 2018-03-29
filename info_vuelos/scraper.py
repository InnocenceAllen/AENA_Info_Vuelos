import requests
from info_vuelos import constants
from info_vuelos.domain_model import Flight, Airport
from bs4 import BeautifulSoup

def getContent(url):
    content = requests.get(url).content
    return BeautifulSoup(content, "html.parser")

def getLocalContent(filename):
    fileHandler = open(filename, encoding="utf8")
    return BeautifulSoup(fileHandler, "html.parser")

def getDeparturesContent(airportCode):
    return getContent(constants.AENA_INFOVUELOS_URL + constants.DEPARTURES + airportCode)

def getArrivalsContent(airportCode):
    return getContent(constants.AENA_INFOVUELOS_URL + constants.ARRIVALS + airportCode)

def getAirportName(fullname):
    return fullname[: fullname.find("(")].strip()

def getAirportCode(fullname):
    return fullname[fullname.find("(") + 1:fullname.find(")")].strip()

def getDetails(flightURL):
    return getContent(constants.AENA_BASE_URL + flightURL)

def clean(rawText):
    return rawText.replace("\n", "").strip()

def get_airports(soup):
    airports = []
    origin = soup.find(id="origin_ac")
    resultSet = origin.find_all("option")
    for op in resultSet:
        aiport = Airport(op['value'], getAirportName(op.text))
        airports.append(aiport)
    airports.pop(0)
    return airports

def getFlightInfo(row):
    cells = row.find_all("td")
    time = cells[0].text
    flightNumber = cells[1].a.text.strip()
    url = cells[1].a['href']
    airport = Airport(getAirportCode(cells[2].text), getAirportName(cells[2].text))
    company = cells[3].text.strip()
    terminal = cells[4].text
    return time, flightNumber, airport, company, terminal, url

def getDepartures(airport):
    flights = []
    soup = getDeparturesContent(airport.code)
    tables = soup.find(id="flightResults").findAll("table")
    for table in tables:
        date = clean(table.caption.text.split(",")[-1])
        rows = table.find("tbody").find_all("tr")
        for row in rows:
            if (row["class"][0] == "principal"):
                time, flightNumber, destiny, company, terminal, url = getFlightInfo(row)
                flight = Flight(date, time, flightNumber, airport, destiny, company, terminal, url)
                flights.append(flight)
    return flights

def getArrivals(airport):
    flights = []
    soup = getArrivalsContent(airport.code)
    tables = soup.find(id="flightResults").findAll("table")
    for table in tables:
        date = clean(table.caption.text.split(",")[-1])
        rows = table.find("tbody").find_all("tr")
        for row in rows:
            if (row["class"][0] == "principal"):
                time, flightNumber, origin, company, terminal, url = getFlightInfo(row)
                flight = Flight(date, time, flightNumber, origin, airport, company, terminal, url)
                flights.append(flight)
    return flights


#soup = getLocalContent(constants.LOCAL_INFOVUELOS_URL)
soup = getContent(constants.AENA_INFOVUELOS_URL)
airports = get_airports(soup)
print('Airports\n' + ''.join(str(a)+'; ' for a in airports))

departures = getDepartures(airports[0])
arrivals = getArrivals(airports[0])
print('Departures\n' + ''.join(str(f) + '\n ' for f in departures))
print('Arrivals\n' + ''.join(str(f) + '\n ' for f in arrivals))
