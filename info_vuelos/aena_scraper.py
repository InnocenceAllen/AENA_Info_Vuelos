import argparse
import logging as log
import threading
import time
import datetime
import queue

from info_vuelos.domain_model import Flight, Airport, FlightInfoMode, FlightType, Departure, Arrival, Weather
from info_vuelos import util, constants


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
    try:
        cells = row.find_all("td")
        # time = cells[0].text
        flightNumber = cells[1].a.text.strip()
        url = cells[1].a['href']
        # airport = Airport(util.getAirportCode(cells[2].text), util.getAirportName(cells[2].text))
        company = cells[3].text.strip()
        # terminal = cells[4].text
        log.info("Scrapping  flight " + flightNumber)
        plane, departure, arrival, type = getFlightDetails(url, flightInfoMode)
        if flightNumber is not None:
            flight = Flight(flightNumber, company, plane, departure, arrival, type, url)
        else:
            flight = None
        print(flight)
        return flight
    except:
        log.error("Error scraping flight details from %s", row)
        return None


def getFlightDetails(relativeUrl, flightInfoMode):
    soup = util.getDetails(relativeUrl)
    table = soup.find("table")
    try:
        plane = table.caption.span.contents[1].strip()

        theads = table.find_all("thead")
        tbodys = table.find_all("tbody")

        if (len(tbodys) > 1):
            departure = getFlightDepartureDetails(theads[0], tbodys[0])
            arrival = getFlightArrivalDetails(theads[1], tbodys[1])
            flight_type = FlightType.NATIONAL
        else:
            if (flightInfoMode == FlightInfoMode.DEPARTURE):
                departure = getFlightDepartureDetails(theads[0], tbodys[0])
                arrival = getFlightArrivalDetails(theads[1], None)
                flight_type = FlightType.INTERNATIONAL_DESTINY
            else:
                departure = getFlightDepartureDetails(theads[0], None)
                arrival = getFlightArrivalDetails(theads[1], tbodys[0])
                flight_type = FlightType.INTERNATIONAL_ORIGIN
        return plane, departure, arrival, flight_type
    except:
        log.error("Error scraping flight details from %s", relativeUrl)
        return None, None, None, None


def getFlightDepartureDetails(thead, tbody):
    tr = thead.tr
    try:
        airport_txt = tr.th.a.text
        airport = Airport(util.getAirportCode(airport_txt), util.getAirportName(airport_txt))
        weather_section = tr.find("span", {"class": "clima"})
        weather_temp = weather_section.contents[1].split()
        weather_desc = tr.img["alt"]
        min_temp = int(weather_temp[0][:-1])
        max_temp = int(weather_temp[1][:-1])
        weather = Weather(min_temp, max_temp, weather_desc)
        cells = tbody.tr.find_all("td", )
        date = cells[0].text
        time = cells[1].text
        terminal = cells[2].text
        counter = cells[3].text
        door = cells[4].text
        if len(cells) == 6:
            status = cells[5].text.strip()
        else:
            status = None
            log.warning('Status not available')
        return Departure(date, time, airport, terminal, status, weather, counter, door)
    except AttributeError as error:
        log.warning('Some field is missing: %s', error)
        return Departure(None, None, airport, None, None, None, None, None)


def getFlightArrivalDetails(thead, tbody):
    tr = thead.tr
    try:
        airport_txt = tr.find(True, {'class': 'aeropVuelo'}).text
        airport = Airport(util.getAirportCode(airport_txt), util.getAirportName(airport_txt))
        weather_section = tr.find("span", {"class": "clima"})
        weather_temp = weather_section.contents[1].split()
        weather_desc = tr.img["alt"]
        min_temp = int(weather_temp[0][:-1])
        max_temp = int(weather_temp[1][:-1])
        weather = Weather(min_temp, max_temp, weather_desc)
        cells = tbody.tr.find_all("td", )
        date = cells[0].text
        time = cells[1].text
        terminal = cells[2].text
        room = cells[3].text
        belt = cells[4].text
        if len(cells) == 6:
            status = cells[5].text.strip()
        else:
            status = None
            log.warning('Status not available')
        return Arrival(date, time, airport, terminal, status, weather, room, belt)
    except AttributeError as error:
        log.warning('Some field is missing: %s', error)
        return Arrival(None, None, airport, None, None, None, None, None)


def getDepartures(airport):
    flights = []
    soup = util.getDeparturesContent(airport.code)
    try:
        tables = soup.find(id="flightResults").findAll("table")
        for table in tables:
            # date = table.caption.text.split(",")[-1].strip()
            rows = table.find("tbody").find_all("tr")
            for row in rows:
                if row["class"][0] == "principal":
                    flight = getFlightInfo(row, FlightInfoMode.DEPARTURE)
                    if flight is not None:
                        flights.append(flight)
                        log.info('Departure: %s', flight)
    except AttributeError:
        log.error('Error scrapping departures from airport %s', airport)
    return flights


def getArrivals(airport):
    flights = []
    soup = util.getArrivalsContent(airport.code)
    try:
        tables = soup.find(id="flightResults").findAll("table")
        for table in tables:
            # date = table.caption.text.split(",")[-1].strip()
            rows = table.find("tbody").find_all("tr")
            for row in rows:
                if row["class"][0] == "principal":
                    flight = getFlightInfo(row, FlightInfoMode.ARRIVAL)
                    if flight is not None:
                        flights.append(flight)
                        log.info('Arrival: %s', flight)
    except AttributeError:
        log.error('Error scraping arrivals to airport %s', airport)
    return flights


def obtainAirportFlights(airport, queue):
    log.info('Scraping flights for airport {}'.format(airport))
    print('Scraping flights for airport {}'.format(airport))
    departures = getDepartures(airport)
    queue.put(departures)
    arrivals = getArrivals(airport)
    queue.put(arrivals)


def drain(q):
  while True:
    try:
      yield q.get_nowait()
    except queue.Empty:
      break

def obtainFlights(airports, filename, end_time, frequency):
    log.info('Scrapping flights starting at {}'.format(datetime.datetime.now()))
    print('\n********** SCRAPING CYCLE STARTED: {}\n'.format(datetime.datetime.now()))
    pool = []
    q = queue.Queue()
    for airport in airports:
        pool.append(threading.Thread(
            target=obtainAirportFlights,
            name='Thread-' + airport.code,
            args=[airport, q]))

    for thread in pool:
        thread.start()

    for thread in pool:
        thread.join()

    for item in drain(q):
        util.save_to_csv(filename, item)

    print('\n********** SCRAPING CYCLE COMPLETED: {}\n'.format(datetime.datetime.now()))

    if (datetime.datetime.now() < end_time):
        threading.Timer(frequency * 60, obtainFlights, [airports, filename, end_time, frequency]).start()


def main(period, frequency):
    filename = 'flights{}.csv'.format(time.strftime("%d-%m-%Y_%I-%M"))
    util.create_csv(filename, constants.DATA_FIELDS, constants.CSV_DELIMITER)

    airports = get_airports(util.getAirportsContent())
    log.info('Scrapping airport names')
    log.info(''.join(str(a) + '; ' for a in airports))

    #util.create_csv("airports.csv", ['airport_name', 'airport_code'], constants.CSV_DELIMITER)
    #util.save_to_csv("airports.csv", airports)

    current_time = datetime.datetime.now()
    end_time = current_time + datetime.timedelta(hours=period)
    obtainFlights(airports, filename, end_time, frequency)
    log.info('Scrapping flights finished at {}'.format(datetime.datetime.now()))


if __name__ == "__main__":
    log.basicConfig(filename='scrapping{}.log'.format(time.strftime("%d-%m-%Y_%I-%M")), level=log.WARNING,
                    format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S')
    parser = argparse.ArgumentParser('Scrape flight info from AENA Infovuelos webpage')
    parser.add_argument('-p','--period', help ='scraping period in hours')
    parser.add_argument('-f','--frequency', help = 'scraping frecuency in minutes')
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()

    period = int(args.period or constants.SCRAPING_PERIOD)
    frequency = int(args.frequency or constants.SCRAPING_FRECUENCY)

    print('Scraping period is {} hours'.format(period))
    print('Scraping file is {} minutes'.format(frequency))
    main(period, frequency)
