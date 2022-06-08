import requests, bs4

releaseDateStart = str(input("Digite a data inicial que deseja buscar os tops filmes. Exemplo 01/01/2000: \n"))
releaseDateEnd =   str(input("Digite a data final que deseja buscar os tops filmes. Exemplo 31/12/2022: \n"  ))

releaseDateStart = releaseDateStart.split("/")
releaseDateEnd = releaseDateEnd.split("/")

releaseDateStart = releaseDateStart[2] + "-"  + releaseDateStart[1] + "-" + releaseDateStart[0]
releaseDateEnd   = releaseDateEnd  [2] + "-"  + releaseDateEnd  [1] + "-" + releaseDateEnd  [0]

site = requests.get("https://www.imdb.com/search/title/?release_date=2000-01-01,2022-01-01")
#site = requests.get("https://www.imdb.com/search/title/?release_date=" + releaseDateStart + ","  + releaseDateEnd)

page = bs4.BeautifulSoup(site.text ,"html.parser")

#Variable to create list
listMove = list()
listVote = list()
listYear = list()

#Variable for amount of movie
rangeMovie = int(input("Digite a quantidade de filmes que deseja buscar: \n"))

for i in range(rangeMovie):
    listMove.append(page.select(".lister-item-header a")[i].getText())
    listVote.append(page.select('span[name="nv"]'      )[i].getText())
    listYear.append(page.select(".lister-item-year"    )[i].getText())
    
print(listVote)

with open("Ranking.csv", "w") as arquivo:
    for movie, vote, year in zip(listMove, listVote , listYear):
        arquivo.write(str(movie) + ";" + 
                      str(vote)  + ";" +
                      year.replace("(", "").replace(")", "").replace("–", " – ") + "\n"
                      )