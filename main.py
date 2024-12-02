from scraper import Scraper
from songs import Song
from document import getDocument

import json


def scrape(document):
    test = input("test mode?: ").upper()
    with open("data.json", "w") as file:
        scraper = Scraper(document)

        scraped_data = {"SampleDataSongs": []}

        scraper.get_elements()
        for element in scraper.elements:
            song_reference = element.a
            if not song_reference:
                continue
            name = song_reference.text
            link = song_reference['href']

            song = Song(link,name)
            song.make_song_model()
            
            scraped_data["SampleDataSongs"].append(song.model)
            if test == "Y":
                return

            
            
        data  = json.dumps(scraped_data)
        file.write(data)
        file.close()

document = getDocument()
scrape(document)