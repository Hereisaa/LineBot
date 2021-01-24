import mask_crawler
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, JoinEvent,
    TextMessage, TextSendMessage, 
    LocationMessage, LocationSendMessage,
    TemplateSendMessage, CarouselTemplate, CarouselColumn,
    PostbackAction, MessageAction, URIAction
)

app = Flask(__name__)

line_bot_api = LineBotApi('Put LineBotApi Here')
handler = WebhookHandler('Put WebhookHandler Here')

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

@handler.add(JoinEvent)
def handle_join(event):
    newcoming_text = "{}嗨 歡迎 ~ ψ(｀∇´)ψ{}\n↓↓ 查詢資訊請輸入 ↓↓\n地址 台中市西屯區台灣大道三段99號\n(e.g.台中市政府)\n\n{}左下角「＋」直接傳送「位置資訊」也行喔!\n\n{}若不想接收提醒，可以點選本畫面右上方的選單圖示，然後關閉「提醒」的設定喔(ok)".format(chr(0x1000A4), chr(0x1000A4), chr(0x100077), chr(0x100077))
    line_bot_api.reply_message(event.reply_token, TextMessage(text=newcoming_text))
    # print("JoinEvent =", JoinEvent)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #print("Handle: reply_token: " + event.reply_token + ", message: " + event.message.text)
    if event.message.text[:2] == '地址':
        content = "{}".format(event.message.text[3:])
        reply_content = mask_crawler.reply(content,'text')
        send_message = []
        for addr, info in reply_content.items():
            send_message.append(LocationSendMessage(
                title=info[0], 
                # 地址 電話 成人數量 兒童數量 距離
                address="{}\n{}\n成人剩餘  {}個\n兒童剩餘  {}個\n與您距離  {} km"
                        .format(addr, info[1], info[2], info[3], info[4]),
                latitude=info[5], 
                longitude=info[6]
            ))

        line_bot_api.reply_message(event.reply_token, send_message)
    elif event.message.text[:2] == '查詢':
        content = '查詢附近藥局口罩數量 ~\n\n輸入 :\n地址 台中市西屯區台灣大道三段99號\n\nP.S.左下角「＋」直接傳送「位置資訊」也行喔!'
        line_bot_api.reply_message( event.reply_token, TextSendMessage(text=content))


@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):

    if event.message.address[3:5] == '台灣':
        reply_content = mask_crawler.reply(event.message.address[5:],'text')
    else:
        reply_content = mask_crawler.reply(event.message.address,'text')

    send_message = []
    for addr, info in reply_content.items():
        send_message.append(LocationSendMessage(
            title=info[0], 
            # 地址 電話 成人數量 兒童數量 距離
            address="{}\n{}\n成人剩餘  {}個\n兒童剩餘  {}個\n與您距離  {} km"
                    .format(addr, info[1], info[2], info[3], info[4]),
            latitude=info[5], 
            longitude=info[6]
        ))

    line_bot_api.reply_message(event.reply_token, send_message)

## Carousel template
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
