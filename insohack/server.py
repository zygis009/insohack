import os
import json
from flask import Flask, request
from dotenv import load_dotenv
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client

app = Flask(__name__)

# Load survey questions into memory
with open('insohack/example_survey.json', 'r') as survey_file:
    pages = json.load(survey_file)['pages']

@app.route('/create-call', methods=['POST'])
def create_call():
    client = Client(os.environ["TWILIO_ACCOUNT_ID"], os.environ["TWILIO_API_TOKEN"])

    call = client.calls.create(
        url=os.environ["WEBHOOK_URL"],
        to=os.environ["NUMBER_TO"],
        from_=os.environ["NUMBER_FROM"]
    )

    return "<3"

@app.route('/start-survey', methods=['POST'])
def start_survey():
    # Start our TwiML response
    response = VoiceResponse()
    # Say some intro stuff and redirect to the questions
    response.say(pages[0]['text'])
    response.redirect('/next-page?page_idx=1', method='POST')  # Redirect to the first question (ID 1)

    return str(response)

@app.route('/next-page', methods=['POST'])
def next_page():
    page_idx = int(request.args.get('page_idx', None))
    if page_idx > 1:
        save_answer_for_question(request, page_idx-1, pages[page_idx-1]['needsFollowUp'])
    # Initialize response
    response = VoiceResponse()

    # Get the current question or end the survey
    page = pages[page_idx]
    if page['type'] == 'question':
        if page['needsFollowUp']:
            action = '/follow-up?page_idx='+str(page_idx)
        else:
            action = '/next-page?page_idx='+str(page_idx+1)
        gather = Gather(input=page['input'], action=action, method='POST', finishOnKey='#')
        gather.say(pages[page_idx]['text'])
        response.append(gather)
    else:
        response.say(pages[page_idx]['text'])
        response.hangup()

    return str(response)

import json
import os

def save_answer_for_question(request, page_idx, is_follow_up):
    # Get transcription and digits
    transcription = request.form.get('SpeechResult', None)
    digits = request.form.get('Digits', None)

    # Check if the responses file exists
    if not os.path.exists('insohack/response.json'):
        responses = {}  # Initialize as empty if the file doesn't exist
    else:
        with open('insohack/response.json', 'r') as openfile:
            responses = json.load(openfile)

    # Ensure the entry for page_idx exists
    page_idx_str = str(page_idx)  # Convert to string if necessary
    if page_idx_str not in responses:
        responses[page_idx_str] = {
            'answer': None,
            'followUpAnswer': None
        }

    # Set the transcription or digits to the appropriate attribute
    attr = 'followUpAnswer' if is_follow_up else 'answer'
    responses[page_idx_str][attr] = transcription if transcription else digits

    # Write back the updated responses to the file
    with open("insohack/response.json", "w") as outfile:
        json.dump(responses, outfile)


# @app.route('/follow-up', methods=['POST'])
# def follow_up():
#     page_idx = int(request.args.get('page_idx', None))
#     # if page_idx != 0:
#     #     save_answer_for_question(request, page_idx, False)
#
#     #prolly gpt this based on the answer from the previous question
#     text = ''
#
#     # Initialize response
#     # response = VoiceResponse()
#     # action = 'next-page?page_idx='+str(page_idx+1)
#     # gather = Gather(input='speech', action=action, timeout=5, method='POST')
#     # gather.say(text)
#     # response.append(gather)
#
#     return str(response)

if __name__ == '__main__':
    load_dotenv()
    app.run(port=8080, debug=True)
