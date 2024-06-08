from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent, LocationMessageContent, StickerMessageContent
from config import Config
from app.storage.cache import UserLocation
from app.map.googlemap import FoodMapApi

def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    configuration = Configuration(access_token=app.config.get('CHANNEL_ACCESS_TOKEN'))
    handler = WebhookHandler(app.config.get('CHANNEL_SECRET'))

    cache = UserLocation()
    food = FoodMapApi(app.config.get('MAP_API_KEY'))
    
    @app.route("/health")
    def health():
        return {'Message': 'OK'}
    
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
            app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
            abort(400)
        return 'OK'
    
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
            # resp = ai.getfoodInfo(location[0], location[1])
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

    return app

