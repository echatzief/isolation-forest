import argparse,os
from scapy.all import *
from progress.bar import Bar

import random, string

def random_name(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def main():
  parser = argparse.ArgumentParser(description='Packet sniffer')
  parser.add_argument('--iface',type=str,help='Interface to sniff')
  parser.add_argument('--filter',type=str,help='BPF Filter')
  parser.add_argument('--out',type=str,help='Pcap file to output')
  parser.add_argument('--len',type=str,help='Pcap file to output')
  args = parser.parse_args()

  if not args.iface:
    print('--iface required')
    os._exit(-1)
  
  # Default argument values
  outfile = "./pcap_files/"+random_name(30)+".pcap"
  filt = None 

  # Configure the arguments
  if args.filter:
    filt = str(args.filter)
  if args.out:
    outfile = str(args.out)

  # Capture packets
  print("Started Capturing...")
  pkts = sniff(filter=filt,iface=args.iface,timeout=100)
  wrpcap(outfile, pkts)

if __name__ == '__main__':
  main()
