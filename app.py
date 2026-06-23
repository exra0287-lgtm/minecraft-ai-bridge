from flask import Flask, request, jsonify, send_from_directory
import itertools
from openai import OpenAI

app = Flask(__name__)

# ضع جميع مفاتيحك هنا - النظام سيوزع الطلبات بينها تلقائياً
API_KEYS = ["sk-...iBcA", "sk-...ivEA", "sk-...wtoA"]
key_cycle = itertools.cycle(API_KEYS)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_message = data.get('message', '')
    
    current_key = next(key_cycle)
    
    try:
        client = OpenAI(api_key=current_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Minecraft assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({"answer": response.choices[0].message.content})
    except Exception:
        return jsonify({"answer": "System busy, please try again."})

if __name__ == '__main__':
    app.run()
