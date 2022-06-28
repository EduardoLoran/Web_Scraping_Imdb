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

print("\nOla!! Você executou um webcraping, para buscar registros do site imdb.\n")
print("Lembrando, programa criado com intuido academico, para fins de conhecimento de webcraping através da linguagém de programação python.\n")
print("Manual do programa:")
print("- Gera um arquivo chamado raking.csv, através da quantidade de filmes escolhida.")
print("- Gera um arquivo chamado ranking.txt, somente com um resumo dos 20 primeiros filmes escolhidos.")
print("- Gerado as 20 primeiras imagens da capa dos filmes, e armazena em uma pasta chamada fotos.\n")


execProg = input('Deseja continuar com a execução do programa [S/N] \n').strip()[0].upper()

if execProg == 'S':
#Request na site do imdb
    rangeMovie = int(input("Digite a quantidade de filmes que deseja buscar:\n"))
    url = "https://www.imdb.com/search/title/?release_date=2000-01-01,2021-01-01&sort=num_votes,desc&start=1&ref_=adv_nxt"
    site = requests.get(url)

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
    while (count <= rangeMovie):
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
        print("Aguarde! Buscando registros......")

    with open("ranking.csv", "w") as arquivo:
        arquivo.write("Rank;Imdb;Metascore;Filme;Votos;Ano\n")
        for ranks, imdbs, metas, movies, votes, years in zip(rank, imdb, meta, movie, vote, year):
            arquivo.write(ranks + ";" +
                        imdbs + ";" +
                        metas + "; " +
                        movies + ";" +
                        votes + ";" +
                        years + "\n")

    #Gerando o .txt
    with open('ranking.txt', 'w') as file:
        while control <= 20:
            file.write(f"{'#' : ^5}{'imdb' : ^8}{'metascore' : ^9}{'filme' : ^40}{'votos' : ^18}{'ano' : ^8}")
            file.write(f"'\n'{rank[control-1] : ^5}{imdb[control-1] : ^8}{meta[control-1] : ^9}{movie[control-1] : ^40}{vote[control-1] : ^18}{year[control-1] : ^8}")
            control += 1

    print("\nExecução terminada!")
    print("Pasta Fotos, arquivo ranking.csv e rankingtxt. Criados com sucesso.\n")
        
else:
    print("Até mais!\n")

print("\nPrograma acabado! Obrigado pelo uso!")
print("Coloboração de desenvolvimento: Eduardo Loran, Gustavo Fischer, Cassiano Henrique, ")
print("Instrução do Professor Leonardo Garcia Tampelini")
print("Inistuição Biopark")
print("Versão 0.1 - 2022")

