import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    #if voice.id == 'brazil' or voice.id == 'portugal':
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-60)
    engine.setProperty('voice', voice.id)
    engine.say("Olá Mundo")
    print(voice.id)
    print(voice.gender)
#engine.say("Bem Vindo Tiago")
engine.runAndWait()