import requests
import ollama
import edge_tts
import asyncio
import os
import tempfile
import playsound

# for response cleaning
import re 
import emoji

def clear_text(text: str):
    text = emoji.replace_emoji(text, replace='')
    text = re.sub(r'[*_~`#]+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text

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

    if "slash" in prompt:
        print("Breaking...")
        break
    else:
        response = client.generate(model=model, prompt=prompt)

        print("Response from Maaya")
        
        responsetxt = response.response
        responsetxt = clear_text(responsetxt)

        async def main():
            tts = edge_tts.Communicate(responsetxt, voice="en-IE-EmilyNeural")
    
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                await tts.save(temp_audio.name)
                print("Maaya's Answer: 🔈")
                print(f"Response : {responsetxt}")
                playsound.playsound(temp_audio.name)
                os.remove(temp_audio.name)

        asyncio.run(main())