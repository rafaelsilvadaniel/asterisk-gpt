#/var/lib/asterisk/agi-bin/whisper_agi.py 


#!/usr/bin/python3
import sys
import subprocess
import re
import boto3
from pydub import AudioSegment
from openai import OpenAI
from asterisk.agi import AGI

polly_client = boto3.Session( aws_access_key_id='SUAKEY', aws_secret_access_key='SUAACCESSKEY', region_name='us-east-1').client('polly')
#Chave ChatGPT
client = OpenAI(api_key="SUAKEY",)
# Load AGI
agi = AGI()
agi.answer()
arg1_passed = sys.argv[1]
arg2_passed = sys.argv[2]
open("/var/log/whisper_agi.log", "a").write("Inicio do script: " + arg1_passed + " " + arg2_passed + "\n")
audio_file = open("{}".format(arg2_passed), "rb")
transcricao = client.audio.transcriptions.create( model="whisper-1", file=audio_file)
transcrito = transcricao.text
open("/var/log/whisper_agi.log", "a").write("Fala reconhecida:" + transcrito + "\n")
completion = client.chat.completions.create( model = 'gpt-3.5-turbo', messages = [ {'role': 'user', 'content': '{}'.format(transcrito)}], temperature = 0)
resposta = completion.choices[0].message.content
open("/var/log/whisper_agi.log", "a").write("Resposta GPT:" + resposta + "\n")
response = polly_client.synthesize_speech(VoiceId='Thiago', LanguageCode='pt-BR', OutputFormat='mp3', SampleRate='8000',  Text = '{}'.format(resposta), Engine = 'neural')
file = open("/var/lib/asterisk/sounds/tmp/{}.mp3".format(arg1_passed), 'wb')
file.write(response['AudioStream'].read())
file.close()
open("/var/log/whisper_agi.log", "a").write("Vocalizou!"+"\n")
audio = AudioSegment.from_mp3("/var/lib/asterisk/sounds/tmp/{}.mp3".format(arg1_passed))
audio += 15
audio.export("/var/lib/asterisk/sounds/tmp/{}.wav".format(arg1_passed), format="wav")
