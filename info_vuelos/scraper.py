from info_vuelos.domain_model import Flight, Airport, FlightSchedule, FlightInfoMode, FlightType
from info_vuelos import util
import logging as log

def get_airports(soup):
    airports = []
    origin = soup.find(id="origin_ac")
    resultSet = origin.find_all("option")
    resultSet.pop(0)
    for op in resultSet:
        aiport = Airport(op['value'], util.getAirportName(op.text))
        airports.append(aiport)
    return airports

def getFlightInfo(row, flightInfoMode):
    cells = row.find_all("td")
    #time = cells[0].text
    flightNumber = cells[1].a.text.strip()
    url = cells[1].a['href']
    #airport = Airport(util.getAirportCode(cells[2].text), util.getAirportName(cells[2].text))
    company = cells[3].text.strip()
    #terminal = cells[4].text
    log.info("Scrapping  flight " + flightNumber)
    plane, departure, arrival, type = getFlightDetails(url, flightInfoMode)
    return Flight(flightNumber, company, plane, departure, arrival, type, url)

def getFlightDetails(relativeUrl, flightInfoMode):
    soup = util.getDetails(relativeUrl)
    table = soup.find("table")
    if (table is not None):
        plane = table.caption.span.contents[1]

        theads = table.find_all("thead")
        tbodys = table.find_all("tbody")

        if (len(tbodys)>1):
            departure = getFlightSchedule(theads[0], tbodys[0])
            arrival = getFlightSchedule(theads[1], tbodys[1])
            flight_type = FlightType.NATIONAL
        else:
            if (flightInfoMode == FlightInfoMode.DEPARTURE):
                departure = getFlightSchedule(theads[0], tbodys[0])
                arrival = getFlightSchedule(theads[1], None)
                flight_type = FlightType.INTERNATIONAL_DESTINY
            else:
                departure = getFlightSchedule(theads[0], None)
                arrival =  getFlightSchedule(theads[1], tbodys[0])
                flight_type = FlightType.INTERNATIONAL_ORIGIN
        return plane, departure, arrival, flight_type
    else:
        log.debug("Error in url " + relativeUrl)
        return None, None, None, None

def getFlightSchedule(thead, tbody):
    tr = thead.tr
    try:
        airport_txt = tr.th.a.text
        airport = Airport(util.getAirportCode(airport_txt), util.getAirportName(airport_txt))
        weather_section = tr.find("span", {"class":"clima"})
        weather_temp = weather_section.contents[1]
        weather_desc = tr.img["alt"]
        weather = "{} {}".format(weather_temp, weather_desc)
        cells = tbody.tr.find_all("td", )
        date = cells[0].text
        time = cells[1].text
        terminal = cells[2].text
        if len(cells) == 6:
            status = cells[5].text
        else:
            status = None
            log.warning('Status not available')
        return FlightSchedule(date, time, airport, terminal, status, weather)
    except AttributeError:
        airport_txt = tr.find_all("span")[1].text
        return Airport(util.getAirportCode(airport_txt), util.getAirportName(airport_txt))

def getDepartures(airport):
    flights = []
    soup = util.getDeparturesContent(airport.code)
    try:
        tables = soup.find(id="flightResults").findAll("table")
        for table in tables:
            date = table.caption.text.split(",")[-1].strip()
            rows = table.find("tbody").find_all("tr")
            for row in rows:
                if row["class"][0] == "principal":
                    flight = getFlightInfo(row, FlightInfoMode.DEPARTURE)
                    flights.append(flight)
                    log.info(str(flight))
    except AttributeError:
        log.error('Error scrapping departures from airport %s', airport)
    return flights

def getArrivals(airport):
    flights = []
    soup = util.getArrivalsContent(airport.code)
    try:
        tables = soup.find(id="flightResults").findAll("table")
        for table in tables:
            date = table.caption.text.split(",")[-1].strip()
            rows = table.find("tbody").find_all("tr")
            for row in rows:
                if row["class"][0] == "principal":
                    flight = getFlightInfo(row, FlightInfoMode.ARRIVAL)
                    flights.append(flight)
                    log.info(str(flight))
    except AttributeError:
        log.error('Error scraping arrivals to airport %s', airport)
    return flights

def main():
    airports = get_airports(util.getAirportsContent())
    log.info('Scrapping airport names')
    log.info(''.join(str(a) + '; ' for a in airports))

    log.info('Scrapping flights')
    flights = []
    for airport in airports:
        departures = getDepartures(airport)
        arrivals = getArrivals(airport)
        flights = flights + departures + arrivals

    log.info('Number of flights (departures + arrivals) = {}'.format(len(flights)))


if __name__ == "__main__":
    #log.basicConfig(filename='scrapping.log', level=log.INFO)
    log.basicConfig(level=log.INFO, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S')
    main()