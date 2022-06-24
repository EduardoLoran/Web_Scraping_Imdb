import requests, bs4

rangeMoive = int(input("Digite a quantidade de filme desejada\n"))

releaseDateStart = str(input("Digite a data inicial que deseja buscar os tops filmes. Exemplo 01/01/2000: \n"))
releaseDateStart = releaseDateStart.split("/")
releaseDateStart = releaseDateStart[2] + "-"  + releaseDateStart[1] + "-" + releaseDateStart[0]
releaseDateEnd =   str(input("Digite a data final que deseja buscar os tops filmes. Exemplo 31/12/2022: \n"  ))
releaseDateEnd = releaseDateEnd.split("/")
releaseDateEnd   = releaseDateEnd  [2] + "-"  + releaseDateEnd  [1] + "-" + releaseDateEnd  [0]

site = requests.get("https://www.imdb.com/search/title/?release_date=" + "releaseDateStart" + ","  + releaseDateEnd)
#site = requests.get("https://www.imdb.com/search/title/?release_date=" + releaseDateStart + ","  + releaseDateEnd + "&start="+ str(count)+"&ref_=adv_nxt")

page = bs4.BeautifulSoup(site.content ,"html.parser")
move_info = page.findAll('div', attrs= {'class': 'lister-item mode-advanced'})


movie = []
vote = []
year = []


for movies in move_info:
    movie.append(movies.h3.a.text)
    vote.append(movies.find_all('span', attrs = {'name': 'nv'})[0].text)
    year.append(movies.h3.find('span', class_ = 'lister-item-year text-muted unbold').text.replace('(', '').replace(')', ''))


with open("Ranking.csv", "w") as arquivo:
    for movies, votes, years in zip(movie, vote , year):
        arquivo.write(str(movies) + ";" + 
                      str(votes)  + ";" +
                      years.replace("(", "").replace(")", "").replace("–", " – ") + "\n"
                      )



"https://github.com/sivasahukar95/CodeStore/blob/master/Scraping%20data%20from%20imdb.ipynb"