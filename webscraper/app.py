from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

source = requests.get('https://maszol.ro/').text

soup = BeautifulSoup(source, 'lxml')

cikk = soup.find('article').find('h2').text

link = soup.find('article').find('h2').find('a').get('href')

# cim = soup.find('<article>').select_one('h2')

print(cikk)
print(link)

app = Flask(__name__)

@app.route('/')
def index():
    cikk = soup.find('article').find('h2').text
    link = soup.find('article').find('h2').find('a').get('href')

    kep = soup.find('picture').find('img').get('src')
   
    return render_template('index.html', cikk=cikk, link=link, kep=kep)

if __name__ == "__main__":
    app.run(debug=True)