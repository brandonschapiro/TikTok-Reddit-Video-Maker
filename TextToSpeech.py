from dataclasses import replace
import pyttsx3
import TextParser

WORDS_PER_MINUTE = 200.0

#Creates title audio from text string
def createTitleAudio(text, saveDir):
    engine = pyttsx3.init()
    engine.setProperty('rate', WORDS_PER_MINUTE)
    text = str(text)
    text = replaceAcronyms(text)
    engine.save_to_file(text, saveDir)
    engine.runAndWait()

#Creates comment audio from text string. Removes newline escape characters as it caused slight pauses in the TTS.
def createCommentAudio(text, saveDir):
    engine = pyttsx3.init()
    engine.setProperty('rate', WORDS_PER_MINUTE)
    text = str(text)
    text = text.replace('\n', ' ')
    text = replaceAcronyms(text)
    engine.save_to_file(text, saveDir)
    engine.runAndWait()

#Given a submission and comments, creates all audio files for the video.
def createAudioSnippets(submission:object, comments=[])->list:
    audioDirList = list()
    saveDir = 'videoComponents/audio/titles/' + str(submission.id) + "-AUDIO.mp3"
    audioDirList.append(saveDir)
    #FILTERING OFF
    #filteredText = Censor.filterTextForAudio(str(submission.title))
    createTitleAudio(str(submission.title), saveDir)
    #If there are no comments, just create audio files of the submission body.
    if(len(comments) == 0):
        parsedBody = TextParser.fragmentText(str(submission.selftext))
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
def estimateAudioLength(text: str):
    numWords = text.count(' ')
    return float((numWords / WORDS_PER_MINUTE))

#Replaces certain acronyms in text to increase the quality of TTS. Ex. SIL -> sister in law.
#Not a conclusive list, will be added to as more acronyms are discovered to not sound the best.
ACRONYMS_TO_REPLACE = {'SIL':'sister in law', 'AITA':'am i the asshole', 'WIBTA':'would i be the asshole','AH':'asshole', 'TIFU':'today i fucked up', 'AFAIK':'as far as i know', 'IMHO':'in my honest opinion','IMO':'in my opinion', 'IIRC': 'if i recall correctly'}
def replaceAcronyms(text: str)->str:
    for acronym in ACRONYMS_TO_REPLACE:
        text = text.replace(acronym, ACRONYMS_TO_REPLACE[acronym])
    return text
