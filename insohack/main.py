import threading
import time
from dotenv import load_dotenv
import json
from llm_access import create_client, send_conversation_message, send_single_message, flush_conversation
import re
from record import detect_sound, record_audio
import pygame
import tts_stt


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


load_dotenv()
pygame.mixer.init()

client, resp = create_client()
openai_client = tts_stt.tts_stt_client()

result = None

stop_event = threading.Event()

while True:
    print(resp.content[0].text+"\n\n")
    tts_stt.tts(openai_client, resp.content[0].text, "../output.mp3")
    stop_event.clear()

    # Start speech detection thread
    speech_detection_thread = threading.Thread(target=detect_sound, args=(stop_event,))
    speech_detection_thread.start()

    # Play the assistant's response
    pygame.mixer.music.load("../output.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        if stop_event.is_set():
            pygame.mixer.music.stop()
            break
        time.sleep(0.1)
    pygame.mixer.music.unload()

    # Wait for user to start speaking
    if stop_event.is_set():
        print("User interrupted responder, recording input...")
    else:
        print("Responder finished, waiting for user input...")

    stop_event.clear()
    record_audio()
    # user_input = input(resp.content[0].text + "\n")
    user_input = tts_stt.stt(openai_client, "../test.wav")
    # if user_input == "exit":
    #     break
    print(user_input+"\n-----------------------------------\n")
    resp = send_conversation_message(client, user_input)

    result = extract_data(resp.content[0].text)
    if result is not None:
        break

print(result)
