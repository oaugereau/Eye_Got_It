#Eye Tracker Buscher Algorithm

import statistics

#return the saccades, glissades and fixations of the gazes
def Nystrom(convertedGazes):
    sacTab=[]
    gliTab=[]
    fixTab=[]
    fixCandidate=[]
    #convertedGazes hold the position, velocity and acceleration of each gaze
    #convertedGazes=VelocityInDeg(gazes,headGazes)
    """velocity=np.zeros(len(convertedGazes))
    for i in range(0,len(convertedGazes)):
        velocity[i]=convertedGazes[i][3]
        print(convertedGazes[i][3])
    print(velocity)
    plt.plot(velocity)
    plt.show()"""
    #calculate velocity treshold in deg/sec
    vt=200
    vtn=0
    glissadeAvancement=0
    firstIteration=True
    while abs(vtn-vt)>1:
        if firstIteration:
            firstIteration=False
        else:
            vt=vtn
        sample=[]
        for i in range(0,len(convertedGazes)):
            if convertedGazes[i][3]<vt:
                sample.append(convertedGazes[i][3]) 
        mean=statistics.mean(sample)
        d=statistics.stdev(sample)
        vtn=mean+4*d
        #print("mean=",mean," deviation=",d," vt=",vt," vtn=",vtn)
    onSetVt=mean+2*d
    offSetVt=0
    #detect saccades
    i=0
    while i < len(convertedGazes):
        #begin saccade detection when velocity is above vtn
        if convertedGazes[i][3]>vtn:
            #print("vitesse=",convertedGazes[i][3])
            #print("i=",i)
            j=i
            previous=convertedGazes[j]
            #detect the onset of the saccade
            while (convertedGazes[j][3]>onSetVt or previous[3]>=convertedGazes[j][3]) and j>0:
                previous=convertedGazes[j]
                j-=1
                #j is the index of the beginning of the saccade
            k=i
            sample=[]
            #collect samples over a 40 millisecond window to calculate local offset treshold
            while (int(convertedGazes[i][2])-int(convertedGazes[k][2]))<=40000:
                sample.append(convertedGazes[k][3])
                k-=1
                #print("duration=",int(convertedGazes[i][2])-int(convertedGazes[k][2]))
                if k<0:
                    break
            #print("sample=",sample)
            if len(sample)==1:
                mean=sample[0]
                d=0
            else:
                mean=statistics.mean(sample)
                d=statistics.stdev(sample)
            #offset treshold is a weighted combinaison of the onset and a local treshold
            offSetVt=(0.7*onSetVt)+(0.3*(mean+2*d))
            #print("offSet=",offSetVt)
            k=i
            previous=convertedGazes[k]
            #detect the onset of the saccade
            while (convertedGazes[k][3]>offSetVt or previous[3]>=convertedGazes[k][3]) and k<len(convertedGazes)-1:
                previous=convertedGazes[k]
                k+=1
                #k is the index of the end of the saccade
            duration=int(convertedGazes[k][2])-int(convertedGazes[j][2])
            #print("duration=",duration)
            if (duration>10000):    
                #if the saccade is long enough(>10ms) we add it to sacTab
                sacTab.append([convertedGazes[j][0],convertedGazes[j][1],convertedGazes[k][0],convertedGazes[k][1],duration,convertedGazes[j][5]])
                #create fixations with the gazes previously added to fixCandidate
                if fixCandidate:
                    if int(fixCandidate[-1][2])-int(fixCandidate[0][2])>40000:
                        fixTab.append(centroid(fixCandidate))
                        fixCandidate=[]
                #glissade detection, k the offset of the saccade is consiered the onset of the glissade
                l=k
                while (int(convertedGazes[l][2])-int(convertedGazes[k][2]))<40000 and l<len(convertedGazes)-1:
                    #a glissade must go above the offset velocity treshold
                    if convertedGazes[l][3]>offSetVt:
                        m=l
                        previous=convertedGazes[m]
                        while previous[3]>=convertedGazes[m][3] and m<len(convertedGazes)-1:
                            previous=convertedGazes[m]
                            m+=1
                        gDuration=int(convertedGazes[m][2])-int(convertedGazes[k][2])
                        #print("gDuration=",duration)
                        #only glissades with a smaller duration than the previous saccade are recorded
                        if gDuration<duration:
                            gliTab.append([convertedGazes[k][0],convertedGazes[k][1],convertedGazes[m][0],convertedGazes[m][1],duration,convertedGazes[k][5]])
                            glissadeAvancement=(m-k)
                            break
                    l+=1
                #print("on avance de ",(k-i),"apres la saccade")
                #print("on avance de ",glissadeAvancement,"apres la glissade")
                i+=(k-i)+glissadeAvancement
                glissadeAvancement=0
        
        #all gazes that are below the treshold are appended to fixCandidate and when a saccade is detected a fixation is created with the candidate and appended to fixTab
        else:
            fixCandidate.append([convertedGazes[i][0],convertedGazes[i][1],convertedGazes[i][2],0,convertedGazes[i][5]])
        i+=1
    #print("velocity treshold=",vtn)
    return sacTab,gliTab,fixTab

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
    c.append((int(gazes[-1][2])-int(gazes[0][2])))
    #unix time of the first gaze
    c.append(gazes[0][4])
    return c
