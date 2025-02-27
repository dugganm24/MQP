import sys
import os
import time 
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Audio2Face", "EmotionGeneration")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Audio2Face", "SpeechGeneration")))

from textToEmotion import emotionGeneration, sendEmotionToAudio2Face
from textToSpeech import speechGeneration, sendSpeechToAudio2Face, playTrack

async def main():

    text = input("Enter text: ")

    start_time = time.time()

    speech_start_time = time.time()
    audioPath = await speechGeneration(text)
    speech_end_time = time.time()
    print(f"Speech generation time: {speech_end_time - speech_start_time:.2f} seconds")

    emotion_start_time = time.time()
    emotion_weights = await emotionGeneration(text)
    emotion_end_time = time.time()
    print(f"Emotion generation time: {emotion_end_time - emotion_start_time:.2f} seconds")

    send_emotion_start_time = time.time()
    await sendEmotionToAudio2Face(emotion_weights)
    send_emotion_end_time = time.time()
    print(f"Send emotion time: {send_emotion_end_time - send_emotion_start_time:.2f} seconds")

    send_speech_start_time = time.time()
    await sendSpeechToAudio2Face(audioPath)
    send_speech_end_time = time.time()
    print(f"Send speech time: {send_speech_end_time - send_speech_start_time:.2f} seconds")

    play_start_time = time.time()
    await playTrack()
    play_end_time = time.time()
    print(f"Play track time: {play_end_time - play_start_time:.2f} seconds")

    end_time = time.time()
    print(f"Total time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())