import pyttsx3

engine = pyttsx3.init('espeak')
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-50)
for voice in voices:
    if voice.name == 'brazil':
        engine.setProperty('voice', voice.id)
        engine.setProperty('age', 100)
#engine.setProperty('voice', 'brazil')
#engine.setProperty('voice', voices[0].id)
#for voice in voices:
    #if voice.id == 'brazil' or voice.id == 'portugal':
#    rate = engine.getProperty('rate')
#    engine.setProperty('rate', rate-60)
#    engine.setProperty('voice', voice.id)
#    engine.say("Olá Mundo")
#    print(voice.id)
#    print(voice.gender)


engine.say("Bem Vindo Tiago")
engine.say("No que posso ajudar?")
engine.runAndWait()