# MQP: AI-Powered 3D Facial Generation for Robotic Interfaces
__Project Overview__  
This project explores the generation of realistic human facial video using 3D Morphable Models (3DMM) and First Order Motion Model (FOMM) and maps these faces onto a 3D surface using Blender. The mapped faces will express emotion and be lip-synced to a speech output using Audio2Face. The primary goal is to assess and enhance the realism of the generated faces when displayed on a flexible LCD screen wrapped around a sphere shaped like a human head. Fréchet Video Distance (FID), CLIP, and SyncNet will be used as metrics in the Stable-Baselines3 reinforcement learning framework to evaluate the realism of the faces throughout the process.

__Project Objectives__    
 - Generate high-quality human facial videos using Audio2Face.  
 - Map these generated faces onto a 3D spherical surface that mimics the shape of a human head using Blender.  
 - Evaluate the realism of the 3D representation using FVD, CLIP, and SyncNet in Stable-Baselines3.  
 - Display the final 3D face on a flexible LCD screen, focusing on realism and adaptability to 3D surfaces.

__Technologies Used__    
 - **Audio2Face**: For generating realistic human faces and syncing facial expressions and lip movements with input audio file.
 - **Blender**: For mapping faces onto a 3D surface and rendering the final display. 
 - **FVD**: To measure the similarity between generated and real videos.
 - **CLIP**: To measure how well generated faces match expressions based on textual input.
 - **SyncNet**: To measure synchronization of lip movements with speech output.
 - **Stable-Baselines3**: Provides RL framework to optimize model based on chosen metrics.
 - **Flexible LCD screen**: To display the generated 3D face on robotic head.
 - **Ainker PowerConf C200 Webcam**: Used to gather image input for RL feedback loop.
 - **NVIDIA GeForce RTX 4090**: NVIDIA GPU to improve processing speeds.

