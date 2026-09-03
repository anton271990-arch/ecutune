from telegram import Bot
import asyncio
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

# Загружаем настройки из .env файла
load_dotenv()
   BOT_TOKEN = os.getenv('BOT_TOKEN')
   ADMIN_ID = os.getenv('ADMIN_ID')

print("=== ПРОВЕРКА ДАННЫХ ПРИ ЗАПУСКЕ ===")
print(f"Токен: {repr(BOT_TOKEN)}")
print(f"ID: {repr(ADMIN_ID)}")
print(f"Длина токена: {len(BOT_TOKEN) if BOT_TOKEN else 0}")
print("===================================")

app = Flask(__name__)

async def send_to_admin(data):
    """Отправляет заявку админу в Telegram"""
    try:
        bot = Bot(token=BOT_TOKEN)
        
        name = data.get('name', 'Не указано')
        phone = data.get('phone', 'Не указано')
        email = data.get('email', 'Не указано')
        message = data.get('message', 'Не указано')
        
        text = f"""
🔔 <b>Новая заявка с сайта!</b>

👤 <b>Имя:</b> {name}
📞 <b>Телефон:</b> {phone}
📧 <b>Email:</b> {email}
💬 <b>Сообщение:</b> {message}
"""
        await bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode='HTML')
        print("✅ Сообщение успешно отправлено в Telegram!")
    except Exception as e:
        print(f"❌ ОШИБКА ОТПРАВКИ В TELEGRAM: {e}")
        raise

@app.route('/webhook', methods=['POST'])
def webhook():
    """Получает данные с сайта"""
    try:
        data = request.json
        print(f"📩 Получены данные: {data}")
        asyncio.run(send_to_admin(data))
        return jsonify({"status": "ok"})
    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА В WEBHOOK: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def home():
    return "Бот работает!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)