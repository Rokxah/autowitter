import google.generativeai as genai
import logging
from typing import Optional, Dict, List
from src.config.settings import settings

class GeminiClient:
    """Google Gemini AI istemcisi"""
    
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = None
        self._setup_logging()
        self._configure_gemini()
    
    def _setup_logging(self):
        """Logging ayarları"""
        self.logger = logging.getLogger(__name__)
    
    def _configure_gemini(self):
        """Gemini yapılandırması"""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.logger.info("Gemini AI başarıyla yapılandırıldı")
        except Exception as e:
            self.logger.error(f"Gemini yapılandırma hatası: {e}")
    
    def generate_hair_content(self, theme: Dict, style_focus: str = None) -> Dict:
        """
        Saç stili içeriği üret
        
        Args:
            theme: Haftalık tema bilgisi
            style_focus: Odaklanılacak stil (opsiyonel)
            
        Returns:
            Dict: Üretilen içerik
        """
        try:
            # Prompt oluştur
            prompt = self._create_content_prompt(theme, style_focus)
            
            # Gemini'den içerik üret
            response = self.model.generate_content(prompt)
            
            if response.text:
                # İçeriği işle
                content = self._process_generated_content(response.text, theme)
                return content
            else:
                self.logger.error("Gemini'den boş yanıt alındı")
                return self._get_fallback_content(theme)
                
        except Exception as e:
            self.logger.error(f"İçerik üretme hatası: {e}")
            return self._get_fallback_content(theme)
    
    def _create_content_prompt(self, theme: Dict, style_focus: str = None) -> str:
        """İçerik üretimi için prompt oluştur"""
        
        base_prompt = f"""
        You are a professional hairstylist and social media influencer.
        
        Today's theme: {theme['name']} {theme['emoji']}
        Concept: {theme['concept']}
        
        Create an engaging Twitter tweet following these criteria:
        
        1. Tweet must not exceed 280 characters
        2. Must be in ENGLISH only
        3. Should be engaging, natural, and authentic (like a real person)
        4. Should be informative about hairstyles
        5. Use appropriate emojis (but not too many)
        6. Include 3-4 relevant hashtags from these: {', '.join(theme['hashtags'][:4])}
        7. Add 1 trending hashtag from: #viral, #trending, #fyp, #inspo, #mood, #aesthetic, #vibes, #goals
        8. Sound like a real hairstylist sharing genuine advice/inspiration
        9. Avoid mentioning any bot names or automated systems
        
        """
        
        if style_focus:
            base_prompt += f"Focus especially on this style: {style_focus}\n"
        
        if 'poll' in theme['content_types']:
            base_prompt += "Include a question or comparison in the content.\n"
        
        if 'tips' in theme['content_types']:
            base_prompt += "Provide a practical tip.\n"
        
        base_prompt += """
        Return only the tweet text, no additional explanations.
        Example format: "Short hair takes courage! ✂️ Show your elegance with a bob cut. Which bob style do you prefer? #ShortHairMonday #bobhair #boldstyle"
        """
        
        return base_prompt
    
    def _process_generated_content(self, generated_text: str, theme: Dict) -> Dict:
        """Üretilen içeriği işle"""
        # Metni temizle
        clean_text = generated_text.strip()
        
        # Çok uzunsa kısalt
        if len(clean_text) > 280:
            clean_text = clean_text[:270] + "..."
        
        return {
            'text': clean_text,
            'theme': theme['name'],
            'concept': theme['concept'],
            'emoji': theme['emoji'],
            'hashtags': theme['hashtags'],
            'generated_by': 'gemini',
            'timestamp': None
        }
    
    def _get_fallback_content(self, theme: Dict) -> Dict:
        """Hata durumunda yedek içerik - İngilizce"""
        fallback_texts = {
            'Short Hair Monday': f"Short hair takes courage! {theme['emoji']} Start the new week with a fresh new style!",
            'Tutorial Tuesday': f"Today's tip {theme['emoji']} Stay tuned for quick and stylish hair tutorials!",
            'Trend Alert': f"Everyone's talking about this! {theme['emoji']} Don't miss the trending hairstyles!",
            'Throwback Hair': f"Timeless elegance from the past {theme['emoji']} The magic of vintage hairstyles!",
            'Hair Care Friday': f"Best care for your hair {theme['emoji']} The secret to healthy hair!",
            'Weekend Glow': f"Weekend vibes {theme['emoji']} Time for fun hairstyles!",
            'Sunday Inspiration': f"Start the new week with inspiration {theme['emoji']} The power of hair transformations!"
        }
        
        text = fallback_texts.get(theme['name'], f"{theme['concept']} {theme['emoji']}")
        
        # Hashtag'leri karıştır - tema + trend
        import random
        theme_hashtags = theme['hashtags'][:3]
        trend_hashtag = random.choice(settings.TRENDING_HASHTAGS)
        all_hashtags = theme_hashtags + [trend_hashtag]
        hashtags = ' '.join(all_hashtags)
        
        return {
            'text': f"{text} {hashtags}",
            'theme': theme['name'],
            'concept': theme['concept'],
            'emoji': theme['emoji'],
            'hashtags': all_hashtags,
            'generated_by': 'fallback',
            'timestamp': None
        }
    
    def generate_image_prompt(self, theme: Dict, style: str) -> str:
        """Görsel üretimi için prompt oluştur"""
        try:
            prompt = f"""
            I want to create a {style} hairstyle image for the {theme['name']} theme.
            
            Suggest an appropriate prompt for the image:
            - Professional hairstyle photography
            - Focused on {style}
            - High quality
            - Studio lighting
            
            Return only the English prompt, no explanations.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip() if response.text else f"Professional {style} hairstyle, studio lighting, high quality"
            
        except Exception as e:
            self.logger.error(f"Görsel prompt üretme hatası: {e}")
            return f"Professional {style} hairstyle, studio lighting, high quality"

# Global Gemini client instance
gemini_client = GeminiClient()