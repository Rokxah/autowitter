#!/usr/bin/env python3
"""
AutoHairTweets - Saç Stili Otomatik Tweet Botu
Ana çalıştırma dosyası
"""

import sys
import os
from datetime import datetime

# Proje kök dizinini Python path'ine ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.bot.hair_bot import hair_bot
from src.bot.weekly_scheduler import weekly_scheduler
from src.content_creator.weekly_planner import weekly_planner
from src.config.settings import settings

def main():
    """Ana fonksiyon"""
    print(f"🤖 {settings.BOT_NAME} başlatılıyor...")
    print(f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👤 Kullanıcı: @{settings.TWITTER_USERNAME}")
    print("-" * 50)
    
    # Bugünün temasını göster
    today_theme = weekly_planner.get_today_theme()
    print(f"🎨 Bugünün Teması: {today_theme['name']} {today_theme['emoji']}")
    print(f"📋 Konsept: {today_theme['concept']}")
    print("-" * 50)
    
    # Bot testi yap
    print("🔍 Bot testi yapılıyor...")
    if hair_bot.test_bot():
        print("✅ Bot testi başarılı!")
        
        # Bot durumunu göster
        status = hair_bot.get_bot_status()
        print(f"📊 Bot Durumu: {status['status']}")
        
        if status.get('user_info'):
            user = status['user_info']
            print(f"👥 Takipçi: {user.get('followers_count', 0)}")
            print(f"📝 Tweet: {user.get('tweet_count', 0)}")
        
        print("\n🚀 Bot hazır! Komutlar:")
        print("1. AI tweet test: python main.py --ai-tweet")
        print("2. Gerçek tweet gönder: python main.py --send-tweet")
        print("3. Haftalık program: python main.py --schedule")
        print("4. Yardım: python main.py --help")
        
    else:
        print("❌ Bot testi başarısız!")
        print("🔧 API anahtarlarını kontrol edin.")

def test_ai_tweet():
    """AI ile tweet içeriği test et"""
    print("🤖 AI ile tweet içeriği üretiliyor...")
    
    # Bugünün temasını göster
    today_theme = weekly_planner.get_today_theme()
    print(f"🎨 Tema: {today_theme['name']} {today_theme['emoji']}")
    
    # AI ile içerik üret
    content = hair_bot.generate_hair_content(use_ai=True)
    print(f"📝 Üretilen İçerik: {content['text']}")
    print(f"🎯 Stil: {content['style']}")
    print(f"🤖 Üretici: {content['generated_by']}")

def send_real_tweet():
    """Gerçek tweet gönder"""
    print("📤 Gerçek tweet gönderiliyor...")
    
    # Twitter kimlik doğrulama
    if not hair_bot.authenticate_twitter():
        print("❌ Twitter kimlik doğrulama başarısız!")
        return
    
    # AI ile tweet gönder
    success = hair_bot.post_hair_tweet(use_ai=True)
    
    if success:
        print("✅ Tweet başarıyla gönderildi!")
    else:
        print("❌ Tweet gönderilemedi!")

def show_weekly_schedule():
    """Haftalık programı göster"""
    print("📅 Bu Haftanın Saç Stili Programı:")
    print("=" * 50)
    
    schedule = weekly_planner.get_week_schedule()
    
    for day, info in schedule.items():
        theme = info['theme']
        date = info['date']
        
        print(f"📅 {day} ({date})")
        print(f"   🎨 {theme['name']} {theme['emoji']}")
        print(f"   📋 {theme['concept']}")
        print()

def show_help():
    """Yardım menüsü"""
    print("🤖 AutoHairTweets - Gelişmiş Saç Stili Botu")
    print("=" * 50)
    print("📋 Komutlar:")
    print("  python main.py --ai-tweet    - AI ile tweet test et")
    print("  python main.py --send-tweet  - Gerçek tweet gönder")
    print("  python main.py --schedule    - Haftalık program")
    print("  python main.py --help        - Yardım")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--ai-tweet":
            test_ai_tweet()
        elif command == "--send-tweet":
            send_real_tweet()
        elif command == "--schedule":
            show_weekly_schedule()
        elif command == "--help":
            show_help()
        else:
            print(f"❌ Bilinmeyen komut: {command}")
            show_help()
    else:
        main()