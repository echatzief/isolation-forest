from sklearn.model_selection import train_test_split
from os import listdir
from os.path import isfile, join
from progress.bar import Bar
from scapy.all import rdpcap,IP,TCP,UDP
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import LabelEncoder
import datetime
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import make_scorer, f1_score
from sklearn import model_selection
from sklearn.datasets import make_classification


def main():
  
  # Read all the csv files
  csvPath = "./processed_csv"
  csvFiles = [f for f in listdir(csvPath) if isfile(join(csvPath, f))]
  
  # Join all the csv
  dfs = [] 
  for cv in csvFiles:
    print("CSV Processing: "+cv)
    dfs.append(pd.read_csv(csvPath+'/'+cv,index_col=False))
  
  df = pd.concat(dfs, ignore_index=True)
  df = df.drop('Unnamed: 0', axis=1)
  
  # Train test split
  X = df.drop('label',axis=1)
  y = [1 if x==b'mice_flow' else -1 for x in df['label']]
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

  # Create the model and start training
  start = datetime.datetime.now()
  clfIF = IsolationForest(max_samples='auto', contamination='auto',n_estimators=100,behaviour="new")   
  clfIF.fit(X_train,y_train)
  end = datetime.datetime.now()  
  
  print("Training Time: "+str(end-start))

  y_pred_train = clfIF.predict(X_train)
 
  print("Training sample :")
  print(y_pred_train)
  print(classification_report(y_train, y_pred_train, target_names=['anomaly', 'normal']))
  print ("AUC: ", "{:.1%}".format(roc_auc_score(y_train, y_pred_train)))
  cm = confusion_matrix(y_train, y_pred_train)
  print(cm)
  #plot_confusion_matrix(cm, title="IF Confusion Matrix - SA")
 

  y_pred_test = clfIF.predict(X_test)
  print("Testing sample :")
  print(y_pred_test)
  print(classification_report(y_test, y_pred_test, target_names=['anomaly', 'normal']))
  print ("AUC: ", "{:.1%}".format(roc_auc_score(y_test, y_pred_test)))
  cm = confusion_matrix(y_test, y_pred_test)
  print(cm)
  #plot_confusion_matrix(cm, title="IF Confusion Matrix - SA")
  
  clf = IsolationForest(random_state=47, behaviour='new')

  param_grid = {'n_estimators': list(range(100, 800, 5)), 
              'max_samples': list(range(100, 500, 5)), 
              'contamination': [0.1, 0.2, 0.3, 0.4, 0.5], 
              'max_features': [5,10,15], 
              'bootstrap': [True, False], 
              'n_jobs': [5, 10, 20, 30]}

  f1sc = make_scorer(f1_score,average='micro')

  grid_dt_estimator = model_selection.GridSearchCV(clf, 
                                                 param_grid,
                                                 scoring=f1sc, 
                                                 refit=True,
                                                 cv=10, 
                                                 return_train_score=True)
  print(grid_dt_estimator)
  print(grid_dt_estimator.fit(X_train, y_train)) 
if __name__ == "__main__":
  main() 
