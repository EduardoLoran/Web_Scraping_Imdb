import requests
import bs4
import os, shutil

#Variaveis matrizes
rank = []
imdb = []
meta = []
movie = []
vote = []
year = []
picture = []

#Variaveis de count
count = 1
control = 1
numFoto = 0

site = requests.get("https://www.imdb.com/search/title/?release_date=2000-01-01,2021-01-01&sort=num_votes,desc&start=1&ref_=adv_nxt")

#Gerando fotos 
pageImage = bs4.BeautifulSoup(site.content, "html.parser")

#Limpando a pasta de fotos ou criando ela
if os.path.exists("./fotos"):
    for the_file in os.listdir('./fotos'):
        file_path = os.path.join('./fotos', the_file)
        os.unlink(file_path) # mesma coisa que remove()
else:
    os.mkdir('./fotos')

for image in pageImage.findAll('img', width="67"):
    photoOrigin = image['loadlate']
    request = requests.get(photoOrigin).content
    picture.append(request)
for numFoto in range(20):
    imageFile = open(os.path.join('fotos', os.path.basename(f"foto{numFoto+1}.jpg")), 'wb+')
    imageFile.write(picture[numFoto])
    numFoto += 1
    imageFile.close()

#Gerando o csv
while (count <= 100):
    pageHtml = bs4.BeautifulSoup(site.content, "html.parser")
    move_infos = pageHtml.findAll('div', attrs={'class': 'lister-item mode-advanced'})
    for movies in move_infos:
        rank.append(movies.find('span').text.replace('.', ''))
        imdb.append(movies.find('div', class_='inline-block ratings-imdb-rating').text.replace('\n', ''))
        meta.append(movies.find('span', class_='metascore').text.replace(' ', '') if movies.find('span', class_='metascore') else '')
        movie.append(movies.h3.a.text)
        vote.append(movies.find_all('span', attrs={'name': 'nv'})[0].text)
        year.append(movies.h3.find('span', class_='lister-item-year text-muted unbold').text.replace('(', '').replace(')', ''))

    count += 50
    url = "https://www.imdb.com/search/title/?release_date=2000-01-01,2021-01-01&sort=num_votes,desc&start=" + str(count) +"&ref_=adv_nxt"
    site = requests.get(url)
    print(url)

with open("Ranking.csv", "w") as arquivo:
    arquivo.write("Rank;Imdb;Metascore;Filme;Votos;Ano\n")
    for ranks, imdbs, metas, movies, votes, years in zip(rank, imdb, meta, movie, vote, year):
        arquivo.write(ranks + ";" +
                      imdbs + ";" +
                      metas + "; " +
                      movies + ";" +
                      votes + ";" +
                      years + "\n")

#Gerando o .txt
while control <= 20:
    if control == 0:
        file = open('ranking.txt', 'x')
        file.write(f"{'#' : ^5}{'imdb' : ^8}{'metascore' : ^9}{'filme' : ^40}{'votos' : ^18}{'ano' : ^8}")
        control += 1
    else:
        file = open('ranking.txt', 'a')
        file.write(f"'\n'{rank[control-1] : ^5}{imdb[control-1] : ^8}{meta[control-1] : ^9}{movie[control-1] : ^40}{vote[control-1] : ^18}{year[control-1] : ^8}")
        control += 1
