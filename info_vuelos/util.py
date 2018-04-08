import csv

import requests
from collections import OrderedDict
from info_vuelos import constants
from bs4 import BeautifulSoup


def getContent(url):
    content = requests.get(url).content
    return BeautifulSoup(content, "html.parser")


def getLocalContent(filename):
    fileHandler = open(filename, encoding="utf8")
    return BeautifulSoup(fileHandler, "html.parser")


def getAirportsContent():
    return getContent(constants.AENA_INFOVUELOS_URL)


def getDeparturesContent(airportCode):
    return getContent(constants.AENA_INFOVUELOS_URL + constants.DEPARTURES + airportCode)


def getArrivalsContent(airportCode):
    return getContent(constants.AENA_INFOVUELOS_URL + constants.ARRIVALS + airportCode)


def getAirportName(fullname):
    return fullname[: fullname.find("(")].strip()


def getAirportCode(fullname):
    return fullname[fullname.find("(") + 1:fullname.find(")")].strip()


def getDetails(flightURL):
    return getContent(constants.AENA_BASE_URL + flightURL)


def clean(rawText):
    return rawText.replace("\n", "").strip()


def unique(a):
    return OrderedDict.fromkeys(a).keys()


def unique_everseen(iterable):
    seen = set()
    for element in iterable:
        if element not in seen:
            seen.add(element)
            yield element


def save_to_csv(filename, data):
    with open(filename, 'a', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(map(lambda x: [repr(x)], data))
