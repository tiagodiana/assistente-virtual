# Imports library
from chatterbot import *
import pyttsx3
from gtts import gTTS
from playsound import playsound
import os
import sys
import speech_recognition as sr 
import requests
from images.face import reconhecimento_facial
from googlesearch import search
from datetime import datetime
import webbrowser



class Main():
    response = ""
    speech = ""
    def __init__(self):
        # Dicionario com acões
        self.dict_brain = {'Que horas são': self.hora, 'previsão do tempo': self.previsaoTempo,'notícias do dia': self.news, 'pesquisar':self.pesquisar, 'Ok obrigado': self.fim, 'Que dia é hoje': self.data}
        
        # Criando Chatbot
        self.bot = ChatBot('Floyd',
                            logic_adapters=[
                            'chatterbot.logic.BestMatch',
                            ],
                            trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer'
                            )
        self.r = sr.Recognizer()
        if reconhecimento_facial() ==  None:
            print("Floyd: Rosto desconhecido")
            self.cria_audio("Rosto desconhecido")
            print("Floyd: Encerrando o sistema")
            self.cria_audio("Encerrando o Sistema")
            sys.exit()
        else:
            nome = reconhecimento_facial()
            print(f"Floyd: Bem vindo {nome}")
            self.cria_audio("Bem vindo " + str(nome))
            print("Floyd: No que posso ajudar?")
            self.cria_audio('No que posso ajudar?')
            self.status = True
            self.principal()
            
                
    def principal(self):
        while self.status:
            self.response = ""
            self.ouvir()
            self.status = False
            for c in self.dict_brain:
                if self.speech.find(c) == 0:
                    self.dict_brain[c](self.speech)
                    self.status = True
                    break
            if not self.status:
                print('Você disse: ', self.speech.capitalize())
                self.response = self.bot.get_response(self.speech.capitalize())
                if float(self.response.confidence) > 0.3:
                    self.response = str(self.response)    
                else:
                    self.response = 'Não posso responder ainda'
                print('Floyd: ', self.response)  
                self.status = True 
            self.cria_audio(str(self.response))
    # FUNCTION OUVIR AUDIO 
    def ouvir(self):
        with sr.Microphone() as s:
            try:
                self.r.adjust_for_ambient_noise(s)
                self.audio = self.r.listen(s)
                self.speech = self.r.recognize_google(self.audio, language='pt-BR')
            except sr.UnknownValueError:
                self.cria_audio("Não ouvi o que você disse")
                self.ouvir()
    # FUNCTION AUDIO CREATE
    def cria_audio(self,audio):
        # ---------------------------- pyttsx AUDIO MALE
        try:
            engine = pyttsx3.init('sapi5')
        except:
            engine = pyttsx3.init('espeak')
        voices = engine.getProperty('voices')
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate-50)
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
    
    # DATA
    def data(self,frase):
        mes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        d = datetime.now().strftime("%d ")
        m = int(datetime.now().strftime('%m'))
        m = mes[m -1]
        a =  datetime.now().strftime("%Y")
        print(f"{d} de {m} de {a}")
        data = f"{d} de {m} de {a}"
        self.cria_audio(data)

    # HORA
    def hora(self, frase):
        h = datetime.now().strftime("%H:%M")
        print(f"Floyd: Agora são {h}")
        self.cria_audio('Agora são ' + h)
        self.principal()
    #API WEATHER
    def previsaoTempo(self,frase):
        result_audio = ''
        try:
            cidade = str(self.speech).split()[-1]
            print(f"Floyd: Buscando a previsão do tempo para {cidade}")
            self.cria_audio('Buscando previsão do tempo para ' + cidade)
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
        except:
            result_audio = "Não foi possivel obter a previsão do tempo tente mais tarde"
        self.cria_audio(result_audio)
        self.principal()


    # API NEWS
    def news(self, frase):
        print("Floyd: Buscando as notícias do dia")
        self.cria_audio("Buscando as notícias do dia")
        url = ('https://newsapi.org/v2/top-headlines?'
        'country=br&'
        'apiKey=05d5ce74721c41698d58009213297db9')
        req = requests.get(url, timeout=3000)
        json = req.json()
        # PERCORRENDO AS 10 PRIMEIRAS NOTÍCIAS
        for c in range(1):
            print('Notícia ' + str(c + 1))
            self.cria_audio('Notícia ' +  str(c + 1))
            print(json['articles'][c]['title'])
            self.cria_audio(json['articles'][c]['title'])
            print(json['articles'][c]['description'])  
            self.cria_audio(json['articles'][c]['description'])  
            if c == 0:
                self.cria_audio('Fim das noticias, deseja algo mais?')
        self.principal()
    
    def pesquisar(self, frase):
        print("Floyd: Diga o que deseja pesquisar")
        self.cria_audio("Diga o que deseja pesquisar")
        self.ouvir()
        p = search(self.speech, stop=2)
        print("Floyd: Iniciando pesquisa")
        self.cria_audio("Iniciando pesquisa")
        tmp = ''
        for c in p:
            webbrowser.open(c)
        os.system(tmp)
        print("Floyd: Pesquisa finalizada ")
        self.cria_audio("Pesquisa finalizada")
        print('Deseja mais alguma coisa?')
        self.cria_audio("Deseja mais alguma coisa?")
        self.principal()

    def fim(self, frase):
        print("Floyd: De nada quando precisar é só chamar")
        self.cria_audio("De nada, quando precisar é só chamar")
        sys.exit()

if __name__ == '__main__':
    inicio = Main()
