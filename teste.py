# Imports library
from chatterbot import *
import pyttsx3
from gtts import gTTS
from playsound import playsound
import os
import sys
import speech_recognition as sr 
import requests
import face
from googlesearch import search

class Main():
    def __init__(self):
        self.bot = ChatBot('Floyd',
                            logic_adapters=[
                            'chatterbot.logic.BestMatch',
                            ],
                            trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer'
                            )
        self.r = sr.Recognizer()
        if face.reconhecimento_facial() ==  None:
            self.cria_audio("Rosto desconhecido")
            print("Floyd: Rosto desconhecido")
            self.cria_audio("Encerrando o Sistema")
            print("Floyd: Encerrando o sistema")
            sys.exit()
        else:
            nome = face.reconhecimento_facial()
            self.cria_audio("Bem vindo " + str(nome))
            print(f"Floyd: Bem vindo {nome}")
            self.cria_audio('No que posso ajudar?')
            print("Floyd: No que posso ajudar?")
            while True:
                self.response = "Estou pronto para ajudar"
                print("Floyd: Estou pronto para ajudar")
                self.ouvir()
                self.dict_action = {'previsão do tempo': self.previsaoTempo(self.speech),'notícias':self.news(), 'ok obrigado': sys.exit()}
                self.action = None
                if self.speech in self.dict_action:
                    self.action = self.action
                self.dict_action[self.action]
                 
    

    # FUNCTION OUVIR AUDIO 
    def ouvir(self):
        with sr.Microphone() as s:
            self.r.adjust_for_ambient_noise(s)
            self.audio = self.r.listen(s)
            self.speech = self.r.recognize_google(self.audio, language='pt-BR')
               
    # FUNCTION AUDIO CREATE
    def cria_audio(self,audio):
        # ---------------------------- pyttsx AUDIO MALE
        engine = pyttsx3.init('espeak')
        voices = engine.getProperty('voices')
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate-60)
        for voice in voices:
            if voice.name == 'brazil':
                engine.setProperty('voice', voice.id)
        engine.say(audio)
        engine.runAndWait()
        engine.stop()
        # -----------------------------
        # ----------------------------- gTTS AUDIO FEMALE
        #if audio != '':
        #    tts = gTTS(audio,lang='pt-br')
        #else:
        #    tts = gTTS('Não entendi o que você disse!',lang='pt-br')
        #    print("Floyd: Não entendi o que vocẽ disse!")
        #Salva o arquivo de audio
        #tts.save('audios/tmp.mp3')
        #Da play ao audio
        #playsound('audios/tmp.mp3')    
        #os.remove('audios/tmp.mp3')    
    #API WEATHER
    def previsaoTempo(self):
        try:
            cidade = str(self.speech).split()[-1]
            self.cria_audio('Buscando previsão do tempo para ' + cidade)
            print(f"Floyd: Buscando a previsão do tempo para {cidade}")
            self.response = self.previsaoTempo(cidade)
            url = 'https://api.hgbrasil.com/weather'
            key = '0418e7f0'
            fields= "only_results,temp,city_name,forecast,max,min,date"
            data = {'key':key,'fields': fields,'city_name': cidade}
            req = requests.get(url, data=data, timeout=3000)
            json = req.json()
            print(f"Cidade:{json['city_name']}")
            print(f"Temperatura:{json['temp']}")
            print(f"Data:{json['forecast'][0]['date']}")
            print(f"Min:{json['forecast'][0]['min']}")
            print(f"Max:{json['forecast'][0]['max']}")
            result_audio = f"Temperatura para {json['city_name']} é, {json['temp']} graus, com mínima de {json['forecast'][0]['min']} e máxima de {json['forecast'][0]['max']}"
            return result_audio
        except:
            return "Não foi possivel obter a previsão do tempo tente mais tarde"
    # API NEWS
    def news(self):
        url = ('https://newsapi.org/v2/top-headlines?'
        'country=br&'
        'apiKey=05d5ce74721c41698d58009213297db9')
        req = requests.get(url, timeout=3000)
        json = req.json()
        # PERCORRENDO AS 10 PRIMEIRAS NOTÍCIAS
        for c in range(10):
            print('Notícia ' + str(c + 1))
            self.cria_audio('Notícia ' +  str(c + 1))
            print(json['articles'][c]['title'])
            self.cria_audio(json['articles'][c]['title'])
            print(json['articles'][c]['description'])  
            self.cria_audio(json['articles'][c]['description'])  
            if c == 9:
                self.cria_audio('Fim das noticias, deseja algo mais?')
    
    def pesquisar(self):
        self.cria_audio("Diga o que deseja pesquisar")
        print("Floyd: Diga o que deseja pesquisar")
        self.ouvir()
        pesq = search(self.speech, stop=2)
        for c in pesq:
            os.system(f'xdg-open {c}')
        self.cria_audio("Pesquisa finalizada")
        print("Floyd: Pesquisa finalizada ")
        self.cria_audio("Deseja mais alguma coisa?")
        print('Deseja mais alguma coisa?')

if __name__ == '__main__':
    inicio = Main()