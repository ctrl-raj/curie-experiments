import requests
import ollama
import edge_tts
import asyncio
import tempfile
from playsound import playsound
import os

try:
    requests.get("http://localhost:11434/api/tags", timeout=3)
    print("✅ Ollama server is running")
except requests.ConnectionError:
    print("❌ Ollama server is not running")
    exit()

# Initialize the Ollama client
client = ollama.Client()

# Define the model and the input prompt
model = "curie"  # Replace with your model name
print("Curie is a CLOWN!!")

while True:
    # Send the query to the model
    prompt = input(">>> ")

    if prompt == "//bye":
        break
    else:
        response = client.generate(model=model, prompt=prompt)
        print("--Curie Responded--")
        responsetxt = response.response

        async def main():
            tts = edge_tts.Communicate(responsetxt, voice="en-GB-SoniaNeural")
    
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                await tts.save(temp_audio.name)
                print("Cruie's Answer: 🔈")
                playsound(temp_audio.name)
                os.remove(temp_audio.name)

        asyncio.run(main())
        print(f"Response : {responsetxt}")
