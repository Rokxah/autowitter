import requests
import os
import logging
import random
from typing import Optional, Dict, List
from src.config.settings import settings

class RealPhotoClient:
    """Gerçek saç fotoğrafları için Unsplash API istemcisi"""
    
    def __init__(self):
        self.access_key = settings.UNSPLASH_ACCESS_KEY
        self.base_url = "https://api.unsplash.com"
        self.logger = logging.getLogger(__name__)
        
        # Saç stili arama terimleri
        self.hair_search_terms = {
            'short hair': ['short hair', 'pixie cut', 'bob haircut', 'short hairstyle'],
            'long hair': ['long hair', 'long hairstyle', 'wavy hair', 'straight hair'],
            'curly hair': ['curly hair', 'natural curls', 'curly hairstyle'],
            'braids': ['braids', 'braided hair', 'french braid', 'dutch braid'],
            'updo': ['updo', 'bun hairstyle', 'elegant updo', 'wedding hair'],
            'bangs': ['bangs', 'fringe', 'curtain bangs', 'side bangs'],
            'color': ['hair color', 'blonde hair', 'brunette hair', 'red hair'],
            'men hair': ['mens haircut', 'mens hairstyle', 'beard', 'male grooming'],
            'vintage': ['vintage hair', 'retro hairstyle', '50s hair', 'classic hair'],
            'trendy': ['trendy hair', 'modern hairstyle', 'fashion hair', 'stylish hair']
        }
    
    def search_hair_photos(self, style_focus: str, theme: str, count: int = 10) -> List[Dict]:
        """
        Saç stili fotoğrafları ara
        
        Args:
            style_focus: Odaklanılacak stil
            theme: Haftalık tema
            count: Kaç fotoğraf getirileceği
            
        Returns:
            List[Dict]: Fotoğraf bilgileri listesi
        """
        if not self.access_key:
            self.logger.warning("Unsplash API anahtarı bulunamadı")
            return []
        
        try:
            # Arama terimini belirle
            search_term = self._get_search_term(style_focus, theme)
            
            # Unsplash API'den ara
            headers = {
                'Authorization': f'Client-ID {self.access_key}'
            }
            
            params = {
                'query': search_term,
                'per_page': count,
                'orientation': 'portrait',
                'content_filter': 'high',
                'order_by': 'relevant'
            }
            
            response = requests.get(
                f"{self.base_url}/search/photos",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                photos = []
                
                for photo in data.get('results', []):
                    photos.append({
                        'id': photo['id'],
                        'url': photo['urls']['regular'],
                        'download_url': photo['urls']['full'],
                        'description': photo.get('description', ''),
                        'alt_description': photo.get('alt_description', ''),
                        'photographer': photo['user']['name'],
                        'photographer_url': photo['user']['links']['html'],
                        'unsplash_url': photo['links']['html']
                    })
                
                self.logger.info(f"Unsplash'dan {len(photos)} fotoğraf bulundu: {search_term}")
                return photos
            else:
                self.logger.error(f"Unsplash API hatası: {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"Fotoğraf arama hatası: {e}")
            return []
    
    def download_photo(self, photo_info: Dict, filename: str = None) -> Optional[str]:
        """
        Fotoğrafı indir
        
        Args:
            photo_info: Fotoğraf bilgileri
            filename: Dosya adı (opsiyonel)
            
        Returns:
            str: İndirilen dosya yolu
        """
        try:
            if not filename:
                filename = f"hair_photo_{photo_info['id']}.jpg"
            
            file_path = os.path.join(settings.IMAGES_DIR, filename)
            
            # Fotoğrafı indir
            response = requests.get(photo_info['download_url'], timeout=30)
            
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                
                self.logger.info(f"Fotoğraf indirildi: {filename}")
                return file_path
            else:
                self.logger.error(f"Fotoğraf indirme hatası: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Fotoğraf indirme hatası: {e}")
            return None
    
    def get_random_hair_photo(self, style_focus: str = None, theme: str = None) -> Optional[str]:
        """
        Rastgele saç fotoğrafı al ve indir
        
        Args:
            style_focus: Stil odağı
            theme: Tema
            
        Returns:
            str: İndirilen fotoğraf yolu
        """
        try:
            # Fotoğrafları ara
            photos = self.search_hair_photos(style_focus or 'hairstyle', theme or 'general', count=20)
            
            if not photos:
                self.logger.warning("Unsplash'dan fotoğraf bulunamadı")
                return None
            
            # Rastgele bir fotoğraf seç
            selected_photo = random.choice(photos)
            
            # Fotoğrafı indir
            filename = f"real_hair_{selected_photo['id']}.jpg"
            file_path = self.download_photo(selected_photo, filename)
            
            if file_path:
                self.logger.info(f"Gerçek saç fotoğrafı hazır: {filename}")
                return file_path
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"Rastgele fotoğraf alma hatası: {e}")
            return None
    
    def _get_search_term(self, style_focus: str, theme: str) -> str:
        """Arama terimi oluştur"""
        
        # Stil odağına göre terim seç
        if style_focus:
            style_lower = style_focus.lower()
            
            for category, terms in self.hair_search_terms.items():
                if any(keyword in style_lower for keyword in category.split()):
                    return random.choice(terms)
        
        # Temaya göre terim seç
        if theme:
            theme_lower = theme.lower()
            
            if 'short' in theme_lower:
                return random.choice(self.hair_search_terms['short hair'])
            elif 'tutorial' in theme_lower:
                return random.choice(['hairstyle tutorial', 'hair styling', 'hair tips'])
            elif 'trend' in theme_lower:
                return random.choice(self.hair_search_terms['trendy'])
            elif 'throwback' in theme_lower or 'vintage' in theme_lower:
                return random.choice(self.hair_search_terms['vintage'])
            elif 'care' in theme_lower:
                return random.choice(['hair care', 'healthy hair', 'hair treatment'])
            elif 'weekend' in theme_lower or 'glow' in theme_lower:
                return random.choice(['beautiful hair', 'gorgeous hairstyle', 'hair goals'])
        
        # Varsayılan terimler
        default_terms = [
            'hairstyle', 'hair inspiration', 'beautiful hair', 
            'hair goals', 'stylish hair', 'hair fashion'
        ]
        
        return random.choice(default_terms)

# Global instance
real_photo_client = RealPhotoClient()