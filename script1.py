import speech_recognition as sr
import os
import asyncio
import edge_tts
import pygame
import requests
import json
api_key = "key"  # Get it from https://openrouter.ai/

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://your-site.com",
    "X-Title": "VoiceBot-Test"
}
# Function: Convert text to natural-sounding voice (Edge-TTS)
async def speak_with_edge_tts(text_to_speak, filename="output.mp3"):
    communicate = edge_tts.Communicate(text=text_to_speak, voice="en-GB-RyanNeural")
    await communicate.save(filename)

# Function: Play audio using pygame
def play_audio(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # Wait until the audio is done playing
    while pygame.mixer.music.get_busy():
        continue

    pygame.mixer.quit()


def llm(text):
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    response_text = response.json()["choices"][0]["message"]["content"]
    return response_text

# Main script
def main():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("🎤 Speak now (you have up to 10 seconds)...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            print("🔊 Got your voice, processing...")

        try:
            textinput = recognizer.recognize_google(audio)
            output = llm(textinput)
        

            # Convert speech to natural voice using Edge TTS
            asyncio.run(speak_with_edge_tts(output, "output.mp3"))

            # Play audio with pygame
            play_audio("output.mp3")

            # Delete the file after playing
            os.remove("output.mp3")
            print("🗑️ Deleted output.mp3")

        except sr.UnknownValueError:
            print("🤔 Sorry, could not understand the audio.")
        except sr.RequestError as e:
            print(f"⚠️ Could not request results from Google; {e}")
        except Exception as ex:
            print(f"🚫 Error: {ex}")

if __name__ == "__main__":
    main()
