import requests
from bs4 import BeautifulSoup

def getDocument(link):
    data = requests.get(link)
    data = data.text
    
    document = BeautifulSoup(data,"html.parser")

    return document
