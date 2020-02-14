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

# @handler.add(MessageEvent, message=LocationMessage)
# def handle_location_message(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         LocationSendMessage(
#             title='Location', 
#             address=event.message.address,
#             latitude=event.message.latitude, 
#             longitude=event.message.longitude
#         )
#     )


@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    image_url = 'https://cdn.hk01.com/di/media/images/564720/org/7a5b31ccd89a2360794c1ef6bf54393f.jpg/0ws2YFTJcguqJ5hF1Hp3V8ELwZfAP_rMiLU2UYi1NlE?v=w1920'
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=image_url,
                        title='this is menu1',
                        text='description1',
                        actions=[
                            PostbackAction(
                                label='postback1',
                                display_text='postback text1',
                                data='action=buy&itemid=1'
                            ),
                            MessageAction(
                                label='message1',
                                text='message text1'
                            ),
                            URIAction(
                                label='uri1',
                                uri='http://example.com/1'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=image_url,
                        title='this is menu2',
                        text='description2',
                        actions=[
                            PostbackAction(
                                label='postback2',
                                display_text='postback text2',
                                data='action=buy&itemid=2'
                            ),
                            MessageAction(
                                label='message2',
                                text='message text2'
                            ),
                            URIAction(
                                label='uri2',
                                uri='http://example.com/2'
                            )
                        ]
                    )
                ]
            )
        )
    )




import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
