import requests
import ollama
from gtts import gTTS

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
    prompt = input(">>> ")

    if prompt == "//bye":
        break
    else:
        response = client.generate(model=model, prompt=prompt)
        # Print the response from the model
        print("Response from Maaya")
        #print(response.response)
        responsetxt = response.response
        break


language = "en"
text = responsetxt

speech = gTTS(
    text = text,
    lang = language,
    slow = False,
    tld = "com.au")

speech.save("ttsoutput.mp3")