from os import path, environ

basedir = path.abspath(path.dirname(__file__))

class Config:
    CHANNEL_ACCESS_TOKEN=environ.get('CHANNEL_ACCESS_TOKEN')
    CHANNEL_SECRET=environ.get('CHANNEL_SECRET')
    MAP_API_KEY=environ.get('MAP_API_KEY')
    AI_KEY=environ.get('AI_KEY')
    CHAT_AI_KEY=environ.get('CHAT_AI_KEY')