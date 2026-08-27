from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import json
from datetime import datetime

app = Flask(__name__)

# РАЗРЕШАЕМ ВСЕ ЗАПРОСЫ ОТОВСЮДУ
CORS(app, origins="*")

# 👇 ТВОЙ ТОКЕН
BOT_TOKEN = "8901154207:AAG0LRh3FMEqyla7mOwrgNrSxWZCecTRMDg"
CHAT_ID = 1549150337  # ТВОЙ ID (ЦИФРЫ)


def send_to_telegram(name, phone, email, comment):
    message = f"""
🆕 НОВАЯ ЗАЯВКА!

👤 Имя: {name}
📱 Телефон: {phone}
📧 Email: {email}
📝 Комментарий: {comment}

📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}
    """

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.post(url, data=payload)
        print(response.status_code, response.text)
        return response.status_code == 200
    except Exception as e:
        print(e)
        return False


@app.route('/', methods=['GET'])
def home():
    return send_from_directory('.', 'index.html')


@app.route('/send_order', methods=['POST', 'OPTIONS'])
def send_order():
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.json
        name = data.get('name', '')
        phone = data.get('phone', '')
        email = data.get('email', '')
        comment = data.get('comment', '')

        if not name or not phone:
            return jsonify({'error': 'Имя и телефон обязательны'}), 400

        success = send_to_telegram(name, phone, email, comment)

        if success:
            return jsonify({'status': 'success', 'message': 'Заявка отправлена!'})
        else:
            return jsonify({'error': 'Ошибка отправки в Telegram'}), 500

    except Exception as e:
        print(f"ОШИБКА: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)