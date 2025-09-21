#!/usr/bin/env python3
"""
AutoHairTweets - Otomatik Zamanlayıcı
Günde 3 tweet gönderir: 09:00, 15:00, 21:00
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import schedule
import time
import logging
from datetime import datetime
from src.bot.hair_bot import hair_bot
from src.image_generator.real_photo_client import real_photo_client
from src.content_creator.weekly_planner import weekly_planner
import uuid

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scheduler.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def send_scheduled_tweet():
    """Zamanlanmış tweet gönder"""
    try:
        logger.info("🤖 Zamanlanmış tweet gönderimi başlıyor...")
        
        # Bugünün temasını al
        today_theme = weekly_planner.get_today_theme()
        logger.info(f"🎨 Tema: {today_theme['name']} {today_theme['emoji']}")
        
        # AI ile içerik üret
        content = hair_bot.generate_hair_content(use_ai=True)
        logger.info(f"📝 İçerik üretildi: {content['text'][:50]}...")
        
        # Gerçek saç fotoğrafı al
        image_path = real_photo_client.get_random_hair_photo(
            style_focus=content['style'],
            theme=content['theme']
        )
        
        if image_path:
            logger.info(f"🖼️ Görsel oluşturuldu: {os.path.basename(image_path)}")
            
            # Unique tweet metni
            unique_id = str(uuid.uuid4())[:8]
            unique_text = f"{content['text']} #{unique_id}"
            
            # Tweet gönder
            success = hair_bot.twitter_client.post_tweet(
                text=unique_text,
                image_path=image_path
            )
            
            if success:
                logger.info("✅ Zamanlanmış tweet başarıyla gönderildi!")
            else:
                logger.error("❌ Zamanlanmış tweet gönderilemedi!")
        else:
            logger.error("❌ Görsel oluşturulamadı!")
            
    except Exception as e:
        logger.error(f"❌ Zamanlanmış tweet hatası: {e}")

def main():
    """Ana zamanlayıcı fonksiyonu"""
    
    print("🤖 AutoHairTweets Zamanlayıcısı Başlatılıyor...")
    print("=" * 60)
    print("📅 Günlük Tweet Programı:")
    print("   🌅 09:00 - Sabah Tweet'i")
    print("   🌞 15:00 - Öğleden Sonra Tweet'i") 
    print("   🌙 21:00 - Akşam Tweet'i")
    print("=" * 60)
    
    # Twitter kimlik doğrulama
    if not hair_bot.authenticate_twitter():
        logger.error("❌ Twitter kimlik doğrulama başarısız!")
        return
    
    logger.info("✅ Twitter bağlantısı başarılı!")
    
    # Zamanlamaları ayarla
    schedule.every().day.at("09:00").do(send_scheduled_tweet)
    schedule.every().day.at("15:00").do(send_scheduled_tweet)
    schedule.every().day.at("21:00").do(send_scheduled_tweet)
    
    logger.info("⏰ Zamanlayıcı aktif! Tweet'ler otomatik gönderilecek...")
    
    # Test tweet'i (hemen gönder)
    print("\n🧪 Test tweet'i gönderiliyor...")
    send_scheduled_tweet()
    
    print("\n🔄 Zamanlayıcı çalışıyor... (Ctrl+C ile durdurun)")
    
    # Sonsuz döngü - zamanlamaları kontrol et
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Her dakika kontrol et
            
    except KeyboardInterrupt:
        logger.info("⏹️ Zamanlayıcı durduruldu!")
        print("\n👋 AutoHairTweets zamanlayıcısı kapatıldı!")

if __name__ == "__main__":
    # Logs klasörünü oluştur
    os.makedirs('logs', exist_ok=True)
    
    main()