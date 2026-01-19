import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import requests
from datetime import datetime, timedelta

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
ADMIN_ID = 'otakuosenpai'

# Music player state
player_state = {
    'playing': False,
    'current_song': None,
    'position': 0,
    'duration': 0,
    'playlist': []
}

# Group management data
group_settings = {}

# Music API - Using JioSaavn API (free)
def search_song(query):
    try:
        url = f"https://saavn.dev/api/search/songs?query={query}&limit=5"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', {}).get('results', [])
    except:
        pass
    return []

def get_song_url(song_id):
    try:
        url = f"https://saavn.dev/api/songs/{song_id}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [{}])[0].get('downloadUrl', [{}])[0].get('url')
    except:
        pass
    return None

# Music Player Controls
def create_player_keyboard(position=0, duration=180):
    keyboard = [
        [
            InlineKeyboardButton("⏮ -10s", callback_data="back_10"),
            InlineKeyboardButton("⏸ Pause" if player_state['playing'] else "▶️ Play", callback_data="play_pause"),
            InlineKeyboardButton("⏭ +10s", callback_data="forward_10")
        ],
        [
            InlineKeyboardButton("🔁 Loop", callback_data="loop"),
            InlineKeyboardButton("⏹ Stop", callback_data="stop"),
            InlineKeyboardButton("📝 Queue", callback_data="queue")
        ]
    ]
    
    # Progress bar
    progress = int((position / duration) * 20) if duration > 0 else 0
    progress_bar = "▓" * progress + "░" * (20 - progress)
    time_str = f"{format_time(position)} {progress_bar} {format_time(duration)}"
    
    return InlineKeyboardMarkup(keyboard), time_str

def format_time(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = f"""
🎵 **Welcome to Emelia Bot!** 🎵

Hi {update.effective_user.first_name}! I'm Emelia, your Telegram music and group management assistant.

**Music Features:**
🎧 /play <song name> - Play a song
⏸️ /pause - Pause playback
▶️ /resume - Resume playback
⏹️ /stop - Stop playback
📝 /queue - Show playlist

**Group Management:**
👮 /ban <user> - Ban user
🔓 /unban <user> - Unban user
🔇 /mute <user> - Mute user
🔊 /unmute <user> - Unmute user
⚠️ /warn <user> - Warn user
🛡️ /settings - Group settings

**Info:**
📊 /stats - Group statistics
ℹ️ /help - Show this message

Created by @{ADMIN_ID}
"""
    await update.message.reply_text(welcome_msg)

# Play Command
async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a song name!\nUsage: /play <song name>")
        return
    
    query = ' '.join(context.args)
    await update.message.reply_text(f"🔍 Searching for: {query}...")
    
    results = search_song(query)
    
    if not results:
        await update.message.reply_text("❌ No songs found. Please try another search.")
        return
    
    # Get first result
    song = results[0]
    player_state['current_song'] = song
    player_state['playing'] = True
    player_state['position'] = 0
    player_state['duration'] = song.get('duration', 180)
    
    song_url = get_song_url(song.get('id'))
    
    keyboard, time_str = create_player_keyboard(0, player_state['duration'])
    
    msg = f"""
🎵 **Now Playing**

**Title:** {song.get('name', 'Unknown')}
**Artist:** {song.get('artists', {}).get('primary', [{}])[0].get('name', 'Unknown') if song.get('artists', {}).get('primary') else 'Unknown'}
**Album:** {song.get('album', {}).get('name', 'Unknown') if song.get('album') else 'Unknown'}

{time_str}
"""
    
    if song.get('image'):
        await update.message.reply_photo(
            photo=song['image'][2]['url'],
            caption=msg,
            reply_markup=keyboard
        )
    else:
        await update.message.reply_text(msg, reply_markup=keyboard)

# Callback Query Handler
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    action = query.data
    
    if action == "play_pause":
        player_state['playing'] = not player_state['playing']
        status = "▶️ Playing" if player_state['playing'] else "⏸️ Paused"
        await query.answer(status)
        
    elif action == "back_10":
        player_state['position'] = max(0, player_state['position'] - 10)
        await query.answer("⏮ -10 seconds")
        
    elif action == "forward_10":
        player_state['position'] = min(player_state['duration'], player_state['position'] + 10)
        await query.answer("⏭ +10 seconds")
        
    elif action == "stop":
        player_state['playing'] = False
        player_state['position'] = 0
        await query.answer("⏹ Stopped")
        
    elif action == "queue":
        queue_msg = "📝 **Queue is empty**"
        if player_state['playlist']:
            queue_msg = "📝 **Current Queue:**\n\n"
            for i, song in enumerate(player_state['playlist'], 1):
                queue_msg += f"{i}. {song.get('name', 'Unknown')}\n"
        await query.message.reply_text(queue_msg)
        return
    
    # Update player UI
    if player_state['current_song']:
        keyboard, time_str = create_player_keyboard(player_state['position'], player_state['duration'])
        
        song = player_state['current_song']
        msg = f"""
🎵 **Now Playing**

**Title:** {song.get('name', 'Unknown')}
**Artist:** {song.get('artists', {}).get('primary', [{}])[0].get('name', 'Unknown') if song.get('artists', {}).get('primary') else 'Unknown'}
**Album:** {song.get('album', {}).get('name', 'Unknown') if song.get('album') else 'Unknown'}

{time_str}
"""
        
        try:
            await query.edit_message_caption(caption=msg, reply_markup=keyboard)
        except:
            await query.edit_message_text(text=msg, reply_markup=keyboard)

# Group Management Commands
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ['group', 'supergroup']:
        await update.message.reply_text("This command can only be used in groups!")
        return
    
    admins = await update.effective_chat.get_administrators()
    admin_ids = [admin.user.id for admin in admins]
    
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text("❌ You need to be an admin to use this command!")
        return
    
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await update.effective_chat.ban_member(user.id)
        await update.message.reply_text(f"🚫 {user.first_name} has been banned!")
    else:
        await update.message.reply_text("Reply to a user's message to ban them.")

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ['group', 'supergroup']:
        await update.message.reply_text("This command can only be used in groups!")
        return
    
    admins = await update.effective_chat.get_administrators()
    admin_ids = [admin.user.id for admin in admins]
    
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text("❌ You need to be an admin to use this command!")
        return
    
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await update.effective_chat.unban_member(user.id)
        await update.message.reply_text(f"✅ {user.first_name} has been unbanned!")
    else:
        await update.message.reply_text("Reply to a user's message to unban them.")

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ['group', 'supergroup']:
        await update.message.reply_text("This command can only be used in groups!")
        return
    
    admins = await update.effective_chat.get_administrators()
    admin_ids = [admin.user.id for admin in admins]
    
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text("❌ You need to be an admin to use this command!")
        return
    
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        from telegram import ChatPermissions
        await update.effective_chat.restrict_member(
            user.id,
            ChatPermissions(can_send_messages=False),
            until_date=datetime.now() + timedelta(days=366)
        )
        await update.message.reply_text(f"🔇 {user.first_name} has been muted!")
    else:
        await update.message.reply_text("Reply to a user's message to mute them.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

# Main Function
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("play", play))
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(CommandHandler("unban", unban_user))
    app.add_handler(CommandHandler("mute", mute_user))
    
    # Callback Handler
    app.add_handler(CallbackQueryHandler(button_callback))
    
    # Start Bot
    print("🎵 Emelia Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
