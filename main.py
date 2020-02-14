from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import urllib.request, urllib.parse, re,random, os, csv
from function import calc,stalk,learn,helps,learn_data, generate

app = Flask(__name__)

line_bot_api = LineBotApi('secret') # Channel Access Token
handler = WebhookHandler('secret') # Channel Secret

cmd_lst = {
    "calc" : calc,
    "stalk" : stalk,
    "learn" : learn,
    "helps" : helps
}

@app.route("/callback", methods=['POST'])
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
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text   # Message from user
    if (text[0] == "/"):
        text = text[1:]

        if " " in text :
            cmd, query = text.split(" ",1)
        else:
            cmd = text

        try :
            if cmd == "learn":
                question, answer = query.split("|",1)
                if answer == '' or text == '':
                    result = TextSendMessage(text = "Message shouldn't be empty")
                else:
                    result = cmd_lst[cmd](question,answer)
            elif cmd in cmd_lst:
                result = cmd_lst[cmd](query)
            else:
                result = TextSendMessage(text ="Command doesn't exist.\nPlease see list of all available commands in : '/helps list'")
        except:
            result = TextSendMessage(text = "Invalid Command. Please see the list command using '/helps list'")
    else:
        visit = 0
        for i in range(len(learn_data)):
            if learn_data[i][0] == text:
                visit = 1
                result = TextSendMessage(text = learn_data[i][1])
        if visit == 0:
            result = TextSendMessage("Tidak semudah itu, Saya tidak mengerti maksud Anda.")

    line_bot_api.reply_message(event.reply_token, result)
    

if __name__ == "__main__":
    generate()
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT', 5000)))
