import os, sys, json, queue, threading, subprocess, socket, requests, atexit
import datetime, random, time, math, shutil, asyncio, re, tempfile
from pathlib import Path
import logging
import psutil


# ══════════════════════════════════════════════════════════════
#  MONITOR DO SISTEMA — thread separada otimizada
# ══════════════════════════════════════════════════════════════
class Monitor:
    def __init__(self):
        self.running = True
        self.cpu = 0.0
        self.ram = 0.0
        self.disco = 0.0
        self.temp = 0.0
        self.bat = 0.0
        self.plugado = True
        self.net_up = 0.0
        self.net_dn = 0.0
        self.hist_cpu = [0.0] * 80
        self._net_old = psutil.net_io_counters()
        self._procs = []
        self._nomes = []
        self._lock = threading.Lock()
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        tick = 0
        while self.running:
            try:
                self.cpu = psutil.cpu_percent(interval=2)
                ram = psutil.virtual_memory()
                self.ram = ram.percent
                self.disco = psutil.disk_usage("/").percent

                # Temperatura — a cada 5 ticks
                if tick % 5 == 0:
                    try:
                        t = psutil.sensors_temperatures()
                        if t:
                            self.temp = list(t.values())[0][0].current
                    except Exception as _e:
                        logging.exception(_e)

                # Bateria — BUG da v7 corrigido (nunca era lida!)
                if tick % 5 == 0:
                    try:
                        b = psutil.sensors_battery()
                        if b:
                            self.bat = b.percent
                            self.plugado = bool(b.power_plugged)
                    except Exception as _e:
                        logging.exception(_e)

                # Rede
                net = psutil.net_io_counters()
                self.net_up = (net.bytes_sent - self._net_old.bytes_sent) / 2048
                self.net_dn = (net.bytes_recv - self._net_old.bytes_recv) / 2048
                self._net_old = net

                # Nomes em cache — atualiza só a cada 30 ticks (~60s)
                if tick % 30 == 0 or not self._nomes:
                    _ignorar = ["Isolated", "WebKit", "kworker", "kthread", "migration",
                                "rcu", "ksoftirq", "irq", "watchdog", "pool_workqueue"]
                    _todos = sorted(psutil.process_iter(["name", "cpu_percent"]),
                                    key=lambda x: x.info["cpu_percent"] or 0, reverse=True)
                    _filt = [p for p in _todos
                             if p.info["name"] and not any(
                                 ig.lower() in p.info["name"].lower() for ig in _ignorar)][:4]
                    with self._lock:
                        self._nomes = [p.info["name"][:22] for p in _filt]

                # % atualiza sempre, nomes ficam fixos (painel não pisca)
                try:
                    _pcts = {p.info["name"][:22]: (p.info["cpu_percent"] or 0.0)
                             for p in psutil.process_iter(["name", "cpu_percent"])
                             if p.info["name"]}
                    with self._lock:
                        self._procs = [(n, _pcts.get(n, 0.0)) for n in self._nomes]
                except Exception as _e:
                    logging.exception(_e)

                # Histórico de CPU com limite
                self.hist_cpu.append(self.cpu)
                if len(self.hist_cpu) > 80:
                    self.hist_cpu = self.hist_cpu[-80:]
            except Exception as _e:
                logging.exception(_e)
                time.sleep(1)
            tick += 1

    def get_procs(self):
        with self._lock:
            return list(self._procs)
