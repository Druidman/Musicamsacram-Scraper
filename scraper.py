import requests, json

from bs4 import BeautifulSoup
import re

def scrape_list_element(document):
    table = document.find(class_="table-responsive")
    body = table.tbody
    elements = body.find_all("td")
    return elements

def getDocument():
    check = input("Update?: (Y or N)").upper()
    if check == "Y":
        data = requests.get("https://musicamsacram.pl/spiewnik/kategorie/17-hymny")
        data = data.text
        with open("data.txt", "w") as file:
            file.write(data)
            file.close()

    else:
        with open("data.txt", "r") as file:
            lines = file.readlines()
            file.close()
        data = ""
        for line in lines:
            data += line
    document = BeautifulSoup(data,"html.parser")

    return document

document = getDocument()
element = scrape_list_element()
