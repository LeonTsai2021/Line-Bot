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

line_bot_api = LineBotApi('yjgs7A9gJQ9JweMyzMKlL1l2rhYyOtqy4GacL03j3YJJMCHRLylVXJ+q7+SwiB5PlLJ1datP1Qjk9svk1W1IANgkKSaNTva//OusGubX0ykDf9ALi1pvWPnIlBr6UERZP3mJaw9xlSV9An+fNWHPaQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9c6a282b57e2941626e929ce91cab750')


@app.route("/callback", methods=['POST'])#接收來自LINE伺服器的訊息，並轉載來處方下方的function
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__": #確保app.py是被直接執行，而不是載入檔案就馬上執行
    app.run()