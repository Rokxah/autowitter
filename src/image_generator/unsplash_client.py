import requests
import os
import logging
from typing import Optional, Dict, List
from PIL import Image
import io
from src.config.settings import settings

class UnsplashClient:
    """Unsplash API istemcisi - Ücretsiz saç stili görselleri"""
    
    def __init__(self):
        # Unsplash Access Key (ücretsiz, kayıt gerekli)
        self.access_key = "YOUR_UNSPLASH_ACCESS_KEY"  # .env'den alınacak
        self.base_url = "https://api.unsplash.com"
        self.logger = logging.getLogger(__name__)
        
    def search_hair_images(self, query: str, theme: str = None) -> List[Dict]:
        """
        Saç stili görselleri ara
        
        Args:
            query: Arama terimi (örn: "bob haircut", "pixie cut")
            theme: Tema (örn: "professional", "casual", "trendy")
            
        Returns:
            List[Dict]: Görsel bilgileri listesi
        """
        try:
            # Arama terimini oluştur
            search_query = f"hairstyle {query}"
            if theme:
                search_query += f" {theme}"
            
            # API isteği
            url = f"{self.base_url}/search/photos"
            params = {
                'query': search_query,
                'per_page': 10,
                'orientation': 'portrait',
                'content_filter': 'high',
                'order_by': 'relevant'
            }
            
            headers = {
                'Authorization': f'Client-ID {self.access_key}'
            }
            
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                images = []
                
                for photo in data.get('results', []):
                    images.append({
                        'id': photo['id'],
                        'url': photo['urls']['regular'],
                        'thumb_url': photo['urls']['thumb'],
                        'description': photo.get('description', ''),
                        'alt_description': photo.get('alt_description', ''),
                        'photographer': photo['user']['name'],
                        'photographer_url': photo['user']['links']['html']
                    })
                
                self.logger.info(f"Unsplash'dan {len(images)} görsel bulundu: {search_query}")
                return images
                
            else:
                self.logger.error(f"Unsplash API hatası: {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"Unsplash arama hatası: {e}")
            return []
    
    def download_image(self, image_url: str, filename: str) -> Optional[str]:
        """
        Görseli indir ve kaydet
        
        Args:
            image_url: Görsel URL'i
            filename: Kaydedilecek dosya adı
            
        Returns:
            str: Kaydedilen dosya yolu
        """
        try:
            # Görseli indir
            response = requests.get(image_url)
            
            if response.status_code == 200:
                # Dosya yolunu oluştur
                file_path = os.path.join(settings.IMAGES_DIR, filename)
                
                # Görseli kaydet
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                
                self.logger.info(f"Görsel kaydedildi: {file_path}")
                return file_path
            else:
                self.logger.error(f"Görsel indirme hatası: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Görsel kaydetme hatası: {e}")
            return None
    
    def get_random_hair_image(self, style: str, theme_name: str) -> Optional[Dict]:
        """
        Rastgele saç stili görseli al
        
        Args:
            style: Saç stili (örn: "bob", "pixie", "long hair")
            theme_name: Tema adı
            
        Returns:
            Dict: Görsel bilgisi ve dosya yolu
        """
        try:
            # Stil bazlı arama terimleri
            style_queries = {
                'bob': 'bob haircut woman',
                'pixie': 'pixie cut short hair',
                'long hair': 'long hairstyle woman',
                'undercut': 'undercut hairstyle',
                'braids': 'braided hairstyle',
                'curly': 'curly hair woman',
                'straight': 'straight hair woman',
                'waves': 'wavy hair woman',
                'updo': 'updo hairstyle elegant',
                'bangs': 'bangs fringe hairstyle'
            }
            
            # Tema bazlı ek terimler
            theme_terms = {
                'Short Hair Monday': 'professional short',
                'Tutorial Tuesday': 'tutorial step by step',
                'Trend Alert': 'trendy modern',
                'Throwback Hair': 'vintage retro',
                'Hair Care Friday': 'healthy shiny',
                'Weekend Glow': 'party glamorous',
                'Sunday Inspiration': 'transformation'
            }
            
            # Arama terimini oluştur
            base_query = style_queries.get(style, style)
            theme_term = theme_terms.get(theme_name, '')
            
            # Görselleri ara
            images = self.search_hair_images(base_query, theme_term)
            
            if images:
                # İlk görseli seç
                selected_image = images[0]
                
                # Dosya adını oluştur
                filename = f"hair_{style}_{theme_name.replace(' ', '_').lower()}_{selected_image['id']}.jpg"
                
                # Görseli indir
                file_path = self.download_image(selected_image['url'], filename)
                
                if file_path:
                    return {
                        'file_path': file_path,
                        'image_info': selected_image,
                        'style': style,
                        'theme': theme_name
                    }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Rastgele görsel alma hatası: {e}")
            return None

# Fallback görseller (Unsplash API yoksa)
class FallbackImageGenerator:
    """Yedek görsel üretici"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def create_text_image(self, text: str, style: str, theme: str) -> Optional[str]:
        """
        Metin tabanlı görsel oluştur
        
        Args:
            text: Görsel üzerindeki metin
            style: Saç stili
            theme: Tema
            
        Returns:
            str: Oluşturulan görsel dosya yolu
        """
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Görsel boyutları
            width, height = 800, 600
            
            # Tema renkları
            theme_colors = {
                'Short Hair Monday': ('#FF6B6B', '#4ECDC4'),
                'Tutorial Tuesday': ('#45B7D1', '#96CEB4'),
                'Trend Alert': ('#FF9F43', '#EE5A24'),
                'Throwback Hair': ('#5F27CD', '#00D2D3'),
                'Hair Care Friday': ('#FF6B9D', '#C44569'),
                'Weekend Glow': ('#FD79A8', '#FDCB6E'),
                'Sunday Inspiration': ('#6C5CE7', '#A29BFE')
            }
            
            # Renkleri al
            bg_color, text_color = theme_colors.get(theme, ('#2C3E50', '#ECF0F1'))
            
            # Görsel oluştur
            img = Image.new('RGB', (width, height), bg_color)
            draw = ImageDraw.Draw(img)
            
            # Metin ekle
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
            
            # Metni ortala
            text_lines = [
                f"✂️ {style.upper()}",
                "",
                theme,
                "",
                "AutoHairTweets",
                "@newhairstylesx"
            ]
            
            y_offset = height // 4
            for line in text_lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2
                draw.text((x, y_offset), line, fill=text_color, font=font)
                y_offset += 60
            
            # Dosya yolunu oluştur
            filename = f"fallback_{style}_{theme.replace(' ', '_').lower()}.png"
            file_path = os.path.join(settings.IMAGES_DIR, filename)
            
            # Görseli kaydet
            img.save(file_path)
            
            self.logger.info(f"Yedek görsel oluşturuldu: {file_path}")
            return file_path
            
        except Exception as e:
            self.logger.error(f"Yedek görsel oluşturma hatası: {e}")
            return None

# Global instances
unsplash_client = UnsplashClient()
fallback_generator = FallbackImageGenerator()