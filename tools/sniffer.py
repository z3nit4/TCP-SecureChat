from scapy.all import sniff, TCP, IP
import datetime

output_file = "sniffed_messages.txt"

def print_packet(pkt):
    if TCP in pkt and (pkt[TCP].sport == 8000 or pkt[TCP].dport == 8000):
        payload = bytes(pkt[TCP].payload)
        if payload:
            try:
                message = payload.decode('ascii', errors='ignore')
            except:
                message = "<non-decodable data>"
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            output = f"[{timestamp}] {pkt[IP].src}:{pkt[TCP].sport} -> {pkt[IP].dst}:{pkt[TCP].dport} | {message}"
            
            print(output)
            with open(output_file, "a") as f:
                f.write(output + "\n")

print(f"Sniffer active on eth0 (209.38.232.217), logging to {output_file}")

sniff(
    filter="tcp port 8000",
    prn=print_packet,
    store=0,
    iface=["lo","eth0"]  # listen on loopback + public interface
)