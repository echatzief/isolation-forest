from os import listdir
from os.path import isfile, join
from progress.bar import Bar
from scapy.all import rdpcap,IP,TCP,UDP
import pandas as pd
from progress.bar import Bar

def main():
  # Read all the pcap files
  pcapPath = "./pcap_files"
  pcapFiles = [f for f in listdir(pcapPath) if isfile(join(pcapPath, f))]

  for p in pcapFiles:

    # Read the current pcap
    pcap = rdpcap(pcapPath+"/"+p)

    print('File processed: '+p)

    # Collect field names from IP/TCP/UDP
    ip_fields = [field.name for field in IP().fields_desc]
    tcp_fields = [field.name for field in TCP().fields_desc]
    udp_fields = [field.name for field in UDP().fields_desc]
    dataframe_fields = ip_fields + ['time'] + tcp_fields
    dataframe_fields = dataframe_fields + ['land']

    dataframe_fields_after = ip_fields + ['time'] + tcp_fields + ['land']
    dataframe_fields_after[dataframe_fields_after.index('flags')] = "ip_flags"
    dataframe_fields_after[dataframe_fields_after.index('flags')] = "tcp_udp_flags"
    dataframe_fields_after[dataframe_fields_after.index('chksum')] = "ip_chksum"
    dataframe_fields_after[dataframe_fields_after.index('chksum')] = "tcp_udp_chksum"
    dataframe_fields_after[dataframe_fields_after.index('options')] = "ip_options"
    dataframe_fields_after[dataframe_fields_after.index('options')] = "tcp_udp_options"

    # Create the dataframe with the data
    df = pd.DataFrame(columns=dataframe_fields)

    for packet in pcap[IP]:
      # Field array for each row of DataFrame
      field_values = []
      # Add all IP fields to dataframe
      for field in ip_fields:
          if field == 'options':
              # Retrieving number of options defined in IP Header
              field_values.append(len(packet[IP].fields[field]))
          else:
              field_values.append(packet[IP].fields[field])
      
      field_values.append(packet.time)
        
      layer_type = type(packet[IP].payload)
      for field in tcp_fields:
          try:
              if field == 'options':
                  field_values.append(len(packet[layer_type].fields[field]))
              else:
                  field_values.append(packet[layer_type].fields[field])
          except:
              field_values.append(None)

      # land option
      if((packet[IP].fields['src'] == packet[IP].fields['dst']) or (packet[layer_type].fields['sport'] == packet[layer_type].fields['dport'])):
        field_values.append(1)
      else:
        field_values.append(0)

      df_append = pd.DataFrame([field_values], columns=dataframe_fields)
      df = pd.concat([df, df_append], axis=0)
    
    
    # Reset Index
    df.columns = dataframe_fields_after
    df = df.reset_index()

    # Drop old index column
    df = df.drop(columns=["index","src","dst","id","ip_chksum","seq","ack","tcp_udp_chksum"])
    df.to_csv('./csv_files/'+p+'.csv',index=False)

if __name__ == '__main__':
  main()