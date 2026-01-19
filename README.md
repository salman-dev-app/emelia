# 🎵 Emelia Telegram Bot

A feature-rich Telegram bot for music playback and group management.

**Created by:** Salman (@otakuosenpai)

## Features

### 🎵 Music Player
- Play songs from JioSaavn API (free)
- Player controls: Play/Pause, ±10 sec seek
- Progress bar with time display
- Queue management
- Album art display

### 🛡️ Group Management
- Ban/Unban users
- Mute/Unmute users
- Warn system
- Admin-only controls

## 🚀 Deployment on Koyeb (Free)

### Step 1: Get Your Bot Token
1. Open Telegram and search for **@BotFather**
2. Send `/newbot` command
3. Choose a name: **Emelia**
4. Choose a username: **emelia_music_bot** (or any available name)
5. Copy the **bot token** (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Create GitHub Repository
1. Go to [GitHub](https://github.com) and sign in
2. Click **"New Repository"** (green button)
3. Name it: `emelia-telegram-bot`
4. Make it **Public**
5. Click **"Create repository"**

### Step 3: Upload Files to GitHub
1. In your new repository, click **"Add file"** → **"Upload files"**
2. Upload these 3 files:
   - `bot.py` (the main bot code from artifact #1)
   - `requirements.txt` (from artifact #2)
   - `Dockerfile` (from artifact #3)
3. Click **"Commit changes"**

### Step 4: Deploy on Koyeb
1. Go to [Koyeb](https://app.koyeb.com) and sign up (free)
2. Click **"Create App"**
3. Select **"GitHub"** as deployment method
4. Connect your GitHub account
5. Select your repository: `emelia-telegram-bot`
6. Configure:
   - **Builder:** Docker
   - **Port:** 8080 (optional, bot uses polling)
   - **Environment Variables:** 
     - Key: `BOT_TOKEN`
     - Value: (paste your bot token from BotFather)
7. Click **"Deploy"**

### Step 5: Start Using Your Bot
1. Open Telegram
2. Search for your bot username
3. Send `/start` to begin!

## 📝 Bot Commands

### Music Commands
- `/play <song name>` - Play a song
- `/pause` - Pause playback
- `/resume` - Resume playback
- `/stop` - Stop playback
- `/queue` - Show playlist

### Group Management (Admin Only)
- `/ban` - Ban user (reply to their message)
- `/unban` - Unban user (reply to their message)
- `/mute` - Mute user (reply to their message)
- `/unmute` - Unmute user (reply to their message)
- `/warn` - Warn user

### General
- `/start` - Welcome message
- `/help` - Show help

## 🎮 Player Controls

When a song is playing, use these buttons:
- **⏮ -10s** - Go back 10 seconds
- **▶️ Play / ⏸ Pause** - Play or pause
- **⏭ +10s** - Skip forward 10 seconds
- **🔁 Loop** - Loop current song
- **⏹ Stop** - Stop playback
- **📝 Queue** - View playlist

## 🔧 Troubleshooting

### Bot doesn't respond
- Check if it's running on Koyeb dashboard
- Verify your BOT_TOKEN is correct

### Music doesn't play
- The bot provides song info and controls
- Actual audio playback requires voice chat integration

### Group commands not working
- Make sure the bot is an admin in your group
- You must also be an admin to use admin commands

## 📞 Support

Created by Salman - Telegram: [@otakuosenpai](https://t.me/otakuosenpai)

## 🔄 Updates

To update your bot:
1. Edit files in GitHub repository
2. Koyeb will automatically redeploy

## ⚠️ Important Notes

- **Free tier limitations:** Koyeb free tier has some limitations
- **API Rate limits:** JioSaavn API may have rate limits
- Keep your BOT_TOKEN secret!
- The bot uses polling, so it doesn't need webhooks

## 📄 License

Free to use and modify!

---

**Enjoy your Emelia Bot! 🎵**
