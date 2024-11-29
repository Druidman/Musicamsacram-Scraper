
class Scraper():
    def __init__(self,document):
        self.document = document
    
    def get_elements(self):
        table = self.document.find(class_="table-responsive")
        body = table.tbody
        self.elements = body.find_all("td")
    



