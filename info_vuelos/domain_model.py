from enum import Enum

import datetime


class FlightInfoMode(Enum):
    DEPARTURE = 1
    ARRIVAL = 2


class FlightType(Enum):
    NATIONAL = 1
    INTERNATIONAL_DESTINY = 2
    INTERNATIONAL_ORIGIN = 3


class Weather:
    def __init__(self, min, max, description):
        self.min = min or '-'
        self.max = max or '-'
        self.description = description or '-'

    def __str__(self):
        return '{} {} {}'.format(self.min, self.max, self.description)

    def __repr__(self):
        return '{};{};{}'.format(self.min, self.max, self.description)


class Airport:
    def __init__(self, code, name):
        self.code = code or '-'
        self.name = name or '-'

    def __str__(self):
        return '{} ({})'.format(self.name, self.code)

    def __repr__(self):
        return '{};{}'.format(self.name, self.code)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.code == other.code
        return False

    def __hash__(self):
        return hash(self.code)


class Flight:
    def __init__(self, flight_number, company, plane, departure, arrival, flight_type, url):
        self.flightNumber = flight_number or '-'
        self.company = company or '-'
        self.plane = plane or '-'
        self.departure = departure or Departure(None, None, None, None, None, None, None, None)
        self.arrival = arrival or Arrival(None, None, None, None, None, None, None, None)
        self.type = flight_type or '-'
        self.url = url or '-'
        self.timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        key_suffix = departure.key if flight_type == FlightType.INTERNATIONAL_DESTINY else arrival.key
        self.key = '{}{}'.format(flight_number, key_suffix)

    def __str__(self):
        return '{} from {} to {}'.format(self.flightNumber, self.departure, self.arrival)

    def __repr__(self):
        return '{};{};{};{};{}'.format(self.flightNumber, self.plane, repr(self.departure), repr(self.arrival),
                                       self.timestamp)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (self.flightNumber, self.departure, self.arrival) == (
                other.flightNumber, other.departure, other.arrival)
        return False

    def __hash__(self):
        return hash((self.flightNumber, self.departure, self.arrival))


class FlightSchedule:
    def __init__(self, date, time, airport, terminal, status, weather):
        self.date = date or '-'
        self.time = time or '-'
        self.airport = airport or Airport(None, None)
        self.terminal = terminal or '-'
        self.status = status or '-'
        self.weather = weather or Weather(None, None, None)
        self.key = '{}{}'.format(date, time)

    def __str__(self):
        return '{} ({} {})'.format(self.airport.name, self.date, self.time)

    def __repr__(self):
        return '{};{};{};{};{};{}'.format(self.date, self.time, repr(self.airport), self.terminal, self.status,
                                          repr(self.weather))

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (self.date, self.time) == (
                other.date, other.time, other.airport)
        return False

    def __hash__(self):
        return hash((self.date, self.time))


class Departure(FlightSchedule):
    def __init__(self, date, time, airport, terminal, status, weather, counter, door):
        super().__init__(date, time, airport, terminal, status, weather)
        self.counter = counter or '-'
        self.door = door or '-'

    def __str__(self):
        return super().__str__() + ''

    def __repr__(self):
        return super().__repr__() + ';{};{}'.format(self.counter, self.door)


class Arrival(FlightSchedule):
    def __init__(self, date, time, airport, terminal, status, weather, room, belt):
        super().__init__(date, time, airport, terminal, status, weather)
        self.room = room or '-'
        self.belt = belt or '-'

    def __str__(self):
        return super().__str__() + ''

    def __repr__(self):
        return super().__repr__() + ';{};{}'.format(self.room, self.belt)
