from bs4 import BeautifulSoup as BS
import requests
import matplotlib
import matplotlib.pyplot as plt


punctuation='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~’‘”“'
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
    for c in punctuation:
        output = output.replace(c," ")        
    output = output.replace("\n",'')


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


plt.style.use('classic')
plt.rcParams["figure.dpi"] = 150

plt.plot([i for i in range(1,len(counts)+1)],counts, color="#12ACAE")

plt.xlim(1, len(counts)+1)
plt.ylim(0, max(counts)+2000)
plt.title(title)
plt.tight_layout(pad=2)
plt.xlabel('Chapter')
plt.ylabel('Words')
plt.grid()
plt.savefig(f"{title}_{len(counts)}.png")

plt.show()
