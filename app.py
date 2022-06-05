from asyncio.windows_events import NULL
from flask import Flask, redirect, render_template, request
from bs4 import BeautifulSoup
import requests
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pymongo import MongoClient
from flask_cors import CORS

source = requests.get('https://maszol.ro/').text

soup = BeautifulSoup(source, 'html.parser')

articles = soup.find_all('article')[0:20]

# # extracting article titles into a list
# titles = []
# for article in articles:
#      title =', '.join([x.get_text() for x in article.find_all('h2')])
#      titles.append(title + '.')

# # translate article titles to english
translator = Translator()
# titles_eng = []
# for title in titles:
#     title_eng = translator.translate(title, src='hu').text
#     titles_eng.append(title_eng)

vader = SentimentIntensityAnalyzer()

# appending label to the articles
for article in articles:
     title = ', '.join([x.get_text() for x in article.find_all('h2')]) # extract article title
     title_eng = translator.translate(title, src='hu').text # translate article title to english
     analyzed_title = vader.polarity_scores(title_eng)
     polarity = analyzed_title['compound'] # identify the polarity of the translated title
     if polarity <= -0.05:
        new_tag = soup.new_tag("p")
        new_tag.append("bad")
        article.append(new_tag)
     elif polarity >= 0.05:
        new_tag = soup.new_tag("p")
        new_tag.append("good")
        article.append(new_tag)
     else:
        new_tag = soup.new_tag("p")
        new_tag.append("neutral")
        article.append(new_tag)

# filtering articles into separate lists by the label
good_articles, bad_articles, neutral_articles = [], [], []

for article in articles:
    if article.find_all("p")[-1].get_text() == 'good':
        good_articles.append(article)
    elif article.find_all("p")[-1].get_text() == 'bad':
        bad_articles.append(article)
    else:
        neutral_articles.append(article)

# managing MongoDB
client = MongoClient()
articles_db = client["articles_db"]
articles_collection = articles_db["articles_collection"]

saved_articles = []

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', articles=articles)

@app.route('/good-news')
def good_news():
    return render_template('index.html', articles=good_articles)

@app.route('/bad-news')
def bad_news():
    return render_template('index.html', articles=bad_articles)

@app.route('/neutral-news')
def neutral_news():
    return render_template('index.html', articles=neutral_articles)

@app.route('/saved-news')
def saved_news():
    return render_template('saved_news.html', articles=list(set(saved_articles)))

@app.route('/save-article', methods=['GET', 'POST'])
def save_article():
    saved_article_string = request.form['article']
    saved_article_soup = BeautifulSoup(saved_article_string, 'html.parser')
    article_dict = {'title' : ', '.join([x.get_text() for x in saved_article_soup.find_all('h2')]), 'content' : saved_article_string }
    articles_collection.insert_one(article_dict)
    print('egy cikk hozzaadasa utan: ' + str(len(list(articles_collection.find()))))
    for element in list(articles_collection.find()):
        saved_articles.append(BeautifulSoup(element['content'], 'html.parser'))
    return redirect('/')

@app.route('/remove-one', methods=['GET', 'POST'])
def remove_one():
    articles_collection.delete_one({ "title": request.form['title'] })
    saved_articles.remove(BeautifulSoup(request.form['content'], 'html.parser'))
    print('egy eltavolitasa utan: ' + str(len(list(articles_collection.find()))))
    return redirect('/saved-news')

@app.route('/remove-all')
def remove_all():
    articles_collection.drop()
    saved_articles = []
    print('osszes eltdobasa utan: ' + str(len(list(articles_collection.find()))))
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)