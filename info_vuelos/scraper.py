import logging as log
import threading
import time
import datetime

import constants
from info_vuelos.domain_model import Flight, Airport, FlightInfoMode, FlightType, Departure, Arrival, Weather
from info_vuelos import util


# global output
# orig_stdout = sys.stdout
# date = time.strftime("%d-%m-%Y_%I-%M")
# f = open('flight' + date + '.csv', 'w')
# sys.stdout = f
# print(constants.HEADER)

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
        plane = table.caption.span.contents[1]

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

def obtainFlights(airports, filename, end_time):
    log.info('Scrapping flights at {}'.format(datetime.datetime.now()))
    for airport in airports:
        log.info('Scraping departures from airport {}'.format(airport))
        departures = getDepartures(airport)
        log.info('Saving {} departures from airport {}'.format(len(departures), airport))
        util.save_to_csv(filename, departures)
        log.info('Scraping arrivals to airport {}'.format(airport))
        arrivals = getArrivals(airport)
        log.info('Saving {} arrivals to airport {}'.format(len(arrivals), airport))
        util.save_to_csv(filename, arrivals)
        print('\n*****************************************\n')
    if (datetime.datetime.now() < end_time):
        threading.Timer(constants.SCRAPING_FRECUENCY*90, obtainFlights,[airports,filename, end_time])

def main():

    filename = 'flights{}.csv'.format(time.strftime("%d-%m-%Y_%I-%M"))
    util.create_csv(filename, constants.DATA_FIELDS, constants.CSV_DELIMITER)

    airports = get_airports(util.getAirportsContent())
    log.info('Scrapping airport names')
    log.info(''.join(str(a) + '; ' for a in airports))

    current_time = datetime.datetime.now()
    end_time = current_time + datetime.timedelta(hours=72)
    obtainFlights(airports, filename, end_time)
    log.info('Scrapping flights finished at {}'.format(datetime.datetime.now()))


if __name__ == "__main__":
    # log.basicConfig(filename='scrapping.log', level=log.INFO)
    log.basicConfig(filename='scrapping.log', level=log.WARNING, format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S')
    main()
