import tweepy
import logging
from typing import Optional, List
from src.config.settings import settings

class TwitterClient:
    """X.com (Twitter) API istemcisi"""
    
    def __init__(self):
        self.api_key = settings.TWITTER_API_KEY
        self.api_secret = settings.TWITTER_API_SECRET
        self.client_id = settings.TWITTER_CLIENT_ID
        self.client_secret = settings.TWITTER_CLIENT_SECRET
        self.username = settings.TWITTER_USERNAME
        self.client = None
        self.api = None
        self._setup_logging()
        
    def _setup_logging(self):
        """Logging ayarları"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{settings.LOGS_DIR}/twitter_bot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def authenticate(self, access_token: str = None, access_token_secret: str = None) -> bool:
        """
        Twitter API kimlik doğrulama
        OAuth 2.0 Bearer Token veya OAuth 1.0a kullanabilir
        """
        try:
            # Eğer access token verilmemişse, settings'den al
            if not access_token:
                access_token = settings.TWITTER_ACCESS_TOKEN
                access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET
            
            # OAuth 1.0a ile (okuma ve yazma için)
            auth = tweepy.OAuth1UserHandler(
                self.api_key,
                self.api_secret,
                access_token,
                access_token_secret
            )
            
            self.api = tweepy.API(auth, wait_on_rate_limit=True)
            
            # OAuth 2.0 Client ile de dene
            try:
                self.client = tweepy.Client(
                    consumer_key=self.api_key,
                    consumer_secret=self.api_secret,
                    access_token=access_token,
                    access_token_secret=access_token_secret,
                    wait_on_rate_limit=True
                )
            except Exception as oauth1_error:
                self.logger.warning(f"OAuth 1.0a hatası: {oauth1_error}")
                # OAuth 2.0 ile dene
                self.client = tweepy.Client(
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    wait_on_rate_limit=True
                )
            
            # Bağlantıyı test et
            if self.client:
                self.logger.info("Twitter API bağlantısı başarılı!")
                return True
            else:
                self.logger.error("Twitter API bağlantısı başarısız!")
                return False
                
        except Exception as e:
            self.logger.error(f"Twitter kimlik doğrulama hatası: {e}")
            return False
    
    def post_tweet(self, text: str, image_path: Optional[str] = None) -> bool:
        """
        Tweet gönder
        
        Args:
            text: Tweet metni
            image_path: Görsel dosya yolu (opsiyonel)
            
        Returns:
            bool: Başarı durumu
        """
        try:
            if not self.client:
                self.logger.error("Twitter client başlatılmamış!")
                return False
            
            # Görsel varsa yükle
            media_id = None
            if image_path and self.api:
                media = self.api.media_upload(image_path)
                media_id = [media.media_id]
            
            # Tweet gönder
            if media_id:
                response = self.client.create_tweet(text=text, media_ids=media_id)
            else:
                response = self.client.create_tweet(text=text)
            
            if response.data:
                tweet_id = response.data['id']
                self.logger.info(f"Tweet başarıyla gönderildi! ID: {tweet_id}")
                return True
            else:
                self.logger.error("Tweet gönderilemedi!")
                return False
                
        except Exception as e:
            self.logger.error(f"Tweet gönderme hatası: {e}")
            return False
    
    def get_user_info(self) -> Optional[dict]:
        """Kullanıcı bilgilerini al"""
        try:
            if not self.client:
                return None
                
            user = self.client.get_me()
            if user.data:
                return {
                    'id': user.data.id,
                    'username': user.data.username,
                    'name': user.data.name,
                    'followers_count': user.data.public_metrics.get('followers_count', 0),
                    'following_count': user.data.public_metrics.get('following_count', 0),
                    'tweet_count': user.data.public_metrics.get('tweet_count', 0)
                }
            return None
            
        except Exception as e:
            self.logger.error(f"Kullanıcı bilgisi alma hatası: {e}")
            return None
    
    def test_connection(self) -> bool:
        """API bağlantısını test et"""
        try:
            user_info = self.get_user_info()
            if user_info:
                self.logger.info(f"Bağlantı testi başarılı! Kullanıcı: @{user_info['username']}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Bağlantı testi hatası: {e}")
            return False

# Global Twitter client instance
twitter_client = TwitterClient()