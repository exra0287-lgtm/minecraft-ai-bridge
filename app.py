from flask import Flask, jsonify, request, render_template_string
import os
import itertools
from openai import OpenAI

app = Flask(__name__)

# سجل المحادثات
chat_history = []
stats = {"requests": 0}

# إعدادات المفاتيح
api_keys = [os.environ.get(f"OPENAI_API_KEY{i}") for i in range(1, 4)]
api_keys = [k for k in api_keys if k]
key_cycle = itertools.cycle(api_keys)

# تصميم الصفحة البيضاء (بسيطة وواضحة)
HTML_CODE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; background: #ffffff; padding: 20px; color: #333; }
        .container { max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .log { margin-bottom: 10px; padding: 8px; border-bottom: 1px solid #eee; }
        .player { color: #555; font-weight: bold; }
        .ai { color: #007bff; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2>AI System Status: <span style="color:green">Online</span></h2>
        <p>Total Requests: {{ stats.requests }}</p>
        <hr>
        <div id="logs">
            {% for log in logs %}
                <div class="log">{{ log | safe }}</div>
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
    msg = data.get('message', '')
    
    chat_history.append(f"<span class='player'>Player:</span> {msg}")
    
    try:
        client = OpenAI(api_key=next(key_cycle))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": msg}]
        )
        ai_reply = response.choices[0].message.content
        chat_history.append(f"<span class='ai'>AI:</span> {ai_reply}")
        return jsonify({"answer": ai_reply})
    except Exception as e:
        chat_history.append(f"<span style='color:red'>Error: {str(e)}</span>")
        return jsonify({"answer": "Error"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
