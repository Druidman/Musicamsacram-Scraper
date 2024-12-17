from scraper import *
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

print("Scraper start...\n\n")
categoryObjects = getCategoryObjects(mainDocument=mainDocument)
print("Got categories\n")
for categoryObj in categoryObjects:
    
    
    category = categoryObj["category"]
    categoryLink = categoryObj["link"]
    print(f"starting work on: {category} category")
    print(f"link {categoryLink}")

    categoryDocument = getDocument(link=categoryLink)
    pageLinks = getPageLinks(categoryDocument=categoryDocument,firstLink=categoryLink)
    print("got page links")
    songs = []
    i = 1
    for pageLink in pageLinks:
        pageDocument = getDocument(link=pageLink)
        songObjects = getSongObjects(pageDocument=pageDocument)
        
        
        for songObj in songObjects:
            title = songObj["title"]
            songLink = songObj["link"]
            print(f"           {i} with link: {songLink}")
            i+=1

            songDocument = getDocument(link=songLink)
            verses = getVerses(songDocument=songDocument)
            song = {
                "title": title,
                "lyrics": []
                }
            
            appendVersesToSong(song,verses)

            filterLyrics(song)
            
            songs.append(song)
            
        
        
    data["data"]["categories"][category] = songs
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
