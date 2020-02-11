import mask_crawler
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('IyA0HxHGBlwnDJaGk+2ukyfU1AMc+7KHfftDNL8vvKG1lAiAK/xWvz0tUZobI+U0T6SM0EbstDr0hjFQqpWefRBb9d7nco9cdqb2hxWqOM/sB9tb8GQSYJDDkyluK7r/NZKQ/7BQlITzQJtd58gmVAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('63453ac0bded625e454be737d1e1196b')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    #content = "{}: {}".format(event.source.user_id, event.message.text)
    content = "{}".format(event.message.text)

    if content[3:] == "口罩":
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text=mask_crawler.reply(content)))
    elif content[3:] != "口罩":
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text='輸入格式錯誤'))
    else:
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text=content))

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
