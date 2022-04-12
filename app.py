from flask import (
    Flask,
    render_template,
    request,
    flash,
)
import urllib.request 
from urllib.parse import urlparse,urljoin
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)
app.secret_key = "secret-key"    

@app.route("/",methods=("GET", "POST"), strict_slashes=False)
def index():
    if request.method == "POST":

        try:
            global requested_url,specific_element,tag

            requested_url = 'https://www.hirmondo.ro/'
            tag = 'h2'

            source = requests.get(requested_url).text
            # parser library?
            soup = BeautifulSoup(source, "html.parser")
            
            specific_element = soup.find_all(tag)
            
            counter = len(specific_element)

            return render_template("index.html",
                url = requested_url,
                counter=counter,
                results = specific_element
                )

        except Exception as e:
            flash(e, "danger")
            
    return render_template("index.html")

    if __name__ == "__main__":
        app.run(debug=False,host='0.0.0.0')