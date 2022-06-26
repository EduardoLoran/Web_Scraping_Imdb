import requests, bs4

rank = []
imdb = []
meta = []
movie = []
vote = []
year = []

site = requests.get("https://www.imdb.com/search/title/?release_date=2000-01-01,2021-01-01&start=1&ref_=adv_nxt")
page = bs4.BeautifulSoup(site.content ,"html.parser")
move_info = page.findAll('div', attrs= {'class': 'lister-item mode-advanced'})

count = 0

for movies in move_info:
    rank.append(movies.find('span').text.replace('.', ''))
    imdb.append(movies.find('div', class_ = 'inline-block ratings-imdb-rating').text.replace('\n', ''))
    meta.append(movies.find('span', class_ = 'metascore').text.replace(' ', '') if movies.find('span', class_ = 'metascore') else '' )
    movie.append(movies.h3.a.text)
    vote.append(movies.find_all('span', attrs = {'name': 'nv'})[0].text)
    year.append(movies.h3.find('span', class_ = 'lister-item-year text-muted unbold').text.replace('(', '').replace(')', ''))
       


'''
with open("Ranking.csv", "w") as arquivo:
    for ranks, imdbs, metas, movies, votes, years in zip(rank, imdb, meta, movie, vote , year):
        arquivo.write(ranks + ";" +
                      imdbs  + ";"  + 
                      metas  + "; " + 
                      movies + ";"  + 
                      votes  + ";"  + 
                      years  + "\n")

'''