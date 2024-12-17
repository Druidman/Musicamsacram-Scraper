import re

def getPageLinks(categoryDocument,firstLink):
    pages_list = categoryDocument.find_all(class_="pagination")[1]
    linkHolders = pages_list.find_all("a")
    links = [firstLink]
    for linkHolder in linkHolders:
        link = linkHolder.get("href")
        if link in links:
            continue
        links.append(link)
    
    
    

    return links

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

def getSongObjects(pageDocument):
    song_container = pageDocument.tbody
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

    
    
    
