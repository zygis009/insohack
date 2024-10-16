import time
import pyaudiowpatch as pyaudio
import wave
import struct
import math
import matplotlib.pyplot as plt
import pygame

CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SAMPLE_SIZE = 2


def rms(data):
    count = len(data) / 2
    format = "%dh" % (count)
    shorts = struct.unpack(format, data)
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0 / 32768)
        sum_squares += n * n
    return math.sqrt(sum_squares / count)


def setup_stream(use_speakers=False):
    p = pyaudio.PyAudio()

    if use_speakers:
        wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
        default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
        if not default_speakers["isLoopbackDevice"]:
            for loopback in p.get_loopback_device_info_generator():
                if default_speakers["name"] in loopback["name"]:
                    default_speakers = loopback
                    break
            else:
                raise IOError("No speaker found")
        channels = default_speakers["maxInputChannels"]
        rate = int(default_speakers["defaultSampleRate"])
        input_device_index = default_speakers["index"]
    else:
        channels = CHANNELS
        rate = RATE
        input_device_index = 0

    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=rate,
                    input_device_index=input_device_index,
                    frames_per_buffer=pyaudio.get_sample_size(FORMAT),
                    input=True)

    return stream, p


def detect_sound(stop_event):
    stream, p = setup_stream()

    while not stop_event.is_set():
        data = stream.read(CHUNK)
        if rms(data) > 0.02:
            stop_event.set()
            break
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    p.terminate()


def record_audio():
    stream, p = setup_stream()

    frames = []

    timestamp = time.time()
    rec_flag = False
    while True:
        data = stream.read(CHUNK)

        if rms(data) > 0.01:
            print("sound detected")
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
            rec_flag = True
            timestamp = time.time()
        if rec_flag:
            frames.append(data)

        if time.time() - timestamp > 4 and len(frames) > 0:
            print("quiet")
            print("saving recording")
            save_recording(frames, {"rate": RATE, "channels": CHANNELS, "sample_size": p.get_sample_size(FORMAT)},
                           "../input.wav")
            break

    stream.stop_stream()
    stream.close()
    p.terminate()


def save_recording(recording, config, filename):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(config["channels"])
    wf.setsampwidth(config["sample_size"])
    wf.setframerate(config["rate"])
    wf.writeframes(b''.join(recording))
    wf.close()
