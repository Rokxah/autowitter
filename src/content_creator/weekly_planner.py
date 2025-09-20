from datetime import datetime, timedelta
from typing import Dict, List
import calendar

class WeeklyContentPlanner:
    """Haftalık içerik planlayıcısı"""
    
    def __init__(self):
        self.weekly_themes = {
            0: {  # Pazartesi
                'name': 'Short Hair Monday',
                'emoji': '✂️',
                'concept': 'Kısa saç ilhamları',
                'styles': ['bob', 'pixie', 'lob', 'buzz cut', 'short layers'],
                'hashtags': ['#ShortHairMonday', '#kısasaç', '#bobsaç', '#pixiecut'],
                'content_types': ['transformation', 'celebrity_inspiration', 'poll']
            },
            1: {  # Salı
                'name': 'Tutorial Tuesday',
                'emoji': '🎥',
                'concept': 'Hızlı saç modelleri ve ipuçları',
                'styles': ['topuz', 'örgü', 'günlük şekillendirme', 'hızlı modeller'],
                'hashtags': ['#TutorialTuesday', '#saçipucu', '#hairtutorial', '#quickhair'],
                'content_types': ['tutorial', 'tips', 'how_to']
            },
            2: {  # Çarşamba
                'name': 'Trend Alert',
                'emoji': '🔥',
                'concept': 'Haftanın trend saç modeli',
                'styles': ['curtain bangs', 'layered cut', 'wolf cut', 'shag', 'modern mullet'],
                'hashtags': ['#TrendAlert', '#trendsaç', '#hairstyletrend', '#modernsaç'],
                'content_types': ['trend_showcase', 'comparison', 'poll']
            },
            3: {  # Perşembe
                'name': 'Throwback Hair',
                'emoji': '🖤',
                'concept': 'Retro & nostaljik saç ilhamı',
                'styles': ['90s grunge', '70s feathers', '50s victory rolls', 'vintage waves'],
                'hashtags': ['#ThrowbackHair', '#vintagesaç', '#retrostyle', '#nostaljik'],
                'content_types': ['vintage_inspiration', 'icon_tribute', 'decade_focus']
            },
            4: {  # Cuma
                'name': 'Hair Care Friday',
                'emoji': '💆‍♀️',
                'concept': 'Saç bakım tüyoları',
                'styles': ['bakım rutini', 'doğal maskeler', 'ürün önerileri'],
                'hashtags': ['#HairCareFriday', '#saçbakımı', '#haircare', '#saçsağlığı'],
                'content_types': ['care_tips', 'product_review', 'diy_masks']
            },
            5: {  # Cumartesi
                'name': 'Weekend Glow',
                'emoji': '🌸',
                'concept': 'Eğlenceli, hafif içerik',
                'styles': ['party hair', 'festival looks', 'fun colors', 'creative styles'],
                'hashtags': ['#WeekendGlow', '#partysaç', '#eğlenceli', '#yaratıcı'],
                'content_types': ['fun_content', 'quiz', 'meme']
            },
            6: {  # Pazar
                'name': 'Sunday Inspiration',
                'emoji': '✨',
                'concept': 'İlham verici saç dönüşümleri',
                'styles': ['dramatic change', 'color transformation', 'length change'],
                'hashtags': ['#SundayInspiration', '#saçdönüşümü', '#transformation', '#ilham'],
                'content_types': ['inspiration', 'before_after', 'motivation']
            }
        }
    
    def get_today_theme(self) -> Dict:
        """Bugünün temasını al"""
        today = datetime.now().weekday()
        return self.weekly_themes[today]
    
    def get_theme_by_day(self, day: int) -> Dict:
        """Belirli bir günün temasını al (0=Pazartesi, 6=Pazar)"""
        return self.weekly_themes.get(day, self.weekly_themes[0])
    
    def get_week_schedule(self) -> Dict:
        """Bu haftanın tam programını al"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        
        schedule = {}
        for i in range(7):
            day_date = week_start + timedelta(days=i)
            day_name = calendar.day_name[i]
            theme = self.weekly_themes[i]
            
            schedule[day_name] = {
                'date': day_date.strftime('%Y-%m-%d'),
                'theme': theme
            }
        
        return schedule
    
    def get_content_suggestions(self, theme: Dict) -> List[str]:
        """Tema için içerik önerileri"""
        suggestions = []
        
        if 'transformation' in theme['content_types']:
            suggestions.append(f"{theme['name']} dönüşümü ile yeni sen! {theme['emoji']}")
        
        if 'tips' in theme['content_types']:
            suggestions.append(f"Bugünün ipucu: {theme['concept']} {theme['emoji']}")
        
        if 'poll' in theme['content_types']:
            suggestions.append(f"Hangisini tercih edersin? {theme['emoji']}")
        
        if 'inspiration' in theme['content_types']:
            suggestions.append(f"{theme['name']} ilhamı {theme['emoji']}")
        
        return suggestions

# Global planner instance
weekly_planner = WeeklyContentPlanner()