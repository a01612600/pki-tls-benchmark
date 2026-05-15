# PKI clásica en TLS — costo de verificación de certificados

Proyecto de investigación enfocado en evaluar empíricamente el costo operativo de la autenticación basada en certificados digitales en TLS 1.3, comparando algoritmos criptográficos clásicos y distintas profundidades de cadena X.509.

## Estado actual

Hasta este punto ya se validó la prueba mínima funcional del entorno experimental.

Se logró:

- configurar un entorno compatible con TLS 1.3,
- generar certificados base para RSA-2048 y ECDSA P-256,
- levantar un servidor TLS local,
- ejecutar handshakes exitosos,
- medir la latencia inicial del handshake,
- guardar los resultados en un archivo CSV,
- simplificar la ejecución mediante un `Makefile`.

Por ahora ya se probaron estas condiciones base:

- `rsa2048`, profundidad `1`
- `ec256`, profundidad `1`

## Entorno utilizado

El proyecto se está ejecutando en macOS con:

- Python 3.14.4
- OpenSSL 3.6.2
- entorno virtual local `.venv`

Para evitar conflictos con el Python y OpenSSL del sistema, se usa Homebrew junto con el entorno virtual del proyecto.

## Estructura actual del repositorio

```text
pki-tls-benchmark/
├── certs/
│   ├── ec256/
│   └── rsa2048/
├── scripts/
│   └── measure_once.py
├── data/
│   └── week1_results.csv
├── analysis/
├── paper/
├── Makefile
└── README.md

📊 Resultados experimentales (Semana 3–5)

Se completó la recolección sistemática de datos para evaluar el costo del handshake TLS bajo distintas configuraciones de certificados.

Configuración experimental
Algoritmos:
    RSA-2048
    RSA-4096
    ECDSA P-256
    ECDSA P-384
Profundidad de cadena:
    1 a 4 certificados
Total de condiciones:
    16 combinaciones (4 algoritmos × 4 profundidades)
Runs por condición:
    ~650
Total de observaciones:
    10,400
Configuración TLS:
    TLS 1.3
Session resumption deshabilitado (-no_ticket)
🧹 Calidad de datos

Se realizó validación preliminar:

Valores nulos: 0
Duplicados: 0
Coeficiente de variación (CV):
mayoría < 20%
algunas condiciones con alta variabilidad documentada

🔐 Integridad del dataset

El dataset final fue versionado y verificado mediante hash SHA-256:
5286440e0078ac054802b4fb3cb204941086f8501a2d9c4333f9fd8bd3575604


🖥️ Entorno experimental

Detalles completos en:

    analysis/system_info.txt

Incluye:

CPU
memoria
sistema operativo
versión de OpenSSL
versión de Python

📁 Dataset final

Ubicación:

data/final_dataset.csv

Estructura:

replica_id, algo, depth, run_id, handshake_ms, timestamp, cert_bytes, session_resumption