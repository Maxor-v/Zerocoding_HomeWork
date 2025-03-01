from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhooks', methods=['POST'])
def handle_webhook():
    print("Получен вебхук:", request.json)  # Логируем данные
    return jsonify({"status": "ok"}), 200  # Обязательно возвращаем 200 OK

if __name__ == '__main__':
    app.run(host='localhost', port=5000, ssl_context=('C:/OpenSSL-Win64/bin/cert.pem', 'C:/OpenSSL-Win64/bin/key.pem'))