import os, sys, json, queue, threading, subprocess, socket, requests, atexit
import datetime, random, time, math, shutil, asyncio, re, tempfile
from pathlib import Path
import logging


# ══════════════════════════════════════════════════════════════
#  VOZ — fila otimizada + interrupção imediata ("para!")
# ══════════════════════════════════════════════════════════════
class Voz:
    def __init__(self):
        self._fila = queue.Queue()
        self._falando = False
        self._proc = None          # processo mpg123 atual
        self._interromper = False
        threading.Thread(target=self._loop, daemon=True).start()

    def falar(self, texto):
        if self._fila.qsize() >= 3:
            return
        txt = re.sub(r'[*#_`\[\]{}|<>●◌◉▸►▶★☆→←↑↓✓✗]', '', texto)
        txt = re.sub(r'https?://\S+', '', txt)
        txt = txt[:300].strip()
        if txt:
            self._fila.put(txt)

    def parar(self):
        """Interrompe a fala AGORA e limpa a fila."""
        self._interromper = True
        try:
            while not self._fila.empty():
                self._fila.get_nowait()
                self._fila.task_done()
        except Exception:
            pass
        if self._proc and self._proc.poll() is None:
            try:
                self._proc.terminate()
            except Exception as _e:
                logging.exception(_e)

    def _loop(self):
        while True:
            texto = self._fila.get()
            self._falando = True
            self._interromper = False
            mp3 = None
            try:
                mp3 = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name

                async def _gerar():
                    import edge_tts
                    com = edge_tts.Communicate(texto[:500], voice="pt-BR-FranciscaNeural")
                    await com.save(mp3)

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(_gerar())
                loop.close()

                if not self._interromper:
                    self._proc = subprocess.Popen(
                        ["mpg123", "-q", mp3],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    self._proc.wait()
            except Exception as _e:
                logging.exception(_e)
            finally:
                self._falando = False
                self._proc = None
                self._fila.task_done()
                try:
                    if mp3 and os.path.exists(mp3):
                        os.remove(mp3)
                except Exception as _e:
                    logging.exception(_e)

    @property
    def falando(self):
        return self._falando
