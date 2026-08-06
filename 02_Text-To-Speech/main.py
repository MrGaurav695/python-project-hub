from gtts import gTTS

print("===== Text to Speech Converter =====")

text = input("Enter the text: ")
language = input("Enter language code (default: en): ").strip()

if language == "":
    language = "en"

filename = input("Enter output file name (without .mp3): ").strip()

if filename == "":
    filename = "output"

tts = gTTS(text=text, lang=language)
tts.save(f"{filename}.mp3")

print(f"Audio saved as {filename}.mp3")