from flask import Flask, render_template, request
import os
from your_module_name import do_synthesize_speech  # Update with the correct import path

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        input_text = request.form.get("input_text")
        selected_voice = request.form.get("voice", None)
        if selected_voice:
            audio_base64 = do_synthesize_speech(input_text, selected_voice)
            return render_template("index.html", input=input_text, voice=selected_voice, audio_base64=audio_base64)
    return render_template("index.html")

# Insert the line below to run on Cloud9    
app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))

if __name__ == '__main__':
    app.run(debug=True)
