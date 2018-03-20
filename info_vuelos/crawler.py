import requests

def getContent(url):
    content = requests.get(url).content
    return content

def getLocalContent(filename):
    fileHandler = open(filename, encoding="utf8")
    return fileHandler