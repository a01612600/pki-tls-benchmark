SHELL := /bin/zsh

PYTHON := .venv/bin/python
OPENSSL_BIN := $(shell brew --prefix openssl@3)/bin/openssl
PORT ?= 4433

.PHONY: help check-env start-rsa start-ec256 measure-rsa measure-ec256 show-results free-port

help:
	@echo "Comandos disponibles:"
	@echo "  make check-env"
	@echo "  make start-rsa"
	@echo "  make start-ec256"
	@echo "  make measure-rsa RUN_ID=1"
	@echo "  make measure-ec256 RUN_ID=1"
	@echo "  make show-results"
	@echo "  make free-port"

check-env:
	@echo "Python usado:"
	@$(PYTHON) -V
	@echo ""
	@echo "OpenSSL usado por Python:"
	@$(PYTHON) -c "import ssl; print(ssl.OPENSSL_VERSION); print('HAS_TLSv1_3 =', ssl.HAS_TLSv1_3)"
	@echo ""
	@echo "OpenSSL del servidor:"
	@$(OPENSSL_BIN) version -a

start-rsa:
	$(OPENSSL_BIN) s_server -accept $(PORT) -cert certs/rsa2048/server.crt -key certs/rsa2048/server.key -tls1_3

start-ec256:
	$(OPENSSL_BIN) s_server -accept $(PORT) -cert certs/ec256/server.crt -key certs/ec256/server.key -tls1_3

measure-rsa:
	@if [ -z "$(RUN_ID)" ]; then echo "Falta RUN_ID. Usa: make measure-rsa RUN_ID=3"; exit 1; fi
	$(PYTHON) scripts/measure_once.py --algo rsa2048 --depth 1 --run-id $(RUN_ID) --cert certs/rsa2048/server.crt

measure-ec256:
	@if [ -z "$(RUN_ID)" ]; then echo "Falta RUN_ID. Usa: make measure-ec256 RUN_ID=3"; exit 1; fi
	$(PYTHON) scripts/measure_once.py --algo ec256 --depth 1 --run-id $(RUN_ID) --cert certs/ec256/server.crt

show-results:
	cat data/week1_results.csv

free-port:
	@PID=$$(lsof -ti :$(PORT)); \
	if [ -n "$$PID" ]; then \
		echo "Matando proceso en puerto $(PORT): $$PID"; \
		kill -9 $$PID; \
	else \
		echo "No hay proceso ocupando el puerto $(PORT)"; \
	fi