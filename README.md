# PMVALO-Miniprojekti
[product backlog](https://docs.google.com/spreadsheets/d/1O9h2HMnEOil8wZUqLVy4tPoe1fWojAbpmapbGNpVOAU/edit?gid=1#gid=1)


## Definition of done
1. Vaatimus on analysoitu
2. Toteutus on suunniteltu ja jaettu tehtäviin
3. Toteutus on ohjelmoitu
4. Koodiin on luettu toisen henkilön toimesta
4. Koodi on testattu robottitesteillä testattu
5. Työ on dokumentoitu
6. Laadittu koodi on integroitu muuhun ohjelmistoon

# Käynnistysohjeet
1. Kloonaa repositorio omalle laitteelle
2. Luo postgre tietokanta esim. Aiven.io tai lokaalisti
3. Lisää tietokannan URL .env tiedostoon DATABASE_URL kohtaan
4. Siirry projektin hakemistoon terminaalissa
5. Asenna riippuvuudet suorittamalla poetry install
6. Siirry virtuaaliympäristöön suorittamalla eval $(poetry env activate)
7. Ennen ensimmäistä käynnistystä alusta tietokanta suorittamalla python src/db_helper.py
8. Käynnistä sovellus suorittamalla python src/index.py
9. Avaa sovellus siirtymällä terminaaliin tulevaan linkkiin
