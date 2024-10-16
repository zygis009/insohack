from openai import OpenAI
import os


def tts_stt_client():
    api_key = os.getenv("OPENAI_KEY")
    return OpenAI(api_key=api_key)


def stt(client: OpenAI, input_filepath_mp3: str) -> str:
    audio_file = open(input_filepath_mp3, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )
    return transcription


def tts(client: OpenAI, input_text: str, output_filepath_mp3: str):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=input_text
    )

    with open(output_filepath_mp3, "wb") as file:
        for chunk in response.iter_bytes():
            file.write(chunk)
