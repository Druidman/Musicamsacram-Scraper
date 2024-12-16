from scraper import getCategoryObjects, getSongObjects, getVerses
from document import getDocument
import json

def appendVersesToSong(song: dict, verses: list):
    for verse in verses:
        song["lyrics"].append(verse)


def filterLyrics(song: dict):
    lyrics = []
    for verse in song["lyrics"]:
        if not verse:
            continue

        verse.strip()
        lyrics.append(verse)

    song["lyrics"] = lyrics


    
    

mainLink = "https://musicamsacram.pl/spiewnik/kategorie"
mainDocument = getDocument(link=mainLink)

data = {
    "data": {
        "categories": {

        }
    }}


categoryObjects = getCategoryObjects(mainDocument=mainDocument)

for categoryObj in categoryObjects:
    category = categoryObj["category"]
    categoryLink = categoryObj["link"]

    categoryDocument = getDocument(link=categoryLink)
    songObjects = getSongObjects(categoryDocument=categoryDocument)
    songs = []

    for songObj in songObjects:
        title = songObj["title"]
        songLink = songObj["link"]

        songDocument = getDocument(link=songLink)
        verses = getVerses(songDocument=songDocument)
        song = {
            "title": title,
            "lyrics": []
            }
        
        appendVersesToSong(song,verses)

        if not song["lyrics"]:
            continue

        filterLyrics(song)
        
        songs.append(song)
        
    data["data"]["categories"][category] = songs
        
    


data = json.dumps(data)

with open("songsData.json","w") as JSONfile:
    JSONfile.write(data)
    JSONfile.close()

    


"""
JSON FORMAT
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
