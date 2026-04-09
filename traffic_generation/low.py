from scapy.all import IP, TCP, send
import time

# -------- CONFIGURATION --------
target_ip = "127.0.0.1"     # Use localhost (safe) OR change to your target IP
target_port = 80            # Common open port (HTTP)

packet_count = 50           # Number of packets (low traffic)
delay = 0.2                 # Delay between packets (slow rate)

# -------- PACKET DEFINITION --------
packet = IP(dst=target_ip)/TCP(dport=target_port, flags="S")

print("Starting LOW traffic generation...")

# -------- TRAFFIC GENERATION --------
for i in range(packet_count):
    send(packet, verbose=0)
    print(f"Packet {i+1} sent")
    time.sleep(delay)

print("LOW traffic generation completed.")