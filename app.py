from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

source = requests.get('https://maszol.ro/').text

soup = BeautifulSoup(source, 'html.parser')

articles = soup.find_all('article')[0:20]

neg_keywords = ['háború', 'bomba', 'konfliktus', 'katona', 'terror', 'kigyulladt', 'villám', 'vihar', 'harc', 'halál',
    'hunyt', 'baleset', 'pusztít', 'akaszt', 'ütköz']

poz_keywords = ['nőtt', 'újít', 'fesztivál', 'ének']

for article in articles:
     h2=', '.join([x.get_text() for x in article.find_all('h2')])
     if any(word in h2 for word in neg_keywords):
        new_tag = soup.new_tag("p")
        new_tag.append("negativ")
        article.append(new_tag)
     elif any(word in h2 for word in poz_keywords):
        new_tag = soup.new_tag("p")
        new_tag.append("pozitiv")
        article.append(new_tag)
     else:
        new_tag = soup.new_tag("p")
        new_tag.append("neutral")
        article.append(new_tag)

# for art in articles:
#     print(type(art))

app = Flask(__name__)

@app.route('/')
def index():
   
    return render_template('index.html', articles=articles)

if __name__ == "__main__":
    app.run(debug=True)