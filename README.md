# MQP: AI-Powered 3D Facial Generation for Robotic Interfaces
__Project Overview__  
This project focuses on generating realistic human facial video and mapping it onto a 3D surface to create expressive, lip-synced animations. Using Audio2Face, the system synchronizes facial movements with speech while incorporating emotion-based animations for enhanced realism. The final output is displayed on a flexible LCD screen wrapped around a sphere, mimicking a human head. By leveraging real-time processing and AI-driven facial animation, this project aims to achieve natural-looking expressions and speech synchronization, enabling more lifelike and interactive robotic displays.

__Project Objectives__    
 - Generate high-quality human facial videos using Audio2Face.  
 - Map these generated faces onto a 3D spherical surface that mimics the shape of a human head using Unreal Engine.  
 - Display the final 3D face on a flexible LCD screen, focusing on realism and adaptability to 3D surfaces.

__Technologies Used__    
 - **NVIDIA Audio2Face**: For generating realistic human faces and syncing facial expressions and lip movements with input audio file.
 - **Google Text-To-Speech**: For converting text into mp3 audio file.
 - **ffmpeg**: For converting gTTS generated mp3 file into wav format for Audio2Face compatibility.
 - **Emotion English DistilRoBERTa-base**: For generating emotion weights based on textual input.
 - **Audio2Face Headless API**: For automatically sending generated audio output and emotion weights to Audio2Face for minimal latency in real time interactions.
 - **Unreal Engine**: For rendering generated emotions and lip-syncing to a MetaHuman for display on LCD. 
 - **NVIDIA GeForce RTX 4090**: NVIDIA GPU to improve processing speeds.

