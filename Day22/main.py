from bs4 import BeautifulSoup
import requests,json
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
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
        movie = requests.get('https://www.imdb.com'+link)
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
        if(info.find('time') == None):
            watch_time = 'Unknow'
        else:
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
        if(soup_movie.find('div', class_='poster') == None):
            poster = None
        else:
            poster = soup_movie.find('div', class_='poster').find('img').get('src')
        
        res = dict()
        res['poster'] = poster
        res['title'] = title
        res['rating'] = rating
        res['watch_time'] = watch_time
        res['movie_type'] = movie_type
        res['release_time'] = release_time
        res['link'] = 'https://www.imdb.com'+link
        ret.append(res)
        print(res)
    return ret

app = Flask(__name__)
# LINE BOT info
line_bot_api = LineBotApi('Channel Access Token')
handler = WebhookHandler('Channel Secret')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# Message event
@handler.add(MessageEvent)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token

    if(message_type == 'text'):
        # star links
        FullStar = 'https://maps.gstatic.com/consumer/images/icons/2x/ic_star_rate_14.png'
        HalfStar = 'https://maps.gstatic.com/consumer/images/icons/2x/ic_star_rate_half_14.png'
        EmptyStar = 'https://maps.gstatic.com/consumer/images/icons/2x/ic_star_rate_empty_14.png'
        
        user_text = event.message.text
        res = search(user_text)
        Card = json.load(open('card.json','r',encoding='utf-8'))
        for i in res:
            bubble = json.load(open('bubble.json','r',encoding='utf-8'))
            # poster
            if(i['poster'] != None):
                bubble['hero']['url'] = i['poster']
            # title
            bubble['body']['contents'][0]['text'] = i['title']
            # ranking
            ranking = float(i['rating'])/2.0
            for j in range(5):
                if(ranking >= 0.8):
                    bubble['body']['contents'][1]['contents'][j]['url'] = FullStar
                elif(ranking >= 0.5):
                    bubble['body']['contents'][1]['contents'][j]['url'] = HalfStar
                else:
                    bubble['body']['contents'][1]['contents'][j]['url'] = EmptyStar
                ranking-=1.0
            bubble['body']['contents'][1]['contents'][5]['text'] = str(i['rating'])
            # watch_time
            bubble['body']['contents'][2]['contents'][1]['contents'][1]['text'] = i['watch_time']
            # movie_type
            bubble['body']['contents'][2]['contents'][2]['contents'][1]['text'] = ','.join(i['movie_type'])
            # release_time
            bubble['body']['contents'][2]['contents'][3]['contents'][1]['text'] = i['release_time']
            # link
            bubble['footer']['contents'][0]['action']['uri'] = i['link']
            bubble['hero']['action']['uri'] = i['link']
            Card['contents'].append(bubble)
        if(len(res) == 0):
            line_bot_api.reply_message(reply_token, TextMessage(text='查無資料!'))
        else:
            line_bot_api.reply_message(reply_token, FlexSendMessage('查詢結果出爐~', Card))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)