import requests
import constants
import crawler
import utils
import re
from bs4 import BeautifulSoup

''''
Nota:Helmut
Este espacio es para especificar las mejoras.
Falta crear una clase y mover el objeto FlightLine
Falta añadir las llegadas ( es llamar a la parte de salidas que tenemos pero con la URL de llegadas)
Falta añadir la verificación de vuelos duplicados como indico Mario.

'''

class FlightLine:
    def __init__(self,airportCode, hora, destino, vuelo,cia,terminal,url):
        self.airportCode = airportCode.replace("\n", "").strip()
        self.hora = hora.replace("\n","").strip()
        self.destino = destino.replace("\n","").strip()
        self.vuelo = vuelo.replace("\n","").strip()
        self.cia = cia.replace("\n", "").strip()
        self.terminal = terminal.replace("\n", "").strip()
        self.url=url;
        self.flightsInfo =loadFromURL(url);
        #print(self);

    def __str__(self):
        str=airportCode+";"+self.hora+";"+self.destino+";"+self.vuelo+";"+self.cia+";"+self.terminal
        for flightInfo in  self.flightsInfo:
            str=str+flightInfo
        return str




def loadFromURL(url):
        #print (url)
        soup=BeautifulSoup(crawler.getContent(url), "html.parser")

        try:
            tables = soup.findAll("table")
        except:
            pass;
        tableIndex = 0
        flightInfo = []
        for table in tables:
            rows = table.find("tbody").find_all("tr")

            for row in rows:
                #print(getFlightInfo(row))
                flightInfo.append(getFlightInfo(row))


        return  flightInfo

def getFlightInfo(row):
    cells = row.find_all("td")
    date = cells[0].text
    time = cells[1].text
    terminal = cells[2].text
    counter = cells[3].text.strip()
    door = cells[4].text
    state=cells[5].text

    #return date,time, counter, door, terminal, state
    return ";"+ date+";"+ time+";"+ counter+";"+door+";"+ terminal+";"+ state


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
flightLines=[]
for airport in airports:
    airportCode=airport[0]
    #print(airportCode)
    soup = BeautifulSoup(getDepartures(airportCode),"html.parser")

    flightResultsTag = soup.find(id="flightResults")
    try:
        tables = flightResultsTag.findAll("table")
    except:
        break;#hay que revisar los que fallan
    tableIndex = 0

    for table in tables:
        '''when = table.caption.text.split(",")[-1]
        print(when)'''
        rows = table.find("tbody").find_all("tr")
        for row in rows:
            flightURL=constants.AENA_URL+ row.a['href']
            flightNumer = row.a.text

            '''hora=cleanhtml(str(row.find(headers="hora_0")))
            destino = cleanhtml(str(row.find(headers="destino_0")))'''
            hora = cleanhtml(str(row.find(headers=re.compile(constants.HORA))))
            destino = cleanhtml(str(row.find(headers=re.compile(constants.DESTINO))))
            cia = cleanhtml(str(row.find(headers=re.compile(constants.CIA))))
            terminal = cleanhtml(str(row.find(headers=re.compile(constants.TERMINAL))))



            flightLines.append(FlightLine(airportCode,hora,destino,flightNumer,cia,terminal,flightURL))
            '''hora=soup.find_all(headers="hora_1")'''
            #print("--------------------------------")
            #print(hora +""+destino+""+ flightNumer+""+cia+""+terminal)
            #print("--------------------------------")
    utils.createCSV("test4.csv", flightLines)


