import pyaudiowpatch as pyaudio
import wave
import struct
import math
import matplotlib.pyplot as plt

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SAMPLE_SIZE = 2

def rms( data ):
    count = len(data)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, data )
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0/32768)
        sum_squares += n*n
    return math.sqrt( sum_squares / count )

def get_recording(num_seconds, use_speakers=False):
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
        channels=default_speakers["maxInputChannels"]
        rate=int(default_speakers["defaultSampleRate"])
        input_device_index=default_speakers["index"]
    else:
        channels=CHANNELS
        rate=RATE
        input_device_index=0


    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=rate,   
                    input_device_index=input_device_index,
                    frames_per_buffer=pyaudio.get_sample_size(FORMAT),
                    input=True)

    print(f"recording for {num_seconds} seconds")

    frames = []

    decay = 0.1
    power_sum = 0.0
    power_series = []
    for _ in range(0, int(RATE / CHUNK * num_seconds)):
        data = stream.read(CHUNK)
        power_sum = (1.0 - decay) * power_sum + decay * rms(data)
        power_series.append(power_sum)
        frames.append(data)
    plt.plot(power_series)
    plt.show()

    print("done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()
    assert SAMPLE_SIZE == p.get_sample_size(FORMAT)

    return frames, {"rate":rate, "channels":channels, "sample_size":p.get_sample_size(FORMAT)}


def save_recording(recording, config, filename):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(config["channels"])
    wf.setsampwidth(config["sample_size"])
    wf.setframerate(config["rate"])
    wf.writeframes(b''.join(recording))
    wf.close()


if __name__ == "__main__":
    recording, config = get_recording(5, False)
    save_recording(recording, config, "test.wav")