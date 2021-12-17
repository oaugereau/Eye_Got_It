#import python Module
import Config


#This function goes through every character in the text to determnine and add the words, their coordinates and their size in wordTab 
#It also separate the text in multiple pages in pageTab if it is too long for the textEdit
def textAdaptation(metrics,text,width,height):
    #fontMetrics() give us the size in pixel of every character depending of the police, the font size and other parameters of textEdit
    xo=int((Config.SCREEN_WIDTH_SIMULATION-width)+5)
    yo=int(Config.SCREEN_HEIGHT_SIMULATION-height)
    pageTab=[]
    pageTemp=''
    wordTab=[]
    temp=[]
    wordTemp=''
    #wTemp is the width of the line, it is incremented at each iteration and set to 0 when there is a line break
    wTemp=0
    x=0
    y=0
    p=0
    firstLetter=True
    firstWordNextPage=False
    specialChar=False
    firstN=True
    for i in range (0,len(text)):
        #letterAdvance is the width in pixel before another character an be written in textEdit
        letterAdvance=metrics.horizontalAdvance(text[i])
        #checking if the character goes beyond the right side of the textEdit
        if (wTemp+letterAdvance+(Config.fontSizeText*0.4) > width):
            y+=3
            x=xo
            wTemp=metrics.horizontalAdvance(wordTemp)
            if wordTemp!='':
                pageTemp=pageTemp[:-len(wordTemp)]
                specialChar=False
            else:
                pageTemp=pageTemp[:-1]
                specialChar=True
            pageTemp+='\n\n\n'+str(wordTemp)
            if specialChar:
                pageTemp+=str(text[i-1])
                wTemp+=metrics.horizontalAdvance(text[i-1])
        #checking if the character goes below the bottom side of the textEdit
        #pageTemp will be added to pageTab when firstWordNextPage is set to True
        if (yo+((y+1)*metrics.height()) > height):
            y=0
            p+=1
            firstWordNextPage=True
        #this condition handle the last character of the text
        if i==(len(text)-1):
            pageTemp+=str(text[i])
            if text[i]!='\ufeff':
                wordTemp+=str(text[i])
            if firstLetter:
                x=wTemp+xo
            #append the wordTemp along with its coordinates to wordTab
            if wordTemp!='':
                #it first remove any special character
                temp.append(wordTemp.translate({ord(i): None for i in '",.!?:;#<>’‘“”'}))
                temp.append(x-3)
                temp.append(yo+(y*metrics.height())-20)
                rect=metrics.boundingRect(wordTemp)
                temp.append(rect.width()+6)
                temp.append(rect.height()+50)
                temp.append(p)
                wordTab.append(temp)
                pageTab.append(pageTemp)
        #this condition handle when there is a line break 
        elif (text[i]=='\n'):
            if firstWordNextPage:
                x=xo
                if wordTemp!='':
                    pageTemp=pageTemp[:-len(wordTemp)]
                pageTab.append(pageTemp)
                pageTemp=wordTemp
                firstWordNextPage=False
            #append the wordTemp along with its coordinates to wordTab
            if wordTemp!='':
                #it first remove any special character
                temp.append(wordTemp.translate({ord(i): None for i in '",.!?:;#<>’‘“”'}))
                temp.append(x-3)
                temp.append(yo+(y*metrics.height())-20)
                rect=metrics.boundingRect(wordTemp)
                temp.append(rect.width()+6)
                temp.append(rect.height()+50)
                temp.append(p)
                wordTab.append(temp)
            #if there is only one line break it add another so that every line is separated by a blank space
            if (text[i+1]!='\n' and firstN):
                pageTemp+='\n\n'
                y+=2
            elif (text[i+1]=='\n' and firstN):
                pageTemp+='\n'
                y+=1
            if firstN:
                firstN=False
            temp=[]
            wordTemp=''
            firstLetter=True
            y+=1
            x=xo
            wTemp=0
        #this condition handle separation between the word
        elif (text[i]==' ' or text[i]=='—' or text[i]=='–' or text[i]=='…' or text[i]=='(' or text[i]==')' or text[i]=='[' or text[i]==']' or text[i]=='{' or text[i]=='}'):
            if firstWordNextPage:
                x=xo
                wTemp=metrics.horizontalAdvance(wordTemp)
                if wordTemp!='':
                    pageTemp=pageTemp[:-len(wordTemp)]
                pageTab.append(pageTemp)
                pageTemp=wordTemp
                firstWordNextPage=False
            #append the wordTemp along with its coordinates to wordTab
            if wordTemp!='':
                #it first remove any special character
                temp.append(wordTemp.translate({ord(i): None for i in '",.!?:;#<>’‘“”'}))
                temp.append(x-3)
                temp.append(yo+(y*metrics.height())-20)
                rect=metrics.boundingRect(wordTemp)
                temp.append(rect.width()+6)
                temp.append(rect.height()+50)
                temp.append(p)
                wordTab.append(temp)
            temp=[]
            wordTemp=''
            wTemp+=letterAdvance
            firstLetter=True
            firstN=True
            if (text[i]=='(' or text[i]=='[' or text[i]=='{'):
                wordTemp+=str(text[i]) 
        #if no other condition is met the character is added to wordTemp 
        else:
            if text[i]!='\ufeff':
                wordTemp+=str(text[i])
            #if it's the first character we set the x coordinate
            if firstLetter:
                x=wTemp+xo
            wTemp+=letterAdvance
            firstLetter=False
            firstN=True
        pageTemp+=str(text[i])
    return wordTab, pageTab
 