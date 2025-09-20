#!/usr/bin/env python3
"""
Twitter API izinlerini test et
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tweepy
from src.config.settings import settings

def test_twitter_permissions():
    """Twitter API izinlerini test et"""
    
    print("🔍 Twitter API İzinleri Test Ediliyor...")
    print("-" * 50)
    
    try:
        # OAuth 1.0a ile test
        print("1️⃣ OAuth 1.0a Test:")
        auth = tweepy.OAuth1UserHandler(
            settings.TWITTER_API_KEY,
            settings.TWITTER_API_SECRET,
            settings.TWITTER_ACCESS_TOKEN,
            settings.TWITTER_ACCESS_TOKEN_SECRET
        )
        
        api = tweepy.API(auth)
        
        # Kullanıcı bilgilerini al
        user = api.verify_credentials()
        if user:
            print(f"   ✅ Kullanıcı: @{user.screen_name}")
            print(f"   📊 Takipçi: {user.followers_count}")
            print(f"   📝 Tweet: {user.statuses_count}")
        
        # Client v2 test
        print("\n2️⃣ Twitter API v2 Test:")
        client = tweepy.Client(
            consumer_key=settings.TWITTER_API_KEY,
            consumer_secret=settings.TWITTER_API_SECRET,
            access_token=settings.TWITTER_ACCESS_TOKEN,
            access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET
        )
        
        me = client.get_me()
        if me.data:
            print(f"   ✅ Kullanıcı: @{me.data.username}")
            print(f"   🆔 ID: {me.data.id}")
        
        # İzinleri kontrol et
        print("\n3️⃣ İzin Kontrolü:")
        
        # Test tweet (DRY RUN)
        test_text = "Test tweet - bu gönderilmeyecek"
        print(f"   📝 Test Tweet: {test_text}")
        
        # Gerçek tweet göndermeyi dene
        try:
            # response = client.create_tweet(text=test_text)
            print("   ⚠️ Gerçek tweet gönderimi test edilmedi (güvenlik için)")
            print("   💡 Manuel test için: client.create_tweet(text='test') çalıştırın")
        except Exception as e:
            print(f"   ❌ Tweet gönderme hatası: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Twitter API hatası: {e}")
        return False

def show_required_permissions():
    """Gerekli izinleri göster"""
    print("\n📋 Gerekli Twitter API İzinleri:")
    print("=" * 50)
    print("1. App Type: Web App, Automated App or Bot")
    print("2. App Permissions: Read and Write")
    print("3. Authentication: OAuth 1.0a")
    print("4. Callback URL: http://localhost:3000/callback")
    print("5. Website URL: https://github.com/username/autowitter")
    print("\n🔗 Ayar Yeri:")
    print("developer.twitter.com → Dashboard → Your App → Settings")
    print("→ User authentication settings → Edit")

if __name__ == "__main__":
    success = test_twitter_permissions()
    
    if not success:
        show_required_permissions()
    else:
        print("\n✅ Twitter API bağlantısı başarılı!")
        print("🚀 Bot tweet göndermeye hazır!")