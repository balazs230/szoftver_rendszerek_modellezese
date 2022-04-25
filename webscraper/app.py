from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

source = requests.get('https://maszol.ro/').text

soup = BeautifulSoup(source, 'html.parser')

articles = soup.find_all('article')[0:5]

kulcsszavak = ['háború', 'bomba', 'konfliktus', 'katona', 'terror', 'kigyulladt', 'villám', 'vihar']
checks = []

for article in articles:
     h2=', '.join([x.get_text() for x in article.find_all('h2')])
     if any(word in h2 for word in kulcsszavak):
         checks.append('-')
     else:
         checks.append('+')
# for art in articles:
#     print(type(art))

app = Flask(__name__)

@app.route('/')
def index():
   
    return render_template('index.html', len=len, articles=articles, kulcsszavak=kulcsszavak, checks=checks)

if __name__ == "__main__":
    app.run(debug=True)