from scraper import *
from document import getDocument
import json
from threading import Thread

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

def handleSong(songObj,songs):
    title = songObj["title"]
    songLink = songObj["link"]
    print(f"           with link: {songLink}")
    

    songDocument = getDocument(link=songLink)
    verses = getVerses(songDocument=songDocument)
    song = {
        "title": title,
        "lyrics": []
        }
    
    appendVersesToSong(song,verses)

    filterLyrics(song)
    
    songs.append(song)

def handlePage(pageLink,songs):
    
    pageDocument = getDocument(link=pageLink)
    songObjects = getSongObjects(pageDocument=pageDocument)
    
    threads = []
    for songObj in songObjects:
        thread = Thread(target=handleSong,args=(songObj,songs))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

def handleCategory(categoryObj,data):
    category = categoryObj["category"]
    categoryLink = categoryObj["link"]
    print(f"starting work on: {category} category")
    print(f"link {categoryLink}")

    categoryDocument = getDocument(link=categoryLink)
    pageLinks = getPageLinks(categoryDocument=categoryDocument,firstLink=categoryLink)
    print("got page links")
    songs = []


    threads = []
    for pageLink in pageLinks:
        thread = Thread(target=handlePage,args=(pageLink,songs))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
        
            
        
        
    data["data"]["categories"][category] = songs

    

mainLink = "https://musicamsacram.pl/spiewnik/kategorie"
mainDocument = getDocument(link=mainLink)

data = {
    "data": {
        "categories": {

        }
    }}

print("Scraper start...\n\n")
categoryObjects = getCategoryObjects(mainDocument=mainDocument)
print("Got categories\n")

threads = []
for categoryObj in categoryObjects:
    thread = Thread(target=handleCategory,args=(categoryObj,data))
    threads.append(thread)
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    
    print("\n\nassigned songs to category\n\n")
    break
        
    


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
