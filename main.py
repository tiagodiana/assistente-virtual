from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot

from gtts import gTTS
from playsound import playsound
import os
import sys

import speech_recognition as sr 

import pyttsx3

import requests

from face import *

def cria_audio(audio):
    tts = gTTS(audio,lang='pt-br')
    #Salva o arquivo de audio
    tts.save('audios/tmp.mp3')
    #Da play ao audio
    playsound('audios/tmp.mp3')

def previsaoTempo(cidade):
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


bot = ChatBot('Jarvis', read_only=True)
r = sr.Recognizer()

fim = None
response = None

if reconhecimento_facial() ==  None:
    cria_audio(f"Rosto desconhecido")
    cria_audio(f"Encerrando o Sistema")
    sys.exit()

else:
    nome = reconhecimento_facial()
    cria_audio("Bem vindo " + nome)
    cria_audio('No que posso ajudar?')
    while True:
        with sr.Microphone() as s:
            try:
                r.adjust_for_ambient_noise(s)

                audio = r.listen(s)
                speech = r.recognize_google(audio, language='pt-BR')
                previsao = speech.find('previsão do tempo')
                fim = speech.find('Ok obrigado')
                if previsao == 0:
                    cidade = str(speech).split()[-1]
                    response = previsaoTempo(cidade)
                elif fim == 0:
                    response = "De nada, quando precisar é só chamar"
                else:
                    print('Você disse: ', speech)
                    response = bot.get_response(speech)
                    print('Bot: ', response)
            except:
                response = "Ainda não posso processar sua requisição"
            
        cria_audio(str(response))
        if fim == 0:
            sys.exit()

