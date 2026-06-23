import os
import itertools
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# هنا الكود يسحب المفاتيح الثلاثة التي وضعتها في Render
api_keys = [
    os.environ.get("OPENAI_API_KEY1"),
    os.environ.get("OPENAI_API_KEY2"),
    os.environ.get("OPENAI_API_KEY3")
]
key_cycle = itertools.cycle(api_keys)

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
    except Exception as e:
        return jsonify({"answer": "Error: " + str(e)})

if __name__ == '__main__':
    app.run()
