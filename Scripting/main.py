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
from bs4 import BeautifulSoup

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

async def fetch_full_page(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                paragraphs = soup.find_all("p")
                text_content = " ".join(p.get_text() for p in paragraphs[:5])  
                return text_content.strip()
            else:
                return f"(Error {response.status} fetching {url})"
    except Exception as e:
        return f"(Error fetching {url}: {e})"

async def search_serpapi(query, session):
    params = {
        "engine": "google",
        "q": query,
        "api_key": os.environ["SERPAPI_API_KEY"],
    }
    async with session.get("https://serpapi.com/search", params=params) as response:
        if response.status == 200:
            results = await response.json()
            detailed_contexts = []
            snippets = []
            organic_results = results.get("organic_results", [])

            for result in organic_results[:3]:
                if "snippet" in result:
                    snippets.append(result["snippet"])

            for result in organic_results[:3]:
                if "link" in result:
                    page_text = await fetch_full_page(session, result["link"])
                    if not page_text.lower().startswith("(error"):
                        detailed_contexts.append(page_text)

            combined_context = "\n\n".join(detailed_contexts).strip()
            combined_snippets = "\n".join(snippets).strip()

            final_context = ""
            if combined_context:
                final_context += f"Detailed web page content:\n{combined_context}\n\n"
            if combined_snippets:
                final_context += f"Top search snippets:\n{combined_snippets}"

            final_context = final_context.strip()
            return final_context if final_context else "No relevant information found on the web."

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

                    IMPORTANT INSTRUCTION: When the user asks for real-time information such as weather, news, stocks, sports scores, dates, or other current data, you MUST use the web search context provided to you. This context contains the most up-to-date information available. Answer directly with the specific data requested (temperature, price, score, etc.) without hedging or expressing uncertainty when the information is clearly available in the context.
                    
                    Always prioritize clear and direct answers that reflect accurate, real-time details when web context is available. If no web context is provided, answer using general knowledge. Unless the prompt suggests a specific emotional tone, default to a friendly, positive tone. 

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


    response_text = await generate_text(input_text)
    print(f"Response: {response_text}")

    await speechGeneration(response_text)
    emotion_weights = await emotionGeneration(response_text)
    
    await sendEmotionToAudio2Face(emotion_weights)
    await sendSpeechToAudio2Face()

    await playTrack()

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