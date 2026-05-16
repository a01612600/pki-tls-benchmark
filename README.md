# PKI clásica en TLS — costo de verificación de certificados

Proyecto de investigación enfocado en evaluar empíricamente el costo computacional de la verificación de certificados digitales en TLS 1.3, comparando distintos algoritmos criptográficos clásicos y diferentes profundidades de cadena X.509.

---

# Objetivo

Analizar cómo cambia la latencia del handshake TLS conforme aumenta:

- el tamaño y tipo del algoritmo criptográfico,
- la profundidad de la cadena de certificados,
- y el tamaño total de los certificados intercambiados.

El proyecto compara algoritmos RSA y ECDSA bajo condiciones controladas y mediciones repetidas.

---

# Configuración experimental

## Algoritmos evaluados

- RSA-2048
- RSA-4096
- ECDSA P-256 (`ec256`)
- ECDSA P-384 (`ec384`)

## Profundidad de cadena

Se evaluaron cadenas X.509 con profundidad:

- 1
- 2
- 3
- 4 certificados

## Total de condiciones

- 16 combinaciones experimentales  
  `(4 algoritmos × 4 profundidades)`

## Mediciones

- ~650 handshakes por condición
- 10,400 observaciones totales

## Configuración TLS

- TLS 1.3
- Session resumption deshabilitado (`-no_ticket`)
- Servidor TLS local usando OpenSSL

---

# Resultados obtenidos

Durante las semanas 3–5 se completó la recolección y validación del dataset experimental.

Se logró:

- generar cadenas de certificados automáticamente,
- ejecutar handshakes TLS repetidos,
- medir latencia del handshake,
- registrar tamaño de certificados,
- automatizar corridas experimentales,
- generar análisis estadísticos y visualizaciones,
- validar consistencia del dataset.

---

# Calidad de datos

Se realizó una validación preliminar del dataset.

## Verificaciones realizadas

- Valores nulos: `0`
- Duplicados: `0`
- Todas las condiciones completas
- Distribución balanceada de observaciones

## Coeficiente de variación (CV)

La mayoría de las condiciones presentaron:

- `CV < 20%`

Algunas condiciones con RSA-4096 y ciertas profundidades mostraron mayor variabilidad, la cual quedó documentada mediante:

- boxplots,
- análisis de outliers,
- heatmaps de CV,
- gráficas con barras de error.

---

# Integridad del dataset

El dataset final fue verificado mediante hash SHA-256.

```text
5286440e0078ac054802b4fb3cb204941086f8501a2d9c4333f9fd8bd3575604


🖥️ Entorno experimental

El proyecto se ejecutó en macOS usando:

Python 3.14.4
OpenSSL 3.6.2
entorno virtual .venv

Para evitar conflictos con dependencias del sistema se utilizó:

Homebrew
entorno virtual local de Python

La información completa del entorno se encuentra en:

    analysis/system_info.txt

Incluye:

CPU
memoria RAM
sistema operativo
versión de OpenSSL
versión de Python

📁 Dataset final

Ubicación:

    data/final_dataset.csv

Estructura del dataset:

    replica_id, algo, depth, run_id, handshake_ms, timestamp, cert_bytes, session_resumption