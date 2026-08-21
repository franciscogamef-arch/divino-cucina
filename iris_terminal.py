#!/usr/bin/env python3
"""
IRIS — Modo Terminal (sem pygame/OpenGL)
Rode com:  python3 iris_terminal.py
           python3 iris_terminal.py --voz    (ativa microfone)
"""
import sys, signal, threading
from pathlib import Path

# ─── garante que a pasta do projeto está no path ─────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))

from iris_core.config import CFG
from iris_core.monitor import Monitor
from iris_core.memoria import Memoria
from iris_core.ia import IA
from iris_core.acoes import Acoes
from iris_core.processador import Processador

CYAN  = "\033[96m"
GREEN = "\033[92m"
GRAY  = "\033[90m"
BOLD  = "\033[1m"
RST   = "\033[0m"
YELLOW = "\033[93m"
RED    = "\033[91m"

BANNER = f"""{CYAN}{BOLD}
╔══════════════════════════════════════════╗
║           IRIS — Modo Terminal           ║
║  'ajuda' → lista de comandos            ║
║  'sair' / Ctrl+C → encerra             ║
╚══════════════════════════════════════════╝{RST}"""


class IRISTerminal:
    def __init__(self, usar_voz: bool = False):
        self.usuario = CFG.get("USUARIO", "Francisco")
        print(f"{GRAY}Inicializando IRIS...{RST}", end="\r", flush=True)
        self.mon  = Monitor()
        self.mem  = Memoria()
        self.ia   = IA(self.usuario, self.mem)
        self.acoes = Acoes(self.usuario, self.mem, self.ia)
        self.voz  = None
        if usar_voz:
            try:
                from iris_core.voz import Voz
                self.voz = Voz()
                print(f"{GREEN}Microfone ativado.{RST}")
            except Exception as e:
                print(f"{YELLOW}Voz não disponível: {e}{RST}")
        self.proc = Processador(self.usuario, self.mem, self.ia,
                                self.acoes, self.mon, self.voz)
        self.acoes.processador = self.proc
        self.acoes.mon = self.mon

    def _prompt(self) -> str:
        return f"{CYAN}{BOLD}[{self.usuario}]>{RST} "

    def _print_resposta(self, texto: str):
        print()
        for linha in str(texto).splitlines():
            print(f"  {GREEN}IRIS:{RST} {linha}")
        print()

    def rodar(self):
        print(BANNER)
        print(f"  Olá, {BOLD}{self.usuario}{RST}! Pronto para ouvir.\n")
        signal.signal(signal.SIGINT, lambda *_: self._encerrar())
        while True:
            try:
                entrada = input(self._prompt()).strip()
            except (EOFError, KeyboardInterrupt):
                self._encerrar()
                break
            if not entrada:
                continue
            if entrada.lower() in ("sair", "exit", "quit", "tchau", "até logo"):
                self._encerrar()
                break
            if entrada.lower() in ("ajuda", "help", "comandos", "lista"):
                self._print_resposta(self.proc.LISTA_COMANDOS)
                continue
            try:
                resposta = self.proc.processar(entrada)
                self._print_resposta(resposta or "(sem resposta)")
            except Exception as e:
                print(f"  {RED}Erro:{RST} {e}\n")

    def _encerrar(self):
        print(f"\n{GRAY}IRIS encerrada. Até logo!{RST}")
        sys.exit(0)


if __name__ == "__main__":
    usar_voz = "--voz" in sys.argv or "-v" in sys.argv
    IRISTerminal(usar_voz=usar_voz).rodar()
