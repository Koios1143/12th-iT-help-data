from bs4 import BeautifulSoup
import requests

def search(keyword):
    ret = []
    r = requests.get('https://www.imdb.com/find?q={}&s=tt&ttype=ft&ref_=fn_ft'.format(keyword))
    print(r.status_code)
    if(r.status_code == requests.codes.ok):
        soup = BeautifulSoup(r.text, 'html.parser')

    result = soup.find_all('td',class_='result_text')[:10]
    links = []
    for i in result:
        links.append(i.find('a').get('href'))

    for link in links:
        movie = requests.get('https://www.imdb.com/'+link)
        if(r.status_code == requests.codes.ok):
            soup_movie = BeautifulSoup(movie.text, 'html.parser')
        # get ranking
        if(soup_movie.find('div', class_='ratingValue') == None):
            rating = 0.0
        else:
            rating = soup_movie.find('div', class_='ratingValue').find('span').string
        
        info = soup_movie.find('div', class_='title_wrapper')
        # get title
        title = info.h1.get_text()
        # get watch_time
        watch_time = info.find('time').string.strip()

        subtext = info.find('div', class_='subtext').find_all('a')
        movie_type = []
        release_time = 'Unknow'
        # get movie_type & release_time
        if((subtext[-1]).get_text()[0].isdigit()):
            for i in subtext[:-1]:
                movie_type.append(i.get_text())
            release_time = subtext[-1].get_text().strip()
        else:
            for i in subtext:
                movie_type.append(i.get_text())
        
        poster = soup_movie.find('div', class_='poster').find('img').get('src')
        
        res = dict()
        res['poster'] = poster
        res['title'] = title
        res['rating'] = rating
        res['watch_time'] = watch_time
        res['movie_type'] = movie_type
        res['release_time'] = release_time
        ret.append(res)
        print(res)
    return ret