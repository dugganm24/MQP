# MQP: AI-Powered 3D Facial Generation for Robotic Interfaces
__Project Overview__  
This project explores the generation of realistic human facial video using 3D Morphable Models (3DMM) and First Order Motion Model (FOMM) and maps these faces onto a 3D surface using Blender. The mapped faces will express emotion and be lip-synced to a speech output using Audio2Face. The primary goal is to assess and enhance the realism of the generated faces when displayed on a flexible LCD screen wrapped around a sphere shaped like a human head. Fréchet Video Distance (FID), CLIP, and SyncNet will be used as metrics in the Stable-Baselines3 reinforcement learning framework to evaluate the realism of the faces throughout the process.

__Project Objectives__    
 - Generate high-quality human facial videos using Audio2Face.  
 - Map these generated faces onto a 3D spherical surface that mimics the shape of a human head using Unreal Engine.  
 - Display the final 3D face on a flexible LCD screen, focusing on realism and adaptability to 3D surfaces.

__Technologies Used__    
 - **Audio2Face**: For generating realistic human faces and syncing facial expressions and lip movements with input audio file.
 - **Google Text-To-Speech**: For converting text into mp3 audio file.
 - **ffmpeg**: For converting gTTS generated mp3 file into wav format for Audio2Face compatibility.
 - **Emotion English DistilRoBERTa-base**: For generating emotion weights based on textual input.
 - **Audio2Face Headless API**: For automatically sending generated audio output and emotion weights to Audio2Face for minimal latency in real time interactions.
 - **Unreal Engine**: For rendering generated emotions and lip-syncing to a MetaHuman for display on LCD. 
 - **NVIDIA GeForce RTX 4090**: NVIDIA GPU to improve processing speeds.

