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
name_bot = "Trần Hào"
ADMIN_ID = '7658079324'
facebook = "no"
users_keys = {}
key = ""
blacklist = []  # hoặc set(), hoặc list chứa sẵn các số
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


start_time = time.time()



@bot.message_handler(commands=['bot','start'])
def send_help(message):
    bot.reply_to(message, """<blockquote>
┌───⭓ Trần Hào
➤ /spam : Spam FREE
➤ /stop : Dừng Spam SĐT
➤ /tv : Tiếng việt cho telegram
➤ /id : Lấy id bản thân
➤ /checkban : Kiểm tra tk có khoá không
➤ /searchff : Tìm tk ff bằng tên
└───Tiện Ích Khác
➤ /like : buff like
➤ /ff : check info
➤ /uptime : Xem Thời gian bot hoạt động
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

#pet
@bot.message_handler(commands=['ff'])
def ff(message):
    try:
        args = message.text.split()
        if len(args) != 3:
            bot.reply_to(message, "Sai cú pháp! Dùng: /ff [uid] [region]")
            return

        uid = args[1]
        region = args[2]
        url = f"https://ariiflexlabs-playerinfo-icxc.onrender.com/ff_info?uid={uid}&region={region}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        account = data.get("AccountInfo", {})
        name = account.get("AccountName", "Unknown")
        level = account.get("AccountLevel", "N/A")
        likes = account.get("AccountLikes", 0)
        br_rank = account.get("BrMaxRank", "N/A")
        br_point = account.get("BrRankPoint", 0)
        cs_rank = account.get("CsMaxRank", "N/A")
        cs_point = account.get("CsRankPoint", 0)
        region = account.get("AccountRegion", "N/A")

        text = (
            f"<b>Tên:</b> {name}\n"
            f"<b>Level:</b> {level}\n"
            f"<b>Region:</b> {region}\n"
            f"<b>Likes:</b> {likes}\n\n"
            f"<b>BR Rank:</b> {br_rank} ({br_point} RP)\n"
            f"<b>CS Rank:</b> {cs_rank} ({cs_point} RP)"
        )

        bot.send_message(message.chat.id, text, parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message, f"Có lỗi xảy ra: {e}")






def call_api(uid):
    try:
        url = f"https://dichvukey.site/likeff2.php?uid={uid}"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        return {"message": f"Lỗi khi gọi API: {e}"}

# Định nghĩa hàm xử lý lỗi API
def handle_api_error(message, note):
    bot.reply_to(message, f"<blockquote>⚠️ {note}</blockquote>", parse_mode="HTML")

# Hàm xử lý lệnh '/like'
@bot.message_handler(commands=['like'])
def like_handler(message):
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "<blockquote>❗ Vui lòng nhập đúng cú pháp: /like 1733997441</blockquote>", parse_mode="HTML")
        return

    uid = args[1]
    data = call_api(uid)

    if "message" in data:
        msg_content = data["message"]
        if isinstance(msg_content, str):
            reply_text = f"<blockquote>⚠️ {msg_content}</blockquote>"
        elif isinstance(msg_content, dict):
            reply_text = (
                f"<blockquote>\n"
                f"🎯 <b>Kết quả buff like:</b><br>"
                f"👤 <b>Tên:</b> {msg_content.get('Name', 'Không xác định')}<br>"
                f"🆔 <b>UID:</b> {msg_content.get('UID', uid)}<br>"
                f"🌎 <b>Khu vực:</b> {msg_content.get('Region', 'Không xác định')}<br>"
                f"📊 <b>Level:</b> {msg_content.get('Level', 'Không xác định')}<br>"
                f"👍 <b>Like trước:</b> {msg_content.get('Likes Before', 'Không xác định')}<br>"
                f"✅ <b>Like sau:</b> {msg_content.get('Likes After', 'Không xác định')}<br>"
                f"➕ <b>Tổng cộng:</b> {msg_content.get('Likes Added', 'Không xác định')} like<br>"
                f"</blockquote>"
            )
        else:
            reply_text = "<blockquote>Dữ liệu trả về không đúng định dạng.</blockquote>"

        bot.reply_to(message, reply_text, parse_mode="HTML")
    else:
        handle_api_error(message, "API không trả về kết quả hợp lệ.")



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
        bot.send_message(message.chat.id, "/spam sdt số_lần như này cơ mà")
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


#tkey
import random
import string
import base64
import zlib
import hashlib
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TEMP_DIR = "temp"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# Biến toàn cục
current_key = None
key_attempts = 0
encryption_method = "base64"

# Tạo key ngẫu nhiên
def generate_random_key(length=16):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# Giao diện tạo key
@bot.message_handler(commands=['tkey'])
def create_key(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Mã hóa base64"), KeyboardButton("Mã hóa nâng cao"))
    bot.send_message(message.chat.id, "Chọn kiểu mã hóa:", reply_markup=markup)
    bot.register_next_step_handler(message, process_encryption_choice)

def process_encryption_choice(message):
    global current_key, key_attempts, encryption_method
    current_key = generate_random_key()
    key_attempts = 1

    if "nâng cao" in message.text.lower():
        encryption_method = "advanced"
    else:
        encryption_method = "base64"

    bot.send_message(
        message.chat.id,
        f"Key đã được tạo: {current_key}\nPhương pháp mã hóa: {encryption_method.upper()}\n"
        f"Bạn có {key_attempts} lần gửi file .py"
    )

# Xử lý file .py gửi lên
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
    obfuscated_file_path = None  # đảm bảo biến tồn tại để dùng trong finally

    msg = bot.reply_to(message, "Đang mã hóa...", parse_mode='HTML')
    time.sleep(2)

    try:
        obfuscated_file_path = obfuscate_file(file_path, current_key, message.from_user, encryption_method)

        # XÓA FILE GỐC trước khi gửi file đã mã hóa
        if os.path.exists(file_path):
            os.remove(file_path)

        bot.send_message(message.chat.id, "Mã hóa hoàn tất! Đang gửi file...")
        with open(obfuscated_file_path, 'rb') as obfuscated_file:
            bot.send_document(message.chat.id, obfuscated_file)

        bot.send_message(message.chat.id, f"Đã gửi: {os.path.basename(obfuscated_file_path)}")

    except Exception as e:
        bot.send_message(message.chat.id, f"Đã xảy ra lỗi khi mã hóa: {e}")

    finally:
        if obfuscated_file_path and os.path.exists(obfuscated_file_path):
            os.remove(obfuscated_file_path)


# Hàm mã hóa file
def obfuscate_file(file_path, key, user, method):
    original_filename = os.path.basename(file_path)
    name_without_ext = os.path.splitext(original_filename)[0]
    obfuscated_filename = f"{name_without_ext}-enc.py"
    obfuscated_file_path = os.path.join(TEMP_DIR, obfuscated_filename)

    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()

    if method == "advanced":
        compressed_code = zlib.compress(code.encode('utf-8'))
        encoded_code = base64.b85encode(compressed_code).decode('utf-8')
        decode_code = f"zlib.decompress(base64.b85decode(encoded)).decode('utf-8')"
        import_lines = "import base64, zlib, hashlib"
    else:
        encoded_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')
        decode_code = f"base64.b64decode(encoded).decode('utf-8')"
        import_lines = "import base64, hashlib"

    hash_code = hashlib.sha256(code.encode('utf-8')).hexdigest()

    username = user.username if user.username else "Không Công Khai"
    user_id = user.id
    time_vietnam = (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime('%Y-%m-%d %H:%M:%S')

    obfuscated_code = f"""# ENCODE BY HAOESPORTS
# Key: {key}
# Method: {method}
# Username Obf: @{username} ({user_id})
# Obf Time: {time_vietnam}

{import_lines}

encoded = '{encoded_code}'
expected_hash = '{hash_code}'

decoded = {decode_code}
current_hash = hashlib.sha256(decoded.encode('utf-8')).hexdigest()

if current_hash != expected_hash:
    raise Exception("I am bot enc test version.")

exec(decoded)
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
    
