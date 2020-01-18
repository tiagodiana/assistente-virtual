from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

import os
import speech_recognition as sr 

bot = ChatBot('Floyd',
                logic_adapters=[
                'chatterbot.logic.BestMatch',
                ],
                trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer'
                )

trainer = ChatterBotCorpusTrainer(bot)

trainer.train(
    "chatterbot.corpus.portuguese"
)

#for _file in os.listdir('chats'):
#    lines = open('chats/' + _file, 'r').readlines()
#    trainer.train(lines)