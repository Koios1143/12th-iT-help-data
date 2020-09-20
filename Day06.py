from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import json

app = Flask(__name__)
# LINE BOT info
line_bot_api = LineBotApi('Channel Access token')
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
    message = event.message.text
    if(message == 'Text'):
        text_message = TextSendMessage(text = 'Hello, World')
        line_bot_api.reply_message(reply_token, text_message)
    elif(message == 'Sticker'):
        sticker_message = StickerSendMessage(package_id='1',sticker_id='1')
        line_bot_api.reply_message(reply_token, sticker_message)
    elif(message == 'Image'):
        image_message = ImageSendMessage(original_content_url='https://file-examples-com.github.io/uploads/2017/10/file_example_PNG_500kB.png',preview_image_url='https://file-examples-com.github.io/uploads/2017/10/file_example_PNG_500kB.png')
        line_bot_api.reply_message(reply_token, image_message)
    elif(message == 'Video'):
        video_message = VideoSendMessage(original_content_url='https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_480_1_5MG.mp4',preview_image_url='https://file-examples-com.github.io/uploads/2017/10/file_example_PNG_500kB.png')
        line_bot_api.reply_message(reply_token, video_message)
    elif(message == 'Audio'):
        audio_message = AudioSendMessage(original_content_url='https://file-examples-com.github.io/uploads/2017/11/file_example_MP3_700KB.mp3',duration=3000)
        line_bot_api.reply_message(reply_token, audio_message)
    elif(message == 'Location'):
        location_message = LocationSendMessage(title='my location',address='Tokyo',latitude=35.65910807942215,longitude=139.70372892916203)
        line_bot_api.reply_message(reply_token, location_message)
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)