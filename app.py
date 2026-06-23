import os
import itertools
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# إعداد المفاتيح من Render
api_keys = [
    os.environ.get("OPENAI_API_KEY1"),
    os.environ.get("OPENAI_API_KEY2"),
    os.environ.get("OPENAI_API_KEY3")
]
# فلترة المفاتيح الفارغة في حال لم يتم إدخالها كلها
api_keys = [key for key in api_keys if key]
key_cycle = itertools.cycle(api_keys)

# مسار الصفحة الرئيسية للتخلص من خطأ Not Found
@app.route('/')
def home():
    return "AI System is Online! The API endpoint is at /ask"

# مسار استقبال أسئلة ماين كرافت
@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        print(f"DEBUG: Received data: {data}") # سيظهر هذا في الـ Logs في Render
        
        if not data or 'message' not in data:
            return jsonify({"answer": "Error: No message provided"}), 400
            
        user_message = data.get('message', '')
        current_key = next(key_cycle)
        
        client = OpenAI(api_key=current_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant for Minecraft."},
                {"role": "user", "content": user_message}
            ]
        )
        
        ai_reply = response.choices[0].message.content
        print(f"DEBUG: AI Reply: {ai_reply}") # سيظهر هذا في الـ Logs في Render
        return jsonify({"answer": ai_reply})
        
    except Exception as e:
        print(f"DEBUG: Error: {str(e)}")
        return jsonify({"answer": "Error: " + str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
