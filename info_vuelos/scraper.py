from info_vuelos.domain_model import Flight, Airport
from info_vuelos import util

def get_airports(soup):
    airports = []
    origin = soup.find(id="origin_ac")
    resultSet = origin.find_all("option")
    for op in resultSet:
        aiport = Airport(op['value'], util.getAirportName(op.text))
        airports.append(aiport)
    airports.pop(0)
    return airports

def getFlightInfo(row):
    cells = row.find_all("td")
    time = cells[0].text
    flightNumber = cells[1].a.text.strip()
    url = cells[1].a['href']
    airport = Airport(util.getAirportCode(cells[2].text), util.getAirportName(cells[2].text))
    company = cells[3].text.strip()
    terminal = cells[4].text
    return time, flightNumber, airport, company, terminal, url

def getDepartures(airport):
    flights = []
    soup = util.getDeparturesContent(airport.code)
    tables = soup.find(id="flightResults").findAll("table")
    for table in tables:
        date = table.caption.text.split(",")[-1].strip()
        rows = table.find("tbody").find_all("tr")
        for row in rows:
            if row["class"][0] == "principal":
                time, flightNumber, destiny, company, terminal, url = getFlightInfo(row)
                flight = Flight(date, time, flightNumber, airport, destiny, company, terminal, url)
                flights.append(flight)
    return flights

def getArrivals(airport):
    flights = []
    soup = util.getArrivalsContent(airport.code)
    tables = soup.find(id="flightResults").findAll("table")
    for table in tables:
        date = table.caption.text.split(",")[-1].strip()
        rows = table.find("tbody").find_all("tr")
        for row in rows:
            if row["class"][0] == "principal":
                time, flightNumber, origin, company, terminal, url = getFlightInfo(row)
                flight = Flight(date, time, flightNumber, origin, airport, company, terminal, url)
                flights.append(flight)
    return flights

airports = get_airports(util.getAirportsContent())
print('Airports\n' + ''.join(str(a)+'; ' for a in airports))

flights = []
uniqueFlights = set()
for airport in airports:
    departures = getDepartures(airport)
    arrivals = getArrivals(airport)
    flights = flights + departures + arrivals
    uniqueFlights.update(departures)
    uniqueFlights.update(arrivals)


print('Number of flights including duplicates = {}'.format(len(flights)))
print('Number of flights removing duplicates = {}'.format(len(uniqueFlights)))

#print('Flights\n' + ''.join(str(f) + '\n ' for f in flights))