import os, sys, json, queue, threading, subprocess, socket, requests, atexit
import datetime, random, time, math, shutil, asyncio, re, tempfile
from pathlib import Path
import logging


# ══════════════════════════════════════════════════════════════
#  REDE NEURONAL TERNÁRIA — simulador de neurônios (Projeto NTM!)
#  Estados: -1, 0, +1 — igual ao seu neurônio físico no protoboard.
#  Inclui: neurônios spiking integra-e-dispara + memória Hopfield
#  ternária para guardar e relembrar padrões.
# ══════════════════════════════════════════════════════════════
class RedeNeuronal:
    SIMB = {-1: "-", 0: "o", 1: "+"}

    def __init__(self, n=16, arq="iris_rede.json"):
        self.n = n
        self.arq = Path(arq)
        self.W = [[0.0] * n for _ in range(n)]   # pesos Hopfield
        self.padroes = []                          # padrões memorizados
        self._carregar()

    # ── persistência: a rede LEMBRA entre sessões ──
    def _carregar(self):
        if self.arq.exists():
            try:
                d = json.loads(self.arq.read_text(encoding="utf-8"))
                self.W = d.get("W", self.W)
                self.padroes = d.get("padroes", [])
                self.n = len(self.W)
            except Exception as _e:
                logging.exception(_e)

    def _salvar(self):
        try:
            self.arq.write_text(json.dumps(
                {"W": self.W, "padroes": self.padroes}), encoding="utf-8")
        except Exception as _e:
            logging.exception(_e)

    def _texto_para_ternario(self, texto):
        """Converte string de +, -, o/0 em vetor ternário. Completa com 0."""
        v = []
        for c in texto.strip():
            if c == "+":
                v.append(1)
            elif c == "-":
                v.append(-1)
            elif c in ("o", "0", "O"):
                v.append(0)
        v = v[:self.n]
        while len(v) < self.n:
            v.append(0)
        return v

    def _vetor_para_texto(self, v):
        return "".join(self.SIMB[x] for x in v)

    # ── HOPFIELD TERNÁRIO: memória associativa ──
    def treinar(self, padrao_txt):
        """Memoriza um padrão (regra de Hebb): 'treina rede ++--oo++'"""
        v = self._texto_para_ternario(padrao_txt)
        if all(x == 0 for x in v):
            return "Padrão vazio! Use os símbolos + - o (ex: ++--oo++)"
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    self.W[i][j] += v[i] * v[j] / self.n
        self.padroes.append(self._vetor_para_texto(v))
        if len(self.padroes) > 12:
            self.padroes = self.padroes[-12:]
        self._salvar()
        return ("Padrão memorizado na rede Hopfield ternária!\n" +
                self._vetor_para_texto(v) +
                "\nTotal de padrões: " + str(len(self.padroes)) +
                "\nTeste com ruído: 'lembra padrao " +
                self._vetor_para_texto(v)[:self.n // 2] + "...'")

    def lembrar(self, padrao_txt, max_iter=10):
        """Recupera padrão completo a partir de versão com ruído/incompleta."""
        v = self._texto_para_ternario(padrao_txt)
        entrada = self._vetor_para_texto(v)
        for _ in range(max_iter):
            novo = []
            for i in range(self.n):
                soma = sum(self.W[i][j] * v[j] for j in range(self.n))
                # Ativação ternária com zona morta — igual seu circuito físico
                novo.append(1 if soma > 0.15 else -1 if soma < -0.15 else 0)
            if novo == v:
                break
            v = novo
        saida = self._vetor_para_texto(v)
        casou = saida in self.padroes
        return ("Entrada:  " + entrada +
                "\nLembrei:  " + saida +
                ("\n>>> Padrão reconhecido na memória!" if casou
                 else "\n(estado convergido — não bate exato com nenhum padrão salvo)"))

    # ── SPIKING: integra-e-dispara com vazamento ──
    def simular_spiking(self, n_neuronios=8, passos=24):
        """Simula neurônios que acumulam potencial e disparam — raster ASCII."""
        n_neuronios = max(2, min(n_neuronios, 16))
        passos = max(5, min(passos, 40))
        potencial = [0.0] * n_neuronios
        limiar = 1.0
        vazamento = 0.90
        linhas = [[] for _ in range(n_neuronios)]
        disparos = 0
        for t in range(passos):
            for i in range(n_neuronios):
                potencial[i] = potencial[i] * vazamento + random.uniform(0.0, 0.38)
                # excitação lateral: vizinho que disparou empurra
                if t > 0 and linhas[(i - 1) % n_neuronios][-1] == "|":
                    potencial[i] += 0.25
                if potencial[i] >= limiar:
                    linhas[i].append("|")     # DISPARO!
                    potencial[i] = 0.0        # reset (período refratário)
                    disparos += 1
                elif potencial[i] > limiar * 0.6:
                    linhas[i].append("+")     # quase lá
                elif potencial[i] > limiar * 0.25:
                    linhas[i].append("o")
                else:
                    linhas[i].append("-")
        raster = "\n".join(
            "N" + str(i + 1).zfill(2) + " " + "".join(l)
            for i, l in enumerate(linhas))
        taxa = round(disparos / (n_neuronios * passos) * 100)
        return ("Rede spiking ternária — " + str(n_neuronios) + " neurônios, " +
                str(passos) + " passos:\n" + raster +
                "\n| = disparo  + = quase  o = carregando  - = repouso" +
                "\nDisparos: " + str(disparos) + " (taxa " + str(taxa) + "%)" +
                "\nMesma lógica do seu neurônio no protoboard, Francisco!")

    def status(self):
        energia = sum(abs(w) for linha in self.W for w in linha)
        return ("Rede neuronal ternária (NTM):\n" +
                str(self.n) + " neurônios Hopfield | " +
                str(len(self.padroes)) + " padrões memorizados | " +
                "energia sináptica: " + str(round(energia, 2)) +
                ("\nPadrões:\n" + "\n".join("  " + p for p in self.padroes[-6:])
                 if self.padroes else "\nNenhum padrão ainda — use: treina rede ++--oo++"))

    def esquecer(self):
        self.W = [[0.0] * self.n for _ in range(self.n)]
        self.padroes = []
        self._salvar()
        return "Rede zerada! Sinapses limpas, pronta para aprender de novo."
