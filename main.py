from scraper import *
from document import getDocument
import json
from threading import Thread

errors = {
    "SONGTHREADS":[],
    "PAGETHREADS":[],
    "CATEGORYTHREADS":[]
}

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
    try:
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
    except Exception as e:
        print(f"\n\nAn error occured in !! SONGTHREAD !! \n Error: {e}\n\n")
        errorObj = {
            "ErrorMsg": f"{e}",
            "Link": songLink
        }
        errors["SONGTHREADS"].append(errorObj)

def handlePage(pageLink,songs):
    try:
        pageDocument = getDocument(link=pageLink)
        songObjects = getSongObjects(pageDocument=pageDocument)
        
        songThreads = []
        for songObj in songObjects:
            thread = Thread(target=handleSong,args=(songObj,songs))
            songThreads.append(thread)

        for thread in songThreads:
            thread.start()

        for thread in songThreads:
            thread.join()
    except Exception as e:
        print(f"\n\nAn error occured in !! PAGETHREAD !! \n Error: {e}\n\n")
        errorObj = {
            "ErrorMsg": f"{e}",
            "Link": pageLink
        }
        errors["PAGETHREADS"].append(errorObj)

def handleCategory(categoryObj,data):
    try:
        category = categoryObj["category"]
        categoryLink = categoryObj["link"]
        print(f"starting work on: {category} category")
        print(f"link {categoryLink}")

        categoryDocument = getDocument(link=categoryLink)
        pageLinks = getPageLinks(categoryDocument=categoryDocument,firstLink=categoryLink)
        print("got page links")
        songs = []


        pageThreads = []
        for pageLink in pageLinks:
            thread = Thread(target=handlePage,args=(pageLink,songs))
            pageThreads.append(thread)

        for thread in pageThreads:
            thread.start()

        for thread in pageThreads:
            thread.join()
        
        data["data"]["categories"][category] = songs
    except Exception as e:
        print(f"\n\nAn error occured in !! CATEGORYTHREAD !! \n Error: {e}\n\n")
        errorObj = {
            "ErrorMsg": f"{e}",
            "Link": categoryLink
        }
        errors["CATEGORYTHREADS"].append(errorObj)


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

categoryThreads = []
for categoryObj in categoryObjects:
    thread = Thread(target=handleCategory,args=(categoryObj,data))
    categoryThreads.append(thread)
    

for thread in categoryThreads:
    thread.start()

for thread in categoryThreads:
    thread.join()
    
print("\n\nassigned songs to category\n\n")
   
data = json.dumps(data)

with open("songsData.json","w") as JSONfile:
    JSONfile.write(data)
    JSONfile.close()


errors = json.dumps(errors)

with open("errors.json","w") as ErrorsFile:
    ErrorsFile.write(errors)
    ErrorsFile.close()

    


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
