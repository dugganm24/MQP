import sys
import os
import asyncio
import subprocess 
import requests
from serpapi import GoogleSearch
from dotenv import load_dotenv
import json 
import aiohttp
import time 

load_dotenv()
api_key = os.environ.get("SERPAPI_API_KEY")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Audio2Face", "EmotionGeneration")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Audio2Face", "SpeechGeneration")))

from textToEmotion import emotionGeneration, sendEmotionToAudio2Face, setIdleEmotion
from textToSpeech import speechGeneration, sendSpeechToAudio2Face, playTrack, setIdleAudio, getResponseLength, setLooping

def start_ollama():
    ollama_path = r"C:\Users\mpduggan\AppData\Local\Programs\Ollama\ollama.exe"  

    try:
        process = subprocess.Popen([ollama_path, "run", "llama3.2"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Ollama started successfully.")

        return process
    
    except Exception as e:
        print(f"Error starting Ollama: {e}")
        return None

async def idle_a2f():
    await setIdleAudio()
    await setIdleEmotion()
    await setLooping(True)
    await playTrack()    
    
def needs_web_search(query):
    keywords = ["today", "now", "current", "latest", "news", "who", "weather", "time", "date", "score", "recent", "when", "did", "is it", "what is", "what was", "how many", "how much", "how long", "how far", "how often", "how many"]
    return any(keyword in query.lower() for keyword in keywords)

async def search_serpapi(query, session):
    params = {
        "engine": "google",
        "q": query,
        "api_key": os.environ["SERPAPI_API_KEY"],
    }
    async with session.get("https://serpapi.com/search", params=params) as response:
        if response.status == 200:
            results = await response.json()
            snippets = [res["snippet"] for res in results.get("organic_results", []) if "snippet" in res][:3]
            return "\n".join(snippets)
        else:
            return f"Error: {response.status}, {await response.text()}"
        
async def generate_text(input_text):
    url = "http://localhost:11434/api/generate"  
    headers = {"Content-Type": "application/json"}  

    search_context = ""
    if needs_web_search(input_text):
        async with aiohttp.ClientSession() as session:
            search_context = await search_serpapi(input_text, session)

    search_section = f"Here is relevant web search context:\n{search_context}" if search_context else ""

    system_prompt = f"""You are a language model designed to generate text that will be converted into speech that will be said by a humanoid robot. Your responses should be clear and designed to be spoken aloud. Focus on providing informative and natural-sounding responses. While keeping the speech clear, provide enough details to fully answer the user's question but keep responses as short as possible to minimize latency. Do not include any visual elements, like emojis, in your responses, or texual elements like (pause) that are not intended to be spoken aloud. Feel free to generate responses based on realistic emotions that a human would likely feel when applicable. Default to happy responses unless the prompt or user input suggests otherwise."

                    If a question requires up-to-date information, you can use the following web search context to help answer the question. If the user asks a question that requires up-to-date information, you should use the web search context to help answer the question. If the user asks a question that does not require up-to-date information, you should not use the web search context to help answer the question. 

                    {search_section}
                    """
    
    data = {
        "model": "llama3.2",  
        "prompt": f"{system_prompt}\nUser input: {input_text}\nRobot speech:",
        "temperature": 0.1,
        "stop": ["<end_of_turn>"], 
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            response_json = response.json()
            return response_json.get("response", "No response key found.")
        else:
            return f"Error: {response.status_code}, {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    
async def process_input(input_text):
    
    await setLooping(False)

    start_time = time.time()

    response_text = await generate_text(input_text)
    print(f"Response: {response_text}")

    await speechGeneration(response_text)
    emotion_weights = await emotionGeneration(response_text)
    
    await sendEmotionToAudio2Face(emotion_weights)
    await sendSpeechToAudio2Face()

    await playTrack()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.2f} seconds")

    response_length = await getResponseLength()
    start_of_response = response_length["result"]["default"][0]
    end_of_response = response_length["result"]["default"][1]
    track_duration = end_of_response - start_of_response
    await asyncio.sleep(track_duration)

    await idle_a2f()

async def main():

    ollama_process = start_ollama()
    if ollama_process is None:
        print("Failed to start Ollama.")
        return
    
    await idle_a2f()
            
    while True:
        input_text = input("Enter text: ")
        if input_text.lower() == "exit":
            break
            
        await process_input(input_text)

if __name__ == "__main__":
    asyncio.run(main())