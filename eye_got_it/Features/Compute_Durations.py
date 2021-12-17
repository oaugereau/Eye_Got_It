#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# import eyeGaze for beginner readers
FeyeGaze1 =  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/facile/eyeTracker1.csv')
FeyeGaze2 =  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/facile/eyeTracker2.csv') 
FeyeGaze3 =  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/facile/eyeTracker3.csv') 
FeyeGaze4 =  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/facile/eyeTracker4.csv') 

# import eyeGaze for intermediate readers
IeyeGaze1 =  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/interm/eyeTracker1.csv')
IeyeGaze2 =  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/interm/eyeTracker2.csv') 
IeyeGaze3 =  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/interm/eyeTracker3.csv') 
IeyeGaze4 =  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/interm/eyeTracker4.csv') 

# import eyeGaze for Advanced readers
AeyeGaze1 =  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/advanced/eyeTracker1.csv')
AeyeGaze2 =  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/advanced/eyeTracker2.csv') 
AeyeGaze3 =  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/advanced/eyeTracker3.csv') 
AeyeGaze4 =  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/advanced/eyeTracker4.csv') 

# calcule de l'eye Gaze duration pour le texte facile
gaze_duration_facile = [ FeyeGaze1['unix_time_ms_gaze'][len(FeyeGaze1['unix_time_ms_gaze'])-1] - FeyeGaze1['unix_time_ms_gaze'][0],
                        FeyeGaze2['unix_time_ms_gaze'][len(FeyeGaze2['unix_time_ms_gaze'])-1] - FeyeGaze2['unix_time_ms_gaze'][0],
                       FeyeGaze3['unix_time_ms_gaze'][len(FeyeGaze3['unix_time_ms_gaze'])-1] - FeyeGaze3['unix_time_ms_gaze'][0],
                       FeyeGaze4['unix_time_ms_gaze'][len(FeyeGaze4['unix_time_ms_gaze'])-1] - FeyeGaze4['unix_time_ms_gaze'][0]]


# calcule de l'eye Gaze duration pour le texte intermidiare
gaze_duration_interm = [ IeyeGaze1['unix_time_ms_gaze'][len(IeyeGaze1['unix_time_ms_gaze'])-1] - IeyeGaze1['unix_time_ms_gaze'][0],
                        IeyeGaze2['unix_time_ms_gaze'][len(IeyeGaze2['unix_time_ms_gaze'])-1] - IeyeGaze2['unix_time_ms_gaze'][0],
                       IeyeGaze3['unix_time_ms_gaze'][len(IeyeGaze3['unix_time_ms_gaze'])-1] - IeyeGaze3['unix_time_ms_gaze'][0],
                        IeyeGaze4['unix_time_ms_gaze'][len(IeyeGaze4['unix_time_ms_gaze'])-1] - IeyeGaze4['unix_time_ms_gaze'][0]]

# calcule de l'eye Gaze duration pour le texte difficle
gaze_duration_Diff = [ AeyeGaze1['unix_time_ms_gaze'][len(AeyeGaze1['unix_time_ms_gaze'])-1] - AeyeGaze1['unix_time_ms_gaze'][0],
                        AeyeGaze2['unix_time_ms_gaze'][len(AeyeGaze2['unix_time_ms_gaze'])-1] - AeyeGaze2['unix_time_ms_gaze'][0],
                       AeyeGaze3['unix_time_ms_gaze'][len(AeyeGaze3['unix_time_ms_gaze'])-1] - AeyeGaze3['unix_time_ms_gaze'][0],
                     AeyeGaze4['unix_time_ms_gaze'][len(AeyeGaze4['unix_time_ms_gaze'])-1] - AeyeGaze4['unix_time_ms_gaze'][0]]

#lire les données de la position du gaze
fixation_facile_1=  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/facile/fixations1.csv')
fixation_facile_2=  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/facile/fixations2.csv')
fixation_facile_3=  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/facile/fixations3.csv')
fixation_facile_4=  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/facile/fixations4.csv')

fixation_interm_1=  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/interm/fixations1.csv')
fixation_interm_2=  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/interm/fixations2.csv')
fixation_interm_3=  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/interm/fixations3.csv')
fixation_interm_4=  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/interm/fixations4.csv')

fixation_advanced_1=  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/advanced/fixations1.csv')
fixation_advanced_2=  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/advanced/fixations2.csv')
fixation_advanced_3=  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/advanced/fixations3.csv')
fixation_advanced_4=  pd.read_csv(r'C:/Users/elbah/Desktop/Eyegaze/advanced/fixations4.csv')

#  calculer la moyenne 
fixation_facile =[fixation_facile_1['duration_us'].mean()*(1/1000),fixation_facile_2['duration_us'].mean()*(1/1000),fixation_facile_3['duration_us'].mean()*(1/1000), fixation_facile_4['duration_us'].mean()*(1/1000)] 
fixation_interm =[fixation_interm_1['duration_us'].mean()*(1/1000),fixation_interm_2['duration_us'].mean()*(1/1000),fixation_interm_3['duration_us'].mean()*(1/1000), fixation_interm_4['duration_us'].mean()*(1/1000)] 
fixation_advanced =[fixation_advanced_1['duration_us'].mean()*(1/1000),fixation_advanced_2['duration_us'].mean()*(1/1000),fixation_advanced_3['duration_us'].mean()*(1/1000), fixation_advanced_4['duration_us'].mean()*(1/1000)] 
 
mean_fixation_facile_ms = np.mean(fixation_facile)
mean_fixation_interm_ms = np.mean(fixation_interm)
mean_fixation_advanced_ms = np.mean(fixation_advanced)

nb_fixation_facile = np.mean([len(fixation_facile_1), len(fixation_facile_2), len(fixation_facile_3), len(fixation_facile_4)])
nb_fixation_interm = np.mean([len(fixation_interm_1), len(fixation_interm_2), len(fixation_interm_3), len(fixation_interm_4)])
nb_fixation_advanced = np.mean([len(fixation_advanced_1), len(fixation_advanced_2), len(fixation_advanced_3), len(fixation_advanced_4)])


x = '    '
print(5*x," EYE GAZE DURATION (ms)")
print(3*x, "    MEAN ", 3*x, " SD" )
print("Beginner      ",np.mean(gaze_duration_facile), x, "",np.std(gaze_duration_facile))
print("Intermediate  ",np.mean(gaze_duration_interm), x, np.std(gaze_duration_interm))
print("Advanced      ",np.mean(gaze_duration_Diff), x, "",np.std(gaze_duration_Diff))

print(" ")
print(6*x,"--------")
print(" ")

print(5*x," FIXATION DURATION (ms)")
print(4*x, "    MEAN ", 5*x, " SD" )
print("Beginner      ",mean_fixation_facile_ms, x, "",np.std(fixation_facile))
print("Intermediate  ",mean_fixation_interm_ms, x, np.std(fixation_interm))
print("Advanced      ",mean_fixation_advanced_ms, x, "",np.std(fixation_advanced))


print(" ")
print(6*x,"--------")
print(" ")

print(1*x," NUMBER OF FIXATIONS")
print(3*x, "   MEAN ")
print("Beginner      ",nb_fixation_facile)
print("Intermediate  ",nb_fixation_interm)
print("Advanced      ",nb_fixation_advanced)


# In[ ]:




