from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

source = requests.get('https://maszol.ro/').text

soup = BeautifulSoup(source, 'html.parser')

articles = soup.find_all('article')[0:20]

neg_keywords = ['háború', 'bomba', 'konfliktus', 'katona', 'terror', 'kigyulladt', 'villám', 'vihar', 'harc', 'halál',
    'hunyt', 'baleset', 'pusztít', 'akaszt', 'ütköz']

poz_keywords = ['nőtt', 'újít', 'fesztivál', 'ének', 'kiemelkedő', 'boldog', 'örül', 'szép']

for article in articles:
     h2=', '.join([x.get_text() for x in article.find_all('h2')])
     if any(word in h2 for word in neg_keywords):
        new_tag = soup.new_tag("p")
        new_tag.append("bad")
        article.append(new_tag)
     elif any(word in h2 for word in poz_keywords):
        new_tag = soup.new_tag("p")
        new_tag.append("good")
        article.append(new_tag)
     else:
        new_tag = soup.new_tag("p")
        new_tag.append("neutral")
        article.append(new_tag)

# for art in articles:
#     print(type(art))

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