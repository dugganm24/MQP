from gtts import gTTS
import requests
import os
import subprocess
import json

def textToSpeech(text):
    output_folder = "C:/Users/mpduggan/MQP/TextToSpeech/WavGeneration/Output"

    file_path_mp3 = os.path.join(output_folder, "speechOutput.mp3")
    file_path_mp3 = os.path.normpath(file_path_mp3)

    tts = gTTS(text, lang='en')
    tts.save(file_path_mp3)

    file_path_wav = os.path.join(output_folder, "speechOutput.wav")
    file_path_wav = os.path.normpath(file_path_wav)

    ffmpeg_path = "C:/Users/mpduggan/MQP/TextToSpeech/WavGeneration/ffmpeg-master-latest-win64-gpl-shared/ffmpeg-master-latest-win64-gpl-shared/bin/ffmpeg.exe"
    subprocess.run([ffmpeg_path, "-y", "-i", file_path_mp3, file_path_wav])

    return file_path_wav

def sendToAudio2Face(audioPath):
    url = 'http://localhost:8011/A2F/Player/SetTrack'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        "a2f_player": "/World/audio2face/Player",
        "file_name": audioPath,  # Directly use the file path here
        "time_range": [0, -1]
    }

    # Send the request as JSON
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Audio sent to Audio2Face")
    else:
        print(f"Error sending audio to Audio2Face: {response.status_code}, {response.text}")

def main():
    text = "Testing auto overwriting of audio files"

    audioPath = textToSpeech(text)
    sendToAudio2Face(audioPath)

if __name__ == "__main__":
    main()