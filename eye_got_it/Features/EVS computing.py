#*****************************************************************
# This code is for computing and ploting the eye voice span mesure
#*****************************************************************

# import libraries
import pandas as pd

# read data ( eye mouvement, aligned audio, text position)
textPosition = pd.read_csv(r'C:/Users/elbah/Eye Got It/Report/N1 Tester_2021_07_30_11_34_05/2021_07_30_11_34_13/textPosition.csv')
alignedAudio = pd.read_csv(r'C:/Users/elbah/Desktop/LeCycl/record1.csv', sep=';')
eyeGaze = pd.read_csv(r'C:/Users/elbah/Eye Got It/Report/N1 Tester_2021_07_30_11_34_05/2021_07_30_11_34_13/eyeTracker.csv')

# create a list containing the region of each word
region = []
for i in range(0,len(textPosition['x'])):
    x_region = [textPosition['x'][i] - textPosition['width'][i]/2, textPosition['x'][i] + textPosition['width'][i]/2]
    y_region = [textPosition['y'][i] - textPosition['height'][i]/2, textPosition['y'][i] + textPosition['height'][i]/2]
    region.append([x_region,y_region])

word_region= pd.Series(region)

# create a new data frame
df = pd.DataFrame()
df['word'] = textPosition['word']
df['word_region'] = word_region

def is_in(x,y,b):
    '''cette fonction verifie si les cordonnées (x,y) sont dans une région du mot '''
    if x >= b[0][0] and x<= b[0][1] and y >= b[1][0] and y <= b[1][1] :
        return True
    else :
        False
# l'erreur 
eps = 10

gazed_word = []
for i in range(len(df['word_region'])):
    if eyeGaze['x_gaze'][i] >=  df['word_region'][i][0][0] and eyeGaze['x_gaze'][i] <=  df['word_region'][i][0][1] and eyeGaze['y_gaze'][i] <=  (df['word_region'][i][1][0] - eps ) and  eyeGaze['y_gaze'][i] <=  (df['word_region'][i][1][1] + eps) :
        gazed_word.append(df['word'][i])
    else :
        None

gazed_word

# gaze = pd.Series(gazed_word, dtype = 'float64') 
gaze = pd.Series(gazed_word)

# create a serie containing time intervalls [t1, t2]
times = []
alignedAudio['END'] = alignedAudio['BEGIN'] + alignedAudio['DURATION']
for i in range(len(alignedAudio['BEGIN'])):
    times.append([alignedAudio['BEGIN'][i],alignedAudio['END'][i]])

Time = pd.Series(times)


res = pd.DataFrame()
# add Time serie to DF
res['Time'] = Time
# add pronouced words in a new serie
res['Pronouced word'] = alignedAudio['ORT']
# add gaze words in a new serie
res['Gazed word'] = gaze

# res = res.dropna()
