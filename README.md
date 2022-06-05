# Szoftver rendszerek modellezese

A PletykAI egy olyan webes alkalmazás, amely egy híroldal (www.maszol.ro) főoldalát fésüli át (webscraping), onnan összegyűjti a cikkeket, majd az adatok elemzése és feldolgozása után azokat osztályozva megjeleníti.

Az alkalmazás célja az, hogy az olvasó hangulat szerint osztályozva lássa a cikkeket, és könnyen választhasson a kategóriák között. Minden cikk rendelkezik egy címkével, amely az adott cikk hangulatát, érzelmi töltetét jelöli, illetve kiválasztható, hogy csak egy bizonyos csoportba tartozó cikkeket jelenítsen meg.

### Felhasznált technológiák
Flask, BeautifulSoup, Bootstrap, VADER, googletrans, MongoDB

### Futtatás:
- függőségek telepítése a requirements.txt fájlból
- python app.py – a fő állomány futtatása
- mongod – az adatbázis elindítása

### Források
- https://analyticsindiamag.com/sentiment-analysis-made-easy-using-vader/
- https://github.com/cjhutto/vaderSentiment
- https://jinja.palletsprojects.com/en/3.1.x/
- https://flask.palletsprojects.com/en/2.1.x/
- https://en.wikipedia.org/wiki/Sentiment_analysis
- https://getbootstrap.com/docs/5.2/getting-started/introduction/
- https://pypi.org/project/googletrans/
- https://pypi.org/project/beautifulsoup4/

