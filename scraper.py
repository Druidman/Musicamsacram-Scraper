import re

def getCategoryObjects(mainDocument):
    category_boxes = mainDocument.find_all(class_="panel-heading")

    categoryObjects = []
    for box in category_boxes:
        category = box.a.text
        link = box.a.get("href")
        pair = {
            "category": category,
            "link": link
                }
        categoryObjects.append(pair)
    return categoryObjects

def getSongObjects(categoryDocument):
    song_container = categoryDocument.tbody
    song_boxes = song_container.find_all("tr")

    songObjects = []
    for box in song_boxes:
        title = box.a.text
        link = box.a.get("href")
        pair = {
            "title": title,
            "link": link
                }
        songObjects.append(pair)

        
    return songObjects

def getVerses(songDocument):
    container = songDocument.find(id="siedl")
    verses = []
    if not container:
        return ""
    
    versesString = container.p.text
    verses = re.split("[0-9].", versesString)
    return verses

    
    
    
