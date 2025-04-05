import telebot
import subprocess
import sys
from requests import post, Session
import time
import datetime
import threading
from urllib.parse import urlparse
import psutil
import tempfile
import random
from gtts import gTTS
import re
import string
import os
from flask import Flask, request
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
admin_diggory = "HaoEsport" 
name_bot = "Trần Hào"
ADMIN_ID = '7912024917'
zalo = "0585019743"
web = "https://dichvukey.site/"
facebook = "no"
bot = telebot.TeleBot(os.environ.get('token')) 
print(os.environ.get('token'))  # Kiểm tra token có tồn tại không
print("Bot đã được khởi động thành công")
users_keys = {}
key = ""
user_cooldown = {}
last_usage = {} 
share_log = []
auto_spam_active = False
last_sms_time = {}
global_lock = Lock()
admin_mode = False
allowed_users = []
processes = []
ADMIN_ID =  7845889525 #nhớ thay id nhé nếu k thay k duyệt dc vip đâu v.L..ong.a
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



def fetch_data(user_id):
    try:
        url = f'https://api.ffcommunity.site/info.php?uid={user_id}'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

@bot.message_handler(commands=['ff'])
def handle_command(message):
    parts = message.text.split()
    if len(parts) != 2:
        bot.reply_to(message, "<blockquote>Sử dụng: /ff ID\nVí dụ: /ff 1733997441</blockquote>", parse_mode="HTML")
        return
    
    command, user_id = parts
    if not user_id.isdigit():
        bot.reply_to(message, "<blockquote>ID không hợp lệ. Vui lòng nhập ID số.</blockquote>", parse_mode="HTML")
        return

    try:
        data = fetch_data(user_id)
        if data is None:
            bot.reply_to(message, "<blockquote>❌ Server API đang bảo trì hoặc quá tải. Vui lòng thử lại sau.</blockquote>", parse_mode="HTML")
            return
            
        basic_info = data
        clan_info = data.get('Guild Information', {})
        leader_info = data.get('Guild Leader Information', {})
        avatar_url = basic_info.get('AccountAvatarId', 'Không có')

        def get_value(key, data_dict):
            return data_dict.get(key, "Không có thông tin")

        info_text = f"""
<blockquote>
<b>Thông tin cơ bản:</b>
Avatar: <a href="{avatar_url}">Nhấn để xem</a>
Nickname: {get_value('AccountName', basic_info)}
Cấp độ: {get_value('AccountLevel', basic_info)}
Khu vực: {get_value('AccountRegion', basic_info)}
Xếp hạng Sinh Tồn: {get_value('BrRank', basic_info)}
Tổng Sao Tử Chiến: {get_value('CsRank', basic_info)}
Số lượt thích: {get_value('AccountLikes', basic_info)}
Lần đăng nhập gần nhất: {get_value('AccountLastLogin (GMT 0530)', basic_info)}
Ngôn ngữ: {get_value('AccountLanguage', basic_info)}
Tiểu sử game: {get_value('AccountSignature', basic_info)}

<b>Thông tin quân đoàn:</b>
Tên quân đoàn: {get_value('GuildName', clan_info)}
Cấp độ quân đoàn: {get_value('GuildLevel', clan_info)}
Sức chứa: {get_value('GuildCapacity', clan_info)}
Số thành viên hiện tại: {get_value('GuildMember', clan_info)}
Chủ quân đoàn: {get_value('LeaderName', leader_info)}
Cấp độ chủ quân đoàn: {get_value('LeaderLevel', leader_info)}
</blockquote>
"""

        bot.reply_to(message, info_text, parse_mode='HTML')

    except Exception as e:
        bot.reply_to(message, "<blockquote>Đã xảy ra lỗi</blockquote>", parse_mode="HTML")


@bot.message_handler(commands=['help','start'])
def send_help(message):
    bot.reply_to(message, """<blockquote>
┌───⭓ Trần Hào
» /spam : Spam + Call FREE
» /status : SĐT Đang Spam
» /stop : Dừng Spam SĐT
» /key : Nhập Key Đã Mua
» /muavip : Mua VIP           
» /checkme : Check VIP
» /warning : Lưu Ý Khi Spam
»/tv : Tiếng việt cho telegram
└───⧕

┌───⭓ Tiện Ích Khác
»/like : Buff Like FF
»/ff : xem thông tin
»/visit : Buff View FF
»/fltik : Buff Follow Tiktok
»/voice : Chuyển văn bản thành giọng nói 
»/hoi : hỏi gamini 
»/band : Kiểm tra tài khoản có khóa không
└───⧕

┌───⭓ Contact
» /admin : Liên Hệ ADMIN
└───⧕
</blockquote>""", parse_mode="HTML")
### /like
API_BASE_URL = "https://dichvukey.site/likeff.php"

def call_api(uid):
    url = f"{API_BASE_URL}?uid={uid}"
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return {"status": "error", "message": "Server quá tải hoặc lỗi kết nối"}

@bot.message_handler(commands=['like'])
def like_handler(message):
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "<blockquote>🔹 Cách dùng: /like [UID]</blockquote>", parse_mode="HTML")
        return

    uid = args[1]
    data = call_api(uid)

    # Kiểm tra API có trả về lỗi không
    if "error" in data:
        bot.reply_to(message, f"<blockquote>❌ {data['error']}</blockquote>", parse_mode="HTML")
        return

    # Nếu API trả về thông tin hợp lệ
    reply_text = (
        f"<blockquote>\n"
        f"🎯 <b>Kết quả buff like:</b>\n"
        f"👤 <b>Tên:</b> {data.get('username', 'Không xác định')}\n"
        f"🆔 <b>UID:</b> {data.get('uid', 'Không xác định')}\n"
        f"👍 <b>Like trước:</b> {data.get('likes_before', 'Không xác định')}\n"
        f"✅ <b>Like sau:</b> {data.get('likes_after', 'Không xác định')}\n"
        f"➕ <b>Tổng cộng:</b> {data.get('likes_given', 'Không xác định')} like\n"
        f"</blockquote>"
    )

    bot.reply_to(message, reply_text, parse_mode="HTML")


@bot.message_handler(commands=['voice'])
def text_to_voice(message):
    text = message.text[7:].strip()  
    if not text:
        bot.reply_to(message, 'Nhập nội dung đi VD : /voice em đẹp trai')
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

@bot.message_handler(commands=['hoi'])
def handle_hoi(message):
    text = message.text[len('/hoi '):].strip()
    
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
   


@bot.message_handler(commands=['spam'])
def spam(message):
    user_id = message.from_user.id
    current_time = time.time()
    if not bot_active:
        msg = bot.reply_to(message, 'Bot hiện đang tắt.')
        time.sleep(10)
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Error deleting message: {e}")
        return
    if admin_mode and user_id not in admins:
        msg = bot.reply_to(message, 'có lẽ admin đang fix gì đó hãy đợi xíu')
    if user_id in last_usage and current_time - last_usage[user_id] < 10:
        bot.reply_to(message, f"Vui lòng đợi {10 - (current_time - last_usage[user_id]):.1f} giây trước khi sử dụng lệnh lại.")
        return

    last_usage[user_id] = current_time

    # Phân tích cú pháp lệnh
    params = message.text.split()[1:]
    if len(params) != 2:
        bot.reply_to(message, "/spam sdt số_lần như này cơ mà")
        return

    sdt, count = params

    if not count.isdigit():
        bot.reply_to(message, "Số lần spam không hợp lệ. Vui lòng chỉ nhập số.")
        return

    count = int(count)

    if count > 25:
        bot.reply_to(message, "/spam sdt số_lần tối đa là 25 - đợi 10giây sử dụng lại.")
        return

    if sdt in blacklist:
        bot.reply_to(message, f"Số điện thoại {sdt} đã bị cấm spam.")
        return
    sdt_request = f"84{sdt[1:]}" if sdt.startswith("0") else sdt


    diggory_chat3 = f'''┌──────⭓ {name_bot}
│✅ Spam: Thành Công 
│🔢 Số Lần Spam Free: {count}
│📞 Đã Tấn Công : {sdt}
│🌍 Vùng : Việt Nam
|🎭 Người Dùng : @None
|🆔 ID Người Dùng : {user_id}
│⚠️ Hạn Chế Spam Nhé!
└─────────────
    '''

    script_filename = "dec.py"  # Tên file Python trong cùng thư mục
    try:
        # Kiểm tra xem file có tồn tại không
        if not os.path.isfile(script_filename):
            bot.reply_to(message, "Không tìm thấy file script. Vui lòng kiểm tra lại.")
            return

        # Đọc nội dung file với mã hóa utf-8
        with open(script_filename, 'r', encoding='utf-8') as file:
            script_content = file.read()

        # Tạo file tạm thời
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(script_content.encode('utf-8'))
            temp_file_path = temp_file.name

        # Chạy file tạm thời
        process = subprocess.Popen(["python", temp_file_path, sdt, str(count)])
        bot.send_message(
            message.chat.id,
            f'<blockquote>{diggory_chat3}</blockquote>\n<blockquote>GÓI NGƯỜI DÙNG: FREE</blockquote>',
            parse_mode='HTML'
        )
    except FileNotFoundError:
        bot.reply_to(message, "Không tìm thấy file.")
    except Exception as e:
        bot.reply_to(message, f"Lỗi xảy ra: {str(e)}")
      
        

blacklist = ["112", "113", "114", "115", "116", "117", "118", "119", "0", "1", "2", "3", "4"]


API_BASE_URL = "https://api.ffcommunity.site/isbanned.php?uid={uid}"


def call_api(uid):
    url = API_BASE_URL.format(uid=uid)
    response = requests.get(url)
    return response.json()

@bot.message_handler(commands=['band'])
def check_ban_status(message):
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "<blockquote>/band 10251125</blockquote>", parse_mode="HTML")
        return

    uid = args[1]
    data = call_api(uid)

    if data.get("status") == "Success":
        info = data["Check Is Banned Account"]
        reply_text = (
            f"<blockquote>\n"
            f"🔍 <b>Kết quả kiểm tra:</b>\n"
            f"🆔 UID: {info['Account UID']}\n"
            f"👤 Tên: {info['Account Name']}\n"
            f"🌍 Khu vực: {info['Account Region']}\n"
            f"🚫 Trạng thái: {'Không bị khóa' if info['Status'] == 'Account is not banned.' else 'Đã bị khóa!'}\n"
            f"</blockquote>"
        )
    else:
        reply_text = "<blockquote>server đang quá tải, báo admin ngay</blockquote>"

    bot.reply_to(message, reply_text, parse_mode="HTML")



@bot.message_handler(commands=['tv'])
def tieng_viet(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton("Tiếng Việt 🇻🇳", url='https://t.me/setlanguage/vi')
    keyboard.add(url_button)
    bot.send_message(chat_id, '<blockquote>Click vào nút "<b>Tiếng Việt</b>" để đổi ngôn ngữ sang Tiếng Việt 🇻🇳</blockquote>', reply_markup=keyboard, parse_mode='HTML')
######


if __name__ == "__main__":
    bot_active = True
    bot.polling()  #
