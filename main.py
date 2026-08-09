import telebot, urllib.parse, random, os, requests
from telebot import types
from flask import Flask
from threading import Thread

# 1. Web Server (Render 24/7 ishlashi uchun)
app = Flask('')
@app.route('/')
def home(): return "Bot Active"
Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

TOKEN = os.environ.get('8559834342:AAGFraSt01b4Mv-cygjqtYQkD854KCBuFSE')
bot = telebot.TeleBot(TOKEN)

ANIMES_LIST = [
    {"title": "Attack on Titan", "score": "9.0", "img": "https://cdn.myanimelist.net/images/anime/10/47347.jpg"},
    {"title": "Jujutsu Kaisen", "score": "8.7", "img": "https://cdn.myanimelist.net/images/anime/1171/109222.jpg"},
    {"title": "Demon Slayer", "score": "8.5", "img": "https://cdn.myanimelist.net/images/anime/1286/99889.jpg"},
    {"title": "One Piece", "score": "8.9", "img": "https://cdn.myanimelist.net/images/anime/6/73245.jpg"},
    {"title": "Naruto Shippuden", "score": "8.2", "img": "https://cdn.myanimelist.net/images/anime/1565/111305.jpg"},
    {"title": "Death Note", "score": "8.6", "img": "https://cdn.myanimelist.net/images/anime/9/9444.jpg"},
    {"title": "Bleach", "score": "7.9", "img": "https://cdn.myanimelist.net/images/anime/3/40451.jpg"},
    {"title": "Solo Leveling", "score": "8.4", "img": "https://cdn.myanimelist.net/images/anime/1172/140880.jpg"},
    {"title": "Spirited Away", "score": "8.8", "img": "https://cdn.myanimelist.net/images/anime/6/79597.jpg"},
    {"title": "Hunter x Hunter", "score": "9.0", "img": "https://cdn.myanimelist.net/images/anime/11/33657.jpg"}
]

WALLPAPERS_POOL = [
    "https://images.alphacoders.com/132/1328328.jpeg",
    "https://images.alphacoders.com/129/1298314.jpg",
    "https://images.alphacoders.com/112/1123013.jpg",
    "https://images.alphacoders.com/128/1288599.png",
    "https://images.alphacoders.com/131/1314562.jpeg"
]

def main_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add("🎲 Tasodifiy Anime", "🖼 Anime Rasm")
    return kb

def get_random_anime():
    try:
        r = requests.get("https://api.jikan.moe/v4/random/anime", timeout=4).json()
        data = r.get('data', {})
        t, s, i = data.get('title'), data.get('score', '8.0'), data.get('images', {}).get('jpg', {}).get('large_image_url')
        if t and i: return t, s, i
    except: pass
    item = random.choice(ANIMES_LIST)
    return item['title'], item['score'], item['img']

def get_random_wp():
    try:
        r = requests.get("https://nekos.best/api/v2/wallpaper", timeout=4).json()
        if r.get('results'): return r['results'][0]['url']
    except: pass
    return random.choice(WALLPAPERS_POOL)

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, f"Salom, {m.from_user.first_name}! 🍿\n\nIstalgan anime nomini yozing yoki pastdagi tugmalardan foydalaning:", reply_markup=main_kb())

@bot.message_handler(func=lambda m: "Tasodifiy Anime" in m.text or m.text == "/random")
def rand_anime(m):
    title, score, img = get_random_anime()
    q = urllib.parse.quote(title)
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🍿 Online Tomosha Qilish", url=f"https://www.google.com/search?q={q}+anime+online+tomosha+qilish"))
    try:
        bot.send_photo(m.chat.id, img, caption=f"🎬 **Nomi:** {title}\n⭐️ **Reytingi:** {score}/10", parse_mode="Markdown", reply_markup=markup)
    except:
        bot.send_message(m.chat.id, f"🎬 **Nomi:** {title}\n⭐️ **Reytingi:** {score}/10", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda m: "Anime Rasm" in m.text or m.text == "/wallpaper")
def send_wp(m):
    url = get_random_wp()
    btn = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔄 Boshqa Random Wallpaper", callback_data="next_wp"))
    try:
        bot.send_photo(m.chat.id, url, caption="🖼 **HD Anime Wallpaper!**", parse_mode="Markdown", reply_markup=btn)
    except:
        bot.send_photo(m.chat.id, random.choice(WALLPAPERS_POOL), caption="🖼 **HD Anime Wallpaper!**", parse_mode="Markdown", reply_markup=btn)

@bot.callback_query_handler(func=lambda c: c.data == "next_wp")
def cb_wp(c):
    url = get_random_wp()
    btn = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔄 Boshqa Random Wallpaper", callback_data="next_wp"))
    try:
        bot.send_photo(c.message.chat.id, url, caption="🖼 **Yangi HD Wallpaper!**", parse_mode="Markdown", reply_markup=btn)
        bot.answer_callback_query(c.id)
    except:
        bot.answer_callback_query(c.id)

@bot.message_handler(func=lambda m: True)
def search(m):
    if m.text.startswith('/'): return
    q = urllib.parse.quote(m.text.strip())
    btn = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🍿 Saytda Online Tomosha Qilish", url=f"https://www.google.com/search?q={q}+anime+online+tomosha+qilish"))
    bot.send_message(m.chat.id, f"🔎 **{m.text}** bo'yicha tomosha qilish havolasi:", parse_mode="Markdown", reply_markup=btn)

bot.polling(none_stop=True)
  
