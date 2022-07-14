from RedditScraper import Scraper
import ImageCreator
import TextToSpeech
import VideoCreator

#Main method allows user to create a video by entering the posts URL, selecting whether you want the comments or body of the post, and then selecting which comments you want to include in the video (if needed)
def main():
    scraper = Scraper()
    val = 1
    while(val == 1):
        #User input to determine what content to actually put in the video
        url = str(input('Enter url of post you would like to create a video of: '))
        post = scraper.getPostByURL(url)
        typeOfVideo = int(input('Get comments of post [0] or get the body of post [1]? '))
        commentsForVideo = list()
        if(typeOfVideo == 0):
            typeOfComments = int(input('Get best [0] or top [1] comments? '))
            if(typeOfComments == 0):
                post.comments_sort = 'best'
            else:
                post.comments_sort = 'top'
            post.comments.replace_more(limit=0)
            comments = post.comments.list()
            if(len(comments) > 100):
                comments = comments[0:100]
            for i in range(len(comments)):
                print(i,str(comments[i].body))
            print('Enter number next to each comment you would like to have in your post. When you are done enter 999')
            inp = 0
            estimatedDuration = 0.0
            while inp != 999:
                inp = int(input())
                if(inp < len(comments) or inp < 0):
                    commentsForVideo.append(comments[inp])
                    estimatedDuration = estimatedDuration + TextToSpeech.estimateAudioLength(comments[inp].body)
                    print('Comment added! Estimated video duration',estimatedDuration)
                else:
                    print('Number out of range')
        print('Creating post...')
        #Creating images and audio, then making a video out of them
        imageDirs = ImageCreator.createImagesFromSubmission(post, commentsForVideo)
        audioDirs = TextToSpeech.createAudioSnippets(post, commentsForVideo)
        tikTokDir = 'TikToks/' + str(post.subreddit) + '-'+ str(post.id) + '-FINISHED.mp4'
        VideoCreator.createTikTok(imageDirs, audioDirs, tikTokDir)
        print('Post created!')
        val = int(input('Finished? [0] or do you want to create another video? [1]'))

if(__name__ == '__main__'):
    main()