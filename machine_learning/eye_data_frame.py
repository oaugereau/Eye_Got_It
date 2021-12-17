import os, csv
import numpy as np

data=[]
for (root,dirs,files) in os.walk('Report', topdown=True):
    print (root," :")
    
    if not root=="Report":
        with open(str(os.path.join(root,"textPosition.csv")),'r', newline='') as csvfile:
            textPosition = csv.reader(csvfile, delimiter='/')
            wordData = [line for line in textPosition]
        fixationData=[]
        eyeTrackerData=[]
        velocityData=[]
        for file in files:
            if "fixations_" in file:
                print(file)
                with open(str(os.path.join(root,file)),'r',newline='') as csvfile:
                    fixations = csv.reader(csvfile, delimiter=',')
                    fixationPage = [line for line in fixations]
                fixationData.append(fixationPage)
            if "eyeTracker_" in file:
                print(file)
                with open(str(os.path.join(root,file)),'r',newline='') as csvfile:
                    eyeTracker = csv.reader(csvfile, delimiter=',')
                    gazePage = [line for line in eyeTracker]
                eyeTrackerData.append(gazePage)
            if "velocityGazes_" in file:
                print(file)
                with open(str(os.path.join(root,file)),'r',newline='') as csvfile:
                    velocityGazes = csv.reader(csvfile, delimiter=',')
                    velocityPage = [line for line in velocityGazes]
                velocityData.append(velocityPage)

        for i in range(1,len(wordData)):
            temp=[]

            first=0
            temp.append(root)
            temp.append(wordData[i][0])
            temp.append(wordData[i][1])
            temp.append(wordData[i][2])
            temp.append(wordData[i][3])
            temp.append(wordData[i][4])
            temp.append(wordData[i][5])
            if int(wordData[i][1])==2:
                first=1
            temp.append(first)
            
            page=int(wordData[i][5])
            
            nbFixation=0
            duration=0
            for j in range (1,len(fixationData[page])):
                x=float(fixationData[page][j][0])
                y=float(fixationData[page][j][1])
                if x>int(wordData[i][1]) and x<int(wordData[i][1])+int(wordData[i][3]) and y>int(wordData[i][2]) and y<int(wordData[i][2])+int(wordData[i][4]):
                    nbFixation+=1
                    duration+=int(fixationData[page][j][2])
            temp.append(nbFixation)
            temp.append(duration)
            
            backward=0
            nbGaze=0
            continuous_group=[]
            continuous_group_temp=[]
            longest_continous_group=[]
            first_iteration=True
            for j in range (1,len(eyeTrackerData[page])):
                x=float(eyeTrackerData[page][j][0])
                y=float(eyeTrackerData[page][j][1])
                if x>int(wordData[i][1]) and x<int(wordData[i][1])+int(wordData[i][3]) and y>int(wordData[i][2]) and y<int(wordData[i][2])+int(wordData[i][4]):
                    nbGaze+=1
                    """if not first_iteration:
                        if x<float(eyeTrackerData[page][j-1][0]):
                            backward=1"""
                    continuous_group_temp.append(x)
                else:
                    if continuous_group_temp:
                        continuous_group.append(continuous_group_temp)
                        continuous_group_temp=[]
                first_iteration=False
            if continuous_group:
                longest_continous_group = max(continuous_group, key = len)
                for j in range(1,len(longest_continous_group)):
                    if longest_continous_group[j]<longest_continous_group[j-1]:
                        backward+=1
            temp.append(nbGaze)
            temp.append(backward)

            nbGaze=0
            velocity=[]
            maxVelocity=0
            meanVelocity=0
            standardDeviationVelocity=0
            acceleration=[]
            maxAcceleration=0
            meanAcceleration=0
            standardDeviationAcceleration=0
            for j in range (1,len(velocityData[page])):
                x=float(velocityData[page][j][0])
                y=float(velocityData[page][j][1])
                if x>int(wordData[i][1]) and x<int(wordData[i][1])+int(wordData[i][3]) and y>int(wordData[i][2]) and y<int(wordData[i][2])+int(wordData[i][4]):
                    nbGaze+=1
                    velocity.append(float(velocityData[page][j][3]))
                    #meanVelocity+=float(velocityData[page][j][3])
                    acceleration.append(float(velocityData[page][j][4]))
                    #meanAcceleration+=float(velocityData[page][j][4])
            if nbGaze>0:
                maxVelocity=max(velocity)
                maxAcceleration=max(acceleration)
                v=np.array(velocity)
                a=np.array(acceleration)
                #meanVelocity=(meanVelocity/nbGaze)
                meanVelocity=np.mean(v)
                standardDeviationVelocity=np.std(v)
                #meanAcceleration=(meanAcceleration/nbGaze)
                meanAcceleration=np.mean(a)
                standardDeviationAcceleration=np.std(a)
            temp.append(maxVelocity)
            temp.append(meanVelocity)
            temp.append(standardDeviationVelocity)
            temp.append(maxAcceleration)
            temp.append(meanAcceleration)
            temp.append(standardDeviationAcceleration)

            temp.append(0)
            data.append(temp)

    print ('--------------------------------')

with open('dataFrame.csv', 'w', newline='') as csvfile:
    df = csv.writer(csvfile, delimiter=',')
    df.writerow(["report_name","word","pos_x_word","pos_y_word","width_word","height_word","page","line_start","number_of_fixations","total_duration_fixation_us","number_of_gazes","backward_read","max_velocity_gaze","mean_velocity_gaze","standard_deviation_velocity","max_acceleration_gaze","mean_acceleration_gaze","standard_deviation_acceleration","class"])
    for elem in data:
        df.writerow(elem)