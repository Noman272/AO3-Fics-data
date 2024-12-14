from bs4 import BeautifulSoup as BS
import requests
import matplotlib.pyplot as plt
import string


site = "https://archiveofourown.org"
    fic = "/works/58203763/chapters/148205701"



def findNext():
    for i in soup.findAll('a'):
        if "Next Chapter →" in i:
            return i.get('href')



def getWords():
    words=[]
    dic = {}
    chapter = soup.find('div',attrs={"class":"userstuff module"})
    
    output = chapter.text    

    for c in string.punctuation:
        output = output.replace(c," ")
    output = output.replace("\n",'')
    output = output.replace("’",'')
    output = output.replace("‘",'')
    output = output.replace("”",'')
    output = output.replace("“",'')

    print(output.split())
    return (len(output.split())-2)


counts=[]
Fic = requests.get(site+fic)
soup = BS(Fic.text, "html.parser")
title= soup.find('h2').text.replace("\n",'').strip()

t = time.time()
while findNext() != None:
    Fic = requests.get(site+fic)
    soup = BS(Fic.text, "html.parser")
    counts.append(getWords()[0])
    fic = findNext()
    print(len(counts))

plt.plot(counts)
plt.title(title)
plt.xlabel('Chapter')
plt.ylabel('Words')

plt.show()

