# Network Latency Analysis using Wireshark and Scapy

This repository contains the implementation and analysis of network latency under different traffic conditions. The experiment was performed using Wireshark for packet capture and Python (Scapy) for controlled traffic generation and graph-based analysis.

## Project Overview

The aim of this project is to study how network latency behaves under different traffic conditions such as low, medium, and high traffic. Controlled traffic was generated using Scapy scripts, and the captured packet data was analyzed to observe delay patterns and variations.

## Tools Used

- Wireshark
- Python
- Scapy
- Matplotlib
- NumPy

## Traffic Generation

Network traffic was generated using TCP SYN packets by controlling the number of packets and delay between them.

- Low Traffic: 50 packets with 0.2 seconds delay  
- Medium Traffic: 150 packets with 0.05 seconds delay  
- High Traffic: 500 packets with 0.005 seconds delay  

These conditions simulate increasing levels of network load.

## Packet Capture

Wireshark was used to capture packets for each traffic condition. Separate `.pcapng` files were created for low, medium, and high traffic scenarios.

## Graph Generation

A Python script was used to analyze the captured packet data and generate latency-related graphs. The analysis includes:

- Extraction of packet timestamps  
- Calculation of inter-arrival time (used as a latency indicator)  
- RTT calculation where possible  
- Generation of 20 graphs to visualize latency behavior  

## Observations

- Latency does not increase strictly in a linear manner with traffic load  
- Low traffic can still produce occasional high latency spikes  
- Medium traffic introduces moderate variability  
- High traffic results in frequent fluctuations
- Most packets have low latency, but a few significantly affect overall performance



1. Install required libraries:
