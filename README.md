# 🤖 AutoHairTweets

Professional hairstyle content automation bot for X.com (Twitter)

## 🎯 Features

- **AI-Powered Content**: Gemini AI generates engaging English tweets
- **Real Photos**: Unsplash API integration for authentic hairstyle images  
- **Weekly Themes**: 7-day rotating content schedule
- **Smart Hashtags**: Trending + theme-based hashtag combinations
- **Automated Scheduling**: 3 tweets per day (09:00, 15:00, 21:00)
- **Professional Tone**: Authentic hairstylist voice

## 📅 Weekly Schedule

- **Monday**: Short Hair Monday ✂️
- **Tuesday**: Tutorial Tuesday 🎥
- **Wednesday**: Trend Alert 🔥
- **Thursday**: Throwback Hair 🖤
- **Friday**: Hair Care Friday 💆‍♀️
- **Saturday**: Weekend Glow 🌸
- **Sunday**: Sunday Inspiration ✨

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/autowitter.git
cd autowitter
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Run the bot**
```bash
# Test single tweet
python test_real_photo_tweet.py

# Start scheduler
python run_scheduler.py
```

### Railway Deployment

1. **Fork this repository**
2. **Connect to Railway**: [railway.app](https://railway.app)
3. **Add environment variables** from `.env.example`
4. **Deploy**: Railway will automatically detect and run the bot

## 🔧 Configuration

### Required API Keys

- **Twitter API**: Get from [developer.twitter.com](https://developer.twitter.com)
- **Gemini AI**: Get from [ai.google.dev](https://ai.google.dev)
- **Unsplash API**: Get from [unsplash.com/developers](https://unsplash.com/developers)

### Environment Variables

```env
# Twitter API
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_CLIENT_ID=your_client_id
TWITTER_CLIENT_SECRET=your_client_secret
TWITTER_USERNAME=your_username

# AI Configuration
GEMINI_API_KEY=your_gemini_key

# Unsplash API
UNSPLASH_ACCESS_KEY=your_unsplash_key

# Bot Settings
TWEETS_PER_DAY=3
BOT_NAME=HairStyleHub
```

## 📁 Project Structure

```
autowitter/
├── src/
│   ├── ai/                 # Gemini AI integration
│   ├── api/                # Twitter API client
│   ├── bot/                # Main bot logic
│   ├── config/             # Configuration settings
│   ├── content_creator/    # Weekly planning system
│   └── image_generator/    # Photo management
├── data/
│   └── images/            # Downloaded photos
├── logs/                  # Application logs
├── main.py               # CLI interface
├── run_scheduler.py      # Automated scheduler
└── requirements.txt      # Dependencies
```

## 🎨 Content Examples

**Short Hair Monday**:
> "Short hair takes courage! ✂️ Starting the week with bold confidence! Which short style speaks to you? #hairstyle #haircut #confidence #trending"

**Tutorial Tuesday**:
> "Quick styling tip 🎥 Swipe for the tutorial! Master this look in under 5 minutes. #haircare #tutorial #hairstylist #fyp"

**Weekend Glow**:
> "Weekend energy activated 🌸 Ready to slay! What's your go-to weekend hairstyle? #beauty #weekendvibes #hairgoals #aesthetic"

## 🔄 Automation Features

- **Smart Scheduling**: Optimal posting times for engagement
- **Content Variety**: Never repeats the same tweet
- **Trend Integration**: Automatically includes viral hashtags
- **Photo Diversity**: Sources fresh images from Unsplash
- **Error Handling**: Graceful fallbacks and logging

## 📊 Performance

- **Daily Output**: 3 high-quality tweets
- **Engagement**: Optimized hashtags and timing
- **Authenticity**: Human-like content generation
- **Reliability**: 99.9% uptime with proper hosting

## 🛠️ Development

### Testing

```bash
# Test AI content generation
python main.py --ai-tweet

# Test photo system
python test_real_photo_tweet.py

# View weekly schedule
python main.py --schedule
```

### Adding New Themes

Edit `src/content_creator/weekly_planner.py` to customize themes:

```python
'Custom Theme': {
    'name': 'Custom Theme',
    'emoji': '🎨',
    'concept': 'Your concept here',
    'styles': ['style1', 'style2'],
    'hashtags': ['#custom', '#theme'],
    'content_types': ['tips', 'inspiration']
}
```

## 📝 License

MIT License - Feel free to use and modify for your projects.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues and questions:
- Open a GitHub issue
- Check the logs in `logs/` directory
- Review the configuration in `.env`

---

**Made with ❤️ for the hairstyling community**