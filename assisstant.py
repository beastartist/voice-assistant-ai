import openai
import pyttsx3
import pygame
import time

# Initialize TTS engine once
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# Initialize pygame mixer once
pygame.mixer.init()

def laugh():
    try:
        pygame.mixer.music.load("laugh.wav")  # Make sure this file exists in your folder
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except Exception as e:
        print(f"Could not play laugh sound: {e}")

# Initialize OpenAI client
client = openai.OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

chat_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

print("Start chatting with your assistant (type 'exit' or 'quit' to stop):")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ['exit', 'quit']:
        print("Goodbye!")
        break

    chat_history.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="mistral-saba-24b",
            messages=chat_history
        )
        reply = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": reply})

        # Speak and print every response
        speak(reply)

        # Play laugh sound if user asked for a joke
        if "joke" in user_input.lower():
            time.sleep(0.5)
            laugh()

    except Exception as e:
        print(f"Error: {e}")
