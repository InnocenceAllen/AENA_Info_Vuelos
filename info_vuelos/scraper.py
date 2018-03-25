import requests
import constants
import crawler
import utils
import re
from bs4 import BeautifulSoup


class FlightLine:
    def __init__(self, hora, destino, vuelo,cia,terminal):
        self.hora = hora.replace("\n","").strip()
        self.destino = destino.replace("\n","").strip()
        self.vuelo = vuelo.replace("\n","").strip()
        self.cia = cia.replace("\n", "").strip()
        self.terminal = terminal.replace("\n", "").strip()

    def __str__(self):

        return self.hora+";"+self.destino+";"+self.vuelo+";"+self.cia+";"+self.terminal


def getContent(url):
    content = requests.get(url).content
    return BeautifulSoup(content, "html.parser")

def getLocalContent(filename):
    fileHandler = open(filename, encoding="utf8")
    return BeautifulSoup(fileHandler, "html.parser")

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def get_airports(soup):
    airports = []
    origin = soup.find(id="origin_ac")
    resultSet = origin.find_all("option")
    for op in resultSet:
        airports.append([op['value'], op.text.strip()])
    airports.pop(0)
    return airports

def getDepartures(airportCode):
    return crawler.getContent(constants.AENA_INFOVUELOS_URL + constants.DEPARTURES + airportCode)

def getArrivals(airportCode):
    return crawler.getContent(constants.AENA_INFOVUELOS_URL + constants.ARRIVALS + airportCode)

soup = BeautifulSoup(crawler.getLocalContent(constants.LOCAL_INFOVUELOS_URL), "html.parser")
airports = get_airports(soup)
code = airports[0][0]

soup = BeautifulSoup(crawler.getLocalContent(constants.LOCAL_SAMPLE_DEPARTURES), "html.parser")

flightResultsTag = soup.find(id="flightResults")
tables = flightResultsTag.findAll("table")
tableIndex = 0
flightLines=[]
for table in tables:
    '''when = table.caption.text.split(",")[-1]
    print(when)'''
    rows = table.find("tbody").find_all("tr")
    for row in rows:
        flightNumer = row.a.text

        '''hora=cleanhtml(str(row.find(headers="hora_0")))
        destino = cleanhtml(str(row.find(headers="destino_0")))'''
        hora = cleanhtml(str(row.find(headers=re.compile(constants.HORA))))
        destino = cleanhtml(str(row.find(headers=re.compile(constants.DESTINO))))
        cia = cleanhtml(str(row.find(headers=re.compile(constants.CIA))))
        terminal = cleanhtml(str(row.find(headers=re.compile(constants.TERMINAL))))



        flightLines.append(FlightLine(hora,destino,flightNumer,cia,terminal))
        '''hora=soup.find_all(headers="hora_1")'''
        print("--------------------------------")
        print(hora +""+destino+""+ flightNumer+""+cia+""+terminal)
        print("--------------------------------")
utils.createCSV("test.csv", flightLines)


