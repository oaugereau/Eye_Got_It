import pandas as pd

df = pd.read_csv('dataFrame.csv',header=0)
print(df.head())
print(df['class'].unique())

dfc = pd.read_csv('dataFrameWithClass.csv',header=0)
print(dfc.head())
print(dfc['class'].unique())

df['class'] = dfc['class']
print(df['class'].unique())
df.to_csv('export_dataframe.csv',index=False)
