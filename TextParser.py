from unidecode import unidecode
TITLE_LINE_LIMIT = 33
COMMENT_LINE_LIMIT = 45


#Call this for titles only
#Breaks texts into lines so they can be drawn onto an image without trailing off the screen.
def addLineBreaks(text, LINE_LIMIT)->str:
    text = unidecode(text)
    listOfWords = text.split(' ')
    fixedString = ''
    charsInLine = 0
    #Adds line breaks whenever adding the next word would cause the string to exceed the character limit on that line. LINE_LIMIT is max amount of characters allowed on a line.
    for word in listOfWords:
        if charsInLine+len(word)+1 < LINE_LIMIT:
            fixedString = fixedString + word + " "
            charsInLine = charsInLine+len(word)+1
        else:
            fixedString = fixedString + "\n" + word + " "
            charsInLine = len(word)
    return fixedString

#Called on comments / posts only, no titles
#Fragments text into sections so that smaller images can be displayed on screen. Ex. A 20 line image would take up too much of the screen so the text is fragmented into 5 line sections.
#The fragmented text is used for both creating images and the audio files.
def fragmentText(text)->list():
    text = cleanTextBeforeFragmenting(text)
    #Removes non unicode characters and adds linebreaks to the text
    text = unidecode(text)
    text = addLineBreaks(text, COMMENT_LINE_LIMIT)
    listOfFragments = list()
    currentString = ''
    numBreaks = 0
    #Goes through string (with line breaks added) and splits into smaller strings of at most 5 lines each. Returns these fragments as a list
    while(True):
        partition = text.partition('\n')
        currentString = currentString + partition[0] +'\n'
        numBreaks = numBreaks + 1
        if(numBreaks >= 5):
            listOfFragments.append(currentString)
            currentString = ''
            numBreaks = 0
        if(partition[2] != ''):
            text = partition[2]
        else:
            break
    if(currentString != ''):
        listOfFragments.append(currentString)
    return listOfFragments

#Cleans up text so that text is displayed cleaner and audio is less choppy.
def cleanTextBeforeFragmenting(text):
    text = text.replace('\n',' ')
    text = text.replace('  ', ' ')
    return text