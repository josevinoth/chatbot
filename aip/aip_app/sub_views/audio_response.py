from gtts import gTTS


def generate_audio_response(text):
    tts = gTTS(text=text, lang='en')
    file_path = "response.mp3"
    tts.save(file_path)
    return file_path