import subprocess
import socket
import ssl
import time
import csv
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
CERTS_DIR = BASE_DIR / "certs"
DATA_DIR = BASE_DIR / "data"

HOST = "127.0.0.1"
PORT = 4443

ALGOS = ["rsa2048", "rsa4096", "ec256", "ec384"]
DEPTHS = [1, 2, 3, 4]

WARMUP_RUNS = 20
MEASURE_RUNS = 650   # 650 × 16 = 10,400 filas
REPLICA_ID = 1       # cambia a 2 o 3 si haces más réplicas


def get_cert_bytes(algo, depth):
    cert_summary = DATA_DIR / "cert_sizes_base.csv"

    with open(cert_summary, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["algo"] == algo and int(row["depth"]) == depth:
                return int(row["chain_bytes"])

    raise ValueError(f"No encontré cert_bytes para {algo} depth {depth}")


def start_server(cert_dir):
    leaf_cert = cert_dir / "leaf_cert.pem"
    leaf_key = cert_dir / "leaf_key.pem"
    chain_file = cert_dir / "chain.pem"

    cmd = [
        "openssl", "s_server",
        "-accept", str(PORT),
        "-cert", str(leaf_cert),
        "-key", str(leaf_key),
        "-tls1_3",
        "-www",
        "-quiet",
        "-no_ticket"
    ]

    if chain_file.exists() and chain_file.stat().st_size > 0:
        cmd.extend(["-cert_chain", str(chain_file)])

    return subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )


def single_handshake(cert_dir):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_REQUIRED

    root_cert = cert_dir / "root_cert.pem"
    context.load_verify_locations(cafile=str(root_cert))

    context.minimum_version = ssl.TLSVersion.TLSv1_3
    context.maximum_version = ssl.TLSVersion.TLSv1_3

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    start = time.perf_counter()

    ssl_sock = context.wrap_socket(sock, server_hostname="localhost")

    end = time.perf_counter()

    ssl_sock.close()
    return (end - start) * 1000


def run_condition(algo, depth, output_csv):
    cert_dir = CERTS_DIR / f"{algo}_depth{depth}"

    if not cert_dir.exists():
        raise FileNotFoundError(f"No existe: {cert_dir}")

    cert_bytes = get_cert_bytes(algo, depth)

    print(f"\n--- Running {algo} depth {depth} ---")

    server = start_server(cert_dir)

    try:
        time.sleep(2)

        if server.poll() is not None:
            out, err = server.communicate()
            print("s_server se cerró antes de tiempo.")
            print("STDOUT:", out)
            print("STDERR:", err)
            raise RuntimeError("No se pudo levantar s_server")

        for _ in range(WARMUP_RUNS):
            single_handshake(cert_dir)

        file_exists = output_csv.exists()

        with open(output_csv, "a", newline="") as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow([
                    "replica_id",
                    "algo",
                    "depth",
                    "run_id",
                    "handshake_ms",
                    "timestamp",
                    "cert_bytes",
                    "session_resumption"
                ])

            for run_id in range(1, MEASURE_RUNS + 1):
                handshake_ms = single_handshake(cert_dir)
                timestamp = datetime.now().isoformat(timespec="seconds")

                writer.writerow([
                    REPLICA_ID,
                    algo,
                    depth,
                    run_id,
                    handshake_ms,
                    timestamp,
                    cert_bytes,
                    "OFF"
                ])

                if run_id % 50 == 0:
                    print(f"{algo} depth {depth} | Run {run_id}/{MEASURE_RUNS}")

    finally:
        server.terminate()
        server.wait()

    print(f"Finished {algo} depth {depth}")


def main():
    output_csv = DATA_DIR / "week5_dataset.csv"

    if output_csv.exists():
        print(f"Appending to existing file: {output_csv}")
    else:
        print(f"Creating new file: {output_csv}")

    for algo in ALGOS:
        for depth in DEPTHS:
            run_condition(algo, depth, output_csv)

    print(f"\nDataset generated at: {output_csv}")


if __name__ == "__main__":
    main()