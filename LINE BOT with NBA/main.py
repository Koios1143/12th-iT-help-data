from flask import Flask, request, abort
import json, datetime
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from GetData import Get_Card
from GetTeam import GetTeam, GetTeam2
from GetAllSchedule import GetAllSchedule
from GetDateSchedule import GetDateSchedule
from GetPlayers import GetPlayers
from GetPlayer import GetPlayer
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
        message = event.message.text
        if(message == '過去戰績'):
            Buttom = json.load(open('json/Score/Buttom.json','r',encoding='utf-8'))
            line_bot_api.reply_message(reply_token, FlexSendMessage('請選擇時間', Buttom))
        elif(message == '本日戰績'):
            nowtime = datetime.datetime.now()
            today = '{}-{}-{}'.format(nowtime.year,nowtime.month,nowtime.day)
            Card = Get_Card(today)
            line_bot_api.reply_message(reply_token, FlexSendMessage('查詢結果出爐~',Card))
        elif(message == '球隊賽程'):
            line_bot_api.reply_message(reply_token, FlexSendMessage('請選擇球隊', GetTeam()))
        elif(message == '球員數據'):
            line_bot_api.reply_message(reply_token, FlexSendMessage('請選擇球隊', GetTeam2()))
@handler.add(PostbackEvent)
def handle_postback(event):
    reply_token = event.reply_token
    data = event.postback.data
    if(data == 'SelectTime'):
        date = event.postback.params['date']
        Card = Get_Card(date)
        line_bot_api.reply_message(reply_token, FlexSendMessage('查詢結果出爐~', Card))
    elif(data.startswith('Get')):
        date = data[3:]
        Card = Get_Card(date)
        line_bot_api.reply_message(reply_token, FlexSendMessage('查詢結果出爐~', Card))
    elif(data.startswith('SelectScheduleFrom')):
        Team = data.split()[1]
        Card = GetAllSchedule(Team)
        line_bot_api.reply_message(reply_token, FlexSendMessage('查詢結果出爐~', Card))
    elif(data.startswith('Schedule')):
        data = data.split()
        Team = data[1]
        Date = data[2]
        Card = GetDateSchedule(Team, Date)
        line_bot_api.reply_message(reply_token, FlexSendMessage('查詢結果出爐~', Card))
    elif(data.startswith('SelectPlayerFrom')):
        Team = data.split()[1]
        Card = GetPlayers(Team)
        line_bot_api.reply_message(reply_token, FlexSendMessage('請選擇球員', Card))
    elif(data.startswith('SelectPlayerName')):
        PlayerName = data.split()[1]
        Card = GetPlayer(PlayerName)
        line_bot_api.reply_message(reply_token, FlexSendMessage('查詢結果出爐~', Card))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)