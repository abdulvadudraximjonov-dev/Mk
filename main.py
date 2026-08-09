import telebot
import urllib.parse
import random
import os
import requests
from telebot import types
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Anigo Bot is active!"

def run_server():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_server).start()

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN') or '8619747331:AAGPCSl7ZJS-RQSaZYBFaHeqDOQPgHWhazo'
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 8113271428  

user_languages = {}
user_states = {}

TEXTS = {
    'uz': {
        'welcome': "👋 **Salom!** Anigo Anime Botiga xush kelibsiz!\n\nIstalgan anime nomini yozing yoki pastdagi menyudan foydalaning:",
        'btn_rand': "🎲 Tasodifiy Anime",
        'btn_wp': "🖼 Anime Rasm",
        'btn_genre': "📂 Janrlar",
        'btn_top': "🏆 Top 10 Animelar",
        'btn_lang': "🌐 Tilni o'zgartirish",
        'btn_help': "ℹ️ Yordam",
        'btn_contact': "✉️ Admin bilan bog'lanish",
        'watch': "🍿 Online Tomosha Qilish",
        'more_wp': "🔄 Yana rasm olish",
        'choose_genre': "🎭 **O'zingizga ma'qul janrni tanlang:**",
        'select_lang': "🌐 **Iltimos, tilni tanlang:**",
        'lang_changed': "✅ Til muvaffaqiyatli o'zgartirildi!",
        'contact_prompt': "✍️ Adminga yubormoqchi bo'lgan xabaringizni yozib qoldiring:",
        'msg_sent': "✅ Xabaringiz adminga yuborildi!",
        'help_text': "🤖 **Anigo Anime Bot**\n\n• Anime izlash uchun shunchaki nomini yozing.\n• Tasodifiy tavsiya va HD rasmlar oling."
    },
    'ru': {
        'welcome': "👋 **Привет!** Добро пожаловать в Anigo Anime Bot!\n\nВведите название аниме или используйте меню:",
        'btn_rand': "🎲 Случайное Аниме",
        'btn_wp': "🖼 Аниме Картинка",
        'btn_genre': "📂 Жанры",
        'btn_top': "🏆 Топ 10 Аниме",
        'btn_lang': "🌐 Язык",
        'btn_help': "ℹ️ Помощь",
        'btn_contact': "✉️ Связаться с админом",
        'watch': "🍿 Смотреть Онлайн",
        'more_wp': "🔄 Ещё картинка",
        'choose_genre': "🎭 **Выберите жанр:**",
        'select_lang': "🌐 **Пожалуйста, выберите язык:**",
        'lang_changed': "✅ Язык успешно изменен!",
        'contact_prompt': "✍️ Напишите ваше сообщение для админа:",
        'msg_sent': "✅ Ваше сообщение отправлено админу!",
        'help_text': "🤖 **Anigo Anime Bot**\n\n• Введите название для поиска аниме."
    },
    'en': {
        'welcome': "👋 **Hello!** Welcome to Anigo Anime Bot!\n\nType any anime name or use the menu:",
        'btn_rand': "🎲 Random Anime",
        'btn_wp': "🖼 Anime Wallpaper",
        'btn_genre': "📂 Genres",
        'btn_top': "🏆 Top 10 Anime",
        'btn_lang': "🌐 Language",
        'btn_help': "ℹ️ Help",
        'btn_contact': "✉️ Contact Admin",
        'watch': "🍿 Watch Online",
        'more_wp': "🔄 Get another wallpaper",
        'choose_genre': "🎭 **Select a genre:**",
        'select_lang': "🌐 **Please select a language:**",
        'lang_changed': "✅ Language changed!",
        'contact_prompt': "✍️ Type your message for the admin:",
        'msg_sent': "✅ Your message has been sent!",
        'help_text': "🤖 **Anigo Anime Bot**\n\n• Type an anime name to search."
    }
}

ANIMES_LIST = [
    {"title": "Attack on Titan", "score": "9.0", "genre": "action", "img": "https://cdn.myanimelist.net/images/anime/10/47347.jpg"},
    {"title": "Jujutsu Kaisen", "score": "8.7", "genre": "action", "img": "https://cdn.myanimelist.net/images/anime/1171/109222.jpg"},
    {"title": "Demon Slayer", "score": "8.5", "genre": "action", "img": "https://cdn.myanimelist.net/images/anime/1286/99889.jpg"},
    {"title": "One Piece", "score": "8.9", "genre": "adventure", "img": "https://cdn.myanimelist.net/images/anime/6/73245.jpg"},
    {"title": "Your Name", "score": "8.8", "genre": "romance", "img": "https://cdn.myanimelist.net/images/anime/5/87048.jpg"}
]

WALLPAPERS_POOL = [
    "https://i.waifu.pics/4q9Xm5_.jpg",
    "https://i.waifu.pics/1vI-wT_.jpg"
]

def get_lang(uid):
    return user_languages.get(uid, 'uz')

def main_kb(uid):
    lang = get_lang(uid)
    t = TEXTS[lang]
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(t['btn_rand'], t['btn_wp'])
    kb.add(t['btn_genre'], t['btn_top'])
    kb.add(t['btn_contact'], t['btn_help'])
    kb.add(t['btn_lang'])
    return kb

def lang_inline_kb():
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("🇺🇿 O'zbek", callback_data="setlang_uz"),
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data="setlang_ru"),
        types.InlineKeyboardButton("🇬🇧 English", callback_data="setlang_en")
    )
    return markup

def genres_kb():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("💥 Action", callback_data="genre_action"),
        types.InlineKeyboardButton("💖 Romance", callback_data="genre_romance"),
        types.InlineKeyboardButton("🔮 Fantasy", callback_data="genre_fantasy")
    )
    return markup

def get_random_wp():
    try:
        r = requests.get("https://api.waifu.pics/sfw/waifu", timeout=4).json()
        if r.get('url'):
            return r['url']
    except:
        pass
    return random.choice(WALLPAPERS_POOL)

@bot.message_handler(commands=['start'])
def start(m):
    user_states[m.chat.id] = None
    lang = get_lang(m.chat.id)
    bot.send_message(m.chat.id, TEXTS[lang]['select_lang'], parse_mode="Markdown", reply_markup=lang_inline_kb())

@bot.callback_query_handler(func=lambda c: c.data.startswith("setlang_"))
def cb_setlang(c):
    lang_code = c.data.split("_")[1]
    user_languages[c.message.chat.id] = lang_code
    t = TEXTS[lang_code]
    bot.answer_callback_query(c.id, t['lang_changed'])
    bot.send_message(c.message.chat.id, t['welcome'], parse_mode="Markdown", reply_markup=main_kb(c.message.chat.id))

@bot.message_handler(func=lambda m: m.text and any(m.text == TEXTS[l]['btn_lang'] for l in TEXTS))
def change_language_msg(m):
    user_states[m.chat.id] = None
    bot.send_message(m.chat.id, "🌐 **Tilni tanlang:**", parse_mode="Markdown", reply_markup=lang_inline_kb())

@bot.message_handler(func=lambda m: m.text and any(m.text == TEXTS[l]['btn_contact'] for l in TEXTS))
def contact_admin_start(m):
    lang = get_lang(m.chat.id)
    user_states[m.chat.id] = 'waiting_feedback'
    bot.send_message(m.chat.id, TEXTS[lang]['contact_prompt'], parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text and (any(m.text == TEXTS[l]['btn_rand'] for l in TEXTS) or m.text == "/random"))
def rand_anime(m):
    user_states[m.chat.id] = None
    lang = get_lang(m.chat.id)
    t = TEXTS[lang]
    item = random.choice(ANIMES_LIST)
    q = urllib.parse.quote(item['title'])
    markup = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(t['watch'], url=f"https://www.google.com/search?q={q}+anime+online")
    )
    bot.send_photo(m.chat.id, item['img'], caption=f"🎬 **{item['title']}**\n⭐️ {item['score']}/10", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and (any(m.text == TEXTS[l]['btn_wp'] for l in TEXTS) or "wallpaper" in m.text.lower() or "rasm" in m.text.lower()))
def send_wp(m):
    user_states[m.chat.id] = None
    lang = get_lang(m.chat.id)
    t = TEXTS[lang]
    url = get_random_wp()
    btn = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(t['more_wp'], callback_data="next_wp"))
    bot.send_photo(m.chat.id, url, caption="🖼 **HD Wallpaper!**", parse_mode="Markdown", reply_markup=btn)

@bot.callback_query_handler(func=lambda c: c.data == "next_wp")
def cb_wp(c):
    lang = get_lang(c.message.chat.id)
    t = TEXTS[lang]
    url = get_random_wp()
    btn = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(t['more_wp'], callback_data="next_wp"))
    bot.send_photo(c.message.chat.id, url, caption="🖼 **HD Wallpaper!**", parse_mode="Markdown", reply_markup=btn)
    bot.answer_callback_query(c.id)

@bot.message_handler(func=lambda m: m.text and any(m.text == TEXTS[l]['btn_genre'] for l in TEXTS))
def send_genres(m):
    user_states[m.chat.id] = None
    lang = get_lang(m.chat.id)
    bot.send_message(m.chat.id, TEXTS[lang]['choose_genre'], parse_mode="Markdown", reply_markup=genres_kb())

@bot.callback_query_handler(func=lambda c: c.data.startswith("genre_"))
def cb_genre(c):
    lang = get_lang(c.message.chat.id)
    t = TEXTS[lang]
    genre = c.data.split("_")[1]
    filtered = [a for a in ANIMES_LIST if a.get('genre') == genre]
    if filtered:
        item = random.choice(filtered)
        q = urllib.parse.quote(item['title'])
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(t['watch'], url=f"https://www.google.com/search?q={q}+anime+online")
        )
        bot.send_photo(c.message.chat.id, item['img'], caption=f"🎬 **{item['title']}**\n⭐️ {item['score']}/10", parse_mode="Markdown", reply_markup=markup)
    bot.answer_callback_query(c.id)

@bot.message_handler(func=lambda m: m.text and any(m.text == TEXTS[l]['btn_top'] for l in TEXTS))
def top_animes(m):
    user_states[m.chat.id] = None
    text = "🏆 **Top Animelar:**\n\n"
    for idx, item in enumerate(ANIMES_LIST, 1):
        text += f"{idx}. **{item['title']}** — ⭐️ {item['score']}/10\n"
    bot.send_message(m.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text and any(m.text == TEXTS[l]['btn_help'] for l in TEXTS))
def about_bot(m):
    user_states[m.chat.id] = None
    lang = get_lang(m.chat.id)
    bot.send_message(m.chat.id, TEXTS[lang]['help_text'], parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID and m.reply_to_message is not None)
def reply_to_user(m):
    try:
        lines = m.reply_to_message.text.split('\n')
        for line in lines:
            if "ID:" in line:
                target_user_id = int(line.split("ID:")[1].strip())
                bot.send_message(target_user_id, f"👨‍💻 **Admin javobi:**\n\n{m.text}")
                bot.send_message(ADMIN_ID, "✅ Javob yetkazildi!")
                return
    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ Xatolik: {e}")

@bot.message_handler(func=lambda m: True)
def handle_all_messages(m):
    if not m.text or m.text.startswith('/'):
        return
    
    if user_states.get(m.chat.id) == 'waiting_feedback':
        user_states[m.chat.id] = None
        lang = get_lang(m.chat.id)
        
        admin_msg = (
            f"📩 **Yangi xabar!**\n\n"
            f"👤 **Kimdan:** {m.from_user.first_name} (@{m.from_user.username or 'yoq'})\n"
            f"🆔 **ID:** {m.chat.id}\n\n"
            f"💬 **Xabar:**\n{m.text}"
        )
        
        try:
            bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")
            bot.send_message(m.chat.id, TEXTS[lang]['msg_sent'], parse_mode="Markdown", reply_markup=main_kb(m.chat.id))
        except:
            bot.send_message(m.chat.id, "❌ Xatolik yuz berdi.", reply_markup=main_kb(m.chat.id))
        return

    lang = get_lang(m.chat.id)
    t = TEXTS[lang]
    q = urllib.parse.quote(m.text.strip())
    btn = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(t['watch'], url=f"https://www.google.com/search?q={q}+anime+online")
    )
    bot.send_message(m.chat.id, f"🔎 **{m.text}** bo'yicha qidiruv:", parse_mode="Markdown", reply_markup=btn)

bot.infinity_polling()

