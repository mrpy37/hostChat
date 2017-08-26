# coding: UTF-8
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
  FollowEvent, PostbackEvent, MessageEvent, TextMessage, TextSendMessage, LocationMessage, TemplateSendMessage, ImageMessage, ImageSendMessage
)
from linebot.models.template import (
  ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, URITemplateAction, PostbackTemplateAction, 
  CarouselTemplate, CarouselColumn
  )
import re

app = Flask(__name__)

 get channel_secret and channel_access_token from your environment variable
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


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
# follow event
@handler.add(FollowEvent)
def handle_follow(event):
  line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=u'Colorful Talk株式会社です。この度、弊社のサービス””をご利用いただき、ありがとうございます。'))
  # get user_id from event
  uId = event.source.user_id
  print(uId)

#get profile from user_id
  profile = line_bot_api.get_profile(uId)
  print(profile.display_name)
  print(profile.user_id)

  text = event.message.text

  if text == 'aaa':
   # line_bot_api.push_message(profile.user_id, TextSendMessage(text='Bello!'))
    print('Success!!!!!!!!1')

  else:
    print('Erroooooooooor')
  

@handler.add(MessageEvent, message=TextMessage) 
def handle_message(event):
  text = event.message.text

  if text == 'start':
    start_menu = ButtonsTemplate(
      title = u'店舗管理メニュー', 
      text = u'操作を選んでください', 
      actions=[
      PostbackTemplateAction(label=u'登録/修正', data='edit', text=u'編集したい商品を選んでください。'),
      PostbackTemplateAction(label=u'確認', data='confirm',text=u'お客様から見たBotのプレビューです。')]
      )
    template_message = TemplateSendMessage(
      alt_text='Buttons alt text', 
      template=start_menu
      )
    line_bot_api.reply_message(event.reply_token, template_message)
  
  elif text == u'編集したい商品を選んでください。':
    pass
  elif text == u'お客様から見たBotのプレビューです。':
    pass

  else:
    line_bot_api.reply_message(
      event.reply_token,
      TextSendMessage(text=u'"start"と入力してください。')
      )

  # get user_id from event
  uId = event.source.user_id
  print(uId)

  #get profile from user_id
  profile = line_bot_api.get_profile(uId)
  print(profile.display_name)
  print(profile.user_id)
  print('reply to text message')
  #line_bot_api.push_message(profile.user_id, TextSendMessage(text='Bello!'))


@handler.add(PostbackEvent) 
def handle_postback(event):
  if event.postback.data == 'ping':
    line_bot_api.reply_message(
      event.reply_token, TextSendMessage(text='pong'))

  elif event.postback.data == 'edit':
    edit_menu = CarouselTemplate(
      columns=[
      CarouselColumn(
        thumbnail_image_url='https://stat.ameba.jp/user_images/20161210/17/dsgkomatsu2/e4/8e/j/o0860121713818171577.jpg?caw=800',
        title='A Shop',
        text='Hello!',
        actions=[
        PostbackTemplateAction(
          label='menu1',
          text='postback text1',
          data='action=buy&itemid=1'),
        MessageTemplateAction(
          label='menu2',
          text='message text1'),
        URITemplateAction(
          label='Calling',
          uri='tel:090-6118-6328'
          )]),
      CarouselColumn(
        thumbnail_image_url='https://s3-us-west-2.amazonaws.com/lineapitest/hamburger_240.jpeg',
        title='Tadano Restraunt',
        text='Welcome!',
        actions=[
        PostbackTemplateAction(
          label='menu1',
          text='postback text1',
          data='action=buy&itemid=1'),
        MessageTemplateAction(
          label='menu2',
          text='message text1'),
        URITemplateAction(
          label='uri1',
          uri='http://example.com/1'
          )]),
      CarouselColumn(
        thumbnail_image_url='https://s3-us-west-2.amazonaws.com/lineapitest/hamburger_240.jpeg',
        title='this is menu2',
        text='description2',
        actions=[
        PostbackTemplateAction(
          label='postback2',
          text='postback text2',
          data='action=buy&itemid=2'),
        MessageTemplateAction(
          label='message2',
          text='message text2'),
        URITemplateAction(
          label='uri2',
          uri='http://example.com/2')])
        ])

    template_message = TemplateSendMessage(
      alt_text='Carousel text', template=edit_menu)
    line_bot_api.reply_message(event.reply_token, template_message)

#  elif event.postback.data == 'confirm':


  else:
    line_bot_api.reply_message(
      event.reply_token, TextSendMessage(text=event.postback.data))

if __name__ == "__main__": 
  app.run()
