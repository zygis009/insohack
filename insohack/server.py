import json
import os
import re
import time

import pygame
import requests
from flask import Flask, request, send_file
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client

from insohack import tts_stt
from insohack.llm_access import create_client, send_conversation_message

app = Flask(__name__)


def extract_data(text):
    # Regex to find everything after <END_OF_CONVERSATION>
    pattern = r'<END_OF_CONVERSATION>\s*(\{.*?\})'

    # Search for the JSON in the text
    match = re.search(pattern, text, re.DOTALL)

    if match:
        json_str = match.group(1)  # Capture the JSON part
        try:
            # Convert the JSON string to a Python dictionary
            json_data = json.loads(json_str)
            return json_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        return None


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/webhook', methods=['POST'])
def webhook():
    """Returns TwiML which prompts the caller to record a message"""
    # Create response audio
    global resp, openai_client
    tts_stt.tts(openai_client, resp.content[0].text, "../output.mp3")

    # Start our TwiML response
    response = VoiceResponse()

    # Use <Say> to give the caller some instructions
    response.play('/play-response')

    # Use <Record> to record the caller's message, transcribe it, and specify an action URL
    response.record(transcribe=False, recording_status_callback='/proccess-recording')

    # End the call with <Hangup>
    response.hangup()

    return str(response)


@app.route('/proccess-recording', methods=['POST'])
def process_recording():
    global client, resp, openai_client
    recording_url = request.form.get('RecordingUrl')

    basic = HTTPBasicAuth(os.environ["TWILIO_ACCOUNT_ID"], os.environ["TWILIO_API_TOKEN"])
    audio_file = requests.get(recording_url, auth=basic)
    with open("../input.wav", "wb") as file:
        file.write(audio_file.content)

    user_input = tts_stt.stt(openai_client, "../input.wav")
    resp = send_conversation_message(client, user_input)

    result = extract_data(resp.content[0].text)
    if result is not None:
        return str(result)

    return str(resp.content[0].text)


@app.route('/play-response')
def play_response():
    return send_file("../output.mp3", mimetype="audio/mpeg")

@app.route('/response', methods=['POST'])
def response():
    """Returns TwiML which prompts the caller to record a message"""
    # Start our TwiML response

    return str(request)


@app.route('/create-call', methods=['POST'])
def create_call():
    client = Client(os.environ["TWILIO_ACCOUNT_ID"], os.environ["TWILIO_API_TOKEN"])

    call = client.calls.create(
        url=os.environ["WEBHOOK_URL"],
        to=os.environ["NUMBER_TO"],
        from_=os.environ["NUMBER_FROM"]
    )

    return str(call)


@app.route('/handle-transcription', methods=['POST'])
def handle_transcription():
    """Handles the transcription callback from Twilio"""
    transcription = request.form.get('TranscriptionText')
    with open("../transcription.txt", "w") as file:
        file.write(f"Transcription: {transcription}")
    return str(transcription)


if __name__ == '__main__':
    load_dotenv()
    pygame.mixer.init()
    global client, resp, openai_client
    client, resp = create_client()
    openai_client = tts_stt.tts_stt_client()

    app.run(port=8080, debug=True)
