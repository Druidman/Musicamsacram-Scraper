import requests
from bs4 import BeautifulSoup

class Song():
    def __init__(self,link,name):
        response = requests.get(link)
        self.document = BeautifulSoup(response.text,"html.parser")

        self.name = name

        self.get_container()
        self.get_lyrics()
        
    def get_container(self):
        self.text_container = self.document.find(class_="tab-content")

    def get_lyrics(self):
        self.lyrics = self.text_container.p.text
        self.format_lyrics()

    def make_song_model(self):      
        self.model = [self.name,self.lyrics]


    def format_lyrics(self): pass