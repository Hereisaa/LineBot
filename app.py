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
    LocationMessage, LocationSendMessage,
    TemplateSendMessage, CarouselTemplate, CarouselColumn,
    PostbackAction, MessageAction, URIAction
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
            TextSendMessage(text=mask_crawler.reply(content,'text')))
    elif content[3:] != "口罩":
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text='輸入格式錯誤'))
    else:
        line_bot_api.reply_message(event.reply_token,
            TextSendMessage(text=content))

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    # reply_content = mask_crawler.reply(event.message.address[5:],'text')
    reply_content = mask_crawler.reply('台東縣台東市更生路62-78','text')
    # info = reply_content.values()

    
        line_bot_api.reply_message(
            event.reply_token,
            [
                for addr, info in reply_content.items():
                    LocationSendMessage(
                        title=info[0], 
                        # 地址 電話 成人數量 兒童數量 距離
                        address="{}\n{}\n成人剩餘  {}個\n兒童剩餘  {}個\n與您距離  {} km"
                                .format(addr, info[1], info[2], info[3], info[4]),
                        latitude=info[5], 
                        longitude=info[6]
                    )
            ]
        )



# @handler.add(MessageEvent, message=LocationMessage)
# def handle_location_message(event):
#     image_url = 'https://cdn.hk01.com/di/media/images/564720/org/7a5b31ccd89a2360794c1ef6bf54393f.jpg/0ws2YFTJcguqJ5hF1Hp3V8ELwZfAP_rMiLU2UYi1NlE?v=w1920'
#     reply_content = mask_crawler.reply(event.message.address,'text')
#     line_bot_api.reply_message(
#         event.reply_token,
#         TemplateSendMessage(
#             alt_text='Carousel template',
#             template=CarouselTemplate(
#                 columns=[
#                     CarouselColumn(
#                         thumbnail_image_url=image_url,
#                         title='this is menu1',
#                         text='description1',
#                         actions=[
#                             PostbackAction(
#                                 label='postback1',
#                                 display_text='postback text1',
#                                 data='action=buy&itemid=1'
#                             ),
#                             MessageAction(
#                                 label='message1',
#                                 text='message text1'
#                             ),
#                             URIAction(
#                                 label='uri1',
#                                 uri='http://example.com/1'
#                             )
#                         ]
#                     )
#                 ]
#             )
#         )
#     )




import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
