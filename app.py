from flask import Flask, jsonify, request, render_template_string
import os
import itertools
from openai import OpenAI

app = Flask(__name__)

# --- إعدادات مفاتيح OpenAI ---
api_keys = [
    os.environ.get("OPENAI_API_KEY1"),
    os.environ.get("OPENAI_API_KEY2"),
    os.environ.get("OPENAI_API_KEY3")
]
api_keys = [key for key in api_keys if key]
key_cycle = itertools.cycle(api_keys)

# --- كود صفحة الويب والعداد ---
HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI System Dashboard</title>
    <style>
        body { background-color: #f0f2f5; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; }
        #timer { font-size: 3em; color: #333; font-weight: bold; }
    </style>
</head>
<body>
    <div class="box">
        <h1>AI System is Online</h1>
        <div id="timer">00:00:00</div>
    </div>
    <script>
        let seconds = 0, minutes = 0, hours = 0;
        function updateTimer() {
            seconds++;
            if (seconds == 60) { seconds = 0; minutes++; }
            if (minutes == 60) { minutes = 0; hours++; }
            document.getElementById('timer').innerText = 
                (hours < 10 ? "0"+hours : hours) + ":" + 
                (minutes < 10 ? "0"+minutes : minutes) + ":" + 
                (seconds < 10 ? "0"+seconds : seconds);
        }
        setInterval(updateTimer, 1000);
    </script>
</body>
</html>
"""

# --- المسارات (Routes) ---

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/ask', methods=['POST'])
def ask():
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
        return jsonify({"answer": "Error: " + str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)