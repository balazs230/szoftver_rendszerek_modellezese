from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests

source = requests.get('https://maszol.ro/').text

soup = BeautifulSoup(source, 'html.parser')

articles = soup.find_all('article')

kulcsszavak = ['háborúban', 'bomba', 'konfliktus', 'katonai', 'terror', 'csökken']

print( any(word in 'robbant egy észak-afganisztáni szunnita terror'.lower() for word in kulcsszavak) )

app = Flask(__name__)

@app.route('/')
def index():

    #print(len(cikkek))
   
    return render_template('index.html', articles=articles, kulcsszavak=kulcsszavak)

if __name__ == "__main__":
    app.run(debug=True)