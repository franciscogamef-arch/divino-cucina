import os, sys, json, queue, threading, subprocess, socket, requests, atexit
import datetime, random, time, math, shutil, asyncio, re, tempfile
from pathlib import Path
import logging


# ══════════════════════════════════════════════════════════════
#  MEMÓRIA PERSISTENTE
# ══════════════════════════════════════════════════════════════
class Memoria:
    def __init__(self, path="iris_memoria.json"):
        self.path = Path(path)
        self.hist_path = Path("iris_historico.txt")
        self.notas_path = Path("iris_notas.txt")
        self._lock = threading.Lock()
        self._data = self._carregar()

    def _carregar(self):
        if self.path.exists():
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as _e:
                logging.exception(_e)
        return {"visitas": 0, "aprendizados": [], "preferencias": {}, "lembretes": []}

    def salvar(self):
        with self._lock:
            try:
                with open(self.path, "w", encoding="utf-8") as f:
                    json.dump(self._data, f, ensure_ascii=False, indent=2)
            except Exception as _e:
                logging.exception(_e)

    def incrementar_visita(self):
        self._data["visitas"] = self._data.get("visitas", 0) + 1
        self.salvar()
        return self._data["visitas"]

    def registrar(self, info):
        self._data.setdefault("aprendizados", []).append({
            "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            "info": info
        })
        if len(self._data["aprendizados"]) > 200:
            self._data["aprendizados"] = self._data["aprendizados"][-200:]
        self.salvar()

    def salvar_conversa(self, quem, texto):
        try:
            with open(self.hist_path, "a", encoding="utf-8") as f:
                agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                f.write("[" + agora + "] " + quem + ": " + texto + "\n")
        except Exception as _e:
            logging.exception(_e)

    def salvar_contexto_sessao(self, historico_ia):
        """Salva histórico da sessão atual para continuar depois."""
        try:
            with open("iris_contexto.json", "w", encoding="utf-8") as f:
                json.dump({"historico": historico_ia[-10:],
                           "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")},
                          f, ensure_ascii=False)
        except Exception as _e:
            logging.exception(_e)

    def carregar_contexto_sessao(self):
        try:
            ctx_path = Path("iris_contexto.json")
            if ctx_path.exists():
                with open(ctx_path, "r", encoding="utf-8") as f:
                    return json.load(f).get("historico", [])
        except Exception as _e:
            logging.exception(_e)
        return []

    def ver_historico(self, linhas=30):
        if not self.hist_path.exists():
            return "Nenhum histórico ainda."
        with open(self.hist_path, "r", encoding="utf-8") as f:
            todas = f.readlines()
        return "".join(todas[-linhas:])

    def salvar_nota(self, texto):
        with open(self.notas_path, "a", encoding="utf-8") as f:
            agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            f.write("\n[" + agora + "]\n" + texto + "\n")
        self.registrar("Nota: " + texto[:40])

    def ver_notas(self):
        if not self.notas_path.exists():
            return "Nenhuma nota ainda."
        with open(self.notas_path, "r", encoding="utf-8") as f:
            return f.read()[-600:]

    @property
    def visitas(self):
        return self._data.get("visitas", 0)

    @property
    def n_aprendizados(self):
        return len(self._data.get("aprendizados", []))
