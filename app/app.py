from flask import Flask, request, jsonify, render_template, send_from_directory
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ.get("NVIDIA_API_KEY")
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_prompt = request.json.get('prompt', '')
    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    try:
        completion = client.chat.completions.create(
            model="nvidia/llama-3.3-nemotron-super-49b-v1",
            messages=[
                {"role": "system", "content": "You are a Finance expert assistant. Provide helpful, accurate, and concise responses about finance topics. Format your responses using Markdown for better readability when appropriate."},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.6,
            top_p=0.7,
            max_tokens=1024,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        return jsonify({"response": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))