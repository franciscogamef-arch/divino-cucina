#!/usr/bin/env python3
"""
IRIS v20.0 — Assistente Pessoal Avançada (modular)
Francisco | Linux Policorp

Agora organizada em módulos dentro de iris_core/ — mais fácil de manter,
testar e expandir, SEM perder nenhuma função da v7 à v19.
Rode com: python3 iris.py
"""
from iris_core.app import IRIS

if __name__ == "__main__":
    IRIS().rodar()
