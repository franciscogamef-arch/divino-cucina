import os, sys, json, queue, threading, subprocess, socket, requests, atexit
import datetime, random, time, math, shutil, asyncio, re, tempfile
from pathlib import Path
import logging


# ══════════════════════════════════════════════════════════════
#  GERENCIADORA DE PROJETOS — a IRIS coordena seus projetos
#  Cada projeto tem tarefas, diário de progresso e contexto que a
#  IA usa para responder. Tudo persiste em iris_projetos.json.
# ══════════════════════════════════════════════════════════════
class GerenciadorProjetos:
    SEED = {
        "iris": {
            "desc": "Assistente pessoal estilo Jarvis em Python (este programa!)",
            "tarefas": [], "diario": [], "criado": "pré-existente"},
        "ntm": {
            "desc": ("Neural Ternary Memory — computação ternária e neuromórfica. "
                     "Linguagem NTM em C, neurônio físico no protoboard, "
                     "rede spiking no FPGA Cyclone IV"),
            "tarefas": [{"txt": "Resolver cabo JTAG (comprar jumpers dupont fêmea-fêmea)",
                         "feita": False}],
            "diario": [], "criado": "pré-existente"},
        "exoesqueleto": {
            "desc": ("Bota robótica assistiva com servos 80kg, Arduino Mega, "
                     "articulação de joelho e tornozelo rotativo"),
            "tarefas": [], "diario": [], "criado": "pré-existente"},
        "impressora3d": {
            "desc": ("Impressora 3D do zero: Arduino Mega 2560 + RAMPS 1.4 + Marlin, "
                     "frame Prusa i3 em alumínio 2020/2040"),
            "tarefas": [], "diario": [], "criado": "pré-existente"},
        "livro": {
            "desc": ("Érebo Kingdoms — fantasia sombria brasileira, isekai +18. "
                     "Protagonista Adam, universo Aethelgard, Monarca Visha"),
            "tarefas": [], "diario": [], "criado": "pré-existente"},
    }

    def __init__(self, arq="iris_projetos.json"):
        self.arq = Path(arq)
        self.ativo = None
        self.dados = self._carregar()

    def _carregar(self):
        if self.arq.exists():
            try:
                return json.loads(self.arq.read_text(encoding="utf-8"))
            except Exception as _e:
                logging.exception(_e)
        d = json.loads(json.dumps(self.SEED))  # cópia profunda
        self._persistir(d)
        return d

    def _persistir(self, dados=None):
        try:
            self.arq.write_text(json.dumps(dados or self.dados,
                                           ensure_ascii=False, indent=2),
                                encoding="utf-8")
        except Exception as _e:
            logging.exception(_e)

    def _achar(self, nome):
        """Busca tolerante: 'exo', 'impressora', '3d' acham o projeto certo."""
        n = nome.lower().strip()
        if n in self.dados:
            return n
        for k in self.dados:
            if n in k or k in n or n in self.dados[k]["desc"].lower():
                return k
        return None

    def listar(self):
        if not self.dados:
            return "Nenhum projeto. Use: registra projeto nome: descrição"
        linhas = ["SEUS PROJETOS:"]
        for k, v in self.dados.items():
            pend = sum(1 for t in v["tarefas"] if not t["feita"])
            marca = ">>> " if k == self.ativo else "    "
            linhas.append(marca + k.upper() + " — " + v["desc"][:60] +
                          (" | " + str(pend) + " tarefa(s) pendente(s)" if pend else ""))
        linhas.append("\nAtive um com: projeto [nome]")
        return "\n".join(linhas)

    def ativar(self, nome):
        k = self._achar(nome)
        if not k:
            return ("Não conheço o projeto '" + nome +
                    "'. Registre com: registra projeto " + nome + ": descrição")
        self.ativo = k
        v = self.dados[k]
        pend = [t["txt"] for t in v["tarefas"] if not t["feita"]]
        return ("MODO PROJETO: " + k.upper() + " ativado!\n" + v["desc"] +
                ("\nPendências:\n" + "\n".join("  - " + t for t in pend[:5])
                 if pend else "\nSem tarefas pendentes.") +
                "\nAgora tudo que conversarmos leva esse contexto. "
                "Comandos: tarefa [x] | tarefas | diario [x] | relatorio | proximo passo")

    def desativar(self):
        if not self.ativo:
            return "Nenhum projeto ativo."
        k = self.ativo
        self.ativo = None
        return "Saí do modo projeto " + k.upper() + ". Voltamos ao geral!"

    def registrar(self, nome, desc):
        k = re.sub(r"[^a-z0-9_]", "", nome.lower().strip().replace(" ", "_"))
        if not k:
            return "Nome inválido!"
        self.dados[k] = {"tarefas": [], "diario": [], "desc": desc.strip() or "Sem descrição",
                         "criado": datetime.datetime.now().strftime("%d/%m/%Y")}
        self._persistir()
        return "Projeto '" + k + "' registrado! Ative com: projeto " + k

    def _exige_ativo(self):
        return ("Nenhum projeto ativo! Use: projeto [nome] "
                "(veja todos com: meus projetos)") if not self.ativo else None

    def add_tarefa(self, texto):
        e = self._exige_ativo()
        if e:
            return e
        self.dados[self.ativo]["tarefas"].append({"txt": texto.strip(), "feita": False})
        self._persistir()
        n = len(self.dados[self.ativo]["tarefas"])
        return "Tarefa #" + str(n) + " adicionada no " + self.ativo.upper() + ": " + texto

    def listar_tarefas(self):
        e = self._exige_ativo()
        if e:
            return e
        ts = self.dados[self.ativo]["tarefas"]
        if not ts:
            return "Nenhuma tarefa no " + self.ativo.upper() + ". Use: tarefa [texto]"
        return ("Tarefas do " + self.ativo.upper() + ":\n" + "\n".join(
            "  " + str(i + 1) + ". " + ("[x] " if t["feita"] else "[ ] ") + t["txt"]
            for i, t in enumerate(ts)))

    def concluir(self, num):
        e = self._exige_ativo()
        if e:
            return e
        ts = self.dados[self.ativo]["tarefas"]
        try:
            t = ts[int(num) - 1]
            t["feita"] = True
            self.dados[self.ativo]["diario"].append({
                "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                "txt": "Concluído: " + t["txt"]})
            self._persistir()
            pend = sum(1 for x in ts if not x["feita"])
            return ("Tarefa " + str(num) + " concluída: " + t["txt"] +
                    "\nRestam " + str(pend) + " pendente(s). Boa, Francisco!")
        except (ValueError, IndexError):
            return "Tarefa inválida. Veja os números com: tarefas"

    def diario(self, texto):
        e = self._exige_ativo()
        if e:
            return e
        self.dados[self.ativo]["diario"].append({
            "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            "txt": texto.strip()})
        if len(self.dados[self.ativo]["diario"]) > 100:
            self.dados[self.ativo]["diario"] = self.dados[self.ativo]["diario"][-100:]
        self._persistir()
        return "Anotado no diário do " + self.ativo.upper() + "!"

    def ver_diario(self, n=8):
        e = self._exige_ativo()
        if e:
            return e
        d = self.dados[self.ativo]["diario"][-n:]
        if not d:
            return "Diário vazio. Registre progresso com: diario [o que fez]"
        return ("Diário do " + self.ativo.upper() + ":\n" + "\n".join(
            "[" + x["data"] + "] " + x["txt"] for x in d))


    def responder_sobre_tarefas(self):
        """Responde 'qual tarefa?' buscando as pendências REAIS dos projetos,
        mesmo sem um projeto ativo. Resolve a IRIS se enrolar nessa pergunta."""
        if self.ativo:
            pend = [t["txt"] for t in self.dados[self.ativo]["tarefas"] if not t["feita"]]
            if pend:
                return ("No projeto " + self.ativo.upper() + ", as tarefas pendentes são:\n" +
                        "\n".join("- " + t for t in pend))
            return "No " + self.ativo.upper() + " você já concluiu tudo! 🎉"
        # sem projeto ativo: junta pendências de todos
        linhas = []
        for nome, v in self.dados.items():
            pend = [t["txt"] for t in v["tarefas"] if not t["feita"]]
            if pend:
                linhas.append(nome.upper() + ": " + "; ".join(pend[:3]))
        if not linhas:
            return "Você não tem tarefas pendentes em nenhum projeto. Tá em dia! 🎉"
        return ("Suas tarefas pendentes por projeto:\n" + "\n".join("- " + l for l in linhas) +
                "\n\nPra focar em um, diga: projeto " + list(self.dados.keys())[0])

    def contexto(self):
        """Contexto que a IA recebe quando um projeto está ativo."""
        if not self.ativo:
            return ""
        v = self.dados[self.ativo]
        pend = [t["txt"] for t in v["tarefas"] if not t["feita"]]
        diario = [x["txt"] for x in v["diario"][-4:]]
        return ("[CONTEXTO DO PROJETO ATIVO: " + self.ativo.upper() + "]\n" +
                "Descrição: " + v["desc"] + "\n" +
                ("Pendências: " + "; ".join(pend[:5]) + "\n" if pend else "") +
                ("Últimos progressos: " + "; ".join(diario) + "\n" if diario else "") +
                "Responda levando esse projeto em conta.")
