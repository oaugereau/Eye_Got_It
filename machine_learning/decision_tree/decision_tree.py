import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
from joblib import dump
import os, sys
from PyQt5 import QtCore, QtWidgets, QtGui
np.random.seed(10)

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

#count the number of words with class 0, 1 and 2
seriesObj0 = df_final.apply(lambda x: True if x['class'] == 0 else False , axis=1)
numOfRows0 = len(seriesObj0[seriesObj0 == True].index)
print('Number of Rows in df_final with class = 0 : ', numOfRows0)
seriesObj1 = df_final.apply(lambda x: True if x['class'] == 1 else False , axis=1)
numOfRows1 = len(seriesObj1[seriesObj1 == True].index)
print('Number of Rows in df_final with class = 1 : ', numOfRows1)
seriesObj2 = df_final.apply(lambda x: True if x['class'] == 2 else False , axis=1)
numOfRows2 = len(seriesObj2[seriesObj2 == True].index)
print('Number of Rows in df_final with class = 2 : ', numOfRows2)

#-------------- boxplot --------------#
"""df_final.boxplot(column='line_start',by='class')
df_final.boxplot(column='number_of_fixations',by='class')
df_final.boxplot(column='total_duration_fixation_us',by='class')
df_final.boxplot(column='number_of_gazes',by='class')
df_final.boxplot(column='backward_read',by='class')
df_final.boxplot(column='max_velocity_gaze',by='class')
df_final.boxplot(column='mean_velocity_gaze',by='class')
df_final.boxplot(column='standard_deviation_velocity',by='class')
df_final.boxplot(column='max_acceleration_gaze',by='class')
df_final.boxplot(column='mean_acceleration_gaze',by='class')
df_final.boxplot(column='standard_deviation_acceleration',by='class')
plt.show()"""

#-------------- splitting data --------------#
#drop the data you don't want to use
X=df_final.drop(['report_name','word','pos_x_word','pos_y_word','width_word','height_word','line_start','class'],axis=1).copy()
#print(X.head())

Y=df_final['class'].copy()
#print(Y.head())
#print(Y.unique())

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state=26)
#sample_weight = Y_train.apply(lambda x: 2 if x==1 else 1)
#print(sample_weight)

#-------------- decision tree creation --------------#
clf_dt = DecisionTreeClassifier(random_state=26)
clf_dt = clf_dt.fit(X_train, Y_train)

"""plt.figure(figsize=(15, 7.5))
#plot_tree(clf_dt, filled=True, rounded=True, class_names=['Compris','Pas compris','Autocorrection'], feature_names=X.columns)
plot_tree(clf_dt, filled=True, rounded=True, class_names=['Compris','Pas compris'], feature_names=X.columns)
print("tree plot")

#plot_confusion_matrix(clf_dt, X_test, Y_test, display_labels=['Compris','Pas compris','Autocorrection'])
plot_confusion_matrix(clf_dt, X_test, Y_test, display_labels=['Compris','Pas compris'])
plt.title("confusion matrix decision tree with all parameters")
print("matrix plot")
print("score decision tree : ",clf_dt.score(X_test, Y_test))
plt.show()"""

#-------------- cost complexity pruning --------------#
path = clf_dt.cost_complexity_pruning_path(X_train,Y_train)
ccp_alphas = path.ccp_alphas
ccp_alphas = ccp_alphas[:-1]

clf_dts = []

for ccp_alpha in ccp_alphas:
    clf_dt = DecisionTreeClassifier(random_state=0, ccp_alpha=ccp_alpha)
    clf_dt.fit(X_train, Y_train)
    clf_dts.append(clf_dt)

train_scores = [clf_dt.score(X_train, Y_train) for clf_dt in clf_dts]
test_scores = [clf_dt.score(X_test, Y_test) for clf_dt in clf_dts]

fig, ax = plt.subplots()
ax.set_xlabel("alpha")
ax.set_ylabel("accuracy")
ax.set_title("Accuracy vs alpha for training and testing sets")
ax.plot(ccp_alphas, train_scores, marker='o', label="train", drawstyle="steps-post")
ax.plot(ccp_alphas, test_scores, marker='o', label="test", drawstyle="steps-post")
ax.legend()
#plt.show()

alpha_loop_values=[]  

for ccp_alpha in ccp_alphas:
    clf_dt = DecisionTreeClassifier(random_state=0, ccp_alpha=ccp_alpha)
    scores = cross_val_score(clf_dt, X_train, Y_train, cv=3)
    alpha_loop_values.append([ccp_alpha, np.mean(scores), np.std(scores)])

alpha_results = pd.DataFrame(alpha_loop_values, columns=['alpha', 'mean_accuracy', 'std'])

alpha_results.plot(x='alpha',y='mean_accuracy', yerr='std', marker='o', linestyle='--')
#plt.show()

#-------------- pruned decision tree creation --------------#
ideal_ccp_alpha=float(alpha_results[(alpha_results['alpha']>0.02) & (alpha_results['alpha']<0.024)]['alpha'])
#print(ideal_ccp_alpha)

clf_dt_pruned = DecisionTreeClassifier(random_state=26, ccp_alpha=ideal_ccp_alpha)
clf_dt_pruned = clf_dt_pruned.fit(X_train, Y_train)

"""plt.figure(figsize=(15, 7.5))
#plot_tree(clf_dt_pruned, filled=True, rounded=True, class_names=['Compris','Pas compris','Autocorrection'], feature_names=X.columns)
plot_tree(clf_dt_pruned, filled=True, rounded=True, class_names=['Compris','Pas compris'], feature_names=X.columns)
print("tree pruned plot")

#plot_confusion_matrix(clf_dt_pruned, X_test, Y_test, display_labels=['Compris','Pas compris','Autocorrection'])
plot_confusion_matrix(clf_dt_pruned, X_test, Y_test, display_labels=['Compris','Pas compris'])
print("matrix plot")
print("score decision tree : ",clf_dt_pruned.score(X_test, Y_test))
plt.show()"""

dump(clf_dt_pruned, 'decisionTree2classes.joblib') 

#-------------- display sample prediction and true class --------------#
y = clf_dt_pruned.predict(X_test)
i0=[]
i1=[]
i2=[]
for i in range(0,len(y)):
    if y[i]==0:
        i0.append(i)
    if y[i]==1:
        i1.append(i)
    if y[i]==2:
        i2.append(i)
"""print(len(y))
print(i0,i1,i2)"""
index0=X_test.iloc[i0].index
index1=X_test.iloc[i1].index
index2=X_test.iloc[i2].index
"""print('mots classés compris:\n',index0)
print('mots classés pas compris:\n',index1)
print('mots classés autocorrection:\n',index2)"""
print(df_no_missing.loc[index0[4]]['page'])
print('longueur',len(index0))
"""for i in range (0,len(index0)):
    print(index0[i])"""

class DisplayWindow(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.currentWord=0
        self.currentClass=0

        self.setWindowTitle("Display Words 'Compris'")

        self.pageDisplay = QtWidgets.QLabel(self)
        
        self.display_page()

    def display_page(self):
        if self.currentClass==0:
            pixmap = QtGui.QPixmap(os.path.join(df_no_missing.loc[index0[self.currentWord]]['report_name'],str('EyeTracker_'+str(df_no_missing.loc[index0[self.currentWord]]['page'])+'.jpg')))
            print(df_no_missing.loc[index0[self.currentWord]])
            x=df_no_missing.loc[index0[self.currentWord]]['pos_x_word']
            y=df_no_missing.loc[index0[self.currentWord]]['pos_y_word']
            width=df_no_missing.loc[index0[self.currentWord]]['width_word']
            height=df_no_missing.loc[index0[self.currentWord]]['height_word']
            if df_no_missing.loc[index0[self.currentWord]]['class']==0:
                color=QtCore.Qt.green
            else:
                color=QtCore.Qt.red
        if self.currentClass==1:
            pixmap = QtGui.QPixmap(os.path.join(df_no_missing.loc[index1[self.currentWord]]['report_name'],str('EyeTracker_'+str(df_no_missing.loc[index1[self.currentWord]]['page'])+'.jpg')))
            print(df_no_missing.loc[index1[self.currentWord]])    
            x=df_no_missing.loc[index1[self.currentWord]]['pos_x_word']
            y=df_no_missing.loc[index1[self.currentWord]]['pos_y_word']
            width=df_no_missing.loc[index1[self.currentWord]]['width_word']
            height=df_no_missing.loc[index1[self.currentWord]]['height_word']
            if df_no_missing.loc[index1[self.currentWord]]['class']==1:
                color=QtCore.Qt.green
            else:
                color=QtCore.Qt.red
        if self.currentClass==2:
            pixmap = QtGui.QPixmap(os.path.join(df_no_missing.loc[index2[self.currentWord]]['report_name'],str('EyeTracker_'+str(df_no_missing.loc[index2[self.currentWord]]['page'])+'.jpg')))
            print(df_no_missing.loc[index2[self.currentWord]])
            x=df_no_missing.loc[index2[self.currentWord]]['pos_x_word']
            y=df_no_missing.loc[index2[self.currentWord]]['pos_y_word']
            width=df_no_missing.loc[index2[self.currentWord]]['width_word']
            height=df_no_missing.loc[index2[self.currentWord]]['height_word']
            if df_no_missing.loc[index2[self.currentWord]]['class']==2:
                color=QtCore.Qt.green
            else:
                color=QtCore.Qt.red
        painter = QtGui.QPainter()
        painter.begin(pixmap)
        self.penRectangle = QtGui.QPen(color)
        self.penRectangle.setWidth(3)
        painter.setPen(self.penRectangle)
        painter.drawRect(x,y,width,height)
        painter.end()
        self.resize(pixmap.width(),pixmap.height())
        self.pageDisplay.setPixmap(pixmap)

    def keyPressEvent(self, event):
        #print(event.key())
        if event.key() == QtCore.Qt.Key_D:
            if self.currentClass==0 and self.currentWord<len(index0)-1:
                self.currentWord+=1
            if self.currentClass==1 and self.currentWord<len(index1)-1:
                self.currentWord+=1
            if self.currentClass==2 and self.currentWord<len(index2)-1:
                self.currentWord+=1
            self.display_page()
        
        if event.key() == QtCore.Qt.Key_E:
            if self.currentClass<2:
                self.currentClass+=1
                self.currentWord=0
            if self.currentClass==0:
                self.setWindowTitle("Display Words 'Compris'")
            if self.currentClass==1:
                self.setWindowTitle("Display Words 'pas Compris'")
            if self.currentClass==2:
                self.setWindowTitle("Display Words 'Autocorrection'")
            self.display_page()
        
        if event.key() == QtCore.Qt.Key_Q:
            if self.currentWord>0:
                self.currentWord-=1
            self.display_page()
        
        if event.key() == QtCore.Qt.Key_A:
            if self.currentClass>0:
                self.currentClass-=1
                self.currentWord=0
            if self.currentClass==0:
                self.setWindowTitle("Display Words 'Compris'")
            if self.currentClass==1:
                self.setWindowTitle("Display Words 'pas Compris'")
            if self.currentClass==2:
                self.setWindowTitle("Display Words 'Autocorrection'")
            self.display_page()
        
        event.accept()

"""app = QtWidgets.QApplication(sys.argv)
window = DisplayWindow()
window.show()
sys.exit(app.exec_())"""

#-------------- decision path analysis ---------------#
"""n_nodes = clf_dt_pruned.tree_.node_count
children_left = clf_dt_pruned.tree_.children_left
children_right = clf_dt_pruned.tree_.children_right
feature = clf_dt_pruned.tree_.feature
threshold = clf_dt_pruned.tree_.threshold

node_depth = np.zeros(shape=n_nodes, dtype=np.int64)
is_leaves = np.zeros(shape=n_nodes, dtype=bool)
stack = [(0, 0)]  # start with the root node id (0) and its depth (0)
while len(stack) > 0:
    # `pop` ensures each node is only visited once
    node_id, depth = stack.pop()
    node_depth[node_id] = depth

    # If the left and right child of a node is not the same we have a split
    # node
    is_split_node = children_left[node_id] != children_right[node_id]
    # If a split node, append left and right children and depth to `stack`
    # so we can loop through them
    if is_split_node:
        stack.append((children_left[node_id], depth + 1))
        stack.append((children_right[node_id], depth + 1))
    else:
        is_leaves[node_id] = True

print("The binary tree structure has {n} nodes and has "
      "the following tree structure:\n".format(n=n_nodes))
for i in range(n_nodes):
    if is_leaves[i]:
        print("{space}node={node} is a leaf node.".format(
            space=node_depth[i] * "\t", node=i))
    else:
        print("{space}node={node} is a split node: "
              "go to node {left} if X[:, {feature}] <= {threshold} "
              "else to node {right}.".format(
                  space=node_depth[i] * "\t",
                  node=i,
                  left=children_left[i],
                  feature=feature[i],
                  threshold=threshold[i],
                  right=children_right[i]))


node_indicator = clf_dt_pruned.decision_path(X_test)
leaf_id = clf_dt_pruned.apply(X_test)

sample_id = 0
# obtain ids of the nodes `sample_id` goes through, i.e., row `sample_id`
node_index = node_indicator.indices[node_indicator.indptr[sample_id]:
                                    node_indicator.indptr[sample_id + 1]]

print('Rules used to predict sample {id}:\n'.format(id=sample_id))
for node_id in node_index:
    # continue to the next node if it is a leaf node
    if leaf_id[sample_id] == node_id:
        continue

    print('debug : ',sample_id)
    # check if value of the split feature for sample 0 is below threshold
    if (X_test[sample_id, feature[node_id]] <= threshold[node_id]):
        threshold_sign = "<="
    else:
        threshold_sign = ">"

    print("decision node {node} : (X_test[{sample}, {feature}] = {value}) "
          "{inequality} {threshold})".format(
              node=node_id,
              sample=sample_id,
              feature=feature[node_id],
              value=X_test[sample_id, feature[node_id]],
              inequality=threshold_sign,
              threshold=threshold[node_id]))"""