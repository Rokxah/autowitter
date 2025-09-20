#!/usr/bin/env python3
"""
Görsel ile tweet gönderme testi
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.bot.hair_bot import hair_bot
from src.image_generator.unsplash_client import fallback_generator
from src.content_creator.weekly_planner import weekly_planner
import uuid

def test_image_tweet():
    """Görsel ile tweet testi"""
    
    print("🖼️ Görsel ile Tweet Testi")
    print("-" * 50)
    
    try:
        # Bugünün temasını al
        today_theme = weekly_planner.get_today_theme()
        print(f"🎨 Tema: {today_theme['name']} {today_theme['emoji']}")
        
        # AI ile içerik üret
        content = hair_bot.generate_hair_content(use_ai=True)
        print(f"📝 İçerik: {content['text']}")
        print(f"🎯 Stil: {content['style']}")
        
        # Görsel oluştur
        print("\n🖼️ Görsel oluşturuluyor...")
        image_path = fallback_generator.create_text_image(
            text=content['text'][:50] + "...",
            style=content['style'],
            theme=content['theme']
        )
        
        if image_path:
            print(f"✅ Görsel oluşturuldu: {image_path}")
            
            # Twitter kimlik doğrulama
            if not hair_bot.authenticate_twitter():
                print("❌ Twitter kimlik doğrulama başarısız!")
                return False
            
            # Unique tweet metni (duplicate hatası olmasın)
            unique_id = str(uuid.uuid4())[:8]
            unique_text = f"{content['text']} #{unique_id}"
            
            print(f"\n📤 Tweet gönderiliyor...")
            print(f"📝 Metin: {unique_text}")
            print(f"🖼️ Görsel: {os.path.basename(image_path)}")
            
            # Tweet gönder
            success = hair_bot.twitter_client.post_tweet(
                text=unique_text,
                image_path=image_path
            )
            
            if success:
                print("✅ Görsel ile tweet başarıyla gönderildi!")
                return True
            else:
                print("❌ Tweet gönderilemedi!")
                return False
        else:
            print("❌ Görsel oluşturulamadı!")
            return False
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

if __name__ == "__main__":
    success = test_image_tweet()
    
    if success:
        print("\n🎉 Görsel tweet sistemi çalışıyor!")
        print("🚀 Bot artık görsel ile tweet gönderebilir!")
    else:
        print("\n⚠️ Görsel tweet sisteminde sorun var.")
        print("🔧 Hata loglarını kontrol edin.")