from flask import Flask, jsonify, request, render_template_string
import os
import itertools
from openai import OpenAI

app = Flask(__name__)

# تخزين الرسائل وسجل الطلبات
chat_history = []
stats = {"requests": 0}

# إعدادات المفاتيح
api_keys = [os.environ.get(f"OPENAI_API_KEY{i}") for i in range(1, 4)]
api_keys = [key for key in api_keys if key]
key_cycle = itertools.cycle(api_keys)

# تصميم لوحة التحكم السوداء
HTML_CODE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI System Dashboard</title>
    <style>
        body { background: #000; color: #0f0; font-family: 'Courier New', monospace; padding: 20px; }
        .box { background: #111; padding: 20px; border-radius: 10px; border: 1px solid #333; max-width: 600px; margin: auto; }
        .log-box { height: 300px; overflow-y: scroll; border: 1px solid #222; padding: 10px; margin-top: 10px; background: #000; }
        .error { color: #f00; }
        .stats { font-size: 1.2em; border-bottom: 1px solid #333; padding-bottom: 10px; }
    </style>
</head>
<body>
    <div class="box">
        <div class="stats">
            <h1>System: <span style="color:green">ONLINE</span></h1>
            <p>Total Requests: {{ stats.requests }}</p>
        </div>
        <div class="log-box">
            {% for log in logs %}
                <div style="margin-bottom:8px;">{{ log }}</div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE, logs=chat_history, stats=stats)

@app.route('/ask', methods=['POST'])
def ask():
    stats["requests"] += 1
    data = request.json
    user_message = data.get('message', '')
    
    # إضافة الرسالة لسجل التحكم
    chat_history.append(f"> Player: {user_message}")
    
    try:
        current_key = next(key_cycle)
        client = OpenAI(api_key=current_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful Minecraft assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        ai_reply = response.choices[0].message.content
        chat_history.append(f"<span style='color:#0ff'>AI: {ai_reply}</span>")
        return jsonify({"answer": ai_reply})
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        chat_history.append(f"<span class='error'>{error_msg}</span>")
        return jsonify({"answer": "خطأ في الاتصال بالذكاء الاصطناعي"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
