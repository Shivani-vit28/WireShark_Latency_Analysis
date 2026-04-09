from scapy.all import IP, TCP, send
import time

# -------- CONFIGURATION --------
target_ip = "127.0.0.1"     # Same as low.py
target_port = 80

packet_count = 200          # More packets
delay = 0.05                # Moderate delay

# -------- PACKET --------
packet = IP(dst=target_ip)/TCP(dport=target_port, flags="S")

print("Starting MEDIUM traffic generation...")

# -------- TRAFFIC --------
for i in range(packet_count):
    send(packet, verbose=0)
    print(f"Packet {i+1} sent")
    time.sleep(delay)

print("MEDIUM traffic generation completed.")