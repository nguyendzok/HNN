from flask import Flask, jsonify
import random, string

app = Flask(__name__)

# Tạo key ngẫu nhiên
def generate_key(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/api/getkey")
def api_getkey():
    key = generate_key()
    return jsonify({"key": key})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
