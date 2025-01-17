from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests
from bs4 import BeautifulSoup 

line_bot_api = LineBotApi('HTExNo62oadvqggyDBnIr0kbeJaNYgffN7FMSLWJ6DTOEGiYIuERbisRuCV9xEuw13I9d2gT65zEHXzL6/4/DjUW8TYaFPc8lS4Bjcl3qQsO6YYM1/tLFp1IwCuT3n3IYURUpbt9XkOpjf2CtoNZlQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler("cf5191a1405dbf6b419917bc1915917c")

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        return HttpResponse("ok")
    else:
        return HttpResponseBadRequest()
    
@handler.add(event=MessageEvent)
def handl_message(event):
   
    response = requests.get(
    "https://travel.ettoday.net/article/2101206.htm"
    )
    soup = BeautifulSoup(response.text, "html.parser")

    titles=soup.find_all("h3",limit=10)
    outInfo=""
    for title in titles:
        outInfo+=title.select_one("a").getText()+"\n"+title.select_one("a").get("href")+"\n"
    message = TextSendMessage(text=outInfo)
    line_bot_api.reply_message(
    event.reply_token,
    message)
