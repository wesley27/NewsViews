'''
Created on Jan 28, 2017

@author: W. Wesley Weidenhamer II, Alexander Tolstoy
'''

from flask import Flask
from flask import render_template
from flask import request
from eventregistry import *
import sys
sys.path.insert(0, "C:/Python27/Scripts")
from client import DiffbotClient, DiffbotCrawl
from config import API_TOKEN
import requests
import json

app = Flask(__name__)
json1 = json.loads(request.POST.get('mydata', '{}'))
json2 = json.loads(request.POST.get('mydata', '{}'))

'''
Creates index.html
'''
@app.route('/')
def index():
    return render_template('index.html', one="inline", two="none", data1="", data2="")

'''
Receives News Source and Search data that has been entered.
Queries API for current news matching the search criteria and displays them for choosing.
'''
@app.route('/entry', methods=['POST'])
def entry():
    language1 = getLanguage(request.form['News Source 1'])
    language2 = getLanguage(request.form['News Source 2'])
    search = request.form['search']
    
    #send search info to news api for query
    #parse Titles out of articles
    #get list of articles in each language
    #save article json info in memory
    search = str(search).split(" ")
    lang1 = language1
    lang2 = language2
    numberOfStories = 5
    er = EventRegistry()
    q = QueryEvents(lang = [lang1,lang2])

    #q = QueryArticles(lang = lang1)


    er.login("atolstoy@umd.edu","448d6cfb11")

    for s in search:
        if(len(s)>=3):
            #js = json.dumps(er.suggestConcepts(s, lang = [lang1,lang2], conceptLang= [lang1,lang2],count = 1)[0])
        
            #print(json.loads(js)["uri"])    
            #q.addConcept(json.loads(js)["uri"]) #change count to larger number to increase breadth
            q.addKeyword(s)



    q.addRequestedResult(RequestEventsInfo(page = 1, count = 1, returnInfo = ReturnInfo(eventInfo = EventInfoFlags(concepts = False,categories = False))))
    res =  er.execQuery(q)

    selectedEvent = 0
    event = res["events"]["results"][selectedEvent]["uri"] #0 is the index of the event that gets retrieved
 
    q2 = QueryEvent(event)
    q2.addRequestedResult(RequestEventArticles(count = numberOfStories, lang = lang1)) 
    res = er.execQuery(q2)

    q3 = QueryEvent(event)
    q3.addRequestedResult(RequestEventArticles(count = numberOfStories, lang = lang2)) 
    res2 = er.execQuery(q3) 
    
    global json1 = res
    global json2 = res2
    
    return render_template('index.html', one="none", two="inline", data1=parseTitles(res, event), data2=parseTitles(res2, event))

'''
Receives chosen article titles.
Loads chosen articles from the URL saved in memory.
Uses API to get text only from the article and translate everything to English.
'''
@app.route('/selection', methods=['POST'])
def selection():
     body1 = request.form['article1']
     body2 = request.form['article2']
     #get article link from whats saved in memory
     #convert article to text
     #send articles to html
     url1 = getURL(json1, body1)
     url2 = getURL(json2, body2)
     
     diffbot = DiffbotClient()
     token = "0e2f4a8a541e26e874c0a76a0ff8cad5"
     version = 2
     url = "http://www.foxnews.com/us/2017/01/28/custom-officials-enforcing-trump-immigration-ban-at-us-airports.html"
     api = "article"
     response = diffbot.request(url, token, api, version=2)

    text = response['text']
    r = requests.post("http://text-processing.com/api/sentiment/", data = {'text':text})
    print(r.text)
    print(text)
     
     return render_template('index.html', one="none", two="inline", article1=1, article2=1)

'''
Converts news source chosen via front-end into a language the news API can search for
'''
def getLanguage(source):
    language = ""
    if(source == "English"):
        return "eng"
    elif(source == "Hispanic"):
        return "spa"
    elif(source == "Italian"):
        return "ita"
    elif(source == "Russian"):
        return "rus"
    elif(source == "German"):
        return "deu"
    elif(source == "Chinese"):
        return "zho"
    elif(source == "French"):
        return "fra"
    return language

def parseTitles(s, article_id):
    titles = []
    for i in range(0,len(s[article_id]["articles"]["results"])):
        titles.append(    s[article_id]["articles"]["results"][i]["body"])
    return titles

def getURL(s, body):
    for key in s.keys():
        for i in range(0,len(s[key]["articles"]["results"])):
            if(body == s[key]["articles"]["results"][i]["body"]):
                return s[key]["articles"]["results"][i]["url"]
    return

if __name__ == '__main__':
    app.run()