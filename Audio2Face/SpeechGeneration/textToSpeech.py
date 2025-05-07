import pyttsx3
import requests
import os
import subprocess
import json
import aiohttp
import asyncio

# Function to generate speech from text using pyttsx3
async def speechGeneration(text):
    output_folder = "C:/Users/mpduggan/MQP/Audio2Face/SpeechGeneration/Output"

    file_path_wav = os.path.join(output_folder, "speechOutput.wav")
    file_path_wav = os.path.normpath(file_path_wav)

    def generate_speech(): 
        engine = pyttsx3.init()

        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 150)

        engine.save_to_file(text, file_path_wav)
        engine.runAndWait()
    
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, generate_speech)
    return file_path_wav

# Function to send the generated speech to Audio2Face
async def sendSpeechToAudio2Face():

    audioPath = "speechOutput.wav"
    url = 'http://localhost:8011/A2F/Player/SetTrack'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        "a2f_player": "/World/audio2face/Player",
        "file_name": "speechOutput.wav", 
        "time_range": [0, -1]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(data)) as response:
            return response.status

# Function to set the audio track to silent when waiting for new response      
async def setIdleAudio():

    silentPath = "C:/Users/mpduggan/MQP/Audio2Face/SpeechGeneration/Output/silent.wav"
    url = 'http://localhost:8011/A2F/Player/SetTrack'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        "a2f_player": "/World/audio2face/Player",
        "file_name": silentPath, 
        "time_range": [0, -1]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(data)) as response:
           return response.status

# Function to get the length of the audio track
async def getResponseLength():
    url = 'http://localhost:8011/A2F/Player/GetRange'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        "a2f_player": "/World/audio2face/Player",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(data)) as response:
            if response.status == 200:
                response_json = await response.json()
                return response_json
            else:
                return None

# Function to play the audio track
async def playTrack():
    url = 'http://localhost:8011/A2F/Player/Play'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        "a2f_player": "/World/audio2face/Player",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(data)) as response:
           return response.status

# Function to stop the audio track
async def setLooping(loop_audio: bool = False):
    url = 'http://localhost:8011/A2F/Player/SetLooping'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        "a2f_player": "/World/audio2face/Player",
        "loop_audio": loop_audio
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(data)) as response:
            return response.status