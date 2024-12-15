from scraper import getCategoryObjects, getSongObjects, getVerses
from document import getDocument
import requests
from bs4 import BeautifulSoup




    

mainLink = "https://musicamsacram.pl/spiewnik/kategorie"
mainDocument = getDocument(link=mainLink)


categoryObjects = getCategoryObjects(mainDocument=mainDocument)

for categoryObj in categoryObjects:
    category = categoryObj["category"]
    categoryLink = categoryObj["link"]

    categoryDocument = getDocument(link=categoryLink)
    songObjects = getSongObjects(categoryDocument=categoryDocument)

    for songObj in songObjects:
        title = songObj["title"]
        songLink = songObj["link"]

        songDocument = getDocument(link=songLink)
        verses = getVerses(songDocument=songDocument)
        print(verses)
    
        


    break

    


"""
    {
        "data": {
            "categories": {
                "< CATEGORY NAME >": [
                    {
                        "name": "< NAME >",
                        "lyrics": [
                            "< verse >",
                            "< VERSE >"
                        ]
                    }
                ]
            }
        }
    }
"""