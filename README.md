# MQP: AI-Powered 3D Facial Generation for Robotic Interfaces
## Project Overview 
This project focuses on generating realistic human facial video and mapping it onto a 3D surface to create expressive, lip-synced animations. Using Audio2Face, the system synchronizes facial movements with speech while incorporating emotion-based animations for enhanced realism. The final output is displayed on a flexible LCD screen wrapped around a sphere, mimicking a human head. By leveraging real-time processing and AI-driven facial animation, this project aims to achieve natural-looking expressions and speech synchronization, enabling more lifelike and interactive robotic displays.

### Project Objectives
 - Generate high-quality human facial videos using Audio2Face.  
 - Map these generated faces onto a 3D spherical surface that mimics the shape of a human head using Unreal Engine.  
 - Display the final 3D face on a flexible LCD screen, focusing on realism and adaptability to 3D surfaces.

### Technologies Used
 - **NVIDIA Audio2Face**: For generating realistic human faces and syncing facial expressions and lip movements with input audio file.
 - **llama3.2**: For generating realistic response based on textual input, run locally through Ollama. 
 - **pyttsx3**: For converting generated text response into wav audio file for Audio2Face integration.
 - **Emotion English DistilRoBERTa-base**: For generating emotion weights based on textual input.
 - **Audio2Face Headless API**: For automatically sending generated audio output and emotion weights to Audio2Face for minimal latency in real time interactions.
 - **Unreal Engine**: For rendering generated emotions and lip-syncing to a MetaHuman for display on LCD through NVIDIA StreamLivelink plugin. 
 - **NVIDIA GeForce RTX 4090**: NVIDIA GPU to improve processing speeds.

 ### Steps to Run
 1. Open NVIDIA Omniverse, launch Audio2Face and open the Metahuman_Streaming USD file
 2. Activate the StreamLivelink plugin in Audio2Face
 3. Open Epic Games Launcher and launch Unreal Engine 5.3
 4. Open the Metahuman_Streaming Unreal Engine project (C: > This PC > Epic Games > UE_5.3 > Unreal Projects > MyProject2 5.3)
 5. Navigate to virtual production under settings and activate the StreamLivelink plugin preset
 6. Launch the PIE simulator in Unreal Engine to project the face in a separate window which can be displayed on the OLED display 
 7. Navigate to Scripting directory of this project and run the main file 
 8. Enter input text and interact with the system 


