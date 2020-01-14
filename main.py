# Imports library
from chatterbot import ChatBot
from gtts import gTTS
from playsound import playsound
import os
import sys
import speech_recognition as sr 
import requests
import face

class Main():
    def __init__(self):
        self.bot = ChatBot('Jarvis', read_only=True)
        self.r = sr.Recognizer()
        self.fim = None
        self.response = None
        if face.reconhecimento_facial() ==  None:
            self.cria_audio(f"Rosto desconhecido")
            self.cria_audio(f"Encerrando o Sistema")
            sys.exit()

        else:
            nome = face.reconhecimento_facial()
            self.cria_audio("Bem vindo " + nome)
            self.cria_audio('No que posso ajudar?')
            while True:
                with sr.Microphone() as s:
                    self.r.adjust_for_ambient_noise(s)
                    try:
                        self.audio = self.r.listen(s)
                        self.speech = self.r.recognize_google(self.audio, language='pt-BR')
                    except EnvironmentError:
                        self.response = "Ainda não posso processar sua requisição"
                        print(EnvironmentError)
                previsao = self.speech.find('previsão do tempo')
                noticias = self.speech.find('notícias')
                self.fim = self.speech.find('Ok obrigado')
                if previsao == 0:
                    cidade = str(self.speech).split()[-1]
                    self.cria_audio('Buscando previsão do tempo para ' + cidade)
                    self.response = self.previsaoTempo(cidade)
                elif noticias == 0:
                    self.cria_audio('Buscando as notícias')
                    self.news()
                elif self.fim == 0:
                    self.response = "De nada, quando precisar é só chamar"
                else:
                    print('Você disse: ', self.speech)
                    self.response = self.bot.get_response(self.speech)
                    print('Bot: ', self.response)
                
                self.cria_audio(str(self.response))
                if self.fim == 0:
                    sys.exit()
    def cria_audio(self,audio):
        if audio != '':
            tts = gTTS(audio,lang='pt-br')
        else:
            tts = gTTS('Não entendi o que você disse!',lang='pt-br')
        #Salva o arquivo de audio
        tts.save('audios/tmp.mp3')
        #Da play ao audio
        playsound('audios/tmp.mp3')
        
    #API WEATHER
    def previsaoTempo(self,cidade):
        try:
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

        for c in range(10):
            self.cria_audio('Notícia ' +  str(c + 1))
            self.cria_audio(json['articles'][c]['title'])
            self.cria_audio(json['articles'][c]['description'])    
            if c == 9:
                self.cria_audio('Fim das noticias, deseja algo mais?')

if __name__ == '__main__':
    inicio = Main()