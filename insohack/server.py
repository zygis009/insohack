from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/webhook', methods=['POST'])
def webhook():
    """Returns TwiML which prompts the caller to record a message"""
    # Start our TwiML response
    response = VoiceResponse()

    # Use <Say> to give the caller some instructions
    response.say('Hello, this is our own question')

    # Use <Record> to record the caller's message, transcribe it, and specify an action URL
    response.record(transcribe=True, finishOnKey='#', transcribe_callback='/handle-transcription')

    # End the call with <Hangup>
    response.hangup()

    return str(response)

@app.route('/response', methods=['POST'])
def response():
    """Returns TwiML which prompts the caller to record a message"""
    # Start our TwiML response

    return str(request)

@app.route('/create-call', methods=['POST'])
def create_call():
    account_sid = "asjndaksjnda"
    auth_token = "get_shreked"
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        url="your_webhook_url",
        to="your_number",
        from_="twilio_number"
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
    app.run(port=8080, debug=True)