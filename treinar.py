from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot


import os
import speech_recognition as sr 

bot = ChatBot('Jarvis')

trainer = ListTrainer(bot)

for _file in os.listdir('chats'):
    lines = open('chats/' + _file, 'r').readlines()

    trainer.train(lines)