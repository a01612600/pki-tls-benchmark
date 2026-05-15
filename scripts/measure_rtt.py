import socket
import ssl
import time
import csv
from pathlib import Path

HOST = "localhost"

tests = [
    {"algorithm": "RSA-2048", "port": 4433},
    {"algorithm": "ECDSA-P256", "port": 4434},
]

output_file = Path("../data/results.csv")
output_file.parent.mkdir(parents=True, exist_ok=True)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
context.minimum_version = ssl.TLSVersion.TLSv1_3
context.maximum_version = ssl.TLSVersion.TLSv1_3

rows = []

for test in tests:
    algorithm = test["algorithm"]
    port = test["port"]

    for i in range(2):
        start = time.perf_counter()

        with socket.create_connection((HOST, port), timeout=3) as sock:
            sock.settimeout(3)
            with context.wrap_socket(sock, server_hostname=HOST) as ssock:
                ssock.settimeout(3)

        end = time.perf_counter()
        rows.append([algorithm, port, i + 1, end - start])

with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["algorithm", "port", "run_id", "rtt_seconds"])
    writer.writerows(rows)

print("CSV generado en:", output_file)