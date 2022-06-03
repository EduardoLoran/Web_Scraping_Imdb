import requests, bs4

site = requests.get("https://www.imdb.com/search/title/?release_date=2000-01-01,2022-01-01")
page = bs4.BeautifulSoup(site.text ,"html.parser")

lista = list()

for i in range(3):
    lista.append(page.select(".lister-item-header a")[i].getText())
    lista.append(page.select('span[name="nv"]')[i].getText())
    lista.append(page.select(".lister-item-year")[i].getText())



with open("Ranking.csv", "w") as arquivo:
    arquivo.write("Filme;Voto;Ano\n")

    for i in lista:
        if lista[i] ==3:
            arquivo.write("\n")

print(lista)




'''

for char in "(–)":
    yearMovie = yearMovie.replace(char, "")
'''

