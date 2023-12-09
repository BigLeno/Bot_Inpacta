#!/bin/bash

# Cria screen "Nome da sua screen"
screen -dmS sua_screen

#Executa o script do loop dentro da screen
screen -S sua_screen -X stuff 'python3 /seu/caminho/para/o/script.py\n'