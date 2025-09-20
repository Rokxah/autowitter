import os
from decouple import config

class Settings:
    """Uygulama ayarları"""
    
    # Twitter API
    TWITTER_API_KEY = config('TWITTER_API_KEY')
    TWITTER_API_SECRET = config('TWITTER_API_SECRET')
    TWITTER_ACCESS_TOKEN = config('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = config('TWITTER_ACCESS_TOKEN_SECRET')
    TWITTER_CLIENT_ID = config('TWITTER_CLIENT_ID')
    TWITTER_CLIENT_SECRET = config('TWITTER_CLIENT_SECRET')
    TWITTER_USERNAME = config('TWITTER_USERNAME')
    
    # AI API
    GEMINI_API_KEY = config('GEMINI_API_KEY')
    
    # Unsplash API (for real photos)
    UNSPLASH_ACCESS_KEY = config('UNSPLASH_ACCESS_KEY', default='')
    
    # Bot ayarları
    TWEETS_PER_DAY = config('TWEETS_PER_DAY', default=4, cast=int)
    BOT_NAME = config('BOT_NAME', default='HairStyleHub')
    
    # Dosya yolları
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    IMAGES_DIR = os.path.join(DATA_DIR, 'images')
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')
    
    # Tweet ayarları
    MAX_TWEET_LENGTH = 280
    # Trending Hashtags (English only)
    HASHTAGS = [
        '#hairstyle', '#haircut', '#haircolor', '#hairgoals',
        '#beauty', '#style', '#haircare', '#hairtrends',
        '#salon', '#hairstylist', '#hairinspiration', '#gorgeous',
        '#trendy', '#chic', '#elegant', '#stunning',
        '#transformation', '#makeover', '#selfcare', '#confidence'
    ]
    
    # Popular trending hashtags to mix in
    TRENDING_HASHTAGS = [
        '#viral', '#trending', '#fyp', '#inspo', '#mood',
        '#aesthetic', '#vibes', '#goals', '#slay', '#iconic'
    ]
    
    @classmethod
    def create_directories(cls):
        """Gerekli klasörleri oluştur"""
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        os.makedirs(cls.IMAGES_DIR, exist_ok=True)
        os.makedirs(cls.LOGS_DIR, exist_ok=True)

# Ayarları başlat
settings = Settings()
settings.create_directories()