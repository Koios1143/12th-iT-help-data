import yaml,sys,os,json
sys.path.append('subsys/')
data_folder = str(os.getcwd()) + '/data/'
now_folder = str(os.getcwd())
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from logger import logger
from get_mask import get_mask
from update import update


app = Flask(__name__)
# LINE BOT info
config_data = open('config.yml','r',newline='')
config = yaml.load(config_data)
line_bot_api = LineBotApi(config['ACCESS_TOKEN'])
handler = WebhookHandler(config['SECRET'])

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
    
    logger.info('message_type: ' + str(message_type))
    logger.info('user_id: ' + str(user_id))

    if(message_type == 'location'):
        update()
        result = get_mask(event)
        Card = json.load(open(data_folder + 'json/Card.json','r',encoding='utf-8'))
        for i in range(len(result)):
            bubble = json.load(open(data_folder + 'json/Bubble.json','r',encoding='utf-8'))
            # 醫事機構代碼
            Code = result[i][0]
            # 藥局名稱
            Name = result[i][1]
            # 地址
            Address = result[i][2]
            # 電話
            Phone = result[i][3]
            # 成人口罩剩餘
            AdultRemain = result[i][4]
            # 兒童口罩剩餘
            KidRemain = result[i][5]
            # 最後更新時間
            LastUpdate = result[i][6]
            # 緯度
            Latitude = result[i][7]
            # 經度
            Longitude = result[i][8]
           
            # 標題
            bubble['body']['contents'][0]['text'] = Name
            # 電話
            bubble['body']['contents'][1]['contents'][1]['text'] = Phone
            # 地址
            bubble['body']['contents'][2]['contents'][1]['text'] = Address
            # 成人口罩剩餘
            bubble['body']['contents'][3]['contents'][1]['text'] = AdultRemain
            # 兒童口罩剩餘
            bubble['body']['contents'][4]['contents'][1]['text'] = KidRemain
            # 最後更新時間
            bubble['body']['contents'][5]['contents'][1]['text'] = LastUpdate[5:-3]
            # PostBack Action
            bubble['footer']['contents'][0]['action']['data'] = 'GetMap {}'.format(Code)
            Card['contents'].append(bubble)
        line_bot_api.reply_message(reply_token, FlexSendMessage('查詢結果出爐~',Card))
    elif(message_type == 'text'):
        user_text = event.message.text
        logger.info('user_text: ' + user_text)
        line_bot_api.reply_message(reply_token, TextSendMessage(text = '早安^^'))

@handler.add(PostbackEvent)
def handle_postback(event):
    if(event.postback.data.startswith('GetMap')):
        px = event.postback.data[7:]
        positions = json.load(open(data_folder + 'json/positions.json','r'))
        name = positions[px]['name']
        lat = positions[px]['lat']
        lng = positions[px]['lng']
        address = positions[px]['address']

        line_bot_api.reply_message(event.reply_token, LocationSendMessage(
            title = name,
            address = address,
            latitude = lat,
            longitude = lng
        ))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)
