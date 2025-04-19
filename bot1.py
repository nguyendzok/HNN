import telebot
import subprocess
import sys
import json
from requests import post, Session
import time
import datetime
import threading
from urllib.parse import urlparse
import psutil
import logging
import tempfile
import random
from gtts import gTTS
import re
import string
import os
import io
from flask import Flask, request
from telebot.types import Message
from threading import Lock
import requests
import sqlite3
from telebot import types
from time import strftime
import queue
import pytz
from datetime import timedelta
from keep_alive import keep_alive
keep_alive()
BOT_TOKEN = os.environ.get('BOT_TOKEN')  # <- thêm dòng này
bot = telebot.TeleBot(BOT_TOKEN)         # <- bot dùng biến này

print(BOT_TOKEN)  # Kiểm tra token có tồn tại không
print("Bot đã được khởi động thành công")
ADMIN_ID = '7658079324'
blacklist = set()# hoặc set(), hoặc list chứa sẵn các số
user_cooldown = {}
active_processes = {}
last_usage = {} 
auto_spam_active = False
last_sms_time = {}
global_lock = Lock()
allowed_users = []
processes = []
user_warnings = {}
admin_mode = False
ADMIN_ID = 7658079324 #nhớ thay id nhé nếu k thay k duyệt dc vip đâu v.L..ong.a
connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()
last_command_time = {}
user_last_command_time = {}

last_command_timegg = 0



def check_command_cooldown(user_id, command, cooldown):
    current_time = time.time()
    
    if user_id in last_command_time and current_time - last_command_time[user_id].get(command, 0) < cooldown:
        remaining_time = int(cooldown - (current_time - last_command_time[user_id].get(command, 0)))
        return remaining_time
    else:
        last_command_time.setdefault(user_id, {})[command] = current_time
        return None

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()

def TimeStamp():
  now = str(datetime.date.today())
  return now

#vLong zz#v





from datetime import datetime, timedelta
@bot.message_handler(commands=['bot', 'start'])
def send_help(message):
    username = message.from_user.username or "None"
    now = datetime.utcnow() + timedelta(hours=7)
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d/%m/%Y")

    bot.reply_to(message, f"""<blockquote>
📑 LIST COMMAND  
Thời Gian : {current_time}  
Ngày : {current_date}  
Người Gọi Lệnh : @{username}  

| Lệnh Free Fire |  
• /start or /bot - Hiển thị danh sách lệnh và hướng dẫn sử dụng.  
• /ff - Check Info  
• /checkban - Kiểm tra tk có khoá không 
• /like - buff like ff
• /vist - buff lượt xem

| Lệnh Spam Sms |  
• /spam - spam sms max 1000   

| Lệnh Cơ Bản |  
• /voice - Chuyển đổi văn bản thành giọng nói  
• /video - Random video gái xinh
• /tv - Dịch tiếng Anh qua tiếng Việt  
• /id - Lấy id bản thân
• /tiktok - xem thông tin tiktok

| Lệnh Admin |  
• /thongbao - Thông báo đến nhóm  
</blockquote>""", parse_mode="HTML")




import time
import requests
from telebot.types import Message

user_last_like_time = {}
LIKE_COOLDOWN = 400

@bot.message_handler(commands=['like'])
def like_handler(message: Message):
    user_id = message.from_user.id
    current_time = time.time()

    try:
        bot.send_chat_action(message.chat.id, "typing")
    except Exception as e:
        print(f"Bot không thể gửi tin nhắn trong group: {e}")
        return

    last_time = user_last_like_time.get(user_id, 0)
    time_diff = current_time - last_time

    if time_diff < LIKE_COOLDOWN:
        wait_time = int(LIKE_COOLDOWN - time_diff)
        bot.reply_to(message, f"<blockquote>⏳ Vui lòng chờ {wait_time} giây trước khi dùng lại lệnh này.</blockquote>", parse_mode="HTML")
        return

    user_last_like_time[user_id] = current_time

    command_parts = message.text.split()
    if len(command_parts) < 2:
        bot.reply_to(message, "<blockquote>Cú pháp đúng: /like 1733997441 [api2]</blockquote>", parse_mode="HTML")
        return

    uid = command_parts[1]
    force_api2 = len(command_parts) == 3 and command_parts[2].lower() == "api2"

    primary_api = f"https://dichvukey.site/likeff2.php?key=vlong&uid={uid}"
    fallback_api = f"https://likes-api-ff.vercel.app/likes?uid={uid}&region=vn&key=Scromnyi225"

    def safe_get(data, key):
        value = data.get(key)
        return str(value) if value not in [None, "", "null"] else "Không xác định"

    def extract_number(text):
        if not text:
            return "Không xác định"
        if isinstance(text, int):
            return str(text)
        for part in str(text).split():
            if part.isdigit():
                return part
        return "Không xác định"

    def fetch_api(url):
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            return response.json()
        except:
            return None

    try:
        loading_msg = bot.reply_to(message, "<blockquote>⏳ Đang tiến hành buff like...</blockquote>", parse_mode="HTML")
    except Exception as e:
        print(f"Lỗi gửi tin nhắn loading: {e}")
        return

    data = None
    source = "primary"

    if force_api2:
        data = fetch_api(fallback_api)
        source = "fallback"
    else:
        data = fetch_api(primary_api)
        if not data or data.get("status") != 1:
            data = fetch_api(fallback_api)
            source = "fallback"
            if not data or data.get("status") != 1:
                bot.edit_message_text("<blockquote>Server đang bảo trì hoặc quá tải, vui lòng thử lại sau.</blockquote>",
                                      chat_id=loading_msg.chat.id, message_id=loading_msg.message_id, parse_mode="HTML")
                return

    status_code = data.get("status")

    if source == "primary":
        name = safe_get(data, 'PlayerNickname')
        uid_str = safe_get(data, 'uid')
        like_before = safe_get(data, 'likes_before')
        like_after = safe_get(data, 'likes_after')
        like_sent = extract_number(data.get('likes_given'))
    else:
        name = safe_get(data, 'PlayerNickname')
        uid_str = safe_get(data, 'UID')
        like_before = safe_get(data, 'LikesbeforeCommand')
        like_after = safe_get(data, 'LikesafterCommand')
        like_sent = extract_number(data.get('LikesGivenByAPI'))

    reply_text = (
        "<blockquote>"
        f"BUFF LIKE THÀNH CÔNG✅ (Dùng {'API phụ' if source == 'fallback' else 'API chính'})\n"
        f"╭👤 Name: {name}\n"
        f"├🆔 UID : {uid_str}\n"
        f"├🌏 Region : vn\n"
        f"├📉 Like trước đó: {like_before}\n"
        f"├📈 Like sau khi gửi: {like_after}\n"
        f"╰👍 Like được gửi: {like_sent}"
    )

    if status_code == 2:
        reply_text += "\n⚠️ Giới hạn like hôm nay, mai hãy thử lại sau."

    reply_text += "</blockquote>"

    try:
        bot.edit_message_text(reply_text, chat_id=loading_msg.chat.id, message_id=loading_msg.message_id, parse_mode="HTML")
    except Exception as e:
        print(f"Lỗi gửi kết quả: {e}")


import time
import re

last_visit_time = {}

@bot.message_handler(commands=['visit'])
def visit_handler(message):
    user_id = message.from_user.id
    now = time.time()

    cooldown = 160  # giây

    if user_id in last_visit_time:
        elapsed = now - last_visit_time[user_id]
        if elapsed < cooldown:
            bot.reply_to(
                message,
                f"⏳ Vui lòng đợi <b>{int(cooldown - elapsed)}</b> giây trước khi dùng lại.",
                parse_mode="HTML"
            )
            return

    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "<code>/visit 1733997441</code>", parse_mode="HTML")
        return

    idgame = args[1]
    url = f'https://visit-plum.vercel.app/send_visit?uid={idgame}'

    try:
        response = requests.get(url, timeout=10)
        text = response.text

        if not text.strip():
            bot.reply_to(message, "❌ API không trả về dữ liệu (rỗng). Vui lòng thử lại sau.", parse_mode="HTML")
            return

        # Dùng regex để trích xuất các giá trị
        def extract(field, default="Không rõ"):
            match = re.search(fr"{field}:\s*(.+)", text)
            return match.group(1).strip() if match else default

        name = extract("name")
        level = extract("level")
        region = extract("region")
        tokens_used = extract("tokens_used", "0")
        views_sent = extract("total_views_sent", "0")
        time_taken = extract("total_time_takes", "0")

        last_visit_time[user_id] = now

        reply_text = (
            "✅ <b>Đã gửi lượt xem thành công!</b>\n\n"
            "<b>Thông tin người chơi:</b>\n"
            f"╭👤 <b>Tên:</b> <code>{name}</code>\n"
            f"├🧬 <b>Level:</b> <code>{level}</code>\n"
            f"╰🌍 <b>Khu vực:</b> <code>{region}</code>\n\n"
            "<b>Kết quả visit:</b>\n"
            f"╭🎯 <b>Lượt xem:</b> <code>{views_sent}</code>\n"
            f"├⚡ <b>Token tiêu tốn:</b> <code>{tokens_used}</code>\n"
            f"╰⏳ <b>Thời gian xử lý:</b> <code>{time_taken} giây</code>"
        )
        

        bot.reply_to(message, reply_text, parse_mode="HTML")

    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"<b>Lỗi kết nối:</b> <code>{str(e)}</code>", parse_mode="HTML")





voicebuoidau = ["lồn", "đong", "hao", "bú", "vlong", "buồi", "cặc"]

@bot.message_handler(commands=['voice'])
def text_to_voice(message):
    text = message.text[7:].strip()  
    if not text:
        bot.reply_to(message, 'Nhập nội dung đi VD: /voice abc')
        return

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            tts = gTTS(text, lang='vi')
            tts.save(temp_file.name)
            temp_file_path = temp_file.name  
       
        with open(temp_file_path, 'rb') as f:
            bot.send_voice(message.chat.id, f, reply_to_message_id=message.message_id)
        if any(word in text.lower() for word in voicebuoidau):
            user_id = message.from_user.id
            bot.reply_to(message, f"ID {user_id} !")

    except Exception as e:
        bot.reply_to(message, f'Đã xảy ra lỗi')
    
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)




import requests
import html
def yes_no_icon(value, yes="Có ✅", no="Không ❌"):
    return yes if value else no

@bot.message_handler(commands=['tiktok'])
def get_tiktok_info(message):
    try:
        args = message.text.split()
        if len(args) != 2:
            bot.reply_to(message, "❗ Vui lòng dùng đúng cú pháp:\n<b>/tiktok &lt;username&gt;</b>", parse_mode="HTML")
            return

        username = args[1]
        url = f"http://145.223.80.56:5009/info_tiktok?username={username}"
        response = requests.get(url)

        if response.status_code != 200:
            bot.reply_to(message, "Không thể lấy thông tin từ API.", parse_mode="HTML")
            return

        data = response.json()

        # Escape toàn bộ để an toàn
        name = html.escape(data.get('name', 'Không rõ'))
        user_id = data.get('user_id', 'Không rõ')
        followers = f"{data.get('followers', 0):,}"
        following = f"{data.get('following', 0):,}"
        hearts = f"{data.get('hearts', 0):,}"
        videos = f"{data.get('videos', 0):,}"
        likes = f"{data.get('digg_count', 0):,}"
        bio = html.escape(data.get('signature', 'Không có'))
        is_private = yes_no_icon(data.get('is_private', False), "Có 🔒", "Không 🔓")
        open_favorite = yes_no_icon(data.get('open_favorite', False), "Có ⭐", "Không ❌")
        profile_pic = data.get('profile_picture', '')
        link = f"https://www.tiktok.com/@{username}"

        # Tạo nội dung blockquote
        blockquote = (
            f"📊 Thông Tin Tài Khoản TikTok\n\n"
            f"✨ Thống Kê:\n"
            f"👍 Lượt thích: {likes}\n"
            f"👥 Người theo dõi: {followers}\n"
            f"👤 Đang theo dõi: {following}\n"
            f"❤️ Lượt tim: {hearts}\n"
            f"🎬 Số video: {videos}\n\n"
            f"🔒 Chi Tiết Tài Khoản:\n"
            f"📛 Tên: {name}\n"
            f"👤 Tên người dùng: @{username}\n"
            f"🆔 ID người dùng: {user_id}\n"
            f"🔒 Tài khoản riêng tư: {is_private}\n"
            f"⭐ Mở mục yêu thích: {open_favorite}\n\n"
            f"📝 Tiểu sử:\n{bio}"
        )

        caption = f"<blockquote>{blockquote}</blockquote>"

        # Nút inline
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("🔗 Mở TikTok", url=link),
            telebot.types.InlineKeyboardButton("📋 Copy Username", callback_data=f"copy_{username}")
        )

        if profile_pic:
            bot.send_photo(message.chat.id, photo=profile_pic, caption=caption, parse_mode='HTML', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, caption, parse_mode='HTML', reply_markup=markup)

    except Exception as e:
        bot.reply_to(message, f"Đã xảy ra lỗi: {html.escape(str(e))}", parse_mode="HTML")

# Xử lý callback khi bấm "Copy Username"
@bot.callback_query_handler(func=lambda call: call.data.startswith("copy_"))
def copy_username_callback(call):
    username = call.data.replace("copy_", "")
    bot.answer_callback_query(call.id, text="Đã sao chép!")
    bot.send_message(call.message.chat.id, f"📋 Username: @{username}")




import requests

def fetch_data(user_id, region):
    url = f'https://freefireinfo-tanhung.onrender.com/info?uid={user_id}&region={region}'
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

@bot.message_handler(commands=['ff'])
def handle_command(message):
    parts = message.text.split()
    if len(parts) != 3:
        try:
            bot.reply_to(message, "<blockquote>❌ Sai cú pháp!\nVí dụ: /ff 12345678 vn</blockquote>", parse_mode="HTML")
        except:
            bot.send_message(message.chat.id, "<blockquote>❌ Sai cú pháp!\nVí dụ: /ff 12345678 vn</blockquote>", parse_mode="HTML")
        return

    _, user_id, region = parts

    try:
        data = fetch_data(user_id, region)
        if not data or data.get('status') != 'success':
            try:
                bot.reply_to(message, "<blockquote>❌ Không tìm thấy người chơi hoặc server quá tải!</blockquote>", parse_mode="HTML")
            except:
                bot.send_message(message.chat.id, "<blockquote>❌ Không tìm thấy người chơi hoặc server quá tải!</blockquote>", parse_mode="HTML")
            return

        basic = data['data'].get('basic_info', {})
        clan = data['data'].get('clan', {})
        leader = clan.get('leader', {})

        def g(key, dic): return dic.get(key, 'Không có')

        info = f"""
<blockquote>
<b>📌 Thông tin tài khoản:</b>
Tên: {g('name', basic)}
ID: {g('id', basic)}
Cấp độ: {g('level', basic)}
Booyah Pass: {g('booyah_pass_level', basic)}
Lượt thích: {g('likes', basic)}
Máy chủ: {g('server', basic)}
Tiểu sử: {g('bio', basic)}
Ngày tạo: {g('account_created', basic)}

<b>👥 Thông tin quân đoàn:</b>
Tên: {g('name', clan)}
Cấp độ: {g('level', clan)}
Thành viên: {g('members_count', clan)}

<b>👑 Chủ quân đoàn:</b>
Tên: {g('name', leader)}
Cấp độ: {g('level', leader)}
Lượt thích: {g('likes', leader)}
Ngày tạo: {g('account_created', leader)}
</blockquote>
"""
        try:
            bot.reply_to(message, info.strip(), parse_mode="HTML")
        except:
            bot.send_message(message.chat.id, info.strip(), parse_mode="HTML")

    except Exception as e:
        try:
            bot.reply_to(message, "<blockquote>⚠️ Đã xảy ra lỗi khi xử lý yêu cầu.</blockquote>", parse_mode="HTML")
        except:
            bot.send_message(message.chat.id, "<blockquote>⚠️ Đã xảy ra lỗi khi xử lý yêu cầu.</blockquote>", parse_mode="HTML")
        print(e)



import requests
@bot.message_handler(commands=['video'])
def random_video(message):
    
    try:
        res = requests.get("https://api.ffcommunity.site/randomvideo.php")
        data = res.json()
        video_url = data.get("url")

        if video_url:
            bot.send_chat_action(message.chat.id, "upload_video")
            bot.send_video(message.chat.id, video=video_url, caption="Video gái xinh hôm nay nè!")
        else:
            bot.send_message(message.chat.id, "Không lấy được video, thử lại sau nhé!")
    except Exception as e:
        bot.send_message(message.chat.id, "Đã xảy ra lỗi khi lấy video.")






ADMINS = [7658079324]  # Thay bằng user_id admin của bạn
GROUP_CHAT_IDS = [-1002639856138]  # Thay bằng chat_id nhóm

@bot.message_handler(commands=['thongbao'])
def thongbao_to_groups(message):
    if message.chat.type != 'private':
        bot.reply_to(message, "⚠️ Vui lòng dùng lệnh này trong chat riêng với bot.")
        return

    if message.from_user.id not in ADMINS:
        bot.reply_to(message, "🚫 Bạn không có quyền dùng lệnh này.")
        return

    try:
        announcement = message.text.split(' ', 1)[1]
    except IndexError:
        bot.reply_to(message, "❗ Vui lòng nhập nội dung: /announce <nội dung>")
        return

    success = 0
    for chat_id in GROUP_CHAT_IDS:
        try:
            bot.send_message(chat_id, f"📢 <b>Thông báo từ Admin</b>:\n\n{announcement}", parse_mode='HTML')
            success += 1
        except Exception as e:
            print(f"Lỗi gửi nhóm {chat_id}: {e}")

    bot.reply_to(message, f"✅ Đã gửi thông báo đến {success} nhóm.")




import time
import requests

cooldown_checkban = {}
COOLDOWN_SECONDS = 500  # Thời gian cooldown 60 giây

@bot.message_handler(commands=['checkban'])
def check_ban(message):
    user_id_telegram = message.from_user.id
    current_time = time.time()

    # Kiểm tra cooldown
    if user_id_telegram in cooldown_checkban:
        elapsed = current_time - cooldown_checkban[user_id_telegram]
        if elapsed < COOLDOWN_SECONDS:
            remaining = int(COOLDOWN_SECONDS - elapsed)
            bot.reply_to(message, f"⏳ Vui lòng đợi {remaining} giây trước khi sử dụng lại lệnh này.")
            return

    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "❗ Vui lòng nhập ID. Ví dụ: /checkban 8324665667")
            return

        uid = args[1]
        api_url = f"https://scromnyi.vercel.app/region/ban-info?uid={uid}"
        response = requests.get(api_url)
        data = response.json()

        nickname = data.get("nickname", "Không rõ")
        ban_status = data.get("ban_status", "Không xác định")
        ban_period = data.get("ban_period", "Không có")
        region = data.get("region", "Không rõ")
        if ban_status.lower() != "not banned":
            reply_text = (
                f"🚫 **ID `{uid}` đã bị BAN**\n"
                f"📛 Nickname: `{nickname}`\n"
                f"🌍 Khu vực: `{region}`\n"
                f"📆 Thời hạn ban: `{ban_period}"
                
            )
        else:
            reply_text = (
                f"✅ **ID `{uid}` không bị ban**\n"
                f"📛 Nickname: `{nickname}`\n"
                f"🌍 Khu vực: `{region}`\n"
                f"📄 Trạng thái: `{ban_status}`"
            )

        bot.reply_to(message, reply_text, parse_mode="Markdown")
        cooldown_checkban[user_id_telegram] = current_time  # Cập nhật cooldown

    except Exception as e:
        bot.reply_to(message, f"⚠️ Đã xảy ra lỗi:\n`{e}`", parse_mode="Markdown")



@bot.message_handler(commands=['hoi'])
def handle_hoi(message):
    text = message.text[len('/hoi '):].strip()
    

    # Nếu hợp lệ, cho spam
    if text:
        url = f"https://dichvukey.site/apishare/hoi.php?text={text}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            reply = data.get("message", "Không có phản hồi.")
        else:
            reply = "Lỗi."
    else:
        reply = "Lệnh Ví Dụ : /hoi xin chào."
    bot.reply_to(message, reply)



GROUP_CHAT_IDS = [-1002639856138, 1002282514761]
@bot.message_handler(commands=['time'])
def handle_time(message):
    if message.chat.id not in GROUP_CHAT_IDS:
        bot.reply_to(message, "Bot này chỉ hoạt động trong nhóm Này https://t.me/+AhM8n6X-63JmNTQ1.")
        return
    uptime_seconds = int(time.time() - start_time)
    
    uptime_minutes, uptime_seconds = divmod(uptime_seconds, 60)
    bot.reply_to(message, f'Bot đã hoạt động được: {uptime_minutes} phút, {uptime_seconds} giây')



@bot.message_handler(commands=['id', 'ID'])
def handle_id_command(message):
    if message.reply_to_message:  
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
        bot.reply_to(message, f"ID của {first_name} là: `{user_id}`", parse_mode='Markdown')
    elif len(message.text.split()) == 1:
        if message.chat.type in ["group", "supergroup"]:
            chat_id = message.chat.id
            chat_title = message.chat.title
            bot.reply_to(message, f"ID của nhóm này là: `{chat_id}`\nTên nhóm: {chat_title}", parse_mode='Markdown')
        else:
            user_id = message.from_user.id
            first_name = message.from_user.first_name
            bot.reply_to(message, f"ID của bạn là: `{user_id}`\nTên: {first_name}", parse_mode='Markdown')


   
import threading
import time
import os
import subprocess
import tempfile
import requests

user_last_command_time = {}
blacklist = []  # Danh sách số bị cấm, bạn có thể thêm vào

@bot.message_handler(commands=['spam'])
def supersms(message):
    user_id = message.from_user.id
    current_time = time.time()

    if user_id in user_last_command_time:
        elapsed_time = current_time - user_last_command_time[user_id]
        if elapsed_time < 100:
            remaining_time = 100 - elapsed_time
            bot.send_message(message.chat.id, f"Vui lòng đợi {remaining_time:.1f} giây trước khi sử dụng lệnh lại.")
            return

    params = message.text.split()[1:]
    if len(params) != 2:
        bot.send_message(message.chat.id,
            "<blockquote>» SAI ĐỊNH DẠNG!!!\n\n"
            "» Vui Lòng Nhập Đúng Định Dạng Bên Dưới\n\n"
            "» /spam + SĐT + SỐ_LẦN\n"
            "» VD: /spam 0987654321 10</blockquote>",
            parse_mode="HTML"
        )
        return

    sdt, count = params

    if not count.isdigit():
        bot.send_message(message.chat.id, "Số lần spam không hợp lệ. Vui lòng chỉ nhập số.")
        return

    count = int(count)

    if count > 1000:
        bot.send_message(message.chat.id, "/spam sdt số_lần tối đa là 1000")
        return

    if sdt in blacklist:
        bot.send_message(message.chat.id, f"Số điện thoại {sdt} đã bị cấm spam.")
        return

    sdt_request = f"84{sdt[1:]}" if sdt.startswith("0") else sdt

    # Gửi hiệu ứng đồng hồ cát
    loading_msg = bot.send_message(message.chat.id, "⏳")
    time.sleep(1.3)
    try:
        bot.edit_message_text(chat_id=loading_msg.chat.id, message_id=loading_msg.message_id, text="⌛")
    except Exception as e:
        print(f"Lỗi khi chuyển ⏳ -> ⌛: {e}")
    time.sleep(1.3)

    diggory_chat3 = f'''┌──⭓ Bot Hào Vip 😘
│ 🚀 Attack Sent Successfully
│ 💳 Plan Vip: Min 1 | Max 1000
│ 📞 Phone: {sdt}
│ ⚔️ Attack By: @{message.from_user.username or "None"}
│ 🔗 Api: 1x (MAX)
│ ⏳ Delay: 20s
│ 📎 Vòng Lặp: {count}
└────────────⭓'''

    try:
        bot.edit_message_text(
            chat_id=loading_msg.chat.id,
            message_id=loading_msg.message_id,
            text=f"<blockquote>{diggory_chat3}</blockquote>",
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Lỗi khi chỉnh tin nhắn kết quả: {e}")

    user_last_command_time[user_id] = time.time()

    def spam_thread():
        try:
            script_filename = "dec.py"
            if not os.path.isfile(script_filename) or os.path.getsize(script_filename) == 0:
                bot.send_message(message.chat.id, "File dec.py không tồn tại hoặc trống.")
                return

            with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
                with open(script_filename, 'r', encoding='utf-8') as file:
                    temp_file.write(file.read().encode('utf-8'))
                temp_file_path = temp_file.name

            subprocess.Popen(
                ["python", temp_file_path, sdt, str(count)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            requests.get(f'https://dichvukey.site/apivl/call1.php?sdt={sdt_request}', timeout=5)
        except Exception as e:
            print(f"Lỗi spam: {e}")

    threading.Thread(target=spam_thread).start()






GROUP_CHAT_IDS = [-1002639856138, 1002282514761]
@bot.message_handler(commands=['tv'])
def tieng_viet(message):
    if message.chat.id not in GROUP_CHAT_IDS:
        bot.reply_to(message, "Bot này chỉ hoạt động trong nhóm Này https://t.me/+AhM8n6X-63JmNTQ1.")
        return
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton("Tiếng Việt 🇻🇳", url='https://t.me/setlanguage/vi')
    keyboard.add(url_button)
    bot.send_message(chat_id, '<blockquote>Click vào nút "<b>Tiếng Việt</b>" để đổi ngôn ngữ sang Tiếng Việt 🇻🇳</blockquote>', reply_markup=keyboard, parse_mode='HTML')
######






if __name__ == "__main__":
    bot_active = True
    bot.polling()  #
    
