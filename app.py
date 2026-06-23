from flask import Flask, jsonify, request, render_template_string
import os
import itertools
from openai import OpenAI

app = Flask(__name__)

# --- إعدادات المراقبة ---
stats = {"requests": 0}

# --- إعدادات مفاتيح OpenAI ---
api_keys = [os.environ.get(f"OPENAI_API_KEY{i}") for i in range(1, 4)]
api_keys = [key for key in api_keys if key]
key_cycle = itertools.cycle(api_keys)

# --- كود صفحة الويب المطور (يظهر حالة الضغط والوقت) ---
HTML_CODE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI System Dashboard</title>
    <style>
        body { font-family: sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); text-align: center; width: 300px; }
        .status { color: #28a745; font-weight: bold; }
        .count { font-size: 2em; color: #007bff; }
        #timer { font-size: 1.5em; color: #555; }
    </style>
</head>
<body>
    <div class="box">
        <h1>System Status: <span class="status">Online</span></h1>
        <p>Total Requests Handled:</p>
        <div class="count">{{ stats.requests }}</div>
        <p>Time Online:</p>
        <div id="timer">00:00:00</div>
    </div>
    <script>
        let s=0,m=0,h=0;
        setInterval(()=>{ s++; if(s==60){s=0;m++} if(m==60){m=0;h++}
        document.getElementById('timer').innerText = (h<10?'0'+h:h)+':'+(m<10?'0'+m:m)+':'+(s<10?'0'+s:s);
        }, 1000);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE, stats=stats)

@app.route('/ask', methods=['POST'])
def ask():
    stats["requests"] += 1  # زيادة عداد الطلبات عند كل استفسار
    try:
        data = request.json
        user_message = data.get('message', '')
        current_key = next(key_cycle)
        
        client = OpenAI(api_key=current_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful Minecraft assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({"answer": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"answer": "Error: Key exhausted or API limit reached."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
