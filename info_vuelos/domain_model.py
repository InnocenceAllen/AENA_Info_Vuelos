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
    def __init__(self, date, ueriríatime, flight_number, origin, destiny, company, terminal, url):
        self.date = date
        self.time = time
        self.flightNumber = flight_number
        self.origin = origin
        self.destiny = destiny
        self.company = company
        self.terminal = terminal
        self.url = url

    def __str__(self):
        return '{} {} {} from {} to {}'.format(self.date, self.time, self.flightNumber, self.origin,
                                               self.destiny)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (self.date, self.flightNumber) == (other.date, other.flightNumber)

    def __hash__(self):
        return hash((self.date, self.flightNumber))