from os import listdir
from os.path import isfile, join
from progress.bar import Bar
from scapy.all import rdpcap,IP,TCP,UDP
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.mixture import GaussianMixture

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
    
    # Clustering in order to define the two categories
    X = np.array(df)
    gmm = GaussianMixture(n_components=2).fit(X)
    labels = gmm.predict(X)
    
    # Add the labels to the dataset
    df['label'] = pd.Series(labels)
    
    # Count the ones and zeros to identify which class if the elephant flow
    ones = np.array(df.loc[df['label'] == 1])
    onesSum = np.sum(ones[:,3])
    zeros = np.array(df.loc[df['label'] == 0])
    zeroSum = np.sum(zeros[:,3])

    # Label the data
    if onesSum >= zeroSum:
        label_map = {
            0:"mice_flow",
            1:"elephant_flow"
        }
        df['label'] = df['label'].map(label_map)
    else:
        label_map = {
            0:"elephant_flow",
            1:"mice_flow",
        }
        df['label'] = df['label'].map(label_map)
    
    df.to_csv('./processed_csv/'+'processed_'+cv)

if __name__ == "__main__":
  main()
