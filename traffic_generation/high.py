from scapy.all import IP, TCP, send

# -------- CONFIGURATION --------
target_ip = "127.0.0.1"     # Same target
target_port = 80

packet_count = 1000         # High number of packets

# -------- PACKET --------
packet = IP(dst=target_ip)/TCP(dport=target_port, flags="S")

print("Starting HIGH traffic generation...")

# -------- TRAFFIC --------
for i in range(packet_count):
    send(packet, verbose=0)
    # No delay → maximum speed

print("HIGH traffic generation completed.")