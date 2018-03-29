class Airport:
    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        return '{} ({})'.format(self.name, self.code)


class Flight:
    def __init__(self, date, time, flight_number, origin, destiny, company, terminal, url):
        self.flightNumber = flight_number
        self.origin = origin
        self.date = date
        self.time = time
        self.origin = origin
        self.destiny = destiny
        self.company = company
        self.terminal = terminal
        self.url = url

    def __str__(self):
        return '{} {} {} from {} to {}'.format(self.date, self.time, self.flightNumber, self.origin,
                                               self.destiny)
