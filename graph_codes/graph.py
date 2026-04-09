from scapy.all import *
import matplotlib.pyplot as plt
import numpy as np

files = {
    "Low": "low.pcapng",
    "Medium": "medium.pcapng",
    "High": "high.pcapng"
}

# ---- Convert timestamps safely to float
def get_times(pkts):
    return np.array([float(pkt.time) for pkt in pkts])

def compute_iat(times):
    if len(times) > 1:
        return np.diff(times)
    return np.array([])

# ---- ICMP RTT calculation
def compute_rtt_icmp(pkts):
    req = {}
    rtt = []
    for pkt in pkts:
        if ICMP in pkt:
            if pkt[ICMP].type == 8:  # request
                req[pkt[ICMP].seq] = float(pkt.time)
            elif pkt[ICMP].type == 0:  # reply
                if pkt[ICMP].seq in req:
                    rtt.append(float(pkt.time) - req[pkt[ICMP].seq])
    return np.array(rtt)

def plot(x, y, title, xlabel, ylabel, fname):
    plt.figure()
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.savefig(fname)
    plt.close()

graph_id = 1

latency_summary = []
labels = []

# ================= MAIN LOOP =================
for label, file in files.items():
    pkts = rdpcap(file)
    times = get_times(pkts)

    if len(times) == 0:
        continue

    times = times - times[0]
    iat = compute_iat(times)
    rtt = compute_rtt_icmp(pkts)

    # ---- 1–3: Latency vs Time (IAT)
    if len(iat) > 0:
        plot(times[1:], iat,
             f"{label}: Latency vs Time (IAT)",
             "Time (s)", "Latency (s)",
             f"graph{graph_id}.png")
    graph_id += 1

    # ---- 4–6: RTT vs Packet Index
    if len(rtt) > 0:
        plot(range(len(rtt)), rtt,
             f"{label}: RTT vs Packet",
             "Packet Index", "RTT (s)",
             f"graph{graph_id}.png")
    elif len(iat) > 0:
        plot(range(len(iat)), iat,
             f"{label}: RTT Proxy (IAT)",
             "Packet Index", "Latency (s)",
             f"graph{graph_id}.png")
    graph_id += 1

    # ---- 7–9: Latency Distribution
    if len(iat) > 0:
        plt.figure()
        plt.hist(iat, bins=40)
        plt.title(f"{label}: Latency Distribution")
        plt.xlabel("Latency (s)")
        plt.ylabel("Frequency")
        plt.savefig(f"graph{graph_id}.png")
        plt.close()
    graph_id += 1

    # ---- 10–12: Moving Average Latency
    if len(iat) > 5:
        window = 5
        ma = np.convolve(iat, np.ones(window)/window, mode='valid')
        plot(range(len(ma)), ma,
             f"{label}: Moving Avg Latency",
             "Packet Index", "Latency (s)",
             f"graph{graph_id}.png")
    graph_id += 1

    # ---- 13–15: Latency Trend
    if len(iat) > 0:
        plot(range(len(iat)), iat,
             f"{label}: Latency Trend",
             "Packet Index", "Latency (s)",
             f"graph{graph_id}.png")
    graph_id += 1

    # ---- Store average latency
    if len(iat) > 0:
        latency_summary.append(float(np.mean(iat)))
    else:
        latency_summary.append(0)

    labels.append(label)

# ================= COMPARISON GRAPHS =================

# ---- 16: Average Latency
plt.figure()
plt.bar(labels, latency_summary)
plt.title("Average Latency vs Traffic Load")
plt.ylabel("Latency (s)")
plt.savefig("graph16.png")
plt.close()

# ---- 17: Maximum Latency
max_vals = []
for f in files.values():
    pkts = rdpcap(f)
    t = get_times(pkts)
    if len(t) > 1:
        t = t - t[0]
        max_vals.append(float(np.max(np.diff(t))))
    else:
        max_vals.append(0)

plt.figure()
plt.bar(labels, max_vals)
plt.title("Maximum Latency vs Traffic Load")
plt.ylabel("Latency (s)")
plt.savefig("graph17.png")
plt.close()

# ---- 18: Latency Variation (Std Dev)
std_vals = []
for f in files.values():
    pkts = rdpcap(f)
    t = get_times(pkts)
    if len(t) > 1:
        t = t - t[0]
        std_vals.append(float(np.std(np.diff(t))))
    else:
        std_vals.append(0)

plt.figure()
plt.bar(labels, std_vals)
plt.title("Latency Variation (Std Dev)")
plt.ylabel("Latency (s)")
plt.savefig("graph18.png")
plt.close()

# ---- 19: Latency Trend Comparison
plt.figure()
for label, file in files.items():
    pkts = rdpcap(file)
    t = get_times(pkts)
    if len(t) > 1:
        t = t - t[0]
        iat = np.diff(t)
        plt.plot(iat, label=label)

plt.legend()
plt.title("Latency Trend Comparison")
plt.ylabel("Latency (s)")
plt.savefig("graph19.png")
plt.close()

# ---- 20: Cumulative Latency
plt.figure()
for label, file in files.items():
    pkts = rdpcap(file)
    t = get_times(pkts)
    if len(t) > 1:
        t = t - t[0]
        iat = np.diff(t)
        plt.plot(np.cumsum(iat), label=label)

plt.legend()
plt.title("Cumulative Latency Growth")
plt.ylabel("Latency (s)")
plt.savefig("graph20.png")
plt.close()

print("✅ All 20 latency-based graphs generated successfully!")