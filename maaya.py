import requests
import ollama
from gtts import gTTS
import edge_tts
import asyncio
import os
import tempfile
import playsound

# STT Script
from speechToText import start_listening

try:
    requests.get("http://localhost:11434/api/tags", timeout=3)
    print("✅ Ollama server is running")
except requests.ConnectionError:
    print("❌ Ollama server is not running")
    exit()

# Initialize the Ollama client
client = ollama.Client()
model = "maaya"

while True:
    # Send the query to the model
    prompt = start_listening()
    print(f"Sending: {prompt}")

    if prompt == "//bye":
        break
    else:
        response = client.generate(model=model, prompt=prompt)
        # Print the response from the model
        print("Response from Maaya")
        #print(response.response)
        responsetxt = response.response
        async def main():
            tts = edge_tts.Communicate(responsetxt, voice="en-IE-EmilyNeural")
    
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                await tts.save(temp_audio.name)
                print("Maaya's Answer: 🔈")
                print(f"Response : {responsetxt}")
                playsound.playsound(temp_audio.name)
                os.remove(temp_audio.name)

        asyncio.run(main())