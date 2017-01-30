'''
Created on Jan 28, 2017

@author: W. Wesley Weidenhamer II, Alexander Tolstoy
'''

from flask import Flask
from flask import render_template
from flask import request
from eventregistry import *
from newspaper import Article
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

'''
Creates index.html
'''
@app.route('/index')
def index():
    return render_template('index.html', one="inline", two="none", three="none", data1="", data2="", source1="", source2="")

'''
Receives News Source and Search data that has been entered.
Queries API for current news matching the search criteria and displays them for choosing.
'''
@app.route('/entry', methods=['POST'])
def entry():
    source1 = request.form['News Source 1']
    source2 = request.form['News Source 2']
    language1 = getLanguage(source1)
    language2 = getLanguage(source2)
    searchText = request.form['search']
    
    search = str(searchText).split(" ")
    lang1 = language1
    lang2 = language2
    numberOfStories = 5
    er = EventRegistry()
    q = QueryEvents(lang = [lang1,lang2])


    er.login("wesleyw@terpmail.umd.edu","ChocolateChipCookies")
    
    for s in search:
        
        if(len(s)>=3):
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
    
    article1 = parseTitles(res, event)
    article2 = parseTitles(res2, event)
    
    return render_template('index.html', one="none", two="inline", three="none", data1=article1, data2=article2, source1=source1, source2=source2)

'''
Receives chosen article titles.
Loads chosen articles from the URL saved in memory.
Uses API to get text only from the article and translate everything to English.
'''
@app.route('/selection', methods=['POST'])
def selection():
    url1 = request.form['article1']
    url2 = request.form['article2']
    news1 = Article(url=url1)
    news1.download()
    news1.parse()
    news1Array = [news1.title, news1.top_image, news1.text, url1]
    
    news2 = Article(url=url2)
    news2.download()
    news2.parse()
    news2Array = [news2.title, news2.top_image, news2.text, url2]
    
    
    return render_template('index.html', one="none", two="none", three="inline", data1=news1Array, data2=news2Array, source1="", source2="")

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
        if len(s[article_id]["articles"]["results"][i]["source"]["title"] + ": " +     s[article_id]["articles"]["results"][i]["title"]) > 77:
            titles.append((s[article_id]["articles"]["results"][i]["source"]["title"] + ": " +     s[article_id]["articles"]["results"][i]["title"])[:77] + "...")
        else:
            titles.append(s[article_id]["articles"]["results"][i]["source"]["title"] + ": " +     s[article_id]["articles"]["results"][i]["title"])
        titles.append(s[article_id]["articles"]["results"][i]["url"])
    return titles

if __name__ == '__main__':
    app.run()