#!/bin/bash

for number in {0..100..10}
do
  sudo python capture_packets.py --iface vethb4c550a  
done


