import requests
import ollama
from gtts import gTTS
import edge_tts
import asyncio
import os
import tempfile
import playsound

try:
    requests.get("http://localhost:11434/api/tags", timeout=3)
    print("✅ Ollama server is running")
except requests.ConnectionError:
    print("❌ Ollama server is not running")
    exit()

# Initialize the Ollama client
client = ollama.Client()

# Define the model and the input prompt
model = "maaya"  # Replace with your model name

while True:
    # Send the query to the model
    prompt = input("Talk with Maaya: ")

    if prompt == "//bye":
        break
    else:
        response = client.generate(model=model, prompt=prompt)
        # Print the response from the model
        print("Response from Maaya")
        #print(response.response)
        responsetxt = response.response
        async def main():
            tts = edge_tts.Communicate(responsetxt, voice="en-GB-SoniaNeural")
    
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                await tts.save(temp_audio.name)
                print("Cruie's Answer: 🔈")
                print(f"Response : {responsetxt}")
                playsound.playsound(temp_audio.name)
                os.remove(temp_audio.name)

        asyncio.run(main())


language = "en"
text = responsetxt

speech = gTTS(
    text = text,
    lang = language,
    slow = False,
    tld = "com.au")

speech.save("ttsoutput.mp3")