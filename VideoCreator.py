from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, AudioFileClip
import os,random


#Creates a video given a list of images and audio files. Each images corresponding audio file must be in the same index as the image for this function to work.
def createTikTok(imageDirs, audioDirs, tikTokDir):
    if(len(imageDirs) == len(audioDirs)):
        imageList = list()
        videoDuration = 0.0
        #Attaches each audio file to its corresponding image and saves it to a list. Also gets the length of the video.
        for i in range(len(imageDirs)):
            image = ImageClip(imageDirs[i]).set_start(videoDuration)
            audio = AudioFileClip(audioDirs[i]).set_start(videoDuration)
            image = image.set_duration(audio.duration).set_audio(audio).set_position(('center', 330))
            videoDuration = videoDuration + audio.duration
            imageList.append(image)
        #Gets random background video and clips a random section of that video
        bgDir = 'assets/backgroundVideos/' + random.choice(os.listdir('assets/backgroundVideos'))
        backgroundVideo = VideoFileClip(bgDir).without_audio()
        startTime = random.randint(0,int(backgroundVideo.duration-videoDuration-5))
        backgroundVideo = backgroundVideo.subclip(startTime, startTime + videoDuration + 1)
        #Adds background video to list of images, combines them all into one clip, and saves the video.
        imageList.insert(0, backgroundVideo)
        video = CompositeVideoClip(imageList)
        video.write_videofile(tikTokDir)
    else:
        print('error, number of images != number of audio files')
