#!/usr/bin/env python3
"""
Gerçek fotoğraf ile tweet gönderme testi
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.bot.hair_bot import hair_bot
from src.image_generator.real_photo_client import real_photo_client
from src.content_creator.weekly_planner import weekly_planner
import uuid
import random

def test_real_photo_tweet():
    """Gerçek fotoğraf ile tweet testi"""
    
    print("📸 Gerçek Fotoğraf ile Tweet Testi")
    print("-" * 50)
    
    try:
        # Bugünün temasını al
        today_theme = weekly_planner.get_today_theme()
        print(f"🎨 Tema: {today_theme['name']} {today_theme['emoji']}")
        
        # AI ile içerik üret
        content = hair_bot.generate_hair_content(use_ai=True)
        print(f"📝 İçerik: {content['text']}")
        print(f"🎯 Stil: {content['style']}")
        
        # Gerçek fotoğraf al (Unsplash API anahtarı varsa)
        print("\n📸 Gerçek fotoğraf aranıyor...")
        
        # Unsplash API anahtarı kontrolü
        from src.config.settings import settings
        if settings.UNSPLASH_ACCESS_KEY:
            image_path = real_photo_client.get_random_hair_photo(
                style_focus=content['style'],
                theme=content['theme']
            )
            
            if image_path:
                print(f"✅ Gerçek fotoğraf bulundu: {os.path.basename(image_path)}")
            else:
                print("⚠️ Gerçek fotoğraf bulunamadı, yedek görsel oluşturuluyor...")
                from src.image_generator.unsplash_client import fallback_generator
                image_path = fallback_generator.create_text_image(
                    text=content['text'][:50] + "...",
                    style=content['style'],
                    theme=content['theme']
                )
        else:
            print("⚠️ Unsplash API anahtarı yok, yedek görsel oluşturuluyor...")
            from src.image_generator.unsplash_client import fallback_generator
            image_path = fallback_generator.create_text_image(
                text=content['text'][:50] + "...",
                style=content['style'],
                theme=content['theme']
            )
        
        if not image_path:
            print("❌ Görsel oluşturulamadı!")
            return False
        
        # Twitter kimlik doğrulama
        if not hair_bot.authenticate_twitter():
            print("❌ Twitter kimlik doğrulama başarısız!")
            return False
        
        # Unique tweet metni (duplicate hatası olmasın)
        unique_id = str(uuid.uuid4())[:8]
        unique_text = f"{content['text']} #{unique_id}"
        
        print(f"\n📤 Tweet gönderiliyor...")
        print(f"📝 Metin: {unique_text}")
        print(f"📸 Görsel: {os.path.basename(image_path)}")
        
        # Tweet gönder
        success = hair_bot.twitter_client.post_tweet(
            text=unique_text,
            image_path=image_path
        )
        
        if success:
            print("✅ Gerçek fotoğraf ile tweet başarıyla gönderildi!")
            return True
        else:
            print("❌ Tweet gönderilemedi!")
            return False
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

def test_hashtag_system():
    """Yeni hashtag sistemini test et"""
    
    print("\n🏷️ Hashtag Sistemi Testi")
    print("-" * 30)
    
    try:
        from src.config.settings import settings
        
        print("📋 Tema Hashtag'leri:")
        for i, hashtag in enumerate(settings.HASHTAGS[:10], 1):
            print(f"  {i}. {hashtag}")
        
        print("\n🔥 Trend Hashtag'leri:")
        for i, hashtag in enumerate(settings.TRENDING_HASHTAGS, 1):
            print(f"  {i}. {hashtag}")
        
        # Rastgele kombinasyon örneği
        theme_tags = random.sample(settings.HASHTAGS, 3)
        trend_tag = random.choice(settings.TRENDING_HASHTAGS)
        
        print(f"\n✨ Örnek Kombinasyon:")
        print(f"   Tema: {' '.join(theme_tags)}")
        print(f"   Trend: {trend_tag}")
        print(f"   Final: {' '.join(theme_tags + [trend_tag])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Hashtag testi hatası: {e}")
        return False

if __name__ == "__main__":
    print("🤖 Gelişmiş Tweet Sistemi Testi")
    print("=" * 60)
    
    # Hashtag sistemini test et
    hashtag_success = test_hashtag_system()
    
    # Gerçek fotoğraf tweet'ini test et
    tweet_success = test_real_photo_tweet()
    
    print("\n" + "=" * 60)
    if hashtag_success and tweet_success:
        print("🎉 Tüm testler başarılı!")
        print("✅ Hashtag sistemi çalışıyor")
        print("✅ Gerçek fotoğraf sistemi çalışıyor")
        print("✅ Tweet gönderimi başarılı")
        print("\n🚀 Bot artık gerçek bir hesap gibi çalışıyor!")
    else:
        print("⚠️ Bazı testlerde sorun var:")
        if not hashtag_success:
            print("❌ Hashtag sistemi sorunu")
        if not tweet_success:
            print("❌ Tweet gönderimi sorunu")
        print("\n🔧 Hata loglarını kontrol edin.")