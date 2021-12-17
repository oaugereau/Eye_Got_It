#Eye Tracker Buscher Algorithm

#return the fixations of the gazes
def fixationBuscher2008(gazes,usFixation=80000,smallSquareSize=30,bigSquareSize=50,consecutiveFails=4):
    fixations=[]
    i=0
    #iterate through all the gazes
    while i < len(gazes):
        fixCandidate=[]
        time=0
        n=0
        remove_n=0

        #append gazes in fixCandidate until there is at least 4 and the duration is long enough
        while ((time<usFixation or len(fixCandidate)<4) and (i+n+1)<=len(gazes)):
            fixCandidate.append(gazes[i+n])
            n+=1
            time=(int(fixCandidate[-1][3])-int(fixCandidate[0][3]))
        
        #check if the fixCandidates fit in the same square
        if insideSquare(fixCandidate,smallSquareSize):
            j=i+len(fixCandidate)
            fail=0

            #add one gaze and check if it fit with the others in a bigger square
            while j<len(gazes):
                fixCandidate.append(gazes[j])
                if not(insideSquare(fixCandidate,bigSquareSize)):
                    fixCandidate = fixCandidate[:-1]
                    remove_n+=1
                    fail+=1
                    #when 4 consecutive gaze don't fit in the bigger square we leave the loop
                    if fail>=consecutiveFails:
                        remove_n-=4
                        break
                else:
                    fail=0
                j+=1

            #calculate the coordinate and duration of the fixation
            fixations.append(centroid(fixCandidate))
            i+=len(fixCandidate)+remove_n+1
        else:
            i+=1
    return fixations

#check if all the gazes can be fitted in the same square
def insideSquare(gazes,size):
    x = [float(p[0]) for p in gazes]
    y = [float(p[1]) for p in gazes]
    xMin=min(x)
    xMax=max(x)
    yMin=min(y)
    yMax=max(y)
    if ((xMax-xMin)<size and (yMax-yMin)<size):
        return True
    else:
        return False

#return the centroid of the gazes wich is the mean of the x and y coordinate
def centroid(gazes):
    x=0
    y=0
    c=[]
    for i in range(0,len(gazes)):
        x+=float(gazes[i][0])
        y+=float(gazes[i][1])
    x/=len(gazes)
    y/=len(gazes)
    #x coordinate
    c.append(x)
    #y coordinate
    c.append(y)
    #duration between the first and last gaze
    c.append((int(gazes[-1][3])-int(gazes[0][3])))
    #unix time of the first gaze
    c.append(gazes[0][4])
    return c