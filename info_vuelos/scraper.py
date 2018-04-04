from info_vuelos.domain_model import Flight, Airport, FlightSchedule
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
    #time = cells[0].text
    flightNumber = cells[1].a.text.strip()
    url = cells[1].a['href']
    #airport = Airport(util.getAirportCode(cells[2].text), util.getAirportName(cells[2].text))
    company = cells[3].text.strip()
    #terminal = cells[4].text

    plane, departure, arrival = getFlightDetails(url)
    return Flight(flightNumber, company, plane, departure, arrival)

def getFlightDetails(relativeUrl):
    soup = util.getDetails(relativeUrl)
    table = soup.find("table")
    plane = table.caption.find_all("span")[1]

    theads = table.find_all("thead")
    tbodys = table.find_all("tbody")

    departure = getFlightSchedule(theads[0], tbodys[0])
    if (len(tbodys)>1):
        arrival =  getFlightSchedule(theads[1], tbodys[1])
    else:
        arrival = getFlightSchedule(theads[1], None)

    return plane, departure, arrival

def getFlightSchedule(thead, tbody):
    tr = thead.tr
    try:
        airport = tr.th.a.text
        weather = tr.img["alt"]
        cells = tbody.tr.find_all("td", )
        date = cells[0].text
        time = cells[1].text
        terminal = cells[2].text
        status = cells[5].text
        return FlightSchedule(date, time, airport, terminal, status, weather)
    except AttributeError:
        airport = tr.find_all("span")[1].text
        return Airport(util.getAirportCode(airport), util.getAirportName(airport))



def getDepartures(airport):
    flights = []
    soup = util.getDeparturesContent(airport.code)
    tables = soup.find(id="flightResults").findAll("table")
    for table in tables:
        date = table.caption.text.split(",")[-1].strip()
        rows = table.find("tbody").find_all("tr")
        for row in rows:
            if row["class"][0] == "principal":
                flight = getFlightInfo(row)
                print(flight)
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
                flight = getFlightInfo(row)
                print(flight)
                flights.append(flight)
    return flights

airports = get_airports(util.getAirportsContent())
print('Airports\n' + ''.join(str(a)+'; ' for a in airports))

flights = []
#uniqueFlights = set()
for airport in airports:
    departures = getDepartures(airport)
    arrivals = getArrivals(airport)
    flights = flights + departures + arrivals
    #uniqueFlights.update(departures)
    #uniqueFlights.update(arrivals)


print('Number of flights (departures + arrivals) = {}'.format(len(flights)))
#print('Number of flights removing duplicates = {}'.format(len(uniqueFlights)))

#print('Flights\n' + ''.join(str(f) + '\n ' for f in flights))