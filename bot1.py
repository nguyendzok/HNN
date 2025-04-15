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
admin_mode = False
ADMIN_ID = 7658079324 #nhớ thay id nhé nếu k thay k duyệt dc vip đâu v.L..ong.a
allowed_group_id = -1002639856138
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
GROUP_CHAT_IDS = [-1002639856138, 1002282514761]
@bot.message_handler(commands=['bot', 'start'])
def send_help(message):
    if message.chat.id not in GROUP_CHAT_IDS:
        bot.reply_to(message, "Bot này chỉ hoạt động trong nhóm Này https://t.me/+AhM8n6X-63JmNTQ1.")
        return

    username = message.from_user.username or "None"
    now = datetime.utcnow() + timedelta(hours=7)
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d/%m/%Y")

    bot.reply_to(message, f"""<blockquote>
📑 List Command  
Thời Gian : {current_time}  
Ngày : {current_date}  
Người Gọi Lệnh : @{username}  

| Lệnh Free Fire |  
• /start or /bot - Hiển thị danh sách lệnh và hướng dẫn sử dụng.  
• /ff - Check Info  
• /checkban - Kiểm tra tk có khoá không  
• /searchff - Tìm tk bằng tên  

| Lệnh Spam Sms |  
• /spam - spam sms max 1000  
• /sms - spam max 5  

| Lệnh Cơ Bản |  
• /voice - Chuyển đổi văn bản thành giọng nói  
• /uptime - Random video gái xinh  
• /tv - Dịch tiếng Anh qua tiếng Việt  
• /id - Lấy id bản thân
• /code - Lấy code web
• /ngl - spam ngl
• /tiktok - xem thông tin tiktok

| Lệnh Game |
• /dangky - Đăng ký tài khoản và nhận 500k
• /dangnhap - Đăng nhập tài khoản
• /game - Chơi tài/xỉu/chẵn/lẻ
• /sodu - Xem số dư tài khoản
• /admin - Trở thành admin
• /buff - Buff tiền cho người chơi (admin)

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


registered_users = {}  # user_id: (username, balance)
admins = set()
@bot.message_handler(commands=["dangky"])
def register(message):
    if message.chat.id not in GROUP_CHAT_IDS:
        bot.reply_to(message, "Bot này chỉ hoạt động trong nhóm Này https://t.me/+AhM8n6X-63JmNTQ1.")
    try:
        args = message.text.split()
        if len(args) < 3:
            return bot.reply_to(message, "❌ /dangky <tên> <mật khẩu>")
        
        username, password = args[1], args[2]
        with open("files.txt", "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 1 and parts[0] == username:
                    return bot.reply_to(message, f"❌ Tên {username} đã tồn tại.")

        with open("files.txt", "a") as f:
            f.write(f"{username} {password} 500000\n")
        bot.reply_to(message, f"✅ Đăng ký thành công, {username}!")
    except Exception as e:
        bot.reply_to(message, f"❌ Lỗi: {str(e)}")

# Đăng nhập
@bot.message_handler(commands=["dangnhap"])
def login(message):
    if message.chat.id not in GROUP_CHAT_IDS:
        bot.reply_to(message, "Bot này chỉ hoạt động trong nhóm Này https://t.me/+AhM8n6X-63JmNTQ1.")
    try:
        args = message.text.split()
        if len(args) < 3:
            return bot.reply_to(message, "❌ /dangnhap <tên> <mật khẩu>")
        
        username, password = args[1], args[2]
        with open("files.txt", "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 3:
                    continue
                if parts[0] == username and parts[1] == password:
                    registered_users[message.from_user.id] = (username, int(parts[2]))
                    return bot.reply_to(message, f"✅ Đăng nhập thành công, {username}!")
        
        bot.reply_to(message, "❌ Tên hoặc mật khẩu sai.")
    except Exception as e:
        bot.reply_to(message, f"❌ Lỗi: {str(e)}")

# Số dư
@bot.message_handler(commands=["sodu"])
def balance(message):
    user = registered_users.get(message.from_user.id)
    if not user:
        return bot.reply_to(message, "❌ Bạn chưa đăng nhập.")
    
    username = user[0]
    with open("files.txt", "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            if parts[0] == username:
                return bot.reply_to(message, f"💰 Số dư của bạn là: {parts[2]}")
    
    bot.reply_to(message, "❌ Không tìm thấy tài khoản.")

# Cập nhật số dư
def update_balance(username, new_balance):
    lines = []
    with open("files.txt", "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            if parts[0] == username:
                lines.append(f"{username} {parts[1]} {new_balance}\n")
            else:
                lines.append(line)
    with open("files.txt", "w") as f:
        f.writelines(lines)

# Game tài xỉu
@bot.message_handler(commands=["game"])
def play_game(message):
    if message.chat.id not in GROUP_CHAT_IDS:
        bot.reply_to(message, "Bot này chỉ hoạt động trong nhóm Này https://t.me/+AhM8n6X-63JmNTQ1.")
    try:
        args = message.text.split()
        if len(args) != 3:
            return bot.reply_to(message, "❌ /game <T/X/C/L> <số tiền>")
        
        bet_type = args[1].upper()
        bet_amount = int(args[2])
        user = registered_users.get(message.from_user.id)

        if not user:
            return bot.reply_to(message, "❌ Bạn chưa đăng nhập.")

        username, balance = user
        if balance < bet_amount:
            return bot.reply_to(message, "❌ Bạn không đủ tiền cược.")

        dice = [random.randint(1, 6) for _ in range(3)]
        total = sum(dice)
        is_even = total % 2 == 0

        win = (
            (bet_type == "T" and total > 10) or
            (bet_type == "X" and total <= 10) or
            (bet_type == "C" and is_even) or
            (bet_type == "L" and not is_even)
        )

        if win:
            balance += bet_amount
            msg = f"🎉 Bạn thắng! 🎲 {dice} = {total} ({'chẵn' if is_even else 'lẻ'}). +{bet_amount}"
        else:
            balance -= bet_amount
            msg = f"😢 Bạn thua! 🎲 {dice} = {total} ({'chẵn' if is_even else 'lẻ'}). -{bet_amount}"

        update_balance(username, balance)
        registered_users[message.from_user.id] = (username, balance)
        bot.reply_to(message, msg)

    except Exception as e:
        bot.reply_to(message, f"❌ Lỗi: {str(e)}")

# Admin key
@bot.message_handler(commands=["admin"])
def make_admin(message):
    args = message.text.split()
    if len(args) != 2 or args[1] != "22062012":
        return bot.reply_to(message, "❌ Key không hợp lệ.")
    
    admins.add(message.from_user.id)
    bot.reply_to(message, "✅ Bạn đã trở thành admin.")

# Buff tiền
@bot.message_handler(commands=["buff"])
def buff_money(message):
    if message.from_user.id not in admins:
        return bot.reply_to(message, "❌ Bạn không phải admin.")
    
    args = message.text.split()
    if len(args) != 2:
        return bot.reply_to(message, "❌ /buff <tên>")
    
    target_username = args[1].lower()
    for uid, (username, balance) in registered_users.items():
        if username.lower() == target_username:
            big_money = 10**36
            registered_users[uid] = (username, balance + big_money)
            update_balance(username, balance + big_money)
            return bot.reply_to(message, f"✅ Đã buff {big_money} cho {username}.")

    bot.reply_to(message, f"❌ Không tìm thấy người dùng {target_username}.")








def html_escape(text):
    return (text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
@bot.message_handler(commands=['tiktok'])
def tiktok_info(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Vui lòng nhập username TikTok. Ví dụ: /tiktok @ho.esports")
        return

    username = args[1].lstrip('@')
    loading_msg = bot.reply_to(message, "⏳ Đang lấy thông tin...")

    try:
        # Fix lỗi 403 bằng User-Agent
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(f"https://api.sumiproject.net/tiktok?info=@{username}", headers=headers)
        res.raise_for_status()
        result = res.json()

        if result.get("code") != 0 or "data" not in result:
            bot.edit_message_text("Không tìm thấy thông tin người dùng.",
                                  chat_id=message.chat.id,
                                  message_id=loading_msg.message_id)
            return

        user = result["data"]["user"]
        stats = result["data"]["stats"]

        caption = f"""
<b>TikTok Info</b>
<blockquote>
<b>Username:</b> @{html_escape(user.get('uniqueId', ''))}<br/>
<b>Tên hiển thị:</b> {html_escape(user.get('nickname', ''))}<br/>
<b>Bio:</b> {html_escape(user.get('signature', ''))}<br/>
<b>Followers:</b> {stats.get('followerCount', 0)}<br/>
<b>Following:</b> {stats.get('followingCount', 0)}<br/>
<b>Videos:</b> {stats.get('videoCount', 0)}<br/>
<b>Tổng lượt thích:</b> {stats.get('heartCount', 0)}<br/>
<b>Đã xác minh:</b> {"✅" if user.get('verified') else "❌"}
</blockquote>
"""

        avatar_url = user.get("avatarLarger") or user.get("avatarMedium") or user.get("avatarThumb")

        bot.send_photo(
            chat_id=message.chat.id,
            photo=avatar_url,
            caption=caption,
            parse_mode="HTML"
        )

        bot.delete_message(chat_id=message.chat.id, message_id=loading_msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"Đã xảy ra lỗi:\n<code>{html_escape(str(e))}</code>",
                              chat_id=message.chat.id,
                              message_id=loading_msg.message_id,
                              parse_mode="HTML")



GROUP_CHAT_IDS = [-1002639856138, 1002282514761]
@bot.message_handler(commands=['ngl'])
def ngl(message):
    if message.chat.id not in GROUP_CHAT_IDS:
        bot.reply_to(message, "Bot này chỉ hoạt động trong nhóm Này https://t.me/+AhM8n6X-63JmNTQ1.")
        return
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


GROUP_CHAT_IDS = [-1002639856138, 1002282514761]
@bot.message_handler(commands=['code'])
def handle_code_command(message):
    if message.chat.id not in GROUP_CHAT_IDS:
        bot.reply_to(message, "Bot này chỉ hoạt động trong nhóm Này https://t.me/+AhM8n6X-63JmNTQ1.")
        return
    command_args = message.text.split(maxsplit=1)
    if len(command_args) < 2:
        bot.reply_to(message, "Ví dụ: /code Https://linkwebcuaban")
        return

    url = command_args[1]
    domain = urlparse(url).netloc
    file_name = f"{domain}.txt"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(response.text)
        with open(file_name, 'rb') as file:
            bot.send_document(message.chat.id, file, caption=f"HTML của trang web {url}")
        bot.reply_to(message, "Đã gửi mã nguồn HTML của trang web cho bạn.")

    except requests.RequestException as e:
        bot.reply_to(message, f"Đã xảy ra lỗi khi tải trang web: {e}")

    finally:
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
            except Exception as e:
                bot.reply_to(message, f"Đã xảy ra lỗi khi xóa file: {e}")






import requests
GROUP_CHAT_IDS = [-1002639856138, 1002282514761]
def fetch_data(user_id):
    url = f'https://scromnyimodz-444.vercel.app/api/player-info?id={user_id}'
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

@bot.message_handler(commands=['ff'])
def handle_command(message):
    if message.chat.id not in GROUP_CHAT_IDS:
        bot.reply_to(message, "Bot này chỉ hoạt động trong nhóm Này https://t.me/+AhM8n6X-63JmNTQ1.")
        return
    parts = message.text.split()
    if len(parts) != 2:
        bot.reply_to(message, "<blockquote>❌ Sai cú pháp!\nVí dụ: /ff 12345678</blockquote>", parse_mode="HTML")
        return

    _, user_id = parts

    try:
        data = fetch_data(user_id)
        if not data or data.get('status') != 'success':
            bot.reply_to(message, "<blockquote>❌ Không tìm thấy người chơi hoặc server quá tải!</blockquote>", parse_mode="HTML")
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
        bot.reply_to(message, info.strip(), parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, "<blockquote>⚠️ Đã xảy ra lỗi khi xử lý yêu cầu.</blockquote>", parse_mode="HTML")
        print(e)



import requests
GROUP_CHAT_IDS = [-1002639856138, 1002282514761]
@bot.message_handler(commands=['uptime'])
def random_video(message):
    if message.chat.id not in GROUP_CHAT_IDS:
        bot.reply_to(message, "Bot này chỉ hoạt động trong nhóm Này https://t.me/+AhM8n6X-63JmNTQ1.")
        return

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

 



GROUP_CHAT_IDS = [-1002639856138, 1002282514761]
@bot.message_handler(commands=['voice'])
def text_to_voice(message):
    if message.chat.id not in GROUP_CHAT_IDS:
        bot.reply_to(message, "Bot này chỉ hoạt động trong nhóm Này https://t.me/+AhM8n6X-63JmNTQ1.")
        return
    text = message.text[7:].strip()  
  
    
    if not text:
        bot.reply_to(message, 'Nhập nội dung đi VD : /voice Tôi là bot')
        return

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            tts = gTTS(text, lang='vi')
            tts.save(temp_file.name)
            temp_file_path = temp_file.name  
       
        with open(temp_file_path, 'rb') as f:
            bot.send_voice(message.chat.id, f, reply_to_message_id=message.message_id)
    
    except Exception as e:
        bot.reply_to(message, f'Đã xảy ra lỗi: {e}')
    
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)



GROUP_CHAT_IDS = [-1002639856138, 1002282514761]
def format_timestamp(timestamp):
    try:
        if not timestamp:
            return "Không rõ"
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%H:%M:%S %d-%m-%Y")
    except:
        return "Không xác định"

def escape_html(text):
    """
    Escape các ký tự đặc biệt để tránh lỗi khi dùng HTML parse mode.
    """
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

@bot.message_handler(commands=['searchff'])
def search_ff(message):
    if message.chat.id not in GROUP_CHAT_IDS:
        bot.reply_to(message, "Bot này chỉ hoạt động trong nhóm Này https://t.me/+AhM8n6X-63JmNTQ1.")
    try:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            bot.reply_to(message, "❗ Vui lòng nhập tên cần tìm. Ví dụ: /searchff Scromnyi")
            return

        username = args[1].strip()
        api_url = f"https://ariflexlabs-search-api.vercel.app/search?name={username}"
        response = requests.get(api_url)

        if response.status_code != 200:
            bot.reply_to(message, f"⚠️ Lỗi từ máy chủ API: {response.status_code}")
            return

        try:
            regions = response.json()
        except ValueError:
            bot.reply_to(message, "⚠️ Không thể phân tích dữ liệu từ API.")
            return

        all_players = []
        for region_data in regions:
            players = region_data.get("result", {}).get("player", [])
            for player in players:
                all_players.append({
                    "nickname": player.get("nickname", "?"),
                    "accountId": player.get("accountId", "?"),
                    "level": player.get("level", "?"),
                    "region": player.get("region", "?"),
                    "lastLogin": format_timestamp(player.get("lastLogin", 0))
                })

        if not all_players:
            bot.reply_to(message, f"❌ Không tìm thấy kết quả cho <code>{escape_html(username)}</code>.", parse_mode="HTML")
            return

        max_results = 10
        reply_text = f"🔎 <b>Kết quả tìm kiếm cho</b> <code>{escape_html(username)}</code>:\n\n"
        for i, player in enumerate(all_players[:max_results], 1):
            reply_text += (
                f"<blockquote>\n"
                f"<b>{i}. {escape_html(player['nickname'])}</b>\n"
                f"🆔 UID: <code>{escape_html(player['accountId'])}</code>\n"
                f"🎮 Level: {player['level']} | 🌍 Region: {escape_html(player['region'])}\n"
                f"⏰ Đăng nhập cuối: {escape_html(player['lastLogin'])}\n"
                f"</blockquote>\n"
            )

        if len(all_players) > max_results:
            reply_text += f"📌 Hiển thị {max_results}/{len(all_players)} kết quả đầu tiên."

        bot.reply_to(message, reply_text, parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Đã xảy ra lỗi:\n<code>{escape_html(str(e))}</code>", parse_mode="HTML")

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

GROUP_CHAT_IDS = [-1002639856138, 1002282514761]
@bot.message_handler(commands=['hoi'])
def handle_hoi(message):
    if message.chat.id not in GROUP_CHAT_IDS:
        bot.reply_to(message, "Bot này chỉ hoạt động trong nhóm Này https://t.me/+AhM8n6X-63JmNTQ1.")
        return
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


GROUP_CHAT_IDS = [-1002639856138, 1002282514761]
@bot.message_handler(commands=['id', 'ID'])
def handle_id_command(message):
    if message.chat.id not in GROUP_CHAT_IDS:
        bot.reply_to(message, "Bot này chỉ hoạt động trong nhóm Này https://t.me/+AhM8n6X-63JmNTQ1.")
        return
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
GROUP_CHAT_IDS = [-1002639856138, 1002282514761]

@bot.message_handler(commands=['spam'])
def supersms(message):
    if message.chat.id not in GROUP_CHAT_IDS:
        bot.reply_to(message, "Bot này chỉ hoạt động trong nhóm Này https://t.me/+AhM8n6X-63JmNTQ1.")
        return
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
        bot.reply_to(message, """» SAI ĐỊNH DẠNG!!!

» Vui Lòng Nhập Đúng Định Dạng Bên Dưới

» /spam + SĐT
» VD: /spam 0987654321""")

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

    # Gửi kết quả ngay lập tức
    diggory_chat3 = f'''┌──⭓ Bot Hào Vip 😘
│ 🚀 Attack Sent Successfully
│ 💳 Plan Vip: Min 1 | Max 1000
│ 📞 Phone: {sdt}
│ ⚔️ Attack By: @{message.from_user.username or "None"}
│ 🔗 Api: 1x (MAX)
│ ⏳ Delay: 20s
│ 📎 Vòng Lặp: {count}
└────────────⭓'''

    bot.reply_to(message, f"<blockquote>{diggory_chat3}</blockquote>", parse_mode="HTML")
    user_last_command_time[user_id] = time.time()

    # Chạy spam và API call trong thread nền
    def spam_thread():
        try:
            script_filename = "dec.py"
            if not os.path.isfile(script_filename):
                return

            with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
                with open(script_filename, 'r', encoding='utf-8') as file:
                    temp_file.write(file.read().encode('utf-8'))
                temp_file_path = temp_file.name

            subprocess.Popen(["python", temp_file_path, sdt, str(count)])
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
    
