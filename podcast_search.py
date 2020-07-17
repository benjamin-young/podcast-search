import requests
import json
import feedparser
import nltk
from nltk.tag import pos_tag
import wikipedia


nltk.download('averaged_perceptron_tagger')

searchTerm = input()
limit = 5

numEps = 3

entity = "podcast"

def getWikiPages(subject):
    searchUrl = "https://en.wikipedia.org/w/api.php?action=query&list=search&utf8=&format=json&srlimit=1&srsearch="+subject
    response = requests.get(searchUrl).json()
    jsonString = json.dumps(response, indent=2)

    jsonDict= json.loads(jsonString)
    
    return jsonDict["query"]["search"][0]["title"]

def getWikiData(page):
    searchUrl = "https://en.wikipedia.org/w/api.php?action=query&list=search&utf8=&format=json&srlimit=1&srsearch="+subject
    response = requests.get(searchUrl).json()
    jsonString = json.dumps(response, indent=2)

    jsonDict= json.loads(jsonString)
    
    return jsonDict["query"]["search"][0]["title"]

def makeItunesUrl(s):
    url = 'https://itunes.apple.com/search?term='
    
    words=s.split(' ')
    temp = url
    for word in words:
        temp = url+word+'+'
        url=temp

    url = url + "&limit=" + str(limit)
    url = url + "&entitys=" + str(entity)

    return url

searchUrl = makeItunesUrl(searchTerm) 

response = requests.get(searchUrl).json()

jsonString = json.dumps(response, indent=2)

feedUrls = {}

jsonDict= json.loads(jsonString)

for result in jsonDict["results"]:
    if result["wrapperType"] == "track":
        try:

            feedUrls[result["trackName"]]=result["feedUrl"]
            print(result["trackName"]+"\n")
            print(result["feedUrl"]+'\n')

        except KeyError:
            pass


for key in feedUrls:
    feed = feedparser.parse(feedUrls[key])
    feed_entries = feed.entries

    index = 0
    for entry in feed.entries:
        if index == numEps:
            break
        else:
            index+=1
        print(entry.title)
        print(entry.summary)

        subjects=[]
        tagged_sent = pos_tag(entry.summary.split())
        for i, (word,tag) in enumerate(tagged_sent):
            
            if tag == 'NNP':
                if i == 0:
                    subjects.append(word)
                else:
                    if tagged_sent[i-1][1] == 'NNP':
                        subjects[len(subjects)-1] = subjects[len(subjects)-1]+" "+word
                    else:
                        subjects.append(word)

                                
        pages=[]
        
        for subject in subjects:
            new_page = getWikiPages(subject)
            if new_page not in pages:
                pages.append(new_page)
        
        print(pages)
        
        for page in pages:
            print(getWikiData(page))
        
        for link in entry.links:
            if link.type == "audio/mpeg":
                print("\n>>>"+link.href)
        print("====\n")

