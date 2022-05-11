from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

source = requests.get('https://maszol.ro/').text

soup = BeautifulSoup(source, 'html.parser')

articles = soup.find_all('article')[0:20]

# extracting article titles into a list
titles = []
for article in articles:
     title =', '.join([x.get_text() for x in article.find_all('h2')])
     titles.append(title + '.')

# translate article titles to english
translator = Translator()
titles_eng = []
for title in titles:
    title_eng = translator.translate(title, src='hu').text
    titles_eng.append(title_eng)

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

# filtering articles by the label
good_articles, bad_articles, neutral_articles = [], [], []

for article in articles:
    if article.find_all("p")[-1].get_text() == 'good':
        good_articles.append(article)
    elif article.find_all("p")[-1].get_text() == 'bad':
        bad_articles.append(article)
    else:
        neutral_articles.append(article)


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

if __name__ == "__main__":
    app.run(debug=True)