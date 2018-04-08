from enum import Enum


class FlightInfoMode(Enum):
    DEPARTURE = 1
    ARRIVAL = 2


class FlightType(Enum):
    NATIONAL = 1
    INTERNATIONAL_DESTINY = 2
    INTERNATIONAL_ORIGIN = 3


class Weather:
    def __init__(self, min, max, description):
        self.min = min
        self.max = max
        self.description = description

    def __str__(self):
        return '{} {} {}'.format(self.min, self.max, self.description)

    def __repr__(self):
        return '{};{};{}'.format(self.min, self.max, self.description)


class Airport:
    def __init__(self, code, name):
        self.code = code
        self.name = name

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
    def __init__(self, flight_number, company, plane, departure, arrival, flight_type, url, timestamp):
        self.flightNumber = flight_number
        self.company = company
        self.plane = plane
        self.departure = departure
        self.arrival = arrival
        self.type = flight_type
        self.url = url
        self.timestamp = timestamp
        key_suffix = departure.key if flight_type == FlightType.INTERNATIONAL_DESTINY else arrival.key
        self.key = '{}{}'.format(flight_number, key_suffix)

    def __str__(self):
        return '{} {} [{}] -> [{}]'.format(self.flightNumber, self.plane, self.departure, self.arrival)

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
        self.date = date
        self.time = time
        self.airport = airport
        self.terminal = terminal
        self.status = status
        self.weather = weather
        self.key = '{}{}'.format(date, time)

    def __str__(self):
        return '{} {} {} {} {} {}'.format(self.date, self.time, self.airport, self.terminal, self.status, self.weather)

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
        self.counter = counter
        self.door = door

    def __str__(self):
        return super().__str__() + ' {} {}'.format(self.counter, self.door)

    def __repr__(self):
        return super().__repr__() + '{};{}'.format(self.counter, self.door)


class Arrival(FlightSchedule):
    def __init__(self, date, time, airport, terminal, status, weather, room, belt):
        super().__init__(date, time, airport, terminal, status, weather)
        self.room = room
        self.belt = belt

    def __str__(self):
        return super().__str__() + ' {} {}'.format(self.room, self.belt)

    def __repr__(self):
        return super().__repr__() + '{};{}'.format(self.room, self.belt)
