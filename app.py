from flask import Flask, render_template, request
import os
#from polly_service import do_synthesize_speech  # Update with the correct import path
import convert 
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


import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import base64
import os
import tempfile

def do_synthesize_speech(input_text, voice_id='Joanna'):
    polly = boto3.client(service_name='polly', region_name='ca-central-1', use_ssl=True)
    
    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=input_text, OutputFormat="mp3", VoiceId=voice_id)
        
        # Access the audio stream from the response
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                # Save audio stream to a temporary file
                with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
                    temp_audio.write(stream.read())
                    temp_audio_path = temp_audio.name

            # Read the audio file and encode it in base64
            with open(temp_audio_path, "rb") as audio_file:
                audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')

            # Clean up the temporary file
            os.remove(temp_audio_path)

            return audio_base64
    except (BotoCoreError, ClientError) as error:
        # Handle error
        print(f"Error: {error}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
