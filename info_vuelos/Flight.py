class Flight:
    def __init__(self, date, time, flight_number, origin, origin_code, destiny, destiny_code, company, terminal):
        self.flightNumber = flight_number
        self.origin = origin
        self.date = date
        self.time = time
        self.origin = origin
        self.originCode = origin_code
        self.destiny = destiny
        self.destinyCode = destiny_code
        self.company = company
        self.terminal = terminal

    def __str__(self):
        return '{} {} {} from {} to {}'.format(self.date, self.time, self.flightNumber, self.origin,
                                                         self.destiny)
