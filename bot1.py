
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
import base64
import hashlib
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
admin_diggory = "HaoEsport" 
name_bot = "SPAM PRO BOT"
ADMIN_ID = '7658079324'
facebook = "no"
users_keys = {}
key = ""
blacklist = set()# hoặc set(), hoặc list chứa sẵn các số
user_cooldown = {}
active_processes = {}
last_usage = {} 
share_log = []
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
• /searchff - Tìm tk bằng tên 
• /like - buff like ff
• /vist - buff lượt xem

| Lệnh Spam Sms |  
• /spam - spam sms max 1000  
• /sms - spam max 5  

| Lệnh Cơ Bản |  
• /voice - Chuyển đổi văn bản thành giọng nói  
• /uptime - Random video gái xinh
• /anhgai - Random ảnh gái xinh
• /tv - Dịch tiếng Anh qua tiếng Việt  
• /id - Lấy id bản thân
• /ngl - spam ngl
• /tiktok - xem thông tin tiktok

| Lệnh Admin |  
• /thongbao - Thông báo đến nhóm  
</blockquote>""", parse_mode="HTML")

VIP_FILE = "vip_users.txt"

def is_user_vip(user_id):
    if not os.path.exists(VIP_FILE):
        return False
    with open(VIP_FILE, "r") as f:
        return str(user_id) in f.read()

def save_vip_user(user_id):
    with open(VIP_FILE, "a") as f:
        f.write(f"{user_id}\n")



ADMIN_ID = 7658079324  # thay bằng ID Telegram của bạn

@bot.message_handler(commands=['themvip'])
def themvip(message: Message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "🚫 Bạn không có quyền sử dụng lệnh này.")
        return

    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.reply_to(message, "❓ Dùng đúng cú pháp: /themvip <user_id>")
        return

    user_id_to_add = int(parts[1])
    save_vip_user(user_id_to_add)
    bot.reply_to(message, f"✅ Đã thêm ID {user_id_to_add} vào danh sách VIP.")





import time

# dict lưu user_id và thời gian cuối cùng gọi lệnh
user_last_like_time = {}

# thời gian chờ (giây)
LIKE_COOLDOWN = 60

@bot.message_handler(commands=['like'])
def like_handler(message: Message):
    user_id = message.from_user.id
    current_time = time.time()

    last_time = user_last_like_time.get(user_id, 0)
    time_diff = current_time - last_time

    if time_diff < LIKE_COOLDOWN:
        wait_time = int(LIKE_COOLDOWN - time_diff)
        bot.reply_to(message, f"<blockquote>⏳ Vui lòng chờ {wait_time} giây trước khi dùng lại lệnh này.</blockquote>", parse_mode="HTML")
        return

    user_last_like_time[user_id] = current_time  # cập nhật thời gian sử dụng

    command_parts = message.text.split()  
    if len(command_parts) != 2:  
        bot.reply_to(message, "<blockquote>like 1733997441</blockquote>", parse_mode="HTML")  
        return  

    idgame = command_parts[1]  
    urllike = f"https://dichvukey.site/likeff2.php?key=vlong&uid={idgame}"  

    def safe_get(data, key):
        value = data.get(key)
        return value if value not in [None, ""] else "Không xác định"

    def extract_number(text):
        if not text:
            return "Không xác định"
        for part in text.split():
            if part.isdigit():
                return part
        return "Không xác định"

    loading_msg = bot.reply_to(message, "<blockquote>⏳ Đang tiến hành buff like...</blockquote>", parse_mode="HTML")

    try:
        response = requests.get(urllike, timeout=15)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException:
        bot.edit_message_text("<blockquote>Server đang quá tải, vui lòng thử lại sau.</blockquote>",
                              chat_id=loading_msg.chat.id, message_id=loading_msg.message_id, parse_mode="HTML")
        return
    except ValueError:
        bot.edit_message_text("<blockquote>Phản hồi từ server không hợp lệ.</blockquote>",
                              chat_id=loading_msg.chat.id, message_id=loading_msg.message_id, parse_mode="HTML")
        return

    status_code = data.get("status")

    reply_text = (
        "<blockquote>"
        "BUFF LIKE THÀNH CÔNG✅\n"
        f"╭👤 Name: {safe_get(data, 'PlayerNickname')}\n"
        f"├🆔 UID : {safe_get(data, 'uid')}\n"
        f"├🌏 Region : vn\n"
        f"├📉 Like trước đó: {safe_get(data, 'likes_before')}\n"
        f"├📈 Like sau khi gửi: {safe_get(data, 'likes_after')}\n"
        f"╰👍 Like được gửi: {extract_number(data.get('likes_given'))}"
    )

    if status_code == 2:
        reply_text += "\n⚠️ Giới hạn like hôm nay, mai hãy thử lại sau."

    reply_text += "</blockquote>"

    bot.edit_message_text(reply_text, chat_id=loading_msg.chat.id, message_id=loading_msg.message_id, parse_mode="HTML")

@bot.message_handler(commands=['visit'])
def visit_handler(message):
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "<b>❗ Dùng đúng cú pháp:</b>\n<code>/visit 1733997441</code>", parse_mode="HTML")
        return

    idgame = args[1]
    url = f'https://visit-plum.vercel.app/send_visit?uid={idgame}'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("success", False):
            bot.reply_to(message, "Lỗi rồi, báo admin fix đi.", parse_mode="Markdown")
            return

        reply_text = (
            f"✅ *Thành công*\n"
            f"👀 *Tổng lượt xem:* {data['total_views_sent']}\n"
            f"⏳ *Thời gian xử lý:* {data['total_time_takes']} giây"
        )
        bot.reply_to(message, reply_text, parse_mode="Markdown")

    except requests.exceptions.RequestException:
        bot.reply_to(message, "*Sever đang quá tải, vui lòng thử lại sau.*", parse_mode="Markdown")





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



@bot.message_handler(commands=['anhgai'])
def send_random_image(message):
    try:
        response = requests.get("https://freerose.onrender.com/random-image")
        data = response.json()
        image_url = data.get("image_url")

        if image_url:
            bot.send_photo(message.chat.id, image_url, caption="Ảnh ngẫu nhiên nè!")
        else:
            bot.reply_to(message, "Không tìm được ảnh nào cả.")
    except Exception as e:
        bot.reply_to(message, f"Đã xảy ra lỗi: {e}")


@bot.message_handler(commands=['ngl'])
def ngl(message):
    args = message.text.split()
    if len(args) != 3:
        bot.reply_to(message, "<blockquote>Ví dụ: /ngl username 10 (tối đa 20)</blockquote>", parse_mode="HTML")
        return

    username = args[1]
    try:
        count = min(20, int(args[2]))
    except ValueError:
        bot.reply_to(message, "<blockquote>Vui lòng nhập một số hợp lệ!</blockquote>", parse_mode="HTML")
        return

    url = "https://ngl.link/api/submit"
    headers = {
        'Host': 'ngl.link',
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'origin': 'https://ngl.link',
        'referer': f'https://ngl.link/{username}',
    }

    data = {
        'username': username,
        'question': 'Tin nhắn spam từ bot vLong https://t.me/spamsmsvlong',
        'deviceId': '0',
        'gameSlug': '',
        'referrer': '',
    }

    success_count = 0
    for _ in range(count):
        try:
            response = requests.post(url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            success_count += 1
        except requests.exceptions.RequestException:
            pass

    sender = message.from_user.username or "Không rõ"

    reply_text = (
        f"<blockquote>"
        f"✅ Thành công!\n"
        f"👤 Người gửi: @{sender}\n"
        f"📨 Đã gửi: {success_count}/{count} tin nhắn\n"
        f"🎯 Người nhận: @{username}"
        f"</blockquote>"
    )

    bot.reply_to(message, reply_text, parse_mode="HTML")





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
@bot.message_handler(commands=['uptime'])
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


import time
import threading
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for member in message.new_chat_members:
        name = member.first_name
        username = f"@{member.username}" if member.username else "Không có username"
        chat_id = message.chat.id

        # Nút URL
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("Liên Hệ Admin", url="https://t.me/@HaoEsports05")
        markup.add(btn)

        caption = f"""
🌟 Xin chào con vợ {username} 🌟
Chào mừng bạn đến với Nhóm - Nơi để share Api FF & Hack FF 
🚫 Luật Box 🚫
📌 Cấm buôn bán , quãng cáo dưới mọi hình thức 
📌 Chat séc = Ban 🗣

Vui lòng đọc nội quy trước khi thảo luận nhé.
"""

        # Gửi video và lưu message
        sent_msg = bot.send_video(
            chat_id,
            video="https://i.imgur.com/8jtefrx.mp4",
            caption=caption,
            reply_markup=markup,
            parse_mode="Markdown"
        )

        # Tạo thread để xóa tin nhắn sau 60 giây
        threading.Thread(target=delete_after_delay, args=(chat_id, sent_msg.message_id, 60)).start()

def delete_after_delay(chat_id, message_id, delay):
    time.sleep(delay)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        print(f"Lỗi xoá message: {e}")




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




@bot.message_handler(commands=['checkban'])
def check_ban(message):
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "❗ Vui lòng nhập ID. Ví dụ: /checkban 8324665667")
            return

        user_id = args[1]
        api_url = f"https://wlx-scorpion.vercel.app/Checkban?key=Scromnyi&id={user_id}"
        response = requests.get(api_url)
        data = response.json()

        if data.get("is_banned") == True:
            reply_text = (
                f"🚫 **ID `{user_id}` đã bị BAN**\n"
                f"📆 Thời hạn ban: {data.get('ban_period', 'Không rõ')} ngày"
            )
        else:
            reply_text = (
                f"✅ **ID `{user_id}` không bị ban**\n"
                f"📄 Trạng thái: {data.get('status', 'Không xác định')}"
            )

        bot.reply_to(message, reply_text, parse_mode="Markdown")

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
#anh sách số bị cấm, bạn có thể cập nhật thêm
# users = {}  # Nếu bạn dùng để lấy plan, username...

@bot.message_handler(commands=['spam'])
def supersms(message):
    user_id = message.from_user.id
    current_time = time.time()

    if user_id in user_last_command_time:
        elapsed_time = current_time - user_last_command_time[user_id]
        if elapsed_time < 100:
            remaining_time = 100 - elapsed_time
            bot.reply_to(message, f"Vui lòng đợi {remaining_time:.1f} giây trước khi sử dụng lệnh lại.")
            return

    params = message.text.split()[1:]
    if len(params) != 2:
        bot.reply_to(message, 
            "<blockquote>» SAI ĐỊNH DẠNG!!!\n\n"
            "» Vui Lòng Nhập Đúng Định Dạng Bên Dưới\n\n"
            "» /spam + SĐT + SỐ_LẦN\n"
            "» VD: /spam 0987654321 10</blockquote>",
            parse_mode="HTML"
        )
        return

    sdt, count = params

    if not count.isdigit():
        bot.reply_to(message, "Số lần spam không hợp lệ. Vui lòng chỉ nhập số.")
        return

    count = int(count)

    if count > 1000:
        bot.reply_to(message, "/spam sdt số_lần tối đa là 1000")
        return

    if sdt in blacklist:
        bot.reply_to(message, f"Số điện thoại {sdt} đã bị cấm spam.")
        return

    sdt_request = f"84{sdt[1:]}" if sdt.startswith("0") else sdt

    # Gửi hiệu ứng đồng hồ cát
    loading_msg = bot.reply_to(message, "⏳")
    time.sleep(1.3)
    bot.edit_message_text(chat_id=loading_msg.chat.id, message_id=loading_msg.message_id, text="⌛")
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

    bot.edit_message_text(
        chat_id=loading_msg.chat.id,
        message_id=loading_msg.message_id,
        text=f"<blockquote>{diggory_chat3}</blockquote>",
        parse_mode="HTML"
    )

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
@bot.message_handler(func=lambda message: message.text and message.text.startswith("/"))
def unknown_command(message):
    known_commands = ['start', 'bot', 'spam', 'uptime', 'voice', 'ngl', 'ff', 'tv', 'checkban', 'tiktok']  # Thêm các lệnh hợp lệ bạn có

    command = message.text.split()[0][1:].split('@')[0]  # Lấy tên lệnh, bỏ dấu "/" và @botname nếu có

    if command not in known_commands:
        bot.reply_to(message, "Lệnh này không tồn tại vui lòng sử dụng lệnh /bot để xem.")


# Hàm gọi API T
def react_to_message(chat_id, message_id, emoji="❤️"):
    url = f"https://api.telegram.org/bot{os.environ.get('BOT_TOKEN')}/setMessageReaction"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "reaction": [{"type": "emoji", "emoji": emoji}],
        "is_big": True
    }
    requests.post(url, json=payload)

import random

# Danh sách emoji tuỳ thích
emojis = ["❤️", "😂", "🔥", "🤔", "👍", "😍", "😎", "💯", "👏", "😢", "😡"]

@bot.message_handler(func=lambda message: True)
def auto_like(message):
    emoji = random.choice(emojis)  # Lấy emoji ngẫu nhiên
    react_to_message(message.chat.id, message.message_id, emoji=emoji)



if __name__ == "__main__":
    bot_active = True
    bot.polling()  #
    
