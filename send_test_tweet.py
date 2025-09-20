#!/usr/bin/env python3
"""
Gerçek test tweet gönder
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tweepy
from src.config.settings import settings

def send_test_tweet():
    """Gerçek test tweet gönder"""
    
    print("📤 Test Tweet Gönderiliyor...")
    print("-" * 50)
    
    try:
        # Twitter Client oluştur
        client = tweepy.Client(
            consumer_key=settings.TWITTER_API_KEY,
            consumer_secret=settings.TWITTER_API_SECRET,
            access_token=settings.TWITTER_ACCESS_TOKEN,
            access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
            wait_on_rate_limit=True
        )
        
        # Test tweet metni
        test_text = "🤖 AutoHairTweets bot test! Ready to share amazing hairstyle content! ✂️ #hairstyle #bot #test"
        
        print(f"📝 Tweet Metni: {test_text}")
        print(f"📏 Karakter Sayısı: {len(test_text)}")
        
        # Tweet gönder
        response = client.create_tweet(text=test_text)
        
        if response.data:
            tweet_id = response.data['id']
            tweet_url = f"https://twitter.com/{settings.TWITTER_USERNAME}/status/{tweet_id}"
            
            print("✅ Tweet başarıyla gönderildi!")
            print(f"🆔 Tweet ID: {tweet_id}")
            print(f"🔗 Tweet URL: {tweet_url}")
            
            return True
        else:
            print("❌ Tweet gönderildi ama yanıt alınamadı")
            return False
            
    except tweepy.Forbidden as e:
        print(f"❌ İzin Hatası (403): {e}")
        print("\n🔧 Çözüm Önerileri:")
        print("1. Twitter Developer Portal → App Settings")
        print("2. User authentication settings → Edit")
        print("3. App permissions → Read and Write")
        print("4. Type of App → Web App, Automated App or Bot")
        print("5. Save changes ve Access Token'ları yenile")
        return False
        
    except tweepy.Unauthorized as e:
        print(f"❌ Yetkilendirme Hatası (401): {e}")
        print("🔧 API anahtarlarını kontrol edin")
        return False
        
    except Exception as e:
        print(f"❌ Genel Hata: {e}")
        return False

if __name__ == "__main__":
    success = send_test_tweet()
    
    if success:
        print("\n🎉 Bot tamamen hazır!")
        print("🚀 Artık otomatik tweet gönderebilir!")
    else:
        print("\n⚠️ İzin ayarlarını kontrol edin.")
        print("📋 Twitter Developer Portal'da gerekli ayarları yapın.")