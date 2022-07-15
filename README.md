# TikTok-Reddit-Video-Maker
TikTok-Reddit-Video-Maker is a program that allows for the fast creation of Reddit post videos. [Example (not from program)](https://www.youtube.com/watch?v=WMld-HUEIcM).

The creation of these videos follow the same process everytime.

1. Take screenshots of the post and comments.

2. Run all the text through a text to speech program and save all the audio files.

3. Match up all of the photos and audio files, then add a background video.

This program automates the process and minimizes the amount of time it makes to create videos like these. Using this program, a Reddit post video can be
created in just a couple minutes!

However, instead of taking screenshots, this program takes in 
the text from the post / comments and generates its own image. This is why the videos created look slightly different.

[Example from the program.](https://www.youtube.com/shorts/bzE6PqjnR1U)

**Technologies Used**

[**praw**](https://github.com/praw-dev/praw): An API wrapper used to access Reddit's API to retrieve posts and comments.

[**Python Imaging Libray**](https://github.com/python-pillow/Pillow): An imaging library used to create the images.

[**pyttsx3**](https://github.com/nateshmbhat/pyttsx3): A text to speech library used to create the audio files.

[**moviepy**](https://github.com/Zulko/moviepy): A video editing library used to put the images, audio, and background video together.
