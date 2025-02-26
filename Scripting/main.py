import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Audio2Face", "EmotionGeneration")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Audio2Face", "SpeechGeneration")))

from textToEmotion import emotionGeneration, sendEmotionToAudio2Face
from textToSpeech import speechGeneration, sendSpeechToAudio2Face, playTrack

def main():
    text = "I am happy because I received good news today, and everything seems to be going well in my life right now."

    audioPath = speechGeneration(text)
    emotion_weights = emotionGeneration(text)

    sendEmotionToAudio2Face(emotion_weights)
    sendSpeechToAudio2Face(audioPath)

    sendEmotionToAudio2Face(emotion_weights)
    playTrack()

    print("Done")

if __name__ == "__main__":
    main()
