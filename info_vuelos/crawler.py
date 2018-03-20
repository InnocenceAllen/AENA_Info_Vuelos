import requests
from bs4 import BeautifulSoup

def getContent(url):
    content = requests.get(url).content
    return BeautifulSoup(content, "html.parser")

def getLocalContent(filename):
    fileHandler = open(filename, encoding="utf8")
    return BeautifulSoup(fileHandler, "html.parser")