import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if voice.name == 'brazil':
        engine.setProperty('voice', voice.id)
rate = engine.getProperty('rate')
engine.setProperty('voices', voices)
engine.setProperty('rate', rate-50)
engine.say("Tudo bem?")
engine.runAndWait()