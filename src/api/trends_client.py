import tweepy
import logging
import random
from typing import List, Dict, Optional
from src.config.settings import settings

class TrendsClient:
    """Twitter Trends API istemcisi"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = None
        self.api = None
        self._setup_client()
        
        # Saç/güzellik ile ilgili trend filtreleri
        self.beauty_keywords = [
            'hair', 'beauty', 'style', 'fashion', 'makeup', 'skincare',
            'salon', 'cut', 'color', 'trend', 'look', 'gorgeous', 'stunning',
            'chic', 'elegant', 'transformation', 'makeover', 'glow', 'aesthetic'
        ]
        
        # Genel popüler hashtag'ler (fallback)
        self.fallback_trends = [
            '#viral', '#trending', '#fyp', '#inspo', '#mood',
            '#aesthetic', '#vibes', '#goals', '#slay', '#iconic',
            '#weekend', '#saturday', '#sunday', '#monday', '#motivation',
            '#selfcare', '#confidence', '#beautiful', '#amazing', '#perfect'
        ]
    
    def _setup_client(self):
        """Twitter API istemcisini ayarla"""
        try:
            # OAuth 1.0a (v1.1 API için)
            auth = tweepy.OAuth1UserHandler(
                settings.TWITTER_API_KEY,
                settings.TWITTER_API_SECRET,
                settings.TWITTER_ACCESS_TOKEN,
                settings.TWITTER_ACCESS_TOKEN_SECRET
            )
            
            self.api = tweepy.API(auth, wait_on_rate_limit=True)
            
            # OAuth 2.0 (v2 API için)
            self.client = tweepy.Client(
                bearer_token=None,  # Bearer token yoksa None
                consumer_key=settings.TWITTER_API_KEY,
                consumer_secret=settings.TWITTER_API_SECRET,
                access_token=settings.TWITTER_ACCESS_TOKEN,
                access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
                wait_on_rate_limit=True
            )
            
            self.logger.info("Trends API istemcisi başarıyla ayarlandı")
            
        except Exception as e:
            self.logger.error(f"Trends API ayarlama hatası: {e}")
    
    def get_trending_hashtags(self, woeid: int = 1, count: int = 10) -> List[str]:
        """
        Trend olan hashtag'leri al
        
        Args:
            woeid: Where On Earth ID (1 = Worldwide, 23424969 = Turkey)
            count: Kaç hashtag alınacağı
            
        Returns:
            List[str]: Trend hashtag'ler listesi
        """
        try:
            if not self.api:
                self.logger.warning("Twitter API bağlantısı yok, fallback hashtag'ler kullanılıyor")
                return random.sample(self.fallback_trends, min(count, len(self.fallback_trends)))
            
            # Trend konuları al
            trends = self.api.get_place_trends(woeid)[0]['trends']
            
            trending_hashtags = []
            
            for trend in trends:
                name = trend['name']
                
                # Hashtag ise ve uygun ise ekle
                if name.startswith('#') and len(name) > 2:
                    # Güzellik/saç ile ilgili mi kontrol et
                    if any(keyword.lower() in name.lower() for keyword in self.beauty_keywords):
                        trending_hashtags.append(name)
                    # Genel popüler hashtag'ler
                    elif any(word in name.lower() for word in ['viral', 'trend', 'mood', 'aesthetic', 'goals']):
                        trending_hashtags.append(name)
                
                if len(trending_hashtags) >= count:
                    break
            
            # Yeterli hashtag bulunamazsa fallback'lerden ekle
            if len(trending_hashtags) < count:
                needed = count - len(trending_hashtags)
                fallback_sample = random.sample(self.fallback_trends, min(needed, len(self.fallback_trends)))
                trending_hashtags.extend(fallback_sample)
            
            self.logger.info(f"{len(trending_hashtags)} trend hashtag bulundu")
            return trending_hashtags[:count]
            
        except Exception as e:
            self.logger.error(f"Trend hashtag alma hatası: {e}")
            # Hata durumunda fallback hashtag'ler döndür
            return random.sample(self.fallback_trends, min(count, len(self.fallback_trends)))
    
    def get_mixed_hashtags(self, base_count: int = 3, trend_count: int = 2) -> List[str]:
        """
        Sabit hashtag'ler + trend hashtag'ler karışımı
        
        Args:
            base_count: Sabit hashtag sayısı
            trend_count: Trend hashtag sayısı
            
        Returns:
            List[str]: Karışık hashtag listesi
        """
        try:
            # Sabit saç hashtag'lerinden seç
            base_hashtags = random.sample(settings.HASHTAGS, min(base_count, len(settings.HASHTAGS)))
            
            # Trend hashtag'leri al
            trend_hashtags = self.get_trending_hashtags(count=trend_count)
            
            # Karıştır ve döndür
            mixed_hashtags = base_hashtags + trend_hashtags
            
            self.logger.info(f"Karışık hashtag'ler: {len(base_hashtags)} sabit + {len(trend_hashtags)} trend")
            return mixed_hashtags
            
        except Exception as e:
            self.logger.error(f"Karışık hashtag oluşturma hatası: {e}")
            # Hata durumunda sadece sabit hashtag'ler
            return random.sample(settings.HASHTAGS, min(base_count, len(settings.HASHTAGS)))
    
    def get_location_trends(self, location: str = "worldwide") -> List[Dict]:
        """
        Belirli lokasyon için trend'leri al
        
        Args:
            location: Lokasyon ("worldwide", "turkey", "usa", etc.)
            
        Returns:
            List[Dict]: Trend bilgileri
        """
        try:
            # Lokasyon WOEID'leri
            location_woeids = {
                "worldwide": 1,
                "turkey": 23424969,
                "usa": 23424977,
                "uk": 23424975,
                "canada": 23424775
            }
            
            woeid = location_woeids.get(location.lower(), 1)
            
            if not self.api:
                return []
            
            trends = self.api.get_place_trends(woeid)[0]['trends']
            
            trend_list = []
            for trend in trends[:20]:  # İlk 20 trend
                trend_list.append({
                    'name': trend['name'],
                    'url': trend['url'],
                    'tweet_volume': trend.get('tweet_volume', 0)
                })
            
            self.logger.info(f"{location} için {len(trend_list)} trend alındı")
            return trend_list
            
        except Exception as e:
            self.logger.error(f"Lokasyon trend'leri alma hatası: {e}")
            return []

# Global trends client instance
trends_client = TrendsClient()