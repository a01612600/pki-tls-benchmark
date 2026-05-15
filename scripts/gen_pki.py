import sys
import subprocess
from pathlib import Path
import shutil
import csv

BASE_DIR = Path(__file__).resolve().parent.parent
CERTS_DIR = BASE_DIR / "certs"
DATA_DIR = BASE_DIR / "data"
OPENSSL = "openssl"


def run(cmd, cwd=None):
    result = subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        capture_output=True
    )
    if result.returncode != 0:
        print("ERROR ejecutando:", " ".join(cmd))
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError("Comando OpenSSL falló")
    return result


def get_algo_config(algo):
    if algo == "rsa2048":
        return {
            "keygen_cmd": [OPENSSL, "genpkey", "-algorithm", "RSA", "-out", "KEYFILE", "-pkeyopt", "rsa_keygen_bits:2048"],
            "label": "RSA-2048"
        }
    elif algo == "rsa4096":
        return {
            "keygen_cmd": [OPENSSL, "genpkey", "-algorithm", "RSA", "-out", "KEYFILE", "-pkeyopt", "rsa_keygen_bits:4096"],
            "label": "RSA-4096"
        }
    elif algo == "ec256":
        return {
            "keygen_cmd": [OPENSSL, "genpkey", "-algorithm", "EC", "-pkeyopt", "ec_paramgen_curve:P-256", "-out", "KEYFILE"],
            "label": "ECDSA-P256"
        }
    elif algo == "ec384":
        return {
            "keygen_cmd": [OPENSSL, "genpkey", "-algorithm", "EC", "-pkeyopt", "ec_paramgen_curve:P-384", "-out", "KEYFILE"],
            "label": "ECDSA-P384"
        }
    else:
        raise ValueError(f"Algoritmo no soportado: {algo}")


def gen_key(algo, out_key):
    config = get_algo_config(algo)
    cmd = [part if part != "KEYFILE" else str(out_key) for part in config["keygen_cmd"]]
    run(cmd)


def write_ext_file(path, is_ca, pathlen=None):
    lines = [
        "basicConstraints = critical," + ("CA:true" if is_ca else "CA:false"),
        "keyUsage = critical," + ("keyCertSign, cRLSign" if is_ca else "digitalSignature, keyEncipherment"),
        "subjectKeyIdentifier = hash",
        "authorityKeyIdentifier = keyid,issuer"
    ]
    if is_ca and pathlen is not None:
        lines[0] = f"basicConstraints = critical,CA:true,pathlen:{pathlen}"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def gen_csr(key_file, csr_file, cn):
    run([
        OPENSSL, "req", "-new",
        "-key", str(key_file),
        "-out", str(csr_file),
        "-subj", f"/CN={cn}"
    ])


def self_sign_root(key_file, cert_file, cn, ext_file):
    run([
        OPENSSL, "x509", "-req",
        "-in", str(cert_file.with_suffix(".csr")),
        "-signkey", str(key_file),
        "-out", str(cert_file),
        "-days", "365",
        "-extfile", str(ext_file)
    ])


def sign_cert(csr_file, ca_cert, ca_key, out_cert, ext_file):
    run([
        OPENSSL, "x509", "-req",
        "-in", str(csr_file),
        "-CA", str(ca_cert),
        "-CAkey", str(ca_key),
        "-CAcreateserial",
        "-out", str(out_cert),
        "-days", "365",
        "-extfile", str(ext_file)
    ])


def append_csv_row(csv_path, row):
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = csv_path.exists()
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["algo", "depth", "cert_name", "cert_bytes"])
        writer.writerow(row)


def generate_pki(algo, depth):
    if depth not in {1, 2, 3, 4}:
        raise ValueError("DEPTH debe ser 1, 2, 3 o 4")

    scenario_dir = CERTS_DIR / f"{algo}_depth{depth}"

    if scenario_dir.exists():
        shutil.rmtree(scenario_dir)
    scenario_dir.mkdir(parents=True, exist_ok=True)

    csv_path = DATA_DIR / "cert_sizes_base.csv"

    # Root
    root_key = scenario_dir / "root_key.pem"
    root_csr = scenario_dir / "root.csr"
    root_cert = scenario_dir / "root_cert.pem"
    root_ext = scenario_dir / "root_ext.cnf"

    gen_key(algo, root_key)
    gen_csr(root_key, root_csr, "RootCA")
    # pathlen = depth-1 intermediates máximos debajo del root
    write_ext_file(root_ext, is_ca=True, pathlen=max(depth - 1, 0))
    run([
        OPENSSL, "x509", "-req",
        "-in", str(root_csr),
        "-signkey", str(root_key),
        "-out", str(root_cert),
        "-days", "365",
        "-extfile", str(root_ext)
    ])

    #append_csv_row(csv_path, [algo, depth, "root_cert.pem", root_cert.stat().st_size])

    parent_cert = root_cert
    parent_key = root_key
    intermediates = []

    # depth 1 = root + leaf
    # depth 2 = root + int1 + leaf
    # depth 3 = root + int1 + int2 + leaf
    # depth 4 = root + int1 + int2 + int3 + leaf
    num_intermediates = depth - 1

    for i in range(1, num_intermediates + 1):
        int_key = scenario_dir / f"int{i}_key.pem"
        int_csr = scenario_dir / f"int{i}.csr"
        int_cert = scenario_dir / f"int{i}_cert.pem"
        int_ext = scenario_dir / f"int{i}_ext.cnf"

        gen_key(algo, int_key)
        gen_csr(int_key, int_csr, f"Intermediate{i}")

        remaining_below = num_intermediates - i
        write_ext_file(int_ext, is_ca=True, pathlen=remaining_below)

        sign_cert(int_csr, parent_cert, parent_key, int_cert, int_ext)

        #append_csv_row(csv_path, [algo, depth, int_cert.name, int_cert.stat().st_size])

        intermediates.append(int_cert)
        parent_cert = int_cert
        parent_key = int_key

    # Leaf
    leaf_key = scenario_dir / "leaf_key.pem"
    leaf_csr = scenario_dir / "leaf.csr"
    leaf_cert = scenario_dir / "leaf_cert.pem"
    leaf_ext = scenario_dir / "leaf_ext.cnf"

    gen_key(algo, leaf_key)
    gen_csr(leaf_key, leaf_csr, "LeafServer")
    write_ext_file(leaf_ext, is_ca=False)

    sign_cert(leaf_csr, parent_cert, parent_key, leaf_cert, leaf_ext)

    #append_csv_row(csv_path, [algo, depth, leaf_cert.name, leaf_cert.stat().st_size])

    # chain.pem = intermediates concatenados
    chain_pem = scenario_dir / "chain.pem"
    with open(chain_pem, "w", encoding="utf-8") as f:
        for cert in intermediates:
            f.write(cert.read_text(encoding="utf-8"))

    # verify
    verify_cmd = [
        OPENSSL, "verify",
        "-CAfile", str(root_cert)
    ]

    if intermediates:
        verify_cmd += ["-untrusted", str(chain_pem)]

    verify_cmd += [str(leaf_cert)]

    result = run(verify_cmd)

    print("Escenario generado:", scenario_dir)
    print("Verificación OpenSSL:")
    print(result.stdout.strip())

    csv_path = DATA_DIR / "cert_sizes_base.csv"

    root_bytes = root_cert.stat().st_size
    leaf_bytes = leaf_cert.stat().st_size
    int_bytes_total = sum(cert.stat().st_size for cert in intermediates)
    chain_bytes = int_bytes_total + leaf_bytes

    file_exists = csv_path.exists()

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "algo",
                "depth",
                "root_bytes",
                "int_bytes_total",
                "leaf_bytes",
                "chain_bytes"
            ])

        writer.writerow([
            algo,
            depth,
            root_bytes,
            int_bytes_total,
            leaf_bytes,
            chain_bytes
        ])

if __name__ == "__main__":
    algos = ["rsa2048", "rsa4096", "ec256", "ec384"]
    depths = [1, 2, 3, 4]

    for algo in algos:
        for depth in depths:
            print(f"\n--- Generando {algo} depth {depth} ---")
            generate_pki(algo, depth)
