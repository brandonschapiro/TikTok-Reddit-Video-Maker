import os,random
from PIL import Image, ImageDraw, ImageFont
import TextParser

REDDIT_ICON = Image.open('assets/redditIcon.jpg').resize((56,56))
SUBREDDIT_TITLE_FONT = ImageFont.truetype('verdanab.ttf',22)
POSTED_BY_FONT = ImageFont.truetype('verdanab.ttf',12)
POST_TITLE_FONT = ImageFont.truetype('verdanab.ttf',17)
COMMENT_AUTHOR_FONT = ImageFont.truetype('verdanab.ttf',11)
COMMENT_BODY_FONT = ImageFont.truetype('assets/verdana.ttf',16)

##Char limits per lines
TITLE_LINE_LIMIT = 33
COMMENT_LINE_LIMIT = 45

#Creates title image given the submission object from the reddit API and where to save the image
def createTitleImage(submission, saveDir):
    subredditText = "r/" + str(submission.subreddit)
    authorText = "Posted by u/" + str(submission.author)
    titleText = TextParser.addLineBreaks(str(submission.title), TITLE_LINE_LIMIT)
    #FILTERING OFF
    #titleText = Censor.filterTitleText(titleText)
    #Creates image with height based on number of lines of text
    numLines = 1 + titleText.count('\n')
    imageToSave = Image.new('RGBA',[430,60 + 21*numLines], color=(0,0,0,127))
    #Adds reddit icon and draws text onto image.
    imageToSave.paste(REDDIT_ICON,[10,10])
    d = ImageDraw.Draw(imageToSave)
    d.text([81,0], subredditText, font=SUBREDDIT_TITLE_FONT, fill=(255,255,255))
    d.text([81,27],authorText, font=POSTED_BY_FONT, fill=(255,255,255))
    d.text([81, 43],titleText, font=POST_TITLE_FONT, fill=(255,255,255))
    imageToSave.save(saveDir)
    imageToSave.close()

#Creates comment image with the author and profile icon. Used for the first text fragment of a comment. Text must have linebreaks added to it beforehand.
def createCommentImageWithAuthor(text, author, saveDir):
    numLines = text.count('\n')
    imageToSave = Image.new('RGBA', [406,50 + 27*numLines], color=(0,0,0,127))
    avatar = 'assets/userAvatars/' + random.choice(os.listdir('assets/userAvatars'))
    REDDIT_AVATAR = Image.open(avatar).resize((33,33))
    imageToSave.paste(REDDIT_AVATAR,[10,10])
    d = ImageDraw.Draw(imageToSave)
    d.text([48,10], str(author),font=COMMENT_AUTHOR_FONT,fill=(255,255,255))
    d.text([10, 50], text, font=COMMENT_BODY_FONT, fill=(255,255,255))
    imageToSave.save(saveDir)

#Creates comment images with just the text from the comment. Used for all fragments after the first as well as for the body text of a post. Text must have linebreaks added to it beforehand.
def createContinuedCommentImage(text, saveDir):
    numLines = 1 + text.count('\n')
    imageToSave = Image.new('RGBA', [406, 15 + 18*numLines], color=(0,0,0,127))
    d = ImageDraw.Draw(imageToSave)
    d.text([5,5],text,font=COMMENT_BODY_FONT, fill=(255,255,255))
    imageToSave.save(saveDir)

#Creates all images given a submission object from the reddit api and a list of the comments to put in the video. This function adds the line breaks and fragments the texts so it doesn't need to be done before being passed in.
def createImagesFromSubmission(submission, comments=[])->list():
    #First creates the title image. A list is also created to store the directory of every image that is created.
    imageDirList = list()
    saveDir = 'videoComponents/titles/'+ str(submission.id)+'-TITLEPAGE.png'
    imageDirList.append(saveDir)
    createTitleImage(submission, saveDir)
    #No comments means post is a story, take text from submission, parse it, and create images
    if(len(comments) == 0):
        parsedBody = TextParser.fragmentText(submission.selftext)
        #FILTERING OFF
        #parsedBody = Censor.filterTextForScreen(parsedBody)
        for i in range (len(parsedBody)):
            saveDir = 'videoComponents/comments/' + str(submission.id) + '-COMMENT-1-' + str(i+1) + '.png'
            imageDirList.append(saveDir)
            createContinuedCommentImage(parsedBody[i], saveDir)
    #If there are comments, go through each comment, break it into fragments, create images and add them to the list of directories.
    else:
        for i in range(len(comments)):
            comment = comments[i].body
            parsedComment = TextParser.fragmentText(comment)
            #FILTERING OFF
            #parsedComment = Censor.filterTextForScreen(parsedComment)
            for j in range(len(parsedComment)):
                saveDir = 'videoComponents/comments/' + str(submission.id) + '-COMMENT-' + str(i+1) + '-' + str(j+1) + '.png'
                imageDirList.append(saveDir)
                #If its the first fragment of a comment, create image with author, otherwise just create an image of the text
                if(j == 0):
                    createCommentImageWithAuthor(parsedComment[j], comments[i].author, saveDir)
                else:
                    createContinuedCommentImage(parsedComment[j], saveDir)
    #Returns list of directories to use for later.
    return imageDirList
