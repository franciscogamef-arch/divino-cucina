import os, sys, json, queue, threading, subprocess, socket, requests, atexit
import datetime, random, time, math, shutil, asyncio, re, tempfile
from pathlib import Path
import logging
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import psutil
from .config import (CFG, CONFIG_PATH, GROQ_API_KEY, GEMINI_API_KEY,
    OPENWEATHER_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, ARDUINO_PORTA, ARDUINO_ATIVO,
    POCO_IP, CIDADE_PADRAO, MODELO_GROQ, MODELO_GEMINI)
from .monitor import Monitor
from .memoria import Memoria
from .voz import Voz
from .ia import IA
from .acoes import Acoes
from .processador import Processador
from .interface import Esfera3D, Painel2D


# ══════════════════════════════════════════════════════════════
#  IRIS — PRINCIPAL
# ══════════════════════════════════════════════════════════════
class IRIS:
    def __init__(self):
        pygame.init()
        self.W, self.H = 1400, 950
        self.ESF_W = 520
        self.ESF_H = 460
        self.SYS_X = 540
        self.SYS_W = self.W - self.SYS_X - 10
        self.usuario = CFG.get("USUARIO", "Francisco")
        pygame.display.set_mode((self.W, self.H), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("IRIS v1.7")
        pygame.key.set_repeat(400, 50)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POINT_SMOOTH)
        # Componentes
        self.mon = Monitor()
        self.mem = Memoria()
        self.voz = Voz()
        self.ia = IA(self.usuario, self.mem)
        self.acoes = Acoes(self.usuario, self.mem, self.ia)
        self.proc = Processador(self.usuario, self.mem, self.ia, self.acoes, self.mon, self.voz)
        self.esfera = Esfera3D(self.ESF_W, self.ESF_H)
        self.painel = Painel2D(self.W, self.H, self.ESF_W, self.ESF_H,
                               self.SYS_X, self.SYS_W, self.usuario)
        self.surf = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        # Estado
        self.mensagens = []
        self.input_texto = ""
        self.estado = "idle"
        self.ouvindo = False
        self.conversa_continua = False
        self.ultima_acao = ""
        self._poco_cache = {"conectado": False}
        threading.Thread(target=self._atualizar_poco, daemon=True).start()
        # Liga callbacks
        self.acoes.processador = self.proc
        self.acoes.mon = self.mon
        self.acoes.ia_callback = lambda msg: (self._msg("iris", msg), self.voz.falar(msg))
        self.acoes.iniciar_ditado = self._comecar_ditado  # v14: modo ditado
        self.acoes._falar_callback = lambda msg: (self._msg("iris", msg), self.voz.falar(msg))  # v19
        self.acoes._disparo_lembrete = self._lembrete_disparado
        self.clock = pygame.time.Clock()
        # Salva contexto ao sair
        atexit.register(lambda: self.mem.salvar_contexto_sessao(self.ia.historico))
        # Guardiã (v12): backup automático de mim mesma e das memórias
        threading.Thread(target=self.acoes.guardia_backup, daemon=True).start()
        # v18: autoverificação silenciosa — só avisa se achar problema
        def _autocheck():
            time.sleep(3)
            try:
                r = self.acoes.autoverificar()
                if "encontrei problemas" in r:
                    self._msg("iris", r)
                    self.voz.falar("Atenção: encontrei um problema na minha integridade.")
            except Exception as _e:
                logging.exception(_e)
        threading.Thread(target=_autocheck, daemon=True).start()
        # Avisos de configuração
        if not GROQ_API_KEY and not GEMINI_API_KEY:
            self._msg("iris", "Atenção: nenhuma chave de IA configurada! "
                              "Edite o arquivo iris_config.json com chaves NOVAS "
                              "(revogue as antigas que estavam no código!).")
        # Visitas e saudação
        visitas = self.mem.incrementar_visita()
        saudacoes = [
            "Oi "+self.usuario+"! Que bom te ver!",
            "Olá! Pronta pra mais um dia!",
            "Ei! O que vamos fazer hoje?",
            "Oi! Dois cérebros à sua disposição!",
        ]
        if visitas > 5:
            saudacoes = [
                "Ei! Já tava com saudades. O que vamos aprontar?",
                "De volta! Novidade no livro ou no FPGA?",
                "Oi! Estava esperando você. Bora!",
            ]
        # v24: se já nos conhecemos, ela te recebe com um briefing real
        if visitas > 1:
            try:
                s = self.acoes.briefing()
            except Exception:
                s = random.choice(saudacoes)
        else:
            s = random.choice(saudacoes)
        self._msg("iris", s)
        self.voz.falar(s)
        # Auto-inicia bot Telegram se token configurado
        if TELEGRAM_TOKEN:
            self.acoes.iniciar_bot_telegram(self.proc.processar)

    def _msg(self, quem, texto):
        self.mensagens.append({"quem": quem, "texto": str(texto),
                               "hora": time.strftime("%H:%M")})
        if len(self.mensagens) > 120:
            self.mensagens.pop(0)
        self.mem.salvar_conversa("IRIS" if quem == "iris" else self.usuario, str(texto))

    def _lembrete_disparado(self, texto):
        msg = "LEMBRETE: " + texto
        self._msg("iris", msg)
        self.voz.falar(msg)

    def abrir_historico(self):
        """v8: pygame só suporta uma janela — o histórico aparece no próprio chat
        (e o arquivo completo fica em iris_historico.txt)."""
        hist = self.mem.ver_historico(40)
        for bloco in [hist[i:i+400] for i in range(0, min(len(hist), 1200), 400)]:
            self._msg("iris", bloco)

    def _atualizar_poco(self):
        """Atualiza dados do Poco X7 a cada 15s; tenta WiFi a cada 5min.
        (BUG da v7 corrigido: este loop estava corrompido e sem sleep)"""
        tick = 0
        while True:
            try:
                if tick % 20 == 0:
                    self.acoes._adb_wifi()
                self._poco_cache = self.acoes.celular_status_painel() or {"conectado": False}
            except Exception as _e:
                logging.exception(_e)
            tick += 1
            time.sleep(15)

    def _processar_async(self, prompt):
        def _run():
            self.estado = "pensando"
            try:
                resposta = self.proc.processar(prompt)
            except Exception as _e:
                logging.exception(_e)
                resposta = "Deu erro aqui: " + str(_e)
            if resposta and not any(x in str(resposta).lower()
                                    for x in ["erro", "nao consigo", "nao posso"]):
                if len(str(resposta)) < 200:
                    self.ultima_acao = str(resposta)[:50]
            self._msg("iris", resposta)
            self.voz.falar(str(resposta))
            self.estado = "idle"
        threading.Thread(target=_run, daemon=True).start()

    def _ouvir(self, continua=False):
        """Reconhecimento de voz. Se continua=True, fica em loop até desativar."""
        self.ouvindo = True
        self.estado = "ouvindo"
        if not continua:
            self._msg("iris", "Ouvindo... fale agora!")
        try:
            import speech_recognition as sr
        except ImportError:
            self._msg("iris", "Instala: pip3 install SpeechRecognition pyaudio --break-system-packages")
            self.ouvindo = False
            self.estado = "idle"
            return
        try:
            r = sr.Recognizer()
            r.energy_threshold = 300
            r.dynamic_energy_threshold = True
            # v1.0 — ESCUTA PACIENTE: antes ela cortava com 0,8s de pausa!
            r.pause_threshold = 2.0          # você pode respirar/pensar sem ela cortar
            r.non_speaking_duration = 0.8    # mas ainda detecta o fim de verdade
            r.phrase_threshold = 0.3
            while True:
                try:
                    with sr.Microphone() as source:
                        r.adjust_for_ambient_noise(source, duration=0.5)
                        # frases de até 90s (antes: 30s) e espera você começar por até 12s
                        audio = r.listen(source, timeout=12, phrase_time_limit=90)
                    texto = r.recognize_google(audio, language="pt-BR")
                    if texto:
                        # comandos de saída do modo contínuo
                        if continua and texto.lower().strip() in (
                                "sair", "para de ouvir", "desliga", "chega"):
                            self._msg("iris", "Saí do modo conversa contínua!")
                            break
                        self._msg("user", texto)
                        self.estado = "pensando"
                        resposta = self.proc.processar(texto)
                        self._msg("iris", resposta)
                        self.voz.falar(str(resposta))
                        # espera terminar de falar antes de ouvir de novo
                        while self.voz.falando:
                            time.sleep(0.2)
                except sr.WaitTimeoutError:
                    if not continua:
                        self._msg("iris", "Não ouvi nada. Aperta F2 e tenta de novo!")
                        break
                except sr.UnknownValueError:
                    if not continua:
                        self._msg("iris", "Não entendi. Fala mais devagar!")
                        break
                if not continua or not self.conversa_continua:
                    break
        except Exception as _e:
            logging.exception(_e)
            self._msg("iris", "Erro no microfone: " + str(_e))
        finally:
            self.ouvindo = False
            self.conversa_continua = False
            self.estado = "idle"

    def _comecar_ditado(self):
        """Inicia o modo ditado em thread. Chamado pelo comando 'ditado' ou F5."""
        if self.ouvindo:
            return "Já estou ouvindo! Termina o que está rolando primeiro."
        threading.Thread(target=self._ditado, daemon=True).start()
        return ("MODO DITADO LIGADO! Pode falar por quanto tempo quiser, "
                "com pausas — eu vou escrevendo tudo.\n"
                "Diga 'fim do ditado' para encerrar e salvar, "
                "ou 'cancela ditado' para descartar.")

    def _ditado(self):
        """Escuta em blocos longos e acumula TUDO até você mandar parar.
        Perfeito para ditar trechos do livro!"""
        self.ouvindo = True
        self.estado = "ouvindo"
        try:
            import speech_recognition as sr
        except ImportError:
            self._msg("iris", "Instala: pip3 install SpeechRecognition pyaudio --break-system-packages")
            self.ouvindo = False
            self.estado = "idle"
            return
        blocos = []
        try:
            r = sr.Recognizer()
            r.energy_threshold = 300
            r.dynamic_energy_threshold = True
            r.pause_threshold = 2.5        # no ditado, pausas longas são normais
            r.non_speaking_duration = 1.0
            silencios = 0
            while True:
                try:
                    with sr.Microphone() as source:
                        r.adjust_for_ambient_noise(source, duration=0.5)
                        audio = r.listen(source, timeout=20, phrase_time_limit=120)
                    texto = r.recognize_google(audio, language="pt-BR").strip()
                    silencios = 0
                    tl = texto.lower()
                    if tl in ("fim do ditado", "fim de ditado", "terminei o ditado",
                              "terminei", "fim"):
                        break
                    if tl in ("cancela ditado", "cancela o ditado", "descarta"):
                        blocos = []
                        self._msg("iris", "Ditado cancelado, nada foi salvo.")
                        return
                    blocos.append(texto)
                    palavras = sum(len(b.split()) for b in blocos)
                    self._msg("user", texto)
                    self._msg("iris", "(anotando... " + str(palavras) +
                              " palavras — continue ou diga 'fim do ditado')")
                except sr.WaitTimeoutError:
                    silencios += 1
                    if silencios >= 3:   # ~1 min de silêncio encerra sozinho
                        break
                except sr.UnknownValueError:
                    continue
        except Exception as _e:
            logging.exception(_e)
            self._msg("iris", "Erro no microfone durante o ditado: " + str(_e))
        finally:
            self.ouvindo = False
            self.estado = "idle"
        if not blocos:
            self._msg("iris", "Ditado encerrado sem texto.")
            return
        texto_final = "\n\n".join(blocos)
        palavras = len(texto_final.split())
        pasta = Path.home() / "IRIS_Projetos" / "Ditados"
        pasta.mkdir(parents=True, exist_ok=True)
        nome = "ditado_" + datetime.datetime.now().strftime("%d%m%Y_%H%M") + ".txt"
        (pasta / nome).write_text(texto_final, encoding="utf-8")
        self.mem.salvar_nota("Ditado (" + str(palavras) + " palavras): " +
                             texto_final[:80] + "...")
        msg = ("DITADO SALVO! " + str(palavras) + " palavras em " +
               str(len(blocos)) + " bloco(s).\nArquivo: ~/IRIS_Projetos/Ditados/" + nome +
               "\nQuer que eu revise? Diga: leia IRIS_Projetos/Ditados/" + nome)
        self._msg("iris", msg)
        self.voz.falar("Ditado salvo! " + str(palavras) + " palavras.")

    def _atualizar_estado(self):
        if self.ouvindo:
            self.estado = "ouvindo"
        elif self.voz.falando:
            self.estado = "falando"
        elif self.estado in ("falando", "ouvindo"):
            self.estado = "idle"

    def _colar_clipboard(self):
        try:
            env = os.environ.copy()
            env.setdefault("DISPLAY", ":0")
            r = subprocess.run(["xclip", "-selection", "clipboard", "-o"],
                               capture_output=True, env=env, timeout=3)
            clip = r.stdout.decode("utf-8", "ignore").strip()
            if clip and len(clip) < 1000:
                self.input_texto += clip
        except Exception as _e:
            logging.exception(_e)

    def rodar(self):
        rodando = True
        while rodando:
            for event in pygame.event.get():
                if event.type == QUIT:
                    rodando = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        rodando = False
                    elif event.key == K_RETURN:
                        if self.input_texto.strip():
                            prompt = self.input_texto.strip()
                            self._msg("user", prompt)
                            self.input_texto = ""
                            self._processar_async(prompt)
                        elif not self.ouvindo:
                            threading.Thread(target=self._ouvir, daemon=True).start()
                    elif event.key == K_BACKSPACE:
                        if pygame.key.get_mods() & KMOD_CTRL:
                            self.input_texto = ""
                        else:
                            self.input_texto = self.input_texto[:-1]
                    elif event.key == K_F2 and not self.ouvindo:
                        threading.Thread(target=self._ouvir, daemon=True).start()
                    elif event.key == K_F3:
                        self.abrir_historico()
                    elif event.key == K_F5:
                        self._msg("iris", self._comecar_ditado())
                    elif event.key == K_F4:
                        if not self.ouvindo:
                            self.conversa_continua = True
                            self._msg("iris", "Modo conversa contínua ATIVO! "
                                              "Diga 'sair' para encerrar.")
                            threading.Thread(target=self._ouvir, args=(True,),
                                             daemon=True).start()
                        else:
                            self.conversa_continua = False
                    elif event.key == K_v and (pygame.key.get_mods() & KMOD_CTRL):
                        self._colar_clipboard()
                    elif event.key == K_a and (pygame.key.get_mods() & KMOD_CTRL):
                        self.input_texto = ""
                    else:
                        if event.unicode and event.unicode.isprintable():
                            self.input_texto += event.unicode
            self._atualizar_estado()
            self.esfera.atualizar(self.estado)
            self.esfera.desenhar(self.W, self.H)
            self.surf.fill((0, 0, 0, 0))
            self.painel.desenhar(
                self.surf, self.mon, self.mensagens,
                self.input_texto, self.estado,
                self.ouvindo, self.ultima_acao,
                self._poco_cache)
            self.painel.renderizar_gl(self.surf, self.W, self.H)
            pygame.display.flip()
            # Reduz FPS quando idle para economizar CPU
            fps = 60 if self.estado in ("falando", "pensando", "ouvindo") else 30
            self.clock.tick(fps)
        # Encerramento limpo
        self.mem.salvar_contexto_sessao(self.ia.historico)
        self.voz.parar()
        pygame.quit()
        sys.exit()
