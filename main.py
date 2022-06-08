import requests, bs4
import pandas as pd

site = requests.get("https://www.imdb.com/search/title/?release_date=2000-01-01,2022-01-01")
page = bs4.BeautifulSoup(site.text ,"html.parser")

filme = list()
voto = list()
ano = list()


for i in range(3):
    filme.append(page.select(".lister-item-header a")[i].getText())
    voto.append(page.select('span[name="nv"]')[i].getText())
    ano.append(page.select(".lister-item-year")[i].getText())

lista= [filme,voto,ano]

listaPrint = pd.DataFrame(lista, columns = ['Filme','Voto','Ano'])


with open("Ranking.csv", "w") as arquivo:
    arquivo.write(str(listaPrint))

'''
for char in "(–)":
    yearMovie = yearMovie.replace(char, "")
'''

