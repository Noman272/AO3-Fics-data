from bs4 import BeautifulSoup as BS
import requests
import matplotlib.pyplot as plt
import string


site = "https://archiveofourown.org"

#put the suffix of the fic here
fic = "/works/58203763/chapters/148205701"


#traversing through the chapters
def findNext():
    for i in soup.findAll('a'):
        if "Next Chapter →" in i:
            return i.get('href')



def getWords():
    chapter = soup.find('div',attrs={"class":"userstuff module"})
    output = chapter.text   #making changes to chapter.text itself doesn't work well 

    #getting rid of punctuations
    for c in string.punctuation:
        output = output.replace(c," ")
        
    output = output.replace("\n",'')
    output = output.replace("’",'')
    output = output.replace("‘",'')
    output = output.replace("”",'')
    output = output.replace("“",'')

    return (len(output.split())-2) #because the find function takes 2 extra words


counts=[]
Fic = requests.get(site+fic)
soup = BS(Fic.text, "html.parser")
title= soup.find('h2').text.replace("\n",'').strip()

while findNext() != None:
    Fic = requests.get(site+fic)
    soup = BS(Fic.text, "html.parser")
    counts.append(getWords())
    fic = findNext()

plt.plot(counts)
plt.title(title)
plt.xlabel('Chapter')
plt.ylabel('Words')

plt.show()
