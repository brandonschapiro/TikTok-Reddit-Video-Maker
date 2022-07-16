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
            #Clip end of audio if next audio clip is part of the same comment / post. Makes reading comments with multiple fragments less choppy
            if(i + 1 == len(imageDirs)):
                hasAnotherSection = False
            else:
                hasAnotherSection = not audioDirs[i+1].endswith('1.mp3')
            if(hasAnotherSection):
                audio = audio.subclip(0,-0.7)
            image = image.set_duration(audio.duration).set_audio(audio).set_position(('center', 330))
            videoDuration = videoDuration + audio.duration
            imageList.append(image)
        #Gets random background video and clips a random section of that video
        bgDir = 'assets/backgroundVideos/' + random.choice(os.listdir('assets/backgroundVideos'))
        backgroundVideo = VideoFileClip(bgDir).without_audio()
        startTime = random.randint(15,int(backgroundVideo.duration-videoDuration-5))
        backgroundVideo = backgroundVideo.subclip(startTime, startTime + videoDuration + 1)
        #Adds ending image telling user to like and follow
        endingImage = ImageClip('assets/endingImage.png')
        endingImage = endingImage.set_duration(3).set_start(backgroundVideo.duration-3).set_position(('center', 600)).crossfadein(1.5)
        imageList.append(endingImage)
        #Adds background video to list of images, combines them all into one clip, and saves the video.
        imageList.insert(0, backgroundVideo)
        video = CompositeVideoClip(imageList)
        video.write_videofile(tikTokDir)
    else:
        print('error, number of images != number of audio files')
