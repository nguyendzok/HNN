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
name_bot = "Trần Hào"
ADMIN_ID = '7658079324'
zalo = "0585019743"
web = "https://dichvukey.site/"
facebook = "no"
users_keys = {}
key = ""
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
def load_users_from_database():
  cursor.execute('SELECT user_id, expiration_time FROM users')
  rows = cursor.fetchall()
  for row in rows:
    user_id = row[0]
    expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
    if expiration_time > datetime.datetime.now():
      allowed_users.append(user_id)


def save_user_to_database(connection, user_id, expiration_time):
  cursor = connection.cursor()
  cursor.execute(
    '''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
  connection.commit()
###

vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')


###
#zalo ...07890416.31

####
start_time = time.time()



video_url = 'https://v16m-default.akamaized.net/b7650db4ac7f717b7be6bd6a04777a0d/66a418a5/video/tos/useast2a/tos-useast2a-ve-0068-euttp/o4QTIgGIrNbkAPGKKLKteXyLedLE7IEgeSzeE2/?a=0&bti=OTg7QGo5QHM6OjZALTAzYCMvcCMxNDNg&ch=0&cr=0&dr=0&lr=all&cd=0%7C0%7C0%7C0&cv=1&br=2576&bt=1288&cs=0&ds=6&ft=XE5bCqT0majPD12cy-773wUOx5EcMeF~O5&mime_type=video_mp4&qs=0&rc=Mzk1OzY7PGdpZjxkOTQ3M0Bpajh1O2w5cmlzbzMzZjgzM0AuNWJgLi02NjMxLzBgXjUyYSNzNmptMmRjazFgLS1kL2Nzcw%3D%3D&vvpl=1&l=202407261543513F37EAD38E23B6263167&btag=e00088000'
@bot.message_handler(commands=['add', 'adduser'])
def add_user(message):
    admin_id = message.from_user.id
    if admin_id != ADMIN_ID:
        bot.reply_to(message, 'Bạn Không Phải admin')
        return

    if len(message.text.split()) == 1:
        bot.reply_to(message, 'VUI LÒNG NHẬP ID NGƯỜI DÙNG VÀ SỐ NGÀY')
        return
    if len(message.text.split()) == 2:
        bot.reply_to(message, 'HÃY NHẬP SỐ NGÀY')
        return
    user_id = int(message.text.split()[1])
    allowed_users.append(user_id)
    days = int(message.text.split()[2])
    expiration_time = datetime.datetime.now() + datetime.timedelta(days)
    connection = sqlite3.connect('user_data.db')
    save_user_to_database(connection, user_id, expiration_time)
    connection.close()

    caption_text = (f'<blockquote>NGƯỜI DÙNG CÓ ID {user_id}\nĐÃ ĐƯỢC THÊM VÀO DANH SÁCH VIP\nTHỜI GIAN: {days} DAY\nLỆNH CÓ THỂ SỬ DỤNG CÁC LỆNH TRONG [/start]</blockquote>')
    bot.send_video(
        message.chat.id,
        video_url,
        caption=caption_text, parse_mode='HTML')

load_users_from_database()

def is_key_approved(chat_id, key):
    if chat_id in users_keys:
        user_key, timestamp = users_keys[chat_id]
        if user_key == key:
            current_time = datetime.datetime.now()
            if current_time - timestamp <= datetime.timedelta(hours=2):
                return True
            else:
                del users_keys[chat_id]
    return False




@bot.message_handler(commands=['bot','start'])
def send_help(message):
    bot.reply_to(message, """<blockquote>
┌───⭓ Trần Hào
➤ /spam : Spam FREE
➤ /spamvip : Spam Vip
➤ /stop : Dừng Spam SĐT
➤ /tv : Tiếng việt cho telegram
➤ /id : Lấy id bản thân
➤ /checkban : Kiểm tra tk có khoá không
➤ /searchff : Tìm tk ff bằng tên
└───Tiện Ích Khác
➤ /time : Xem Thời gian bot hoạt động
➤ /voice : Chuyển văn bản thành giọng nói 
➤ /hoi : hỏi gamini 
➤ /tiktokinfo : xem thông tin tiktok
➤ /tkey : Mã Hoá File .py
└───Contact
➤ /admin : Liên Hệ admin
➤ /themvip : Thêm Vip
└───
</blockquote>""", parse_mode="HTML")
### /like

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



@bot.message_handler(commands=['voice'])
def text_to_voice(message):
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




def format_timestamp(ts):
    try:
        dt = datetime.fromtimestamp(ts)
        return dt.strftime("%d/%m/%Y %H:%M")
    except:
        return "Không rõ"

@bot.message_handler(commands=['searchff'])
def search_ff(message):
    try:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            bot.reply_to(message, "❗ Vui lòng nhập tên cần tìm. Ví dụ: /searchff Scromnyi")
            return

        username = args[1]
        api_url = f"https://ariflexlabs-search-api.vercel.app/search?name={username}"
        response = requests.get(api_url)
        regions = response.json()

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
            bot.reply_to(message, f"❌ Không tìm thấy kết quả cho `{username}`.", parse_mode="Markdown")
            return

        # Giới hạn kết quả nếu quá nhiều
        max_results = 10
        reply_text = f"🔎 **Kết quả tìm kiếm cho `{username}`:**\n\n"
        for i, player in enumerate(all_players[:max_results], 1):
            reply_text += (
                f"{i}. 👤 {player['nickname']}\n"
                f"🆔 UID: `{player['accountId']}`\n"
                f"🎮 Level: {player['level']} | 🌍 Region: {player['region']}\n"
                f"⏰ Đăng nhập cuối: {player['lastLogin']}\n"
                f"───────────────\n"
            )

        if len(all_players) > max_results:
            reply_text += f"📌 Hiển thị {max_results}/{len(all_players)} kết quả đầu tiên."

        bot.reply_to(message, reply_text, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"⚠️ Đã xảy ra lỗi:\n`{e}`", parse_mode="Markdown")



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




@bot.message_handler(commands=['time'])
def handle_time(message):
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


   
def detect_carrier(phone_number: str) -> str:
    phone_number = phone_number.strip().replace("+84", "0")
    prefixes = {
        "Viettel": ["086", "096", "097", "098", "032", "033", "034", "035", "036", "037", "038", "039"],
        "Mobifone": ["089", "090", "093", "070", "076", "077", "078", "079"],
        "Vinaphone": ["088", "091", "094", "081", "082", "083", "084", "085"],
        "Vietnamobile": ["092", "056", "058"],
        "Gmobile": ["099", "059"],
    }

    for name, prefix_list in prefixes.items():
        if any(phone_number.startswith(p) for p in prefix_list):
            return name
    return "Không xác định"


def animate_loading(chat_id, message_id, stop_event):
    emojis = ['⏳', '⌛']
    idx = 0
    while not stop_event.is_set():
        try:
            bot.edit_message_text(
                f"{emojis[idx % 2]} Đang xử lý...",
                chat_id=chat_id,
                message_id=message_id
            )
            idx += 1
            time.sleep(1)
        except Exception as e:
            print(f"Lỗi khi update loading: {e}")
            break

@bot.message_handler(commands=['spam'])
def spam(message):
    user_id = message.from_user.id
    current_time = time.time()

    if user_id in last_usage and current_time - last_usage[user_id] < 10:
        bot.reply_to(message, f"⏳ Vui lòng đợi {10 - (current_time - last_usage[user_id]):.1f} giây trước khi dùng lại.")
        return

    params = message.text.split()[1:]
    if len(params) != 2:
        warn = bot.reply_to(message, "/spam sdt số_lần như này cơ mà")
        time.sleep(5)
        try:
            bot.delete_message(message.chat.id, warn.message_id)
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
        return

    sdt, count = params
    carrier = detect_carrier(sdt)

    if not count.isdigit():
        bot.reply_to(message, "Số lần spam không hợp lệ. Vui lòng chỉ nhập số.")
        return

    count = int(count)

    if count > 25:
        bot.reply_to(message, "/spam sdt số_lần tối đa là 25 - đợi 10 giây sử dụng lại.")
        return

    if sdt in blacklist:
        bot.reply_to(message, f"Số điện thoại {sdt} đã bị cấm spam.")
        return

    sdt_request = f"84{sdt[1:]}" if sdt.startswith("0") else sdt
    username = message.from_user.username if message.from_user.username else "Không có username"

    diggory_chat3 = f'''┌──────⭓ {name_bot}
│ 🚀 Attack Sent Successfully
│ 💳 Plan Free: Min 1 | Max 5
│ 📞 Phone: {sdt}
│ ⚔️ Attack By: @{username}
│ ⏳ Delay: 20s
│ 📎 Vòng Lặp: {count}
└────────────⭓
'''

    script_filename = "dec.py"
    try:
        if not os.path.isfile(script_filename):
            bot.reply_to(message, "Không tìm thấy file script.")
            return

        # Gửi loading ban đầu
        loading_msg = bot.send_message(message.chat.id, "⏳ Đang xử lý...")

        # Bắt đầu hiệu ứng loading động
        stop_loading = threading.Event()
        loading_thread = threading.Thread(
            target=animate_loading,
            args=(message.chat.id, loading_msg.message_id, stop_loading)
        )
        loading_thread.start()

        # Đọc nội dung file script
        with open(script_filename, 'r', encoding='utf-8') as file:
            script_content = file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(script_content.encode('utf-8'))
            temp_file_path = temp_file.name

        # Chạy script spam
        process = subprocess.Popen(["python", temp_file_path, sdt, str(count)])
        active_processes[sdt] = process

        # Dừng hiệu ứng loading và xóa tin nhắn đó
        stop_loading.set()
        bot.delete_message(chat_id=message.chat.id, message_id=loading_msg.message_id)

        # Gửi kết quả
        bot.send_message(
            message.chat.id,
            f'<blockquote>{diggory_chat3}</blockquote>',
            parse_mode='HTML'
        )

        last_usage[user_id] = current_time

    except FileNotFoundError:
        bot.reply_to(message, "Không tìm thấy file.")
    except Exception as e:
        bot.reply_to(message, f"Lỗi xảy ra: {str(e)}")


@bot.message_handler(commands=['stop'])
def stop_spam(message):
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "Dùng đúng cú pháp: /stop 098xxxxxxx")
        return

    sdt = args[1]
    process = active_processes.get(sdt)

    if process:
        process.terminate()  # Dừng tiến trình
        del active_processes[sdt]  # Xóa khỏi danh sách
        bot.reply_to(message, f"⛔️ Đã dừng spam số {sdt}")
    else:
        bot.reply_to(message, f"Không tìm thấy tiến trình spam với số {sdt}. Có thể đã hoàn thành hoặc sai số.")




@bot.message_handler(commands=['tiktokinfo'])
def get_tiktok_info(message):
    chat_id = message.chat.id
    args = message.text.split()

    if len(args) < 2:
        bot.send_message(chat_id, "⚠️ Vui lòng nhập tên người dùng TikTok!\nVí dụ: /tiktokinfo ho.esports", parse_mode="Markdown")
        return

    username = args[1]
    api_url = f"https://api.sumiproject.net/tiktok?info={username}"

    try:
        response = requests.get(api_url)
        data = response.json()

        if data['code'] != 0 or 'data' not in data:
            bot.send_message(chat_id, "❌ Không tìm thấy tài khoản TikTok!", parse_mode="Markdown")
            return

        user = data['data']['user']
        stats = data['data']['stats']

        profile_message = f"""
======[ 𝙏𝙄𝙆𝙏𝙊𝙆 𝙄𝙉𝙁𝙊 ]======  

👤 Tên hiển thị: {user['nickname']}  
🆔 Username: @{user['uniqueId']}  
🔗 Profile: [Xem trên TikTok](https://www.tiktok.com/@{user['uniqueId']})  

📊 Thống kê:  
├ 👥 Người theo dõi: {stats['followerCount']}  
├ 👤 Đang theo dõi: {stats['followingCount']}  
├ ❤️ Tổng lượt thích: {stats['heartCount']}  
├ 🎥 Số video: {stats['videoCount']}  

🔗 Mạng xã hội khác:  
{f"▶️ [YouTube](https://www.youtube.com/channel/{user['youtube_channel_id']})" if user.get('youtube_channel_id') else "🚫 Không có YouTube"}  
{f"📌 Bio: {user['signature']}" if user.get('signature') else "🚫 Không có mô tả"}  
        """

        bot.send_photo(chat_id, user['avatarLarger'], caption=profile_message, parse_mode="Markdown")

    except Exception as error:
        bot.send_message(chat_id, "⚠️ Lỗi khi lấy thông tin tài khoản TikTok!", parse_mode="Markdown")
        print(error)


TEMP_DIR = "temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

# Biến để chứa key và số lần nhập
key_attempts = 1
current_key = None

def generate_random_key(length=30):
    characters = 'haoesportQWERTYUIOPASDFGHJKLZXCVBBNM123456789'
    return ''.join(random.choice(characters) for i in range(length))

@bot.message_handler(commands=['tkey'])
def create_key(message):
    global current_key, key_attempts
    current_key = generate_random_key()
    key_attempts = 1
    bot.send_message(message.chat.id, f"Key đã được tạo: {current_key}\nBạn có {key_attempts} lần gửi file\nvui lòng gửi file .py")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    global key_attempts, current_key

    if current_key is None:
        bot.send_message(message.chat.id, "Vui lòng tạo key trước khi gửi file bằng lệnh /tkey.")
        return

    file_info = bot.get_file(message.document.file_id)
    file_extension = message.document.file_name.split('.')[-1]

    if file_extension != 'py':
        bot.send_message(message.chat.id, "Vui lòng gửi một file .py hợp lệ.")
        return

    if key_attempts <= 0:
        bot.send_message(message.chat.id, "Số lần gửi file đã hết. Vui lòng tạo lại key.")
        return

    downloaded_file = bot.download_file(file_info.file_path)
    original_filename = message.document.file_name
    file_path = os.path.join(TEMP_DIR, original_filename)

    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    key_attempts -= 1

    msg = bot.reply_to(message, "Đang mã hóa...", parse_mode='HTML')
    time.sleep(2)

    try:
        obfuscated_file_path = obfuscate_file(file_path, current_key, message.from_user)

        bot.send_message(message.chat.id, "Mã hóa hoàn tất! Đang gửi file...")

        with open(obfuscated_file_path, 'rb') as obfuscated_file:
            bot.send_document(message.chat.id, obfuscated_file)

    except Exception as e:
        bot.send_message(message.chat.id, f"Đã xảy ra lỗi khi mã hóa: {e}")
    finally:
        # Xóa cả file gốc và file mã hóa sau khi xử lý
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(obfuscated_file_path):
            os.remove(obfuscated_file_path)

def obfuscate_file(file_path, key, user):
    original_filename = os.path.basename(file_path)
    name_without_ext = os.path.splitext(original_filename)[0]
    obfuscated_filename = f"{name_without_ext}-enc.py"
    obfuscated_file_path = os.path.join(TEMP_DIR, obfuscated_filename)

    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()

    encoded_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')
    hash_code = hashlib.sha256(code.encode('utf-8')).hexdigest()

    username = user.username if user.username else "Không Công Khai"
    user_id = user.id
    time_vietnam = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime('%Y-%m-%d %H:%M:%S')

    obfuscated_code = f"""
# ENCODE BY HAOESPORTS
# Key: {key}
# Trial version
# Username Obf: @{username} ({user_id})
# Obf Time: {time_vietnam}

import base64
import hashlib

expected_hash = '{hash_code}'
current_hash = hashlib.sha256(base64.b64decode('{encoded_code}')).hexdigest()
if current_hash != expected_hash:
    raise Exception("I am bot enc test version.")

exec(base64.b64decode('{encoded_code}').decode('utf-8'))
"""

    with open(obfuscated_file_path, 'w', encoding='utf-8') as obf_file:
        obf_file.write(obfuscated_code)

    return obfuscated_file_path



@bot.message_handler(commands=['tv'])
def tieng_viet(message):
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
    
