from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)  


BOT_TOKEN = "8901154207:AAG0LRh3FMEqyla7mOwrgNrSxWZCecTRMDg"
CHAT_ID = "1549150337"


def send_to_telegram(name, phone, email, comment):
    """Отправляет заявку в Telegram"""
    message = f"""
🆕 НОВАЯ ЗАЯВКА!

👤 Имя: {name}
📱 Телефон: {phone}
📧 Email: {email}
📝 Комментарий: {comment}

📅 {__import__('datetime').datetime.now().strftime('%d.%m.%Y %H:%M')}
    """

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.post(url, data=payload)
        return response.status_code == 200
    except:
        return False


@app.route('/send_order', methods=['POST'])
def send_order():
    try:
        print("📩 Получен запрос!")
        data = request.json
        print(f"Данные: {data}")

        name = data.get('name', '')
        phone = data.get('phone', '')
        email = data.get('email', '')
        comment = data.get('comment', '')

        print(f"Имя: {name}, Телефон: {phone}")


        if not name or not phone:
            print("❌ Ошибка: Имя или телефон пустые")
            return jsonify({'error': 'Имя и телефон обязательны'}), 400

        success = send_to_telegram(name, phone, email, comment)
        print(f"Результат отправки в Telegram: {success}")

        if success:
            return jsonify({'status': 'success', 'message': 'Заявка отправлена'})
        else:
            print("❌ Ошибка отправки в Telegram")
            return jsonify({'error': 'Ошибка отправки в Telegram'}), 500

    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/', methods=['GET'])
def home():
    return "Сервер для лендинга работает! 🚀"


if __name__ == '__main__':
    app.run(debug=True, port=5000)