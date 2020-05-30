from os import listdir
from os.path import isfile, join
from progress.bar import Bar
from scapy.all import rdpcap,IP,TCP,UDP
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.ensemble import IsolationForest

def main():
  
  # Read all the csv files
  csvPath = "./csv_files"
  csvFiles = [f for f in listdir(csvPath) if isfile(join(csvPath, f))]
  
  # Process all the csv file
  for cv in csvFiles:
    print("CSV Processing: "+cv)
      
    # Read the csv and save it to dataframe
    df = pd.read_csv(csvPath+'/'+cv)
    
    # Turn every column to numeric
    cols = [c for c in df.columns]
    
    nom_cols = ['ip_flags','tcp_udp_flags']    
    for c in nom_cols:
      le = LabelEncoder()
      df[c] = le.fit_transform(df[c])

    # Fill NaN
    df = df.fillna(df.mean())

    # Use the isolation forest to find the anomalies -1: anomaly 1:normal 
    anomalies_ratio = 0.09
    clf = IsolationForest(n_estimators = 100, max_samples = 10, contamination = anomalies_ratio, behaviour='new')
    clf.fit(df)
    
    df['label']=clf.predict(df) 
    df.to_csv('./processed_csv/'+'processed_'+cv)

if __name__ == "__main__":
  main()
