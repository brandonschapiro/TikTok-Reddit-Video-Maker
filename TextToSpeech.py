import pyttsx3
import TextParser

WORDS_PER_MINUTE = 200.0

#Creates title audio from text string
def createTitleAudio(text, saveDir):
    engine = pyttsx3.init()
    engine.setProperty('rate', WORDS_PER_MINUTE)
    text = str(text)
    engine.save_to_file(text, saveDir)
    engine.runAndWait()

#Creates comment audio from text string. Removes newline escape characters as it caused slight pauses in the TTS.
def createCommentAudio(text, saveDir):
    engine = pyttsx3.init()
    engine.setProperty('rate', WORDS_PER_MINUTE)
    text = str(text)
    text = text.replace('\n', '')
    engine.save_to_file(text, saveDir)
    engine.runAndWait()

#Given a submission and comments, creates all audio files for the video.
def createAudioSnippets(submission, comments=[])->list:
    audioDirList = list()
    saveDir = 'videoComponents/audio/titles/' + str(submission.id) + "-AUDIO.mp3"
    audioDirList.append(saveDir)
    #FILTERING OFF
    #filteredText = Censor.filterTextForAudio(str(submission.title))
    createTitleAudio(str(submission.title), saveDir)
    #If there are no comments, just create audio files of the submission body.
    if(len(comments) == 0):
        parsedBody = TextParser.fragmentText(submission.selftext)
        #FILTERING OFF
        #parsedBody = Censor.filterTextForAudio(parsedBody)
        for i in range(len(parsedBody)):
            saveDir = 'videoComponents/audio/comments/' + str(submission.id) + '-AUDIO-1-' + str(i+1) + '.mp3'
            audioDirList.append(saveDir)
            createCommentAudio(parsedBody[i],saveDir)
    else:
        #Fragment comments and create audio files for each one.
        for i in range(len(comments)):
            comment = comments[i].body
            parsedComment = TextParser.fragmentText(comment)
            #FILTERING OFF
            #parsedComment = Censor.filterTextForAudio(parsedComment)
            for j in range(len(parsedComment)):
                saveDir = 'videoComponents/audio/comments/' + str(submission.id) + '-AUDIO-' + str(i+1) +'-' + str(j+1) + '.mp3'
                audioDirList.append(saveDir)
                createCommentAudio(parsedComment[j], saveDir)
    #Returns the list of audio file directories.
    return audioDirList

#Function to estimate the length of an audio file given the text. Used to estimate length of video when the user chooses the comments they would like to add.
def estimateAudioLength(text):
    text = str(text)
    numWords = text.count(' ')
    return float((numWords / WORDS_PER_MINUTE))
