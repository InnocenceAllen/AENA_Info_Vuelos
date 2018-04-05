from enum import Enum

class FlightInfoMode(Enum):
    DEPARTURE = 1
    ARRIVAL = 2

class FlightType(Enum):
    NATIONAL = 1
    INTERNATIONAL_DESTINY = 2
    INTERNATIONAL_ORIGIN = 3

class Airport:
    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        return '{} ({})'.format(self.name, self.code)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.code == other.code
        return False

    def __hash__(self):
        return hash(self.code)

class Flight:
    def __init__(self, flight_number, company, plane, departure, arrival, type, url):
        self.flightNumber = flight_number
        self.company = company
        self.plane = plane
        self.departure = departure
        self.arrival = arrival
        self.type = type
        self.url = url

    def __str__(self):
        return '{} {} [{}] -> [{}]'.format(self.flightNumber, self.plane, str(self.departure),  str(self.arrival))


    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (self.flightNumber, self.departure, self.arrival) == (other.flightNumber, other.departure, other.arrival)

    def __hash__(self):
        return hash((self.flightNumber, self.departure, self.arrival))


class FlightSchedule:
    def __init__(self, date, time, airport, terminal, status, weather):
        self.date = date
        self.time = time
        self.airport = airport
        self.terminal = terminal
        self.status = status
        self.weather = weather

    def __str__(self):
        return '{} {} {} {} {} {}'.format(self.date, self.time, self.airport, self.terminal, self.status, self.weather)

class Departure (FlightSchedule):
    def __init__(self, date, time, airport, terminal, status, counter, door):
        FlightSchedule.__init__(date, time, airport, terminal, status)
        self.counter = counter
        self.door = door

class Arrival (FlightSchedule):
    def __init__(self, date, time, terminal, status, room, belt):
        FlightSchedule.__init__(date, time, terminal, status)
        self.room = room
        self.belt = belt
