import random
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any
from src.api.twitter_client import twitter_client
from src.config.settings import settings
from src.content_creator.weekly_planner import weekly_planner
from src.ai.gemini_client import gemini_client
from src.image_generator.real_photo_client import real_photo_client

class HairStyleBot:
    """Saç stili paylaşım botu ana sınıfı"""
    
    def __init__(self):
        self.twitter_client = twitter_client
        self.logger = logging.getLogger(__name__)
        
        # Örnek saç stili içerikleri (başlangıç için)
        self.sample_contents = [
            {
                'text': 'Klasik erkek saç kesimi ile şıklığınızı tamamlayın! ✂️ #saçstili #hairstyle #erkeksaçı',
                'style': 'klasik'
            },
            {
                'text': 'Kadın bob saç modeli - zamansız şıklık! 💇‍♀️ #bobsaç #kadınsaçı #saçmodelleri',
                'style': 'bob'
            },
            {
                'text': 'Undercut saç stili ile modern görünüm! 🔥 #undercut #modernsaç #trendsaç',
                'style': 'undercut'
            },
            {
                'text': 'Uzun dalgalı saçlar için bakım önerileri 🌊 #uzunsaç #dalgalısaç #saçbakımı',
                'style': 'dalgalı'
            },
            {
                'text': 'Pixie cut ile cesur ve şık! ✨ #pixiecut #kısasaç #cesursaç',
                'style': 'pixie'
            }
        ]
    
    def authenticate_twitter(self, access_token: str = None, access_token_secret: str = None) -> bool:
        """Twitter kimlik doğrulama"""
        return self.twitter_client.authenticate(access_token, access_token_secret)
    
    def generate_hair_content(self, use_ai: bool = True) -> Dict[str, Any]:
        """
        Saç stili içeriği üret
        
        Args:
            use_ai: AI kullanarak içerik üret (True) veya örnek içerik kullan (False)
        """
        if use_ai:
            # Bugünün temasını al
            today_theme = weekly_planner.get_today_theme()
            
            # Temaya uygun stil seç
            style_focus = random.choice(today_theme['styles']) if today_theme['styles'] else None
            
            # Gemini ile içerik üret
            ai_content = gemini_client.generate_hair_content(today_theme, style_focus)
            
            return {
                'text': ai_content['text'],
                'style': style_focus or today_theme['name'],
                'theme': today_theme['name'],
                'concept': today_theme['concept'],
                'generated_by': ai_content['generated_by'],
                'timestamp': datetime.now().isoformat()
            }
        else:
            # Eski yöntem - örnek içerikler
            content = random.choice(self.sample_contents)
            
            # Hashtag'leri ekle
            hashtags = random.sample(settings.HASHTAGS, k=random.randint(3, 5))
            hashtag_text = ' '.join(hashtags)
            
            # Tweet metnini oluştur
            base_text = content['text']
            if len(base_text + ' ' + hashtag_text) <= settings.MAX_TWEET_LENGTH:
                final_text = f"{base_text} {hashtag_text}"
            else:
                final_text = base_text
            
            return {
                'text': final_text,
                'style': content['style'],
                'theme': 'classic',
                'generated_by': 'sample',
                'timestamp': datetime.now().isoformat()
            }
    
    def post_hair_tweet(self, image_path: Optional[str] = None, use_ai: bool = True) -> bool:
        """
        Saç stili tweet'i gönder
        
        Args:
            image_path: Görsel dosya yolu (opsiyonel)
            
        Returns:
            bool: Başarı durumu
        """
        try:
            # İçerik üret
            content = self.generate_hair_content(use_ai=use_ai)
            
            # Eğer görsel yolu verilmemişse, gerçek saç fotoğrafı al
            if not image_path:
                style_focus = content.get('style', 'hairstyle')
                theme = content.get('theme', 'general')
                
                image_path = real_photo_client.get_random_hair_photo(
                    style_focus=style_focus,
                    theme=theme
                )
                
                if image_path:
                    self.logger.info(f"Gerçek saç fotoğrafı alındı: {image_path}")
                else:
                    self.logger.warning("Gerçek fotoğraf alınamadı, sadece metin gönderilecek")
            
            # Tweet gönder
            success = self.twitter_client.post_tweet(
                text=content['text'],
                image_path=image_path
            )
            
            if success:
                self.logger.info(f"Saç stili tweet'i gönderildi: {content['style']} (Tema: {content.get('theme', 'N/A')})")
                return True
            else:
                self.logger.error("Tweet gönderilemedi!")
                return False
                
        except Exception as e:
            self.logger.error(f"Tweet gönderme hatası: {e}")
            return False
    
    def get_bot_status(self) -> Dict[str, Any]:
        """Bot durumu bilgilerini al"""
        try:
            user_info = self.twitter_client.get_user_info()
            
            return {
                'bot_name': settings.BOT_NAME,
                'username': settings.TWITTER_USERNAME,
                'user_info': user_info,
                'tweets_per_day': settings.TWEETS_PER_DAY,
                'status': 'active' if user_info else 'inactive',
                'last_check': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Bot durumu alma hatası: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'last_check': datetime.now().isoformat()
            }
    
    def test_bot(self) -> bool:
        """Bot fonksiyonlarını test et"""
        try:
            self.logger.info("Bot testi başlatılıyor...")
            
            # Twitter bağlantısını test et
            if not self.twitter_client.test_connection():
                self.logger.error("Twitter bağlantı testi başarısız!")
                return False
            
            # İçerik üretimini test et
            content = self.generate_hair_content()
            self.logger.info(f"Test içeriği üretildi: {content['text'][:50]}...")
            
            self.logger.info("Bot testi başarılı!")
            return True
            
        except Exception as e:
            self.logger.error(f"Bot testi hatası: {e}")
            return False

# Global bot instance
hair_bot = HairStyleBot()