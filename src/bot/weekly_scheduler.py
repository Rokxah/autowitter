import schedule
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List
from src.bot.hair_bot import hair_bot
from src.content_creator.weekly_planner import weekly_planner
from src.config.settings import settings

class WeeklyScheduler:
    """Haftalık tweet zamanlayıcısı"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        self.tweet_times = [
            "09:00",  # Sabah
            "13:00",  # Öğle
            "17:00",  # Akşam
            "20:00"   # Gece
        ]
    
    def setup_daily_schedule(self):
        """Günlük tweet programını ayarla"""
        try:
            # Mevcut programı temizle
            schedule.clear()
            
            # Her gün için tweet zamanlarını ayarla
            daily_tweet_count = min(settings.TWEETS_PER_DAY, len(self.tweet_times))
            selected_times = self.tweet_times[:daily_tweet_count]
            
            for tweet_time in selected_times:
                schedule.every().day.at(tweet_time).do(self.send_scheduled_tweet)
                self.logger.info(f"Tweet zamanlandı: Her gün {tweet_time}")
            
            # Haftalık rapor (Pazartesi 08:00)
            schedule.every().monday.at("08:00").do(self.send_weekly_report)
            
            self.logger.info(f"Günlük {daily_tweet_count} tweet zamanlandı")
            
        except Exception as e:
            self.logger.error(f"Zamanlama ayarlama hatası: {e}")
    
    def send_scheduled_tweet(self):
        """Zamanlanmış tweet gönder"""
        try:
            self.logger.info("Zamanlanmış tweet gönderiliyor...")
            
            # Bugünün temasını kontrol et
            today_theme = weekly_planner.get_today_theme()
            self.logger.info(f"Bugünün teması: {today_theme['name']} {today_theme['emoji']}")
            
            # Tweet gönder (AI ile)
            success = hair_bot.post_hair_tweet(use_ai=True)
            
            if success:
                self.logger.info("✅ Zamanlanmış tweet başarıyla gönderildi!")
            else:
                self.logger.error("❌ Zamanlanmış tweet gönderilemedi!")
                
        except Exception as e:
            self.logger.error(f"Zamanlanmış tweet hatası: {e}")
    
    def send_weekly_report(self):
        """Haftalık rapor tweet'i"""
        try:
            week_schedule = weekly_planner.get_week_schedule()
            
            report_text = "🗓️ Bu haftanın saç stili programı:\n\n"
            for day, info in week_schedule.items():
                theme = info['theme']
                report_text += f"{day[:3]}: {theme['name']} {theme['emoji']}\n"
            
            report_text += "\n#HaftalıkProgram #hairstyle #Beauty #Stylish"
            
            # Raporu tweet olarak gönder
            success = hair_bot.twitter_client.post_tweet(report_text)
            
            if success:
                self.logger.info("📊 Haftalık rapor gönderildi!")
            else:
                self.logger.error("❌ Haftalık rapor gönderilemedi!")
                
        except Exception as e:
            self.logger.error(f"Haftalık rapor hatası: {e}")
    
    def start_scheduler(self):
        """Zamanlayıcıyı başlat"""
        try:
            self.logger.info("🚀 Haftalık zamanlayıcı başlatılıyor...")
            
            # Programı ayarla
            self.setup_daily_schedule()
            
            # Twitter bağlantısını test et
            if not hair_bot.authenticate_twitter():
                self.logger.error("❌ Twitter kimlik doğrulama başarısız!")
                return False
            
            self.is_running = True
            self.logger.info("✅ Zamanlayıcı aktif! Bekleyen görevler:")
            
            # Bekleyen görevleri listele
            for job in schedule.jobs:
                self.logger.info(f"   - {job}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Zamanlayıcı başlatma hatası: {e}")
            return False
    
    def run_scheduler(self):
        """Zamanlayıcıyı çalıştır (sürekli döngü)"""
        if not self.start_scheduler():
            return
        
        self.logger.info("⏰ Zamanlayıcı döngüsü başladı...")
        
        try:
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # Her dakika kontrol et
                
        except KeyboardInterrupt:
            self.logger.info("⏹️ Zamanlayıcı kullanıcı tarafından durduruldu")
        except Exception as e:
            self.logger.error(f"Zamanlayıcı döngü hatası: {e}")
        finally:
            self.stop_scheduler()
    
    def stop_scheduler(self):
        """Zamanlayıcıyı durdur"""
        self.is_running = False
        schedule.clear()
        self.logger.info("🛑 Zamanlayıcı durduruldu")
    
    def get_next_jobs(self) -> List[Dict]:
        """Sonraki görevleri al"""
        jobs = []
        for job in schedule.jobs:
            jobs.append({
                'job': str(job.job_func.__name__),
                'next_run': job.next_run.strftime('%Y-%m-%d %H:%M:%S') if job.next_run else 'N/A',
                'interval': str(job.interval),
                'unit': job.unit
            })
        return jobs
    
    def manual_tweet_now(self):
        """Manuel tweet gönder"""
        self.logger.info("📤 Manuel tweet gönderiliyor...")
        return self.send_scheduled_tweet()

# Global scheduler instance
weekly_scheduler = WeeklyScheduler()