import requests
import bs4
import os
import smtplib
import email.message
import win32com.client as win32

rank = []
imdb = []
meta = []
movie = []
vote = []
year = []
count = 1
c = 0
numFoto = 1

site = requests.get("https://www.imdb.com/search/title/?release_date=2000-01-01,2021-01-01&sort=num_votes,desc&start=1&ref_=adv_nxt")

while (count <= 2000):
    page = bs4.BeautifulSoup(site.content, "html.parser")
    move_info = page.findAll('div', attrs={'class': 'lister-item mode-advanced'})
    for movies in move_info:
        rank.append(movies.find('span').text.replace('.', ''))
        imdb.append(movies.find('div', class_='inline-block ratings-imdb-rating').text.replace('\n', ''))
        meta.append(movies.find('span', class_='metascore').text.replace(' ', '') if movies.find('span', class_='metascore') else '')
        movie.append(movies.h3.a.text)
        vote.append(movies.find_all('span', attrs={'name': 'nv'})[0].text)
        year.append(movies.h3.find('span', class_='lister-item-year text-muted unbold').text.replace('(', '').replace(')', ''))
    while numFoto <= 50:
        for image in page.findAll('img', width="67"):
            photoOrigin = image['loadlate']
            r = requests.get(photoOrigin).content
            imageFile = open(os.path.join('fotos', os.path.basename(f"foto{numFoto}.jpg")), 'wb+')
            imageFile.write(r)
            numFoto += 1
            imageFile.close()
    count = count + 50
    countString = str(count)
    webpage = "https://www.imdb.com/search/title/?release_date=2000-01-01,2021-01-01&sort=num_votes,desc&start={}&ref_=adv_nxt".format(countString)
    print(webpage)
    site = requests.get(webpage)

while c <= 20:
    if c == 0:
        file = 'ranking.txt'
        f = open(file, 'x')
        f.write(
            f"{'#' : ^5}{'imdb' : ^8}{'metascore' : ^9}{'filme' : ^40}{'votos' : ^18}{'ano' : ^8}")
        c += 1
        # print(c)
    else:
        file = 'ranking.txt'
        f = open(file, 'a')
        f.write(
            f"'\n'{rank[c-1] : ^5}{imdb[c-1] : ^8}{meta[c-1] : ^9}{movie[c-1] : ^40}{vote[c-1] : ^18}{year[c-1] : ^8}")
        c += 1
       # print(c)

with open("Ranking.csv", "w") as arquivo:
    arquivo.write("Rank;Imdb;Metascore;Filme;Votos;Ano\n")
    for ranks, imdbs, metas, movies, votes, years in zip(rank, imdb, meta, movie, vote, year):
        arquivo.write(ranks + ";" +
                      imdbs + ";" +
                      metas + "; " +
                      movies + ";" +
                      votes + ";" +
                      years + "\n")

sendEmail = input('Arquivo ranking.txt gerado com SUCESSO gostaria que eles seja enviado para o seu e-mail? [S/N] ').strip()[0].upper()

if sendEmail == 'S':
    emailEnviar = input("Digite seu e-mail: ").strip().lower()
    f = open("ranking.txt", "r")
    corpo_email = "\n"
    for line in f.readlines():
        corpo_email = (corpo_email + line + "\n")
    f.close()
    print(corpo_email)

    outlook = win32.Dispatch('outlook.application')
    email = outlook.CreateItem(0)
    email.To = f"{emailEnviar}"
    email.Subject = 'Ranking filmes - IMDB'
    email.HTMLBody = f'''
    <p>Olá, aqui segue o Ranking de filmes - IMDB</p>

    <p>{corpo_email}</p>
    
    <p>Atenciosamente, Equipe CEGK</p>
    <p>Este e-mail foi enviado automaticamente!</p>'''

    email.Send()

    '''msg = email.message.Message()
    msg['Subject'] = 'Ranking filmes - IMDB'
    msg['From'] = 'testwebscraping22@gmail.com'
    msg['To'] = emailEnviar
    password = 'admin123admin'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))'''
    print('Email enviado com SUCESSO!')
else:
    print("Até mais!\n")
