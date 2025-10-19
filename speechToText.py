# SCRIPT - Speech To Text

import sounddevice as sd
import numpy as np
import queue
import threading
import mlx_whisper
import threading
import time

# Settings 
samplerate = 16000
block_duration = 0.5 # in seconds
chunk_duration = 3 # also in seconds 
channels = 1 

frames_per_block = int(samplerate * block_duration)
frames_per_chunk = int(samplerate * chunk_duration)

stop_event = threading.Event()
audio_queue = queue.Queue()
audio_buffer = []


# code 
def audio_callback(indata, frames, time, status):
    if status:
        pass
    audio_queue.put(indata.copy())

def recorder():
    with sd.InputStream(samplerate=samplerate,
                        channels=channels,
                        callback=audio_callback,
                        blocksize=frames_per_block,
                        latency="low"):
        print("Model is Listening...(running on M4 MPU) ^C to stop")
        while not stop_event.is_set():
            sd.sleep(100)

def transcriber():
    global audio_buffer
    while not stop_event.is_set() or not audio_queue.empty():
        
        try:
            block = audio_queue.get()
        except queue.Empty:
            if stop_event.is_set():
                break
            continue

        audio_buffer.append(block)
        
        total_frames = sum(len(b) for b in audio_buffer)
        if total_frames >= frames_per_chunk:
            audio_data = np.concatenate(audio_buffer)[:frames_per_chunk]
            audio_buffer = []
            audio_data = audio_data.flatten().astype(np.float32)

            result = mlx_whisper.transcribe(
                audio_data,
                path_or_hf_repo="mlx-community/whisper-large-v3-mlx",
                language="en",
            )

            for segment in result["segments"]:
                    text = segment["text"].strip()
                    if text:
                        print(f"[Live] {text}", flush=True)
                        transcribed_texts.append(text)


def start_listening():
    """Start the recorder and transcriber threads for Maaya."""
    global transcribed_texts
    transcribed_texts = []

    stop_event.clear()  # reset in case it was used before

    recorder_thread = threading.Thread(target=recorder, daemon=True)
    transcriber_thread = threading.Thread(target=transcriber, daemon=True)
    
    recorder_thread.start()
    transcriber_thread.start()
    time.sleep(0.5) 

    try:
        while True:
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\n--Recording Paused--")
        stop_event.set()
        recorder_thread.join(timeout=0.2)
        transcriber_thread.join(timeout=6)

    full_text = " ".join(transcribed_texts).strip()
    return full_text 