import logging
from os import environ
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent, LocationMessageContent, StickerMessageContent
from library.storage.cache import UserLocation
from library.map.googlemap import FoodMapApi

configuration = Configuration(access_token=environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(environ.get('CHANNEL_SECRET'))
cache = UserLocation()
food = FoodMapApi(environ.get('MAP_API_KEY'))

def lambda_handler(event, context):
    # get X-Line-Signature header value
    signature = event['headers']['x-line-signature']

    # get request body as text
    body = event['body']

    logging.debug("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logging.error("Invalid signature. Please check your channel access token/channel secret.")
        return {
            'statusCode': 400,
            'body': 'Invalid signature'
        }
    except  Exception as e:
        logging.error("Error: " + str(e))
        return {
            'statusCode': 500,
            'body': 'Internal server error'
        }
    return {
        'statusCode': 200,
        'body': 'OK'
    }

@handler.add(MessageEvent, message=TextMessageContent)
@handler.add(MessageEvent, message=StickerMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        location = cache.getLocation(event.source.user_id)
        if location is None:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token, messages=[TextMessage(text="send your location first")]))
            return
        resp = food.getRecommend(location[0], location[1])

        line_bot_api.reply_message_with_http_info( 
            ReplyMessageRequest( 
                reply_token=event.reply_token, messages=[TextMessage(text=resp)]))
    
@handler.add(MessageEvent, message=LocationMessageContent)
def handle_location(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        latitude = event.message.latitude
        longitude = event.message.longitude
        user_id = event.source.user_id
        cache.setLocation(user_id, latitude, longitude)

        resp = food.getRecommend(latitude, longitude)
        line_bot_api.reply_message_with_http_info( 
            ReplyMessageRequest( 
                reply_token=event.reply_token, messages=[TextMessage(text=resp)]))
