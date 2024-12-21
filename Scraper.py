from bs4 import BeautifulSoup as BS
import requests
import matplotlib
import matplotlib.pyplot as plt
from pandas import DataFrame



punctuation='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~’‘”“…\n'
letters="abcdefghijklmnopqrstuvwxyzéà0123456789"
letterTTable = dict.fromkeys(map(ord, letters), None)
puncTTable = dict.fromkeys(map(ord, punctuation), " ")
site = "https://archiveofourown.org"

#put the suffix of the fic here
ficLink = "/works/60374203/chapters/154095100"
Fic = requests.get(site+ficLink)
soup = BS(Fic.text, "html.parser")

class ficDetails:

    def __init__(self,ficLink):
        site = "https://archiveofourown.org"
        Fic = requests.get(site+ficLink)
        soup = BS(Fic.text, "html.parser")

        #titles and authors
        self.title = soup.find('h2').text.replace("\n",'').strip()
        self.author= soup.find('h3',attrs={"class":"byline heading"}).text.replace("\n",'').split(',')

        '''metadata'''
        #rating
        self.rating = soup.find('dd',attrs={"class":"rating tags"}).text.replace("\n","")

        #warnings
        self.warnings=[]
        for i in soup.find('dd',attrs={"class":"warning tags"}).findAll('li'):
            self.warnings.append(i.text)
            
        #category
        self.categories=[]
        try:
            for i in soup.find('dd',attrs={"class":"category tags"}).findAll('li'):
                self.categories.append(i.text)
        except AttributeError:
            pass

        #fandom
        self.fandom=[]
        for i in soup.find('dd',attrs={"class":"fandom tags"}).findAll('li'):
            self.fandom.append(i.text)  

        #relationships
        self.relationships=[]
        try:
            for i in soup.find('dd',attrs={"class":"relationships tags"}).findAll('li'):
                self.relationships.append(i.text)
        except AttributeError:
            pass

        #characters
        self.characters=[]
        try:
            for i in soup.find('dd',attrs={"class":"character tags"}).findAll('li'):
                self.characters.append(i.text)
        except AttributeError:
            pass

        #additional tags
        self.additional_tags=[]
        try:
            for i in soup.find('dd',attrs={"class":"freeform tags"}).findAll('li'):
                self.additional_tags.append(i.text)
        except AttributeError:
            pass

        #language
        self.language=soup.find('dd',attrs={"class":"language"}).text

        '''stats'''
        #publish date
        self.publish_date = soup.find('dd',attrs={"class":"published"}).text
        

        #last updated
        try:
            self.last_update = soup.find('dd',attrs={"class":"status"}).text
            
        except AttributeError:
            self.last_update=None
    
        #words
        words = soup.find('dd',attrs={"class":"words"})
        self.words = int(words.text.replace(',',''))
           
        #chapter count
        chapters = soup.find('dd',attrs={"class":"chapters"})
        self.chapters = int(chapters.text.split('/')[0].replace(',',''))
        
        #comments
        try:
            comments = soup.find('dd',attrs={"class":"comments"})
            self.comments = int(comments.text.replace(',',''))
        except AttributeError:
            self.comments=None
    
        #kudos
        try:
            self.kudos = soup.find('dd',attrs={"class":"kudos"})
        except ValueError:
            self.kudos = int(soup.find('dd',attrs={"class":"kudos"}).text.replace(',',''))
        except AttributeError:
            self.kudos=None       
    
        #bookmarks
        try:    
            self.bookmarks = int(soup.find('dd',attrs={"class":"bookmarks"}).text.replace(',',''))
        except AttributeError:
            self.bookmarks=None
            
        #hits
        self.hits = int(soup.find('dd',attrs={"class":"hits"}).text.replace(',',''))
        




#traversing through the chapters
def findNext(soup):
    for i in soup.findAll('a'):
        if "Next Chapter →" in i:
            return i.get('href')



def chapterWords():
    chapter = soup.find('div',attrs={"class":"userstuff module"})
    output = chapter.text 
    output = output.lower()
    #getting rid of punctuations
    for c in punctuation:
        output = output.replace(c," ")
    output = output.replace("\n",'')

    return (len(output.split())-2) #because the find function takes 2 extra words

def WordFreq(ficLink):
    Fic = requests.get(site+ficLink)
    soup = BS(Fic.text, "html.parser")
    freq={}
    print("1")
    while findNext(soup) != None:
        print("2")
        Fic = requests.get(site+ficLink)
        soup = BS(Fic.text, "html.parser")
        chapter = soup.find('div',attrs={"class":"userstuff module"})
        output = chapter.text
        output = output.lower()
        output = output.translate(puncTTable)
        for i in output.split():
            if i in freq:
                freq[i]+=1
            else:
                freq[i]=1
        ficLink = findNext(soup)
    del freq["chapter"]
    del freq["text"]
    return freq
    

def PunctuationFrequency():
    chapter = soup.find('div',attrs={"class":"userstuff module"})
    output = chapter.text
    output = output.lower()
    output = output.translate(letterTTable)
    for c in punctuation:
        output = output.replace(c,f"{c} ")
    return output.split()

def graphBar(dic,title,xLab,counts):
    
    plt.bar(x=dic.keys(),height=dic.values(),color="#12ACAE")
    plt.title(title)
    plt.xlabel(xLab)
    plt.ylabel("Frequency")
    plt.savefig(f"{title.split()[:4]}_{len(counts)}.png")
    plt.show()

counts=[]
puncs={}


title= soup.find('h2').text.replace("\n",'').strip()

'''
while findNext() != None:
    Fic = requests.get(site+ficLink)
    soup = BS(Fic.text, "html.parser")
    for i in PunctuationFrequency():
        if i in puncs:
            puncs[i]+=1
        else:
            puncs[i]=1
    #counts.append(chapterWords())
    ficLink = findNext()




plt.style.use('classic')
plt.rcParams["figure.dpi"] = 150
#plt.tight_layout(pad=2.5)
#plt.plot([i for i in range(1,len(counts)+1)],counts, color="#12ACAE")
#plt.xlim(1, len(counts)+1)
#plt.ylim(0, max(counts)+2000)
#plt.title(title)
#
#plt.xlabel('Chapter')
#plt.ylabel('Words')
#plt.grid()
#plt.savefig(f"{title}_{len(counts)}.png")

#plt.show()'''
