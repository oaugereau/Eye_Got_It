import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
from joblib import load

#-------------- dataFrame creation --------------#
#extract data from dataFram.csv
df = pd.read_csv('dataFrame.csv',header=0)

#move all class 2 words to class 0("autocorrection" to "compris")
df['class'] = df.apply(lambda x: 0 if x['class'] == 2 else x['class'] , axis=1)
#print(df.head())
#print(df.dtypes)
print('len df : ',len(df))

#here we remove randomly part of class 0 words
remove_n = int(len(df)*0.98)
drop_indices = np.random.choice(df.index, remove_n, replace=False)
n=[]
for i in range(0,len(drop_indices)):
    #print(drop_indices[i])
    if df.iloc[drop_indices[i]]['class']==1 or df.iloc[drop_indices[i]]['class']==2:
        #print('remove',drop_indices[i],df.iloc[drop_indices[i]]['class'])
        n.append(i)
n=np.array(n)
drop_indices=np.delete(drop_indices,n)
print('number of class 0 words removed : ',len(drop_indices))
df_subset = df.drop(drop_indices)
print('len df_subset : ',len(df_subset))

#remove words without any gaze attach to it
df_no_missing = df_subset.loc[(df_subset['number_of_gazes']!=0)]# & (df_subset['number_of_fixations']!=0)
print('len df_no_missing : ',len(df_no_missing))

df2=df_no_missing.loc[(df_no_missing['class']==1)]
#print(df2.head())

df_equal=df_no_missing.append(df2)

"""df_no_line_start=df_no_missing.loc[(df_no_missing['line_start']!=1)]
print('df_no_line_start : ',len(df_no_line_start))"""

df_final=df_no_missing

#X=df_final.drop(['report_name','word','pos_x_word','pos_y_word','width_word','height_word','line_start','total_duration_fixation_us','backward_read','max_velocity_gaze','mean_velocity_gaze','standard_deviation_velocity','max_acceleration_gaze','mean_acceleration_gaze','standard_deviation_acceleration','class'],axis=1).copy()
X=df_final.drop(['report_name','word','pos_x_word','pos_y_word','width_word','height_word','line_start','class'],axis=1).copy()
print(X.head())

Y=df_final['class'].copy()

clf = load('decisionTree2classes.joblib')

y = clf.predict(X)

print(y)