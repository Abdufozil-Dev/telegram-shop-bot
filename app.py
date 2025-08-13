import os
from flask import Flask, request, jsonify, render_template_string
import telebot

TOKEN = os.getenv("TOKEN", "TOKEN = "8443927280:AAGG-hrnp1_anHSqAPfeif-gaTijnYe4sYw"
")  # Bot token
ADMIN_ID = int(os.getenv("ADMIN_ID", "6413273899"))  # Admin ID

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Mahsulotlar ro'yxati (namuna)
products = [
    {"id": 1, "name": "Kostyum", "price": 500000, "img": "https://via.placeholder.com/150"},
    {"id": 2, "name": "Ko'ylak", "price": 200000, "img": "https://via.placeholder.com/150"},
    {"id": 3, "name": "Shim", "price": 250000, "img": "https://via.placeholder.com/150"},
]

# Telegram bot komandasi
@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton(
        text="🛍 Do‘konga kirish",
        web_app=telebot.types.WebAppInfo(url=os.getenv("APP_URL", "https://google.com"))
    )
    markup.add(btn)
    bot.send_message(message.chat.id, "Salom! Bizning erkaklar kiyimlari do‘konimizga xush kelibsiz!", reply_markup=markup)

# Buyurtmani qabul qilish
@app.route("/order", methods=["POST"])
def order():
    data = request.json
    user_name = data.get("name")
    phone = data.get("phone")
    product = data.get("product")

    # Admin'ga xabar yuborish
    bot.send_message(ADMIN_ID, f"📦 Yangi buyurtma!\n👤 Ism: {user_name}\n📞 Tel: {phone}\n🛍 Mahsulot: {product}")

    return jsonify({"status": "success"})

# Mini-app sahifasi (oddiy HTML)
@app.route("/")
def index():
    html = """
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Do‘kon</title>
    </head>
    <body>
        <h1>🛍 Erkaklar kiyimlari</h1>
        {% for p in products %}
            <div style="border:1px solid #ccc;margin:10px;padding:10px;">
                <img src="{{p.img}}" width="100"><br>
                <b>{{p.name}}</b><br>
                Narx: {{p.price}} so'm<br>
                <button onclick="buy('{{p.name}}')">Sotib olish</button>
            </div>
        {% endfor %}
        <script>
            function buy(product) {
                let name = prompt("Ismingiz:");
                let phone = prompt("Telefon raqamingiz:");
                fetch("/order", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({name, phone, product})
                }).then(r=>r.json()).then(d=>alert("Buyurtma qabul qilindi!"));
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html, products=products)

# Webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
