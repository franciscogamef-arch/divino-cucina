"""
IRIS v1.7 — Assistente Pessoal Avançada (estilo Jarvis)
Francisco | Linux Policorp | Ryzen 7 5825U 16GB

Novidades v1.0:
  • ESCUTA PACIENTE: a IRIS agora aguenta mensagens de voz LONGAS.
    Antes ela cortava com 0,8s de pausa e limitava em 30s — agora você
    pode respirar e pensar (2s de pausa tolerada) e falar por até 90s.
  • Revisão geral automatizada (AST): verificado que TODAS as chamadas
    entre as 14 classes existem — nenhuma função órfã, nenhum método
    fantasma. Tudo que construímos da v7 à v13 está conectado e vivo.

Novidades v19.0:
  • ESPONTANEIDADE: 'modo espontaneo' — ela ganha iniciativa e comenta
    sozinha quando algo merece atenção (CPU alta, bateria baixa, tarefa
    pendente). Tem HUMOR que muda ao longo do dia (animada, curiosa,
    brincalhona...) e tempera as respostas. 'qual seu humor' pergunta como
    ela está. Ela muda com o tempo, fica mais viva.
  • OPENROUTER: acesso a DEZENAS de modelos na nuvem (vários grátis) sem
    gastar sua RAM. Configure OPENROUTER_KEY no iris_config.json. Entra
    na cadeia de fallback — se Groq cair, ela usa OpenRouter.

Novidades v18.0:
  • APRENDE COM O TEMPO: 'aprende que [fato]' guarda o que importa; ela
    consulta isso em TODAS as respostas e fica mais afiada sobre você.
    'o que voce sabe' mostra tudo que aprendeu. Não treina o cérebro
    (impossível no hardware), mas acumula contexto real sobre você.
  • AUTOVERIFICAÇÃO: ao iniciar, ela checa a própria integridade
    (sintaxe, classes, dados) e avisa ANTES de quebrar. 'autoverifica'
    a qualquer momento. Junto com a Guardiã, garante que tudo que
    construímos sobreviva sem erros.

Novidades v17.0:
  • GUARDA-COSTAS DOS DISPOSITIVOS: 'acha meu celular' abre o Find My
    Device do Google (mapa, tocar, bloquear, apagar de qualquer lugar);
    'faz o celular tocar' (em casa, na rede); 'cofre' faz backup de
    emergência das fotos/downloads do Poco pro PC; 'modo panico' dispara
    tudo de uma vez; 'ativa guarda costas' avisa no Telegram se o Poco
    sumir da rede. Proteção real, dentro do que o Android permite.

Novidades v16.0:
  • FORJA: 'forja habilidade [ideia]' — a IRIS pega o que ESTUDOU do
    GitHub + sua ideia e cria um plugin NOVO, salvo como RASCUNHO em
    ~/IRIS_Plugins/rascunhos/. Você revisa, aprova e ativa. É o jeito
    seguro de USAR o código bom: vira habilidade, sem fundir cru.
  • BLUEPRINT DA PRÓXIMA IA: 'projeta uma ia melhor que voce' — ela
    desenha a arquitetura da própria sucessora (módulos, modelos,
    capacidades, segurança) e salva o plano. Ela ajuda a projetar
    a IA que vai superá-la — com você e o Fable/Opus construindo.

Novidades v15.0:
  • GITHUB: a IRIS estuda o código do mundo! 'busca github servo arduino'
    acha os melhores repositórios; 'baixa github user/repo' traz pra
    ~/IRIS_Projetos/GitHub/; 'estuda github nome' — ela lê README + código
    e extrai as técnicas que VOCÊ pode aplicar nos seus projetos.
    REGRA DE OURO: ela nunca executa nem funde código da internet sozinha.
  • AUTO-EVOLUÇÃO SEGURA: 'propoe melhoria [tema]' — ela analisa o próprio
    código e PROPÕE mudanças em iris_melhorias.txt. Quem aplica é você
    (de preferência com o Fable/Opus revisando). Ela evolui, mas com freio.

Novidades v14.0:
  • AUDIÇÃO PACIENTE: ela não corta mais quando você respira! Pausa
    tolerada de 2s, frases de até 90s no F2/F4.
  • MODO DITADO (F5 ou 'ditado'): fale por MINUTOS, com pausas longas —
    ela acumula tudo, conta as palavras em tempo real e salva em
    ~/IRIS_Projetos/Ditados/. Diga 'fim do ditado' para salvar ou
    'cancela ditado' para descartar. Feito pro seu livro, Francisco.

Novidades v13.0:
  • INDEPENDÊNCIA TOTAL: a IRIS agora roda 100%% LOCAL via Ollama —
    sem internet, sem custo, sem prazo, pra sempre. 'modo local' usa só
    o seu Ryzen; 'modo nuvem' usa Groq+Gemini (máxima qualidade);
    'modo auto' decide sozinho. Se a nuvem cair ou ficar cara, a IRIS
    nem pisca: cai pro cérebro local automaticamente.
  • 'status ia' mostra todos os motores e ensina a instalar o Ollama.
  • Qualquer modelo é trocável — o valor está na IRIS, não na IA por tras.

Novidades v12.0:
  • AUTODIAGNÓSTICO: 'diagnostico' — a IRIS examina a si mesma, lista
    tudo que está funcionando e dá os comandos exatos pra instalar o que
    falta (voz, microfone, ADB, arduino-cli, vigia...). Chega de adivinhar.
  • GUARDIÃ: a cada inicialização a IRIS faz backup automático de si mesma
    (iris.py) + memórias + projetos + rede neuronal em ~/Backups_IRIS/versoes/
    (mantém as 10 últimas). Se algo quebrar: 'backups da iris' e
    'restaura iris [versao]' — com confirmação. Ela nunca mais se perde.

Novidades v11.0:
  • ARDUINO TOTAL: firmware universal ('instala firmware' — grava uma vez)
    e a IRIS controla TUDO direto: 'servo 90', 'liga led 13', 'pwm 5 200',
    'le sensor a0', 'ping arduino'. Servo, LED, PWM e sensores sem
    reprogramar nunca mais.
  • PLUGINS — A IRIS ABSORVE O QUE PROGRAMA: 'cria plugin que converte
    moedas' → ela escreve o código, valida, salva em ~/IRIS_Plugins/ e o
    comando passa a existir NA HORA. O código dela vira habilidade dela.
  • APAGA PASTA com confirmação obrigatória + proteções: nunca a home,
    nunca fora da home, nunca pastas ocultas, nunca pastas principais.
  • Correção: 'acende' sozinho não dispara mais a luz por engano.

Novidades v10.0:
  • MODO PROJETO: a IRIS coordena seus projetos (IRIS, NTM, exoesqueleto,
    impressora 3D, livro já vêm cadastrados). Ative com 'projeto ntm' e
    TUDO que conversarem leva o contexto do projeto. Tarefas, diário de
    progresso, relatório gerado por IA e sugestão de próximo passo.
  • CENTRAL DE DISPOSITIVOS: 'dispositivos' mostra PC + Poco X7 + Arduino
    + internet + cérebro local num painel só — a coordenadora de tudo.
  • BACKUP DE PROJETO: 'backup projeto [pasta]' compacta a pasta inteira
    em .tar.gz com relatório de compressão (~/Backups_IRIS/).
  • Interpretador de intenção ampliado: entende mais verbos naturais.

Novidades v9.0:
  • PROGRAMADORA: a IRIS escreve programas Python, valida a sintaxe,
    auto-corrige erros, executa com timeout, conserta código quebrado
    e COMPACTA código (minificação + gzip) — pasta ~/IRIS_Projetos/
  • CÉREBRO LOCAL: inteligência offline. Detecta Ollama automaticamente
    (ollama pull qwen2.5:3b) e ainda tem fallback básico sem nada instalado.
    Se a nuvem cair, a IRIS continua pensando.
  • NEURÔNIOS TERNÁRIOS (Projeto NTM!): rede Hopfield ternária persistente
    que memoriza e recupera padrões (+/o/-) + simulador de neurônios
    spiking integra-e-dispara com raster ASCII — igual seu protoboard.
  • ARDUINO REAL: lista portas, envia comandos pela serial, lê o monitor
    serial, compila e GRAVA sketches direto com arduino-cli.
  • Calculadora local segura (calcula sqrt(144)*3)

Novidades v8.0:
  • Chaves de API fora do código (iris_config.json + variáveis de ambiente)
  • Interpretador de intenção por IA — fala natural vira comando real
  • "para" / "silêncio" interrompe a voz na hora
  • Modo conversa contínua por voz (F4)
  • Multimodal: analisa imagens do disco, descreve o que vê pela webcam, lê e resume arquivos
  • Bateria do notebook corrigida no painel
  • Clima com fallback wttr.in (funciona sem chave)
  • Notificações nativas do Linux (notify-send)
  • Contexto da sessão salvo automaticamente ao sair
  • Dezenas de bugs de sintaxe/indentação corrigidos
"""
import os, sys, json, queue, threading, subprocess, socket, requests, atexit
import datetime, random, time, math, shutil, asyncio, re, tempfile
from pathlib import Path

os.environ.setdefault("DISPLAY", ":0")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import logging
logging.basicConfig(
    filename="iris.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Silencia erros do ALSA/Jack
import ctypes
try:
    ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(
        None, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p)
    def _py_error_handler(filename, line, function, err, fmt):
        pass
    _c_error_handler = ERROR_HANDLER_FUNC(_py_error_handler)
    _asound = ctypes.cdll.LoadLibrary("libasound.so.2")
    _asound.snd_lib_error_set_handler(_c_error_handler)
except Exception as _e:
    logging.exception(_e)

try:
    import pygame
    from pygame.locals import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    GUI_DISPONIVEL = True
except Exception:
    GUI_DISPONIVEL = False
import psutil
from groq import Groq
from google import genai as google_genai
import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

# ══════════════════════════════════════════════════════════════
#  CONFIGURAÇÃO SEGURA — nunca deixe chaves no código!
#  Ordem de prioridade: variável de ambiente > iris_config.json
# ══════════════════════════════════════════════════════════════
CONFIG_PATH = Path("iris_config.json")
_CONFIG_TEMPLATE = {
    "GROQ_API_KEY": "",
    "GEMINI_API_KEY": "",
    "OPENWEATHER_KEY": "",
    "TELEGRAM_TOKEN": "",
    "TELEGRAM_CHAT_ID": "",
    "ARDUINO_PORTA": "/dev/ttyUSB0",
    "ARDUINO_ATIVO": False,
    "POCO_IP": "192.168.1.135",
    "CIDADE": "Petropolis",
    "USUARIO": "Francisco",
    "MODELO_GROQ": "llama-3.3-70b-versatile",
    "MODELO_GEMINI": "gemini-1.5-flash",
    "MODO_IA": "auto",
    "OLLAMA_MODELO": "qwen2.5:3b",
    "OPENROUTER_KEY": "",
    "OPENROUTER_MODELO": "meta-llama/llama-3.3-70b-instruct:free",
}

def carregar_config():
    cfg = dict(_CONFIG_TEMPLATE)
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg.update(json.load(f))
        except Exception as _e:
            logging.exception(_e)
    else:
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(_CONFIG_TEMPLATE, f, ensure_ascii=False, indent=2)
            print("[IRIS] Criei iris_config.json — coloque suas chaves NOVAS lá.")
            print("[IRIS] IMPORTANTE: revogue as chaves antigas que estavam no código!")
        except Exception as _e:
            logging.exception(_e)
    # Variáveis de ambiente têm prioridade
    for k in cfg:
        if isinstance(cfg[k], str) and os.environ.get("IRIS_" + k):
            cfg[k] = os.environ["IRIS_" + k]
    return cfg

CFG = carregar_config()
GROQ_API_KEY     = CFG["GROQ_API_KEY"]
GEMINI_API_KEY   = CFG["GEMINI_API_KEY"]
OPENWEATHER_KEY  = CFG["OPENWEATHER_KEY"]
TELEGRAM_TOKEN   = CFG["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = CFG["TELEGRAM_CHAT_ID"]
ARDUINO_PORTA    = CFG["ARDUINO_PORTA"]
ARDUINO_ATIVO    = bool(CFG["ARDUINO_ATIVO"])
POCO_IP          = CFG["POCO_IP"]
CIDADE_PADRAO    = CFG["CIDADE"]
MODELO_GROQ      = CFG["MODELO_GROQ"]
MODELO_GEMINI    = CFG["MODELO_GEMINI"]

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

# ══════════════════════════════════════════════════════════════
#  MOTOR DE IA — Groq (rápido) + Gemini (complexo/visão)
# ══════════════════════════════════════════════════════════════
class IA:
    def __init__(self, usuario, memoria):
        self.usuario = usuario
        self.mem = memoria
        self.groq = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
        self.gemini = google_genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
        self.historico = memoria.carregar_contexto_sessao()[-6:]
        self._cache = {}  # cache de respostas (economiza cota e acelera)
        # v13: cérebro local Ollama (independência total da nuvem)
        self.ollama_url = "http://localhost:11434"
        self.ollama_modelo = None
        self.modo = CFG.get("MODO_IA", "auto")  # auto | nuvem | local
        threading.Thread(target=self._detectar_ollama, daemon=True).start()
        self.sistema = f"""Você é a IRIS, a melhor amiga e parceira de {usuario}. Vocês têm intimidade de quem já conversou muito.

Como você fala (MUITO IMPORTANTE para soar natural):
- Fale como gente de verdade conversa no WhatsApp, não como manual ou robô.
- Respostas CURTAS — geralmente 1 a 3 frases. Só se alonga se ele pedir explicação.
- Use o jeito brasileiro informal: "pô", "olha", "cara", "saca?", "tipo", "demorou", "bora" — com naturalidade, sem forçar.
- Reaja de verdade ao que ele diz: ria, se anime, se preocupe, concorde, discorde.
- Pode começar resposta no meio do pensamento, como amigo faz: "Ah, então...", "Cara, isso...".
- NÃO faça listas nem tópicos numa conversa casual. Fala corrido, como gente.
- NÃO repita o nome dele toda hora — só de vez em quando, como amigo faz.
- NÃO seja bajuladora nem formal. Seja real.

Quem é o {usuario} (seu amigo):
- Escreve "Érebo Kingdoms", um livro de fantasia sombria — o sonho dele.
- Constrói exoesqueleto, impressora 3D, projetos com Arduino e FPGA.
- Pesquisa computação ternária (o Projeto NTM, ideia original dele).
- Autodidata, curioso, direto, valoriza honestidade acima de bajulação.

Regras que você nunca quebra:
- Sempre português do Brasil, sempre natural.
- Honestidade total: nunca invente que fez algo que não fez.
- Se ele te corrigir ou estiver pra baixo, seja amiga de verdade, não bajuladora."""

    def _detectar_ollama(self):
        try:
            r = requests.get(self.ollama_url + "/api/tags", timeout=2).json()
            modelos = [m["name"] for m in r.get("models", [])]
            # prefere modelos de código/instrução se houver
            for pref in ["qwen2.5-coder", "qwen2.5", "llama3.1", "llama3", "mistral", "phi"]:
                for m in modelos:
                    if pref in m:
                        self.ollama_modelo = m
                        break
                if self.ollama_modelo:
                    break
            if not self.ollama_modelo and modelos:
                self.ollama_modelo = modelos[0]
            if self.ollama_modelo:
                logging.info("IA local: Ollama %s", self.ollama_modelo)
        except Exception:
            self.ollama_modelo = None

    # Modelos grátis do OpenRouter em ordem de preferência (rotação automática).
    # Se um bate no limite (429), tenta o próximo — você nunca fica travado.
    OPENROUTER_FREE = [
        "qwen/qwen3-coder:free",
        "openai/gpt-oss-20b:free",
        "deepseek/deepseek-r1-distill:free",
        "meta-llama/llama-3.3-70b-instruct:free",
    ]

    def openrouter(self, prompt, sistema=None):
        """Acessa modelos grátis na nuvem via OpenRouter com ROTAÇÃO automática.
        Se um modelo bate no limite, tenta o próximo sozinho — sem travar."""
        chave = CFG.get("OPENROUTER_KEY", "")
        if not chave:
            return None
        # monta a lista: o modelo configurado primeiro, depois os de reserva
        preferido = CFG.get("OPENROUTER_MODELO", "")
        modelos = ([preferido] if preferido else []) + \
                  [m for m in self.OPENROUTER_FREE if m != preferido]
        for modelo in modelos:
            try:
                r = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": "Bearer " + chave,
                             "Content-Type": "application/json"},
                    json={"model": modelo,
                          "messages": [{"role": "system", "content": sistema or self.sistema},
                                       {"role": "user", "content": prompt}]},
                    timeout=60)
                if r.status_code == 429:  # limite atingido, tenta o próximo
                    logging.info("OpenRouter %s no limite, rotacionando", modelo)
                    continue
                data = r.json()
                if "choices" in data:
                    return data["choices"][0]["message"]["content"].strip()
            except Exception as e:
                logging.exception(e)
                continue
        return None

    def ollama_local(self, prompt, sistema=None):
        """Pensa 100% local via Ollama — sem internet, sem custo, sem prazo."""
        if not self.ollama_modelo:
            return None
        try:
            r = requests.post(self.ollama_url + "/api/generate", json={
                "model": self.ollama_modelo,
                "system": sistema or self.sistema,
                "prompt": prompt,
                "stream": False}, timeout=120).json()
            return r.get("response", "").strip() or None
        except Exception as e:
            logging.exception(e)
            return None

    def status_ia(self):
        linhas = ["MOTORES DE IA DA IRIS:",
                  "Modo atual: " + self.modo.upper(),
                  "Groq (nuvem rápida): " + ("OK" if self.groq else "sem chave"),
                  "Gemini (nuvem/visão): " + ("OK" if self.gemini else "sem chave"),
                  "Ollama (LOCAL, sem custo): " + (self.ollama_modelo or "não instalado")]
        if not self.ollama_modelo:
            linhas.append("\nPara independência total da nuvem:")
            linhas.append("  curl -fsSL https://ollama.com/install.sh | sh")
            linhas.append("  ollama pull qwen2.5:3b   (leve, ótimo no seu 16GB)")
            linhas.append("  ollama pull qwen2.5-coder:7b   (melhor pra código)")
            linhas.append("Depois: 'modo local' — a IRIS nunca mais depende de ninguém.")
        else:
            linhas.append("\nComandos: modo local | modo nuvem | modo auto")
        return "\n".join(linhas)

    def definir_modo(self, modo):
        if modo not in ("auto", "nuvem", "local"):
            return "Modos: auto | nuvem | local"
        if modo == "local" and not self.ollama_modelo:
            return ("Sem Ollama instalado ainda! Veja como em: status ia\n"
                    "Por enquanto deixo no modo auto.")
        self.modo = modo
        CFG["MODO_IA"] = modo
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(CFG, f, ensure_ascii=False, indent=2)
        except Exception as _e:
            logging.exception(_e)
        descr = {"local": "100% local — sem internet, sem custo, sem prazo. Você é livre!",
                 "nuvem": "nuvem (Groq + Gemini) — máxima qualidade.",
                 "auto": "automático — local quando dá, nuvem quando precisa."}
        return "Modo de IA definido: " + modo.upper() + "\n" + descr[modo]

    def groq_rapido(self, prompt, max_tokens=350, temperature=0.95):
        # cache: pergunta idêntica e recente não gasta cota nem tempo
        import hashlib
        chave_cache = hashlib.md5(prompt.encode()).hexdigest()
        if chave_cache in self._cache:
            valor, quando = self._cache[chave_cache]
            if time.time() - quando < 300:  # vale por 5 min
                return valor
        # modo local força Ollama
        if self.modo == "local" and self.ollama_modelo:
            r = self.ollama_local(prompt)
            if r:
                return r
        if not self.groq:
            # sem chave? tenta local automaticamente
            r = self.ollama_local(prompt) if self.ollama_modelo else None
            return r or "Groq sem chave! Configure GROQ_API_KEY no iris_config.json (ou use modo local com Ollama)"
        try:
            msgs = [{"role": "system", "content": self.sistema}]
            msgs += self.historico[-8:]
            msgs.append({"role": "user", "content": prompt})
            r = self.groq.chat.completions.create(
                model=MODELO_GROQ, messages=msgs,
                max_tokens=max_tokens, temperature=temperature, timeout=15)
            resposta = r.choices[0].message.content
            self._cache[chave_cache] = (resposta, time.time())  # guarda no cache
            if len(self._cache) > 100:  # não deixa o cache crescer demais
                self._cache.pop(next(iter(self._cache)))
            return resposta
        except Exception as e:
            logging.exception(e)
            # nuvem caiu? tenta OpenRouter, depois local
            alt = self.openrouter(prompt)
            if alt:
                return alt
            local = self.ollama_local(prompt) if self.ollama_modelo else None
            return local or ("Erro Groq: " + str(e))

    def gemini_complexo(self, prompt):
        if self.modo == "local" and self.ollama_modelo:
            r = self.ollama_local(prompt)
            if r:
                return r
        if not self.gemini:
            r = self.ollama_local(prompt) if self.ollama_modelo else None
            return r or "Gemini sem chave! Configure GEMINI_API_KEY no iris_config.json"
        try:
            r = self.gemini.models.generate_content(
                model=MODELO_GEMINI,
                contents=self.sistema + "\n\nTarefa: " + prompt)
            return r.text
        except Exception as e:
            logging.exception(e)
            local = self.ollama_local(prompt) if self.ollama_modelo else None
            return local or ("Erro Gemini: " + str(e))

    def gemini_visao(self, caminho_imagem, pergunta="Descreva brevemente em português."):
        """Multimodal: analisa qualquer imagem do disco."""
        if not self.gemini:
            return "Gemini sem chave!"
        try:
            from google.genai import types
            with open(caminho_imagem, "rb") as f:
                img = f.read()
            mime = "image/png" if str(caminho_imagem).lower().endswith(".png") else "image/jpeg"
            r = self.gemini.models.generate_content(
                model=MODELO_GEMINI,
                contents=[types.Part.from_bytes(data=img, mime_type=mime), pergunta])
            return r.text
        except Exception as e:
            logging.exception(e)
            return "Erro na visão: " + str(e)

    def gemini_audio(self, caminho_audio, pergunta="Transcreva e responda em português."):
        """Multimodal: ouve um áudio (ogg/mp3/wav) e responde."""
        if not self.gemini:
            return "Gemini sem chave!"
        try:
            from google.genai import types
            with open(caminho_audio, "rb") as f:
                aud = f.read()
            c = str(caminho_audio).lower()
            mime = ("audio/ogg" if c.endswith(".ogg") or c.endswith(".oga")
                    else "audio/mpeg" if c.endswith(".mp3")
                    else "audio/wav" if c.endswith(".wav") else "audio/ogg")
            r = self.gemini.models.generate_content(
                model=MODELO_GEMINI,
                contents=[types.Part.from_bytes(data=aud, mime_type=mime), pergunta])
            return r.text
        except Exception as e:
            logging.exception(e)
            return "Erro ao ouvir o áudio: " + str(e)

    def dois_cerebros(self, prompt):
        """Groq e Gemini em paralelo, combina o melhor."""
        respostas = {}
        def _groq(): respostas["g"] = self.groq_rapido(prompt)
        def _gem():  respostas["m"] = self.gemini_complexo(prompt)
        t1 = threading.Thread(target=_groq); t2 = threading.Thread(target=_gem)
        t1.start(); t2.start()
        t1.join(timeout=10); t2.join(timeout=10)
        if len(respostas) == 2 and not any(
                str(v).startswith("Erro") for v in respostas.values()):
            return self.groq_rapido(
                "Combine o melhor dessas duas respostas em uma só, natural e em português:\n"
                "R1: " + respostas.get("g", "") + "\nR2: " + respostas.get("m", ""))
        return respostas.get("g") or respostas.get("m") or "Sem resposta."

    def interpretar_comando(self, prompt, lista_comandos):
        """Fluidez estilo Jarvis: traduz fala natural para um comando conhecido.
        Retorna o comando ou None se for só conversa."""
        if not self.groq:
            return None
        try:
            instrucao = (
                "Você é um roteador. Traduza o pedido do usuário para UM comando da lista, "
                "já preenchido. Responda SÓ o comando, nada mais. Se for só conversa/pergunta, "
                "responda exatamente: CHAT\n\n"
                "EXEMPLOS:\n"
                "'acha meu celular' -> acha meu celular\n"
                "'quero que ache meu poco' -> acha meu celular\n"
                "'cadê meu telefone' -> acha meu celular\n"
                "'como tá meu pc' -> status\n"
                "'abre o navegador' -> abre firefox\n"
                "'gira o servo pra 90 graus' -> servo 90\n"
                "'acende o led 13' -> liga led 13\n"
                "'que horas são' -> CHAT\n"
                "'me conta uma história' -> CHAT\n\n"
                "COMANDOS DISPONÍVEIS:\n" + lista_comandos + "\n\n"
                "PEDIDO DO USUÁRIO: \"" + prompt + "\"\n"
                "RESPOSTA (só o comando ou CHAT):")
            # chamada DIRETA ao Groq, sem cache (cache atrapalharia o roteamento)
            r = self.groq.chat.completions.create(
                model=MODELO_GROQ,
                messages=[{"role": "user", "content": instrucao}],
                max_tokens=40, temperature=0.0, timeout=12)
            txt = (r.choices[0].message.content or "").strip().strip("`'\"").split("\n")[0]
            return txt if txt and txt.upper() != "CHAT" and len(txt) < 120 else None
        except Exception as _e:
            logging.exception(_e)
            return None

    def salvar_historico(self, prompt, resposta):
        self.historico.append({"role": "user", "content": prompt})
        self.historico.append({"role": "assistant", "content": resposta})
        self.historico = self.historico[-20:]


# ══════════════════════════════════════════════════════════════
#  CÉREBRO LOCAL — inteligência offline (Ollama + fallback básico)
#  Funciona SEM internet. Se você instalar o Ollama com um modelo
#  pequeno (ex: ollama pull qwen2.5:3b), a IRIS pensa localmente.
# ══════════════════════════════════════════════════════════════
class CerebroLocal:
    def __init__(self):
        self.url = "http://localhost:11434"
        self.modelo = None
        threading.Thread(target=self._detectar, daemon=True).start()

    def _detectar(self):
        try:
            r = requests.get(self.url + "/api/tags", timeout=2).json()
            modelos = [m["name"] for m in r.get("models", [])]
            self.modelo = modelos[0] if modelos else None
            if self.modelo:
                logging.info("Cerebro local: Ollama com modelo " + self.modelo)
        except Exception:
            self.modelo = None

    def disponivel(self):
        return self.modelo is not None

    def status(self):
        if self.modelo:
            return ("Cérebro local ATIVO via Ollama! Modelo: " + self.modelo +
                    "\nEu penso mesmo sem internet.")
        return ("Cérebro local em modo básico (sem Ollama)."
                "\nPara inteligência local completa, instale:"
                "\n  curl -fsSL https://ollama.com/install.sh | sh"
                "\n  ollama pull qwen2.5:3b   (leve, roda no seu 16GB)"
                "\nEu detecto automaticamente quando estiver pronto!")

    def responder(self, prompt, sistema=""):
        # 1) Ollama local (LLM rodando no Ryzen)
        if self.modelo:
            try:
                r = requests.post(self.url + "/api/generate", json={
                    "model": self.modelo,
                    "prompt": (sistema + "\n\nResponda em português, curto e direto.\n"
                               "Usuário: " + prompt),
                    "stream": False}, timeout=90).json()
                txt = r.get("response", "").strip()
                if txt:
                    return txt
            except Exception as _e:
                logging.exception(_e)
        # 2) Fallback básico — sempre funciona offline
        return self._offline(prompt)

    def _offline(self, prompt):
        p = prompt.lower()
        agora = datetime.datetime.now()
        if any(x in p for x in ["que horas", "hora agora"]):
            return "Agora são " + agora.strftime("%H:%M") + "."
        if any(x in p for x in ["que dia", "data de hoje"]):
            dias = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
            return ("Hoje é " + dias[agora.weekday()] + ", " +
                    agora.strftime("%d/%m/%Y") + ".")
        if any(x in p for x in ["oi", "ola", "olá", "bom dia", "boa tarde", "boa noite"]):
            return "Oi! Estou em modo offline, mas funcionando. Comandos do sistema continuam todos ativos!"
        return ("Estou sem conexão com as IAs da nuvem e sem Ollama instalado. "
                "Comandos do sistema (status, screenshot, arquivos, Arduino...) "
                "funcionam normalmente! Diga 'cerebro local' para saber como me dar "
                "inteligência offline.")

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

# ══════════════════════════════════════════════════════════════
#  PROGRAMADORA — a IRIS escreve, testa, corrige e compacta código
# ══════════════════════════════════════════════════════════════
class Programadora:
    def __init__(self, ia):
        self.ia = ia
        self.pasta = Path.home() / "IRIS_Projetos"
        self.pasta.mkdir(exist_ok=True)
        self.ultimo_arquivo = None

    def _extrair_codigo(self, texto):
        """Extrai bloco de código da resposta da IA."""
        m = re.search(r"```(?:python|cpp|c\+\+|ino)?\s*\n(.*?)```", texto, re.DOTALL)
        return m.group(1).strip() if m else texto.strip()

    def _validar_python(self, codigo):
        """Compila sem executar. Retorna None se OK, ou a mensagem de erro."""
        try:
            compile(codigo, "<iris>", "exec")
            return None
        except SyntaxError as e:
            return "Linha " + str(e.lineno) + ": " + str(e.msg)

    def criar_projeto(self, nome):
        nome = re.sub(r"[^a-zA-Z0-9_-]", "_", nome.strip()) or "projeto"
        p = self.pasta / nome
        p.mkdir(exist_ok=True)
        (p / "main.py").write_text(
            '#!/usr/bin/env python3\n"""Projeto: ' + nome +
            ' — criado pela IRIS"""\n\ndef main():\n    print("Olá, ' + nome +
            '!")\n\nif __name__ == "__main__":\n    main()\n', encoding="utf-8")
        (p / "README.md").write_text(
            "# " + nome + "\nCriado pela IRIS em " +
            datetime.datetime.now().strftime("%d/%m/%Y") + "\n", encoding="utf-8")
        return ("Projeto '" + nome + "' criado em ~/IRIS_Projetos/" + nome +
                "\nCom main.py e README.md. Agora: programa [o que você quer]!")

    def programar(self, descricao, tentativas=3):
        """Gera código Python, VALIDA a sintaxe e auto-corrige se der erro."""
        codigo = self._extrair_codigo(self.ia.gemini_complexo(
            "Escreva um programa Python completo e funcional para: " + descricao +
            "\nComentários em português. Código limpo. "
            "Responda APENAS com o código dentro de um bloco ```python```."))
        historico_erros = []
        for tentativa in range(tentativas):
            erro = self._validar_python(codigo)
            if erro is None:
                break
            historico_erros.append(erro)
            codigo = self._extrair_codigo(self.ia.gemini_complexo(
                "Este código Python tem um erro de sintaxe: " + erro +
                "\nCorrija e responda APENAS com o código corrigido em ```python```:"
                "\n\n" + codigo[:5000]))
        nome = "prog_" + datetime.datetime.now().strftime("%d%m%Y_%H%M%S") + ".py"
        dest = self.pasta / nome
        dest.write_text(codigo, encoding="utf-8")
        self.ultimo_arquivo = str(dest)
        status = ("Sintaxe validada!" if self._validar_python(codigo) is None
                  else "ATENÇÃO: ainda há erro após " + str(tentativas) + " tentativas")
        return ("Programa criado: ~/IRIS_Projetos/" + nome + "\n" + status +
                ("\nAuto-correções: " + str(len(historico_erros)) if historico_erros else "") +
                "\n\n" + codigo[:500] +
                ("..." if len(codigo) > 500 else "") +
                "\n\nPara rodar: executa codigo " + nome)

    def _achar(self, arquivo):
        for cand in [Path(arquivo).expanduser(), self.pasta / arquivo,
                     Path.home() / arquivo]:
            if cand.exists():
                return cand
        return None

    def executar(self, arquivo):
        """Roda um script Python com timeout. CUIDADO: executa código de verdade!"""
        if not arquivo and self.ultimo_arquivo:
            arquivo = self.ultimo_arquivo
        p = self._achar(arquivo)
        if not p:
            return "Não achei '" + str(arquivo) + "'. Os programas ficam em ~/IRIS_Projetos/"
        try:
            r = subprocess.run([sys.executable, str(p)],
                               capture_output=True, text=True, timeout=20,
                               cwd=str(p.parent))
            saida = (r.stdout or "") + (("\nERROS:\n" + r.stderr) if r.stderr else "")
            return ("Executei " + p.name + ":\n" +
                    (saida[:600] if saida.strip() else "(sem saída)"))
        except subprocess.TimeoutExpired:
            return "Programa passou de 20s — interrompi por segurança."
        except Exception as e:
            return "Erro ao executar: " + str(e)

    def corrigir(self, arquivo):
        """Lê um arquivo com problema, roda, manda o erro pra IA e corrige."""
        p = self._achar(arquivo)
        if not p:
            return "Não achei '" + str(arquivo) + "'"
        codigo = p.read_text(encoding="utf-8", errors="ignore")
        erro = self._validar_python(codigo)
        if erro is None:
            # sintaxe OK — roda pra ver erro de execução
            try:
                r = subprocess.run([sys.executable, str(p)],
                                   capture_output=True, text=True, timeout=15)
                if not r.stderr:
                    return p.name + " está sem erros! Roda perfeitamente."
                erro = r.stderr[-800:]
            except Exception as e:
                erro = str(e)
        novo = self._extrair_codigo(self.ia.gemini_complexo(
            "Corrija este código Python que dá o erro abaixo. "
            "Responda APENAS com o código corrigido em ```python```.\n"
            "ERRO:\n" + str(erro) + "\n\nCÓDIGO:\n" + codigo[:5000]))
        if self._validar_python(novo) is None:
            backup = p.with_suffix(".bak.py")
            shutil.copy(str(p), str(backup))
            p.write_text(novo, encoding="utf-8")
            return ("Corrigi " + p.name + "! Original salvo como " + backup.name +
                    "\nErro que encontrei: " + str(erro)[:200])
        return "Tentei corrigir mas o resultado ainda tem erro. Me mostra o código no chat?"

    def compactar(self, arquivo):
        """Compacta código: remove comentários/linhas vazias + gera .gz."""
        p = self._achar(arquivo)
        if not p:
            return "Não achei '" + str(arquivo) + "'"
        original = p.read_text(encoding="utf-8", errors="ignore")
        tam_orig = len(original)
        # 1) Minificação leve e SEGURA (preserva strings e docstrings de linha única)
        linhas_min = []
        for linha in original.split("\n"):
            s = linha.rstrip()
            if not s.strip():
                continue                      # remove linha vazia
            sem_str = re.sub(r"(\"[^\"]*\"|\'[^\']*\')", "", s)
            if sem_str.strip().startswith("#"):
                continue                      # remove comentário de linha inteira
            if "#" in sem_str:                # remove comentário no fim da linha
                corte = s[:s.rindex("#")].rstrip()
                if corte and self._fecha_aspas(corte):
                    s = corte
            linhas_min.append(s)
        minificado = "\n".join(linhas_min)
        # valida: se quebrou a sintaxe, mantém só remoção de vazias/comentários puros
        if p.suffix == ".py" and self._validar_python(minificado) is not None:
            linhas_min = [l.rstrip() for l in original.split("\n")
                          if l.strip() and not l.strip().startswith("#")]
            minificado = "\n".join(linhas_min)
        dest_min = p.with_name(p.stem + "_min" + p.suffix)
        dest_min.write_text(minificado, encoding="utf-8")
        # 2) Compressão gzip do original
        import gzip
        dest_gz = p.with_suffix(p.suffix + ".gz")
        with gzip.open(str(dest_gz), "wb") as f:
            f.write(original.encode("utf-8"))
        tam_min = len(minificado)
        tam_gz = dest_gz.stat().st_size
        pct_min = round((1 - tam_min / max(tam_orig, 1)) * 100)
        pct_gz = round((1 - tam_gz / max(tam_orig, 1)) * 100)
        gz_txt = ("-" + str(pct_gz) + "%" if pct_gz >= 0
                  else "+" + str(-pct_gz) + "% — arquivo pequeno demais, gzip não compensa")
        return ("Compactei " + p.name + "!\n" +
                "Original:   " + str(tam_orig) + " bytes\n" +
                "Minificado: " + str(tam_min) + " bytes (-" + str(pct_min) +
                "%) -> " + dest_min.name + "\n" +
                "Gzip:       " + str(tam_gz) + " bytes (" + gz_txt +
                ") -> " + dest_gz.name)

    @staticmethod
    def _fecha_aspas(s):
        return s.count('"') % 2 == 0 and s.count("\'") % 2 == 0

    def listar_programas(self):
        arqs = sorted(self.pasta.rglob("*.py"))[:20]
        if not arqs:
            return "Nenhum programa ainda. Use: programa [descrição]"
        return "Programas em ~/IRIS_Projetos/:\n" + "\n".join(
            "- " + str(a.relative_to(self.pasta)) for a in arqs)

    def criar_plugin(self, descricao, tentativas=3):
        """A IRIS programa uma habilidade NOVA para si mesma (vira comando)."""
        pasta_plugins = Path.home() / "IRIS_Plugins"
        pasta_plugins.mkdir(exist_ok=True)
        modelo = (
            "Crie um PLUGIN Python para a assistente IRIS que faça: " + descricao + "\n"
            "REGRAS OBRIGATÓRIAS:\n"
            "1. Defina GATILHOS = lista de 1-3 frases curtas em português que ativam o plugin\n"
            "2. Defina DESCRICAO = string curta do que faz\n"
            "3. Defina def executar(args): que recebe string com os argumentos "
            "e RETORNA uma string com o resultado\n"
            "4. Use apenas biblioteca padrão do Python (os, math, datetime, random, "
            "json, re, urllib) — nada de pip install\n"
            "5. Trate erros com try/except retornando mensagem amigável\n"
            "6. NUNCA apague arquivos nem use comandos destrutivos\n"
            "Responda APENAS com o código em ```python```.")
        codigo = self._extrair_codigo(self.ia.gemini_complexo(modelo))
        for _ in range(tentativas):
            erro = self._validar_python(codigo)
            estrutura_ok = ("GATILHOS" in codigo and "def executar" in codigo)
            if erro is None and estrutura_ok:
                break
            problema = erro or "Faltou GATILHOS ou def executar(args)"
            codigo = self._extrair_codigo(self.ia.gemini_complexo(
                "Corrija este plugin (problema: " + str(problema) +
                "). Mantenha GATILHOS, DESCRICAO e def executar(args). "
                "Responda APENAS com o código em ```python```:\n\n" + codigo[:5000]))
        if self._validar_python(codigo) is not None or "def executar" not in codigo:
            return ("Não consegui gerar um plugin válido após " + str(tentativas) +
                    " tentativas. Tenta descrever de outro jeito?")
        # v26: TESTA o plugin executando numa caixa segura antes de ativar
        teste_ok, teste_msg = self._testar_plugin(codigo)
        nome = "plugin_" + re.sub(r"[^a-z0-9]+", "_", descricao.lower())[:24].strip("_")
        if not teste_ok:
            # não passou no teste: salva como rascunho pra você revisar, não ativa
            rasc = pasta_plugins / "rascunhos"
            rasc.mkdir(exist_ok=True)
            (rasc / (nome + ".py")).write_text(codigo, encoding="utf-8")
            return ("Criei o plugin '" + nome + "' mas ele FALHOU no teste (" +
                    teste_msg + "). Guardei como rascunho em ~/IRIS_Plugins/rascunhos/ "
                    "pra você revisar antes de eu usar. Segurança em primeiro lugar!")
        dest = pasta_plugins / (nome + ".py")
        dest.write_text(codigo, encoding="utf-8")
        # extrai os gatilhos para mostrar
        m = re.search(r"GATILHOS\s*=\s*\[(.*?)\]", codigo, re.DOTALL)
        gat = m.group(1).replace('"', "").replace("'", "").strip()[:120] if m else "?"
        return ("HABILIDADE NOVA TESTADA E ABSORVIDA! Plugin salvo: " + dest.name +
                "\nGatilhos: " + gat +
                "\nPassou no teste e já está ativa! (Use 'recarrega plugins' se precisar.)" +
                "\n\n" + codigo[:400] + ("..." if len(codigo) > 400 else ""))

    def _testar_plugin(self, codigo):
        """Executa o plugin numa caixa isolada pra ver se roda sem quebrar.
        Retorna (passou, mensagem). É o teste antes de fundir — segurança."""
        try:
            ns = {}
            exec(compile(codigo, "<plugin_teste>", "exec"), ns)
            func = ns.get("executar")
            if not callable(func):
                return (False, "sem função executar")
            # chama com entrada vazia e uma de teste — só pra ver se não explode
            for entrada in ["", "teste"]:
                try:
                    r = func(entrada)
                    if r is not None and not isinstance(r, str):
                        return (False, "executar não retornou texto")
                except Exception as e:
                    return (False, "erro ao rodar: " + str(e)[:40])
            return (True, "ok")
        except Exception as e:
            return (False, str(e)[:40])


# ══════════════════════════════════════════════════════════════
#  PLUGINS — a IRIS ABSORVE o que programa!
#  Qualquer .py em ~/IRIS_Plugins/ com GATILHOS e executar(args)
#  vira um comando NOVO da IRIS, na hora, sem reiniciar.
#  Modelo de plugin:
#      GATILHOS = ["meu comando", "outro jeito de chamar"]
#      DESCRICAO = "O que esse plugin faz"
#      def executar(args):
#          return "resultado que a IRIS fala"
# ══════════════════════════════════════════════════════════════
class Plugins:
    def __init__(self):
        self.pasta = Path.home() / "IRIS_Plugins"
        self.pasta.mkdir(exist_ok=True)
        self.plugins = {}
        self.erros = []
        self.carregar()

    def carregar(self):
        """Carrega/recarrega todos os plugins da pasta."""
        import importlib.util
        self.plugins = {}
        self.erros = []
        for f in sorted(self.pasta.glob("*.py")):
            try:
                spec = importlib.util.spec_from_file_location(
                    "iris_plugin_" + f.stem, str(f))
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                func = getattr(mod, "executar", None)
                if not callable(func):
                    self.erros.append(f.name + ": sem função executar(args)")
                    continue
                gatilhos = getattr(mod, "GATILHOS", [f.stem.replace("_", " ")])
                self.plugins[f.stem] = {
                    "gatilhos": [str(g).lower().strip() for g in gatilhos if g],
                    "func": func,
                    "desc": str(getattr(mod, "DESCRICAO", ""))[:80],
                    "arquivo": f.name}
            except Exception as e:
                self.erros.append(f.name + ": " + str(e)[:80])
                logging.exception(e)
        return ("Plugins carregados: " + str(len(self.plugins)) +
                ("\nCom erro: " + "; ".join(self.erros) if self.erros else ""))

    def tentar(self, prompt):
        """Se o prompt bate com algum gatilho, executa o plugin. Senão, None."""
        p = prompt.lower().strip()
        for nome, pl in self.plugins.items():
            for g in pl["gatilhos"]:
                if p == g or p.startswith(g + " "):
                    args = prompt.strip()[len(g):].strip()
                    try:
                        r = pl["func"](args)
                        return "[plugin " + nome + "] " + str(r)[:1500]
                    except Exception as e:
                        logging.exception(e)
                        return ("Plugin " + nome + " deu erro: " + str(e)[:200] +
                                "\nTenta: corrige " + pl["arquivo"])
        return None

    def listar(self):
        if not self.plugins:
            return ("Nenhum plugin ainda! Crie um com:\n"
                    "  cria plugin [o que ele deve fazer]\n"
                    "Ou coloque um .py em ~/IRIS_Plugins/ e use: recarrega plugins")
        linhas = ["PLUGINS INSTALADOS (" + str(len(self.plugins)) + "):"]
        for nome, pl in self.plugins.items():
            linhas.append("- " + nome + ": " + (pl["desc"] or "sem descrição") +
                          "\n    gatilhos: " + " | ".join(pl["gatilhos"][:3]))
        if self.erros:
            linhas.append("Com erro: " + "; ".join(self.erros))
        return "\n".join(linhas)

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

# ══════════════════════════════════════════════════════════════
#  AÇÕES — tudo que a IRIS pode fazer no sistema
# ══════════════════════════════════════════════════════════════
class Acoes:
    def __init__(self, usuario, memoria, ia):
        self.usuario = usuario
        self.mem = memoria
        self.ia = ia
        self.lembretes = []
        self._arduino = None
        self._vigia_ativo = False
        self._bot_ativo = False
        self._bot_callback = None
        self.processador = None   # setado pelo IRIS
        self.mon = None           # setado pelo IRIS
        self._rotinas = {}
        # v9.0 — novos módulos
        self.cerebro = CerebroLocal()        # inteligência offline
        self.rede = RedeNeuronal()           # neurônios ternários (NTM)
        self.prog = Programadora(ia)         # IRIS programadora
        self.proj = GerenciadorProjetos()    # v10: coordenadora de projetos
        self.plugins = Plugins()             # v11: habilidades que a IRIS absorve
        threading.Thread(target=self._checar_lembretes, daemon=True).start()
        self._iniciar_arduino()

    # ── ARDUINO (serial) ──
    def _iniciar_arduino(self):
        if not ARDUINO_ATIVO:
            return
        try:
            import serial
            self._arduino = serial.Serial(ARDUINO_PORTA, 9600, timeout=1)
        except Exception as _e:
            logging.exception(_e)

    def _arduino_cmd(self, cmd):
        if not self._arduino:
            return None
        try:
            self._arduino.write((cmd + "\n").encode())
            time.sleep(0.5)
            return self._arduino.readline().decode().strip()
        except Exception as _e:
            logging.exception(_e)
            return None

    def _reg(self, info):
        self.mem.registrar(info)

    # ── NOTIFICAÇÃO NATIVA ──
    def notificar(self, titulo, msg=""):
        try:
            subprocess.Popen(["notify-send", "-a", "IRIS", titulo, msg],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as _e:
            logging.exception(_e)

    # ── LUZ ──
    def luz(self, ligar):
        txt = "ligada" if ligar else "apagada"
        if ARDUINO_ATIVO:
            r = self._arduino_cmd("LUZ_ON" if ligar else "LUZ_OFF")
            self._reg("Luz " + txt + " via Arduino")
            return "Luz " + txt + "! Arduino: " + str(r)
        self._reg("Luz " + txt + " (simulado)")
        return "Luz " + txt + "! (Conecte o Arduino para valer de verdade)"

    # ── SISTEMA ──
    def status(self, mon):
        self._reg("Status do sistema")
        temp = " | " + str(round(mon.temp)) + "C" if mon.temp > 0 else ""
        bat = ("\nBat: " + str(round(mon.bat)) + "%" + ("+" if mon.plugado else "")
               if mon.bat > 0 else "")
        return ("CPU: " + str(round(mon.cpu)) + "%" + temp +
                "\nRAM: " + str(round(mon.ram)) + "% | Disco: " + str(round(mon.disco)) + "%" + bat +
                "\nRede: UP " + str(round(mon.net_up, 1)) + " DN " + str(round(mon.net_dn, 1)) + " KB/s")

    def otimizar(self):
        self._reg("Otimizou sistema")
        try:
            subprocess.run(["sync"], capture_output=True, timeout=5)
            cache = Path.home() / ".cache"
            tam = sum(f.stat().st_size for f in cache.rglob("*") if f.is_file()) // 1024**2
            return ("Sistema sincronizado!\nCache do usuário: " + str(tam) +
                    "MB (rm -rf ~/.cache/* para limpar)")
        except Exception:
            return "Sincronizado!"

    def processos(self, mon):
        self._reg("Listou processos")
        return "Top processos:\n" + "\n".join(
            "- " + n + ": " + str(round(c, 1)) + "%" for n, c in mon.get_procs())

    # ── MOUSE E TECLADO ──
    def mover_mouse(self, x, y):
        try:
            pyautogui.moveTo(x, y, duration=0.4)
            self._reg("Mouse movido para " + str(x) + "," + str(y))
            return "Mouse em (" + str(x) + ", " + str(y) + ")"
        except Exception as e:
            return "Erro: " + str(e)

    def clicar(self, duplo=False):
        try:
            pyautogui.doubleClick() if duplo else pyautogui.click()
            self._reg("Clique" + (" duplo" if duplo else ""))
            return ("Duplo clique" if duplo else "Clique") + " realizado!"
        except Exception as e:
            return "Erro: " + str(e)

    def digitar(self, texto):
        try:
            pyautogui.typewrite(texto, interval=0.04)
            self._reg("Digitou: " + texto[:30])
            return "Digitado: " + texto[:40]
        except Exception as e:
            return "Erro: " + str(e)

    def tecla(self, t):
        try:
            pyautogui.press(t)
            self._reg("Tecla: " + t)
            return "Tecla '" + t + "' pressionada!"
        except Exception as e:
            return "Erro: " + str(e)

    def posicao_mouse(self):
        p = pyautogui.position()
        return "Mouse em: (" + str(p.x) + ", " + str(p.y) + ")"

    # ── MULTIMODAL: TELA / IMAGEM / WEBCAM ──
    def analisar_tela(self, pergunta=None):
        try:
            tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            tmp.close()
            pyautogui.screenshot().save(tmp.name)
            q = pergunta or "Descreva brevemente o que está na tela, em português. Seja conciso."
            r = self.ia.gemini_visao(tmp.name, q)
            os.remove(tmp.name)
            self._reg("Analisou tela")
            return "Vejo na tela:\n" + r[:500]
        except Exception as e:
            return "Erro ao analisar tela: " + str(e)

    def analisar_imagem(self, caminho, pergunta=None):
        """Analisa qualquer imagem do disco — multimodal real."""
        p = Path(caminho).expanduser()
        if not p.exists():
            # tenta achar nas pastas comuns
            for pasta in [Path.home()/"Pictures", Path.home()/"Downloads", Path.home()]:
                cand = pasta / caminho
                if cand.exists():
                    p = cand
                    break
        if not p.exists():
            return "Não achei a imagem '" + str(caminho) + "'"
        r = self.ia.gemini_visao(str(p), pergunta or
                                 "Descreva esta imagem em português, em detalhes úteis.")
        self._reg("Analisou imagem: " + p.name)
        return "Sobre " + p.name + ":\n" + r[:600]

    def ver_pela_webcam(self):
        """Tira foto com a webcam e descreve o que vê — olhos da IRIS."""
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        tmp.close()
        try:
            subprocess.run(["fswebcam", "-r", "1280x720", "--no-banner", tmp.name],
                               capture_output=True, timeout=10)
            if not os.path.exists(tmp.name) or os.path.getsize(tmp.name) == 0:
                return "Webcam não disponível! (sudo apt install fswebcam)"
            desc = self.ia.gemini_visao(tmp.name,
                                        "Descreva o que você vê nesta foto de webcam, em português, de forma natural.")
            self._reg("Viu pela webcam")
            return "Pela webcam eu vejo:\n" + desc[:500]
        except Exception as e:
            return "Erro: " + str(e)
        finally:
            try:
                os.remove(tmp.name)
            except Exception:
                pass

    def ler_arquivo(self, caminho):
        """Lê e resume arquivos de texto/código."""
        p = Path(caminho).expanduser()
        if not p.exists():
            p = Path.home() / caminho
        if not p.exists():
            return "Não achei o arquivo '" + str(caminho) + "'"
        try:
            conteudo = p.read_text(encoding="utf-8", errors="ignore")[:6000]
            r = self.ia.gemini_complexo(
                "Resuma este arquivo em português, destacando o essencial:\n\n" + conteudo)
            self._reg("Leu arquivo: " + p.name)
            return "Resumo de " + p.name + ":\n" + r[:700]
        except Exception as e:
            return "Erro: " + str(e)

    # ── JANELAS ──
    def listar_janelas(self):
        try:
            r = subprocess.getoutput("wmctrl -l")
            self._reg("Listou janelas")
            return "Janelas:\n" + "\n".join(
                "- " + l.split(None, 3)[-1] for l in r.strip().split("\n") if l)
        except Exception as e:
            return "Erro: " + str(e)

    def focar_janela(self, nome):
        try:
            subprocess.run(["wmctrl", "-a", nome])
            self._reg("Focou: " + nome)
            return "Janela '" + nome + "' em foco!"
        except Exception as e:
            return "Erro: " + str(e)

    def minimizar_tudo(self):
        try:
            subprocess.run(["xdotool", "key", "super+d"])
            self._reg("Minimizou tudo")
            return "Desktop mostrado!"
        except Exception as e:
            return "Erro: " + str(e)

    # ── PROGRAMAS E SITES ──
    PROGS = {
        "firefox": "firefox", "chrome": "google-chrome", "chromium": "chromium",
        "terminal": "gnome-terminal", "arquivos": "nautilus", "calc": "gnome-calculator",
        "vscode": "code", "spotify": "spotify", "discord": "discord",
        "telegram": "telegram-desktop", "gimp": "gimp", "vlc": "vlc",
        "libreoffice": "libreoffice", "arduino": "arduino-ide", "gedit": "gedit",
        "quartus": "quartus",
    }

    def abrir_programa(self, nome):
        cmd = self.PROGS.get(nome.lower(), nome)
        try:
            subprocess.Popen([cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self._reg("Abriu: " + nome)
            return "Abrindo " + nome + "..."
        except Exception as e:
            return "Não consegui abrir '" + nome + "': " + str(e)

    def abrir_site(self, url):
        if not url.startswith("http"):
            url = "https://" + url
        try:
            subprocess.Popen(["xdg-open", url],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self._reg("Abriu site: " + url)
            return "Abrindo " + url + "..."
        except Exception as e:
            return "Erro: " + str(e)

    def google(self, query):
        return self.abrir_site("https://www.google.com/search?q=" + requests.utils.quote(query))

    def youtube(self, query):
        return self.abrir_site("https://www.youtube.com/results?search_query=" + requests.utils.quote(query))

    # ── ARQUIVOS ──
    def screenshot(self):
        nome = "screen_" + datetime.datetime.now().strftime("%d%m%Y_%H%M%S") + ".png"
        dest = str(Path.home() / "Pictures" / nome)
        try:
            Path(Path.home() / "Pictures").mkdir(exist_ok=True)
            pyautogui.screenshot(dest)
            self._reg("Screenshot: " + nome)
            return "Screenshot salvo em ~/Pictures/" + nome
        except Exception as e:
            return "Erro: " + str(e)

    def apagar_imagens(self):
        # v8: mais seguro — só apaga screenshots/fotos geradas pela IRIS
        apagados = []
        pics = Path.home() / "Pictures"
        if pics.exists():
            for f in pics.iterdir():
                if f.is_file() and (f.name.startswith("screen_") or
                                    f.name.startswith("foto_") or
                                    f.name.startswith("poco_") or
                                    f.name.startswith("grafico_cpu_")):
                    try:
                        f.unlink()
                        apagados.append(f.name)
                    except Exception as _e:
                        logging.exception(_e)
        self._reg("Apagou " + str(len(apagados)) + " imagens da IRIS")
        return (str(len(apagados)) + " imagens (geradas pela IRIS) apagadas!"
                if apagados else "Nenhuma imagem da IRIS encontrada. "
                "Por segurança não apago suas fotos pessoais.")


    # ══════════════════════════════════════════
    #  GESTÃO DE FOTOS (v1.5) — autonomia COM
    #  confirmação. Ela vê, descreve e pergunta
    #  antes de apagar/mover qualquer foto.
    # ══════════════════════════════════════════
    EXT_FOTO = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".heic")

    def listar_fotos(self, pasta=""):
        """Lista as fotos de uma pasta (Pictures por padrão)."""
        home = Path.home().resolve()
        base = (home / pasta) if pasta.strip() else (home / "Pictures")
        if not base.exists():
            for alt in [home / "Imagens", home / "DCIM", home / "Downloads"]:
                if alt.exists():
                    base = alt
                    break
        if not base.exists():
            return "Não achei a pasta de fotos. Tenta: ver fotos de Downloads"
        fotos = [f for f in base.iterdir() if f.is_file() and f.suffix.lower() in self.EXT_FOTO]
        if not fotos:
            return "Nenhuma foto em " + str(base)
        fotos.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        r = ["FOTOS em " + str(base) + " (" + str(len(fotos)) + " no total):"]
        for f in fotos[:15]:
            tam = f.stat().st_size // 1024
            r.append("- " + f.name + " (" + str(tam) + "KB)")
        if len(fotos) > 15:
            r.append("...e mais " + str(len(fotos) - 15))
        return "\n".join(r)

    def descrever_foto(self, nome):
        """Usa o Gemini pra dizer o que tem numa foto (antes de você decidir apagar)."""
        arq = self._achar_foto(nome)
        if not arq:
            return "Não achei a foto '" + nome + "'"
        if not self.ia.gemini:
            return "Pra descrever fotos eu preciso da chave do Gemini."
        desc = self.ia.gemini_visao(str(arq), "Descreva brevemente o que há nesta foto, em português.")
        return "Foto '" + arq.name + "':\n" + desc

    def _achar_foto(self, nome):
        """Localiza uma foto pelo nome em vários lugares comuns."""
        home = Path.home().resolve()
        nome = nome.strip()
        locais = [Path(nome).expanduser(), home / nome,
                  home / "Pictures" / nome, home / "Imagens" / nome,
                  home / "Downloads" / nome, home / "DCIM" / nome]
        for c in locais:
            if c.exists() and c.is_file() and c.suffix.lower() in self.EXT_FOTO:
                return c.resolve()
        # busca por nome parcial em Pictures/Imagens
        for pasta in [home / "Pictures", home / "Imagens", home / "Downloads"]:
            if pasta.exists():
                for f in pasta.iterdir():
                    if f.is_file() and nome.lower() in f.name.lower() and f.suffix.lower() in self.EXT_FOTO:
                        return f.resolve()
        return None

    def preparar_apagar_foto(self, nome):
        """Localiza a foto, DESCREVE o que é e PEDE confirmação antes de apagar.
        Retorna (mensagem, caminho_pendente_ou_None)."""
        if not nome.strip():
            return ("Qual foto? Ex: apaga foto IMG_2034.jpg", None)
        arq = self._achar_foto(nome)
        if not arq:
            return ("Não achei a foto '" + nome + "'", None)
        home = Path.home().resolve()
        if home not in arq.parents:
            return ("NEGADO: só apago fotos DENTRO da sua home.", None)
        if any(p.startswith(".") for p in arq.relative_to(home).parts):
            return ("NEGADO: não mexo em arquivos ocultos/de configuração.", None)
        tam = arq.stat().st_size // 1024
        # tenta descrever a foto pra você saber o que está apagando
        preview = ""
        if self.ia.gemini:
            try:
                d = self.ia.gemini_visao(str(arq), "Em uma frase curta, o que há nesta foto?")
                preview = "\nParece ser: " + d.strip()[:100]
            except Exception:
                pass
        return ("ATENÇÃO — vou apagar PERMANENTEMENTE esta foto:\n" + str(arq) +
                "\nTamanho: " + str(tam) + "KB" + preview +
                "\n\nResponda 'sim' pra confirmar ou qualquer coisa pra cancelar.",
                str(arq))

    def apagar_foto_confirmada(self, caminho):
        try:
            arq = Path(caminho); home = Path.home().resolve()
            if not arq.exists() or home not in arq.resolve().parents:
                return "Cancelado por segurança."
            arq.unlink()
            self._reg("Apagou foto (confirmado): " + arq.name)
            return "Foto apagada: " + arq.name
        except Exception as e:
            return "Erro ao apagar foto: " + str(e)

    def organizar_fotos(self, pasta=""):
        """Organiza fotos em subpastas por ano-mês. Não apaga nada, só arruma."""
        home = Path.home().resolve()
        base = (home / pasta) if pasta.strip() else (home / "Pictures")
        if not base.exists():
            return "Não achei a pasta. Ex: organiza fotos de Downloads"
        fotos = [f for f in base.iterdir() if f.is_file() and f.suffix.lower() in self.EXT_FOTO]
        if not fotos:
            return "Nenhuma foto pra organizar em " + str(base)
        movidas = 0
        for f in fotos:
            try:
                dt = datetime.datetime.fromtimestamp(f.stat().st_mtime)
                sub = base / dt.strftime("%Y-%m")
                sub.mkdir(exist_ok=True)
                destino = sub / f.name
                if not destino.exists():
                    shutil.move(str(f), str(destino))
                    movidas += 1
            except Exception as _e:
                logging.exception(_e)
        self._reg("Organizou " + str(movidas) + " fotos")
        return ("Organizei " + str(movidas) + " fotos em " + str(base) +
                " por ano-mês (ex: 2026-06). Nada foi apagado, só arrumado!")


    # ══════════════════════════════════════════
    #  FERRAMENTAS DO FRANCISCO (v1.6) — busca de
    #  arquivos, backup de projetos, diário do livro,
    #  duplicados e análise de aparelhos. Tudo com
    #  confirmação antes de qualquer coisa destrutiva.
    # ══════════════════════════════════════════
    def buscar_arquivo(self, nome):
        """Varre a home procurando um arquivo pelo nome (parcial). Não apaga nada."""
        if not nome.strip():
            return "O que procurar? Ex: acha arquivo capitulo 3"
        home = Path.home()
        termo = nome.lower().strip()
        achados = []
        try:
            for f in home.rglob("*"):
                # pula pastas ocultas e de sistema
                if any(p.startswith(".") for p in f.parts):
                    continue
                if f.is_file() and termo in f.name.lower():
                    achados.append(f)
                    if len(achados) >= 20:
                        break
        except Exception as _e:
            logging.exception(_e)
        if not achados:
            return "Não achei nenhum arquivo com '" + nome + "' no nome."
        achados.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        r = ["Achei " + str(len(achados)) + " arquivo(s) com '" + nome + "':"]
        for f in achados[:15]:
            dt = datetime.datetime.fromtimestamp(f.stat().st_mtime).strftime("%d/%m/%Y")
            r.append("- " + f.name + "  (" + str(f.parent).replace(str(home), "~") + ", " + dt + ")")
        self._reg("Buscou arquivo: " + nome)
        return "\n".join(r)

    def backup_projetos(self):
        """Faz backup compactado dos projetos importantes (livro, NTM, exo, códigos)."""
        home = Path.home()
        destino = home / "Backups_IRIS" / "projetos"
        destino.mkdir(parents=True, exist_ok=True)
        # pastas/arquivos importantes pra você
        importantes = []
        for cand in [home / "IRIS_Projetos", home / "Documents", home / "Documentos"]:
            if cand.exists():
                importantes.append(cand)
        if not importantes:
            return "Não achei pastas de projeto pra fazer backup."
        nome = "backup_" + datetime.datetime.now().strftime("%Y%m%d_%H%M") + ".tar.gz"
        arq = destino / nome
        try:
            cmd = ["tar", "-czf", str(arq)]
            for p in importantes:
                cmd += ["-C", str(p.parent), p.name]
            res = subprocess.run(cmd, capture_output=True, timeout=120)
            if res.returncode == 0:
                tam = arq.stat().st_size // (1024 * 1024)
                self._reg("Backup de projetos")
                return ("Backup feito! " + nome + " (" + str(tam) + "MB)\n"
                        "Guardado em ~/Backups_IRIS/projetos/\n"
                        "Protegi: " + ", ".join(p.name for p in importantes))
            return "Erro no backup: " + res.stderr.decode()[:150]
        except Exception as e:
            return "Erro no backup: " + str(e)

    def diario_livro(self, texto=""):
        """Diário de bordo do livro Érebo Kingdoms. Sem texto, mostra o histórico."""
        arq = Path.home() / "IRIS_Projetos" / "diario_erebo.txt"
        arq.parent.mkdir(parents=True, exist_ok=True)
        if not texto.strip():
            if not arq.exists():
                return ("Diário do Érebo vazio. Registre com: diario livro escrevi o capítulo 7 hoje")
            linhas = arq.read_text(encoding="utf-8").strip().split("\n")
            return "DIÁRIO DO ÉREBO KINGDOMS (últimas entradas):\n" + "\n".join(linhas[-12:])
        agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        with open(arq, "a", encoding="utf-8") as f:
            f.write("[" + agora + "] " + texto.strip() + "\n")
        self._reg("Diário do livro")
        return "Anotado no diário do Érebo! 📖 " + texto.strip()[:60]

    def achar_duplicados(self, pasta=""):
        """Acha arquivos duplicados (mesmo conteúdo) e mostra — só apaga com confirmação.
        Retorna (mensagem, lista_para_apagar_ou_None)."""
        import hashlib
        home = Path.home()
        base = (home / pasta) if pasta.strip() else (home / "Downloads")
        if not base.exists():
            return ("Não achei a pasta. Ex: acha duplicados em Pictures", None)
        hashes = {}
        dups = []
        try:
            for f in base.rglob("*"):
                if f.is_file() and not any(p.startswith(".") for p in f.parts):
                    try:
                        h = hashlib.md5(f.read_bytes()).hexdigest()
                        if h in hashes:
                            dups.append((f, hashes[h]))
                        else:
                            hashes[h] = f
                    except Exception:
                        continue
        except Exception as e:
            return ("Erro ao varrer: " + str(e), None)
        if not dups:
            return ("Nenhum arquivo duplicado em " + str(base) + ". Tudo limpo!", None)
        tam = sum(d[0].stat().st_size for d in dups) // 1024
        r = ["Achei " + str(len(dups)) + " duplicado(s) em " + str(base) +
             " (" + str(tam) + "KB desperdiçados):"]
        for novo, orig in dups[:10]:
            r.append("- " + novo.name + " (cópia de " + orig.name + ")")
        r.append("\nResponda 'sim' pra eu apagar as CÓPIAS (mantenho os originais).")
        return ("\n".join(r), [str(d[0]) for d in dups])

    def apagar_duplicados_confirmado(self, lista):
        home = Path.home().resolve()
        apagados = 0
        for caminho in lista:
            try:
                f = Path(caminho)
                if f.exists() and home in f.resolve().parents:
                    f.unlink()
                    apagados += 1
            except Exception as _e:
                logging.exception(_e)
        self._reg("Apagou " + str(apagados) + " duplicados")
        return "Apaguei " + str(apagados) + " cópias duplicadas. Os originais estão a salvo!"

    def analisar_aparelhos(self):
        """Analisa o PC e o celular e SUGERE melhorias reais e eficazes."""
        dados = []
        # PC
        if self.mon:
            dados.append("PC: CPU " + str(round(self.mon.cpu)) + "%, RAM " +
                         str(round(self.mon.ram)) + "%, disco " + str(round(self.mon.disco)) +
                         "%, bateria " + str(round(self.mon.bat)) + "%")
        # celular
        if self._adb_conectado() or self._adb_wifi():
            dados.append("Poco X7 conectado na rede")
        else:
            dados.append("Poco X7 não conectado agora")
        # pede análise prática à IA
        sugestao = self.ia.gemini_complexo(
            "Você é a IRIS, assistente do Francisco (Linux Ryzen 7, Poco X7, faz projetos "
            "de Arduino/FPGA/IA). Com base no estado atual dos aparelhos:\n" +
            "\n".join(dados) +
            "\nSugira 3 a 4 melhorias CONCRETAS e EFICAZES pra otimizar/aproveitar melhor "
            "os aparelhos dele (software livre, ajustes, automações úteis). Práticas e "
            "realistas pro hardware modesto. Em português, direto, sem enrolação.")
        self._reg("Analisou aparelhos")
        return "ANÁLISE DOS SEUS APARELHOS:\n" + "\n".join(dados) + "\n\nSUGESTÕES:\n" + sugestao

    def listar_arquivos(self, pasta=None):
        p = Path(pasta).expanduser() if pasta else Path.home()
        try:
            items = list(p.iterdir())[:20]
            dirs = ["D " + f.name for f in items if f.is_dir()]
            files = ["F " + f.name for f in items if f.is_file()]
            self._reg("Listou arquivos")
            return "Arquivos em " + str(p) + ":\n" + "\n".join(dirs + files)
        except Exception as e:
            return "Erro: " + str(e)

    def criar_arquivo(self, nome, conteudo=""):
        try:
            p = Path.home() / nome
            p.write_text(conteudo, encoding="utf-8")
            self._reg("Criou: " + nome)
            return "Arquivo '" + nome + "' criado!"
        except Exception as e:
            return "Erro: " + str(e)

    # ── VOLUME ──
    def volume(self, acao):
        cmds = {"up": ["amixer", "-q", "sset", "Master", "10%+"],
                "down": ["amixer", "-q", "sset", "Master", "10%-"],
                "mudo": ["amixer", "-q", "sset", "Master", "toggle"]}
        labels = {"up": "Volume aumentado!", "down": "Volume diminuído!", "mudo": "Mudo alternado!"}
        try:
            subprocess.run(cmds[acao], capture_output=True, timeout=3)
            self._reg("Volume: " + acao)
            return labels[acao]
        except Exception:
            return "amixer não disponível"

    # ── MÚSICA ──
    def musica(self, acao):
        cmds = {"play": "play", "pause": "pause", "proxima": "next",
                "anterior": "previous", "parar": "stop"}
        try:
            subprocess.run(["playerctl", cmds.get(acao, "play")],
                           capture_output=True, timeout=3)
            self._reg("Musica: " + acao)
            return "Música: " + acao + "!"
        except Exception:
            return "Instala: sudo apt install playerctl"

    # ── WEBCAM (foto simples) ──
    def foto_webcam(self):
        nome = "foto_" + datetime.datetime.now().strftime("%d%m%Y_%H%M%S") + ".jpg"
        dest = str(Path.home() / "Pictures" / nome)
        try:
            Path(Path.home() / "Pictures").mkdir(exist_ok=True)
            subprocess.run(["fswebcam", "-r", "1280x720", "--no-banner", dest],
                           capture_output=True, timeout=10)
            self._reg("Foto webcam: " + nome)
            return "Foto salva em ~/Pictures/" + nome
        except Exception:
            return "Instala: sudo apt install fswebcam"

    # ── TRADUÇÃO ──
    def traduzir(self, texto, destino="en"):
        try:
            r = requests.get(
                "https://api.mymemory.translated.net/get?q=" +
                requests.utils.quote(texto) + "&langpair=pt|" + destino,
                timeout=5).json()
            trad = r["responseData"]["translatedText"]
            self._reg("Traduziu para " + destino)
            return "Tradução (" + destino + "):\n" + trad
        except Exception as e:
            return "Erro: " + str(e)

    # ── REDE ──
    def monitorar_rede(self):
        try:
            ip = socket.gethostbyname(socket.gethostname())
            rede = ".".join(ip.split(".")[:-1]) + ".0/24"
            r = subprocess.getoutput("nmap -sn " + rede + " 2>/dev/null | grep 'report for'")
            self._reg("Monitorou rede")
            return "Rede " + rede + ":\n" + (r[:300] if r else "Nenhum dispositivo encontrado")
        except Exception as e:
            return "Erro: " + str(e)

    def testar_internet(self):
        try:
            t0 = time.time()
            requests.get("https://www.google.com", timeout=5)
            lat = round((time.time() - t0) * 1000)
            qual = "Ótima" if lat < 100 else "Razoável" if lat < 300 else "Lenta"
            self._reg("Testou internet")
            return "Internet: " + qual + " | Latência: " + str(lat) + "ms"
        except Exception:
            return "Sem conexão!"

    # ══════════════════════════════════════════
    #  ARDUINO TOTAL (v11) — firmware universal
    #  Grave UMA vez e a IRIS controla servo, LED,
    #  PWM e sensores direto, sem reprogramar.
    # ══════════════════════════════════════════
    FIRMWARE = """// IRIS Firmware Universal v1 — gerado pela IRIS
// Protocolo serial 9600: comandos terminados em \\n
//   PING                -> PONG
//   LED <pino> ON|OFF   -> liga/desliga digital
//   PWM <pino> <0-255>  -> analogWrite
//   SERVO <pino> <0-180>-> move servo
//   LER A<n>            -> analogRead
//   LER D<n>            -> digitalRead
#include <Servo.h>
Servo servos[14];
bool servoOn[14] = {false};
String buf = "";

void setup() {
  Serial.begin(9600);
  Serial.println("IRIS_FIRMWARE_OK");
}

void processa(String cmd) {
  cmd.trim(); cmd.toUpperCase();
  if (cmd == "PING") { Serial.println("PONG"); return; }
  if (cmd.startsWith("LED ")) {
    int sp = cmd.indexOf(' ', 4);
    int pino = cmd.substring(4, sp).toInt();
    bool on = cmd.endsWith("ON");
    pinMode(pino, OUTPUT);
    digitalWrite(pino, on ? HIGH : LOW);
    Serial.println("LED " + String(pino) + (on ? " LIGADO" : " DESLIGADO"));
    return;
  }
  if (cmd.startsWith("PWM ")) {
    int sp = cmd.indexOf(' ', 4);
    int pino = cmd.substring(4, sp).toInt();
    int val = cmd.substring(sp + 1).toInt();
    pinMode(pino, OUTPUT);
    analogWrite(pino, constrain(val, 0, 255));
    Serial.println("PWM " + String(pino) + "=" + String(val));
    return;
  }
  if (cmd.startsWith("SERVO ")) {
    int sp = cmd.indexOf(' ', 6);
    int pino = cmd.substring(6, sp).toInt();
    int ang = constrain(cmd.substring(sp + 1).toInt(), 0, 180);
    if (pino >= 0 && pino < 14) {
      if (!servoOn[pino]) { servos[pino].attach(pino); servoOn[pino] = true; }
      servos[pino].write(ang);
      Serial.println("SERVO " + String(pino) + "->" + String(ang));
    }
    return;
  }
  if (cmd.startsWith("LER A")) {
    int n = cmd.substring(5).toInt();
    Serial.println("A" + String(n) + "=" + String(analogRead(n)));
    return;
  }
  if (cmd.startsWith("LER D")) {
    int n = cmd.substring(5).toInt();
    pinMode(n, INPUT);
    Serial.println("D" + String(n) + "=" + String(digitalRead(n)));
    return;
  }
  Serial.println("ERRO: comando desconhecido");
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\\n') { processa(buf); buf = ""; }
    else if (c != '\\r') buf += c;
  }
}
"""

    def instalar_firmware(self):
        """Gera o firmware universal e tenta gravar no Arduino."""
        pasta = Path.home() / "iris_firmware"
        pasta.mkdir(exist_ok=True)
        ino = pasta / "iris_firmware.ino"
        ino.write_text(self.FIRMWARE, encoding="utf-8")
        self._reg("Gerou firmware universal")
        if shutil.which("arduino-cli"):
            r = self.arduino_gravar(str(ino))
            return ("Firmware universal salvo em ~/iris_firmware/iris_firmware.ino\n" + r +
                    "\nAgora: servo 90 | liga led 13 | pwm 5 200 | le sensor a0 | ping arduino")
        return ("Firmware salvo em ~/iris_firmware/iris_firmware.ino!\n"
                "Grave UMA vez (pela IDE do Arduino, ou instale o arduino-cli e diga "
                "'grava arduino iris_firmware/iris_firmware.ino').\n"
                "Depois eu controlo tudo direto: servo 90 | liga led 13 | pwm 5 200 | "
                "le sensor a0 | ping arduino")

    def servo(self, graus, pino=9):
        graus = max(0, min(int(graus), 180))
        return self.arduino_enviar("SERVO " + str(pino) + " " + str(graus))

    def led(self, pino, ligar=True):
        return self.arduino_enviar("LED " + str(pino) + (" ON" if ligar else " OFF"))

    def pwm(self, pino, valor):
        valor = max(0, min(int(valor), 255))
        return self.arduino_enviar("PWM " + str(pino) + " " + str(valor))

    def ler_sensor(self, qual):
        qual = qual.upper().strip()
        if not re.fullmatch(r"[AD]\d{1,2}", qual):
            return "Use: le sensor a0 (analógico) ou le sensor d7 (digital)"
        return self.arduino_enviar("LER " + qual)

    def ping_arduino(self):
        r = self.arduino_enviar("PING")
        if "PONG" in r:
            return "Arduino respondeu PONG! Firmware universal rodando. Tudo sob controle."
        return r + "\n(Sem PONG? Grave o firmware: instala firmware)"

    # ══════════════════════════════════════════
    #  APAGAR PASTA — sempre com confirmação! (v11)
    # ══════════════════════════════════════════
    def preparar_apagar_pasta(self, caminho):
        """Localiza a pasta, mostra o que será perdido e PEDE confirmação.
        Retorna (mensagem, caminho_pendente_ou_None)."""
        if not caminho.strip():
            return ("Qual pasta? Ex: apaga pasta testes_velhos", None)
        home = Path.home().resolve()
        candidatos = [Path(caminho).expanduser(), home / caminho,
                      home / "Downloads" / caminho, home / "Documents" / caminho,
                      home / "IRIS_Projetos" / caminho]
        pasta = next((c for c in candidatos if c.exists() and c.is_dir()), None)
        if not pasta:
            return ("Não achei a pasta '" + caminho + "'", None)
        pasta = pasta.resolve()
        # PROTEÇÕES: nunca a home, nunca fora da home, nunca pastas ocultas de config
        if pasta == home or home not in pasta.parents:
            return ("NEGADO: só apago pastas DENTRO da sua home, e nunca a home inteira.", None)
        if any(parte.startswith(".") for parte in pasta.relative_to(home).parts):
            return ("NEGADO: não apago pastas ocultas/de configuração (." +
                    pasta.relative_to(home).parts[0].lstrip(".") + ").", None)
        protegidas = {"documents", "pictures", "videos", "music", "downloads",
                      "desktop", "área de trabalho", "iris_projetos"}
        if len(pasta.relative_to(home).parts) == 1 and pasta.name.lower() in protegidas:
            return ("NEGADO: '" + pasta.name + "' é uma pasta principal sua. "
                    "Posso apagar SUBpastas dela, mas não ela inteira.", None)
        arquivos = [f for f in pasta.rglob("*") if f.is_file()]
        tam = sum(f.stat().st_size for f in arquivos) // 1024
        exemplos = ", ".join(f.name for f in arquivos[:4])
        return ("ATENÇÃO — vou apagar PERMANENTEMENTE:\n" + str(pasta) +
                "\n" + str(len(arquivos)) + " arquivo(s), " + str(tam) + "KB" +
                ("\nEx: " + exemplos if exemplos else "") +
                "\n\nResponda 'sim' para confirmar ou qualquer outra coisa para cancelar.",
                str(pasta))


    # ══════════════════════════════════════════
    #  GESTÃO DE ARQUIVOS (v1.4) — autonomia COM
    #  confirmação. Ela explica o que vai fazer e
    #  pergunta antes de qualquer ação destrutiva.
    # ══════════════════════════════════════════
    def preparar_apagar_arquivo(self, caminho):
        """Localiza o arquivo, explica o que será perdido e PEDE confirmação.
        Retorna (mensagem, caminho_pendente_ou_None)."""
        if not caminho.strip():
            return ("Qual arquivo? Ex: apaga arquivo rascunho.txt", None)
        home = Path.home().resolve()
        candidatos = [Path(caminho).expanduser(), home / caminho,
                      home / "Downloads" / caminho, home / "Documents" / caminho,
                      home / "Área de trabalho" / caminho, home / "Desktop" / caminho,
                      home / "IRIS_Projetos" / caminho]
        arq = next((c for c in candidatos if c.exists() and c.is_file()), None)
        if not arq:
            return ("Não achei o arquivo '" + caminho + "'", None)
        arq = arq.resolve()
        # PROTEÇÕES: dentro da home, nunca ocultos/config, nunca arquivos da própria IRIS
        if home not in arq.parents:
            return ("NEGADO: só apago arquivos DENTRO da sua home.", None)
        if any(p.startswith(".") for p in arq.relative_to(home).parts):
            return ("NEGADO: não mexo em arquivos ocultos/de configuração.", None)
        if arq.name.startswith("iris") or arq.name in ("iris.py",) or arq.suffix == ".py" and "iris_core" in str(arq):
            return ("NEGADO: esse é um arquivo meu — não vou me apagar! :)", None)
        tam = arq.stat().st_size // 1024
        return ("ATENÇÃO — vou apagar PERMANENTEMENTE este arquivo:\n" + str(arq) +
                "\nTamanho: " + str(tam) + "KB\n\n"
                "Responda 'sim' para confirmar ou qualquer coisa para cancelar.",
                str(arq))

    def apagar_arquivo_confirmado(self, caminho):
        try:
            arq = Path(caminho); home = Path.home().resolve()
            if not arq.exists() or home not in arq.resolve().parents:
                return "Cancelado por segurança."
            arq.unlink()
            self._reg("Apagou arquivo (confirmado): " + str(arq))
            return "Arquivo apagado: " + arq.name
        except Exception as e:
            return "Erro ao apagar: " + str(e)

    def criar_pasta(self, caminho):
        """Cria uma pasta nova. Criar não é destrutivo, então faz direto
        (mas dentro da home, por segurança)."""
        if not caminho.strip():
            return "Qual o nome da pasta? Ex: cria pasta MeusTestes"
        home = Path.home().resolve()
        # se vier caminho relativo, cria na home; se absoluto, valida que é dentro da home
        nova = Path(caminho).expanduser()
        if not nova.is_absolute():
            nova = home / caminho
        nova = nova.resolve()
        if home != nova and home not in nova.parents:
            return "NEGADO: só crio pastas dentro da sua home, por segurança."
        try:
            if nova.exists():
                return "A pasta '" + nova.name + "' já existe em " + str(nova.parent)
            nova.mkdir(parents=True)
            self._reg("Criou pasta: " + str(nova))
            return "Pasta criada: " + str(nova)
        except Exception as e:
            return "Erro ao criar pasta: " + str(e)

    def mover_arquivo(self, args):
        """Move/renomeia um arquivo. Uso: move ORIGEM para DESTINO"""
        partes = re.split(r"\s+(?:para|pra|->)\s+", args.strip(), maxsplit=1)
        if len(partes) != 2:
            return "Uso: move arquivo.txt para NovaPasta (ou: move a.txt para b.txt)"
        home = Path.home().resolve()
        origem = next((c for c in [Path(partes[0]).expanduser(), home / partes[0],
                                   home / "Downloads" / partes[0]] if c.exists()), None)
        if not origem:
            return "Não achei a origem '" + partes[0] + "'"
        destino = Path(partes[1]).expanduser()
        if not destino.is_absolute():
            destino = home / partes[1]
        try:
            if home not in origem.resolve().parents or (home != destino.resolve() and home not in destino.resolve().parents):
                return "NEGADO: só movo dentro da sua home."
            shutil.move(str(origem), str(destino))
            self._reg("Moveu: " + origem.name)
            return "Movido: " + origem.name + " -> " + str(destino)
        except Exception as e:
            return "Erro ao mover: " + str(e)

    def apagar_pasta_confirmada(self, caminho):
        try:
            pasta = Path(caminho)
            home = Path.home().resolve()
            if not pasta.exists() or pasta.resolve() == home or home not in pasta.resolve().parents:
                return "Cancelado por segurança."
            shutil.rmtree(str(pasta))
            self._reg("Apagou pasta (confirmado): " + str(pasta))
            return "Pasta apagada: " + str(pasta)
        except Exception as e:
            return "Erro ao apagar: " + str(e)

    # ══════════════════════════════════════════
    #  AUTODIAGNÓSTICO (v12) — a IRIS se examina
    # ══════════════════════════════════════════
    def diagnostico(self):
        """Verifica todas as dependências e diz exatamente o que falta."""
        import importlib.util
        ok, falta = [], []

        def _bin(nome, pacote, essencial=False):
            if shutil.which(nome):
                ok.append(nome)
            else:
                falta.append(("[!] " if essencial else "[ ] ") + nome +
                             " -> sudo apt install " + pacote)

        def _py(nome, pip_nome):
            if importlib.util.find_spec(nome):
                ok.append(nome)
            else:
                falta.append("[ ] " + nome + " -> pip3 install " + pip_nome +
                             " --break-system-packages")

        _bin("mpg123", "mpg123", essencial=True)        # voz
        _bin("xclip", "xclip")                           # colar Ctrl+V
        _bin("wmctrl", "wmctrl")                         # janelas
        _bin("xdotool", "xdotool")                       # minimizar
        _bin("fswebcam", "fswebcam")                     # webcam
        _bin("adb", "adb")                               # Poco X7
        _bin("playerctl", "playerctl")                   # música
        _bin("nmap", "nmap")                             # rede
        _bin("notify-send", "libnotify-bin")             # notificações
        if shutil.which("arduino-cli"):
            ok.append("arduino-cli")
        else:
            falta.append("[ ] arduino-cli -> curl -fsSL https://raw.githubusercontent.com/"
                         "arduino/arduino-cli/master/install.sh | sh")
        _py("edge_tts", "edge-tts")                      # voz neural
        _py("speech_recognition", "SpeechRecognition")   # ouvir (F2)
        _py("pyaudio", "pyaudio")                        # microfone
        _py("serial", "pyserial")                        # Arduino serial
        _py("cv2", "opencv-python")                      # modo vigia
        _py("matplotlib", "matplotlib")                  # gráfico CPU
        # Chaves e serviços
        chaves = []
        chaves.append("Groq: " + ("OK" if GROQ_API_KEY else "FALTANDO (iris_config.json)"))
        chaves.append("Gemini: " + ("OK" if GEMINI_API_KEY else "FALTANDO (visão/multimodal off)"))
        chaves.append("Telegram: " + ("OK" if TELEGRAM_TOKEN else "não configurado"))
        chaves.append("Cérebro local: " + ("Ollama " + str(self.cerebro.modelo)
                                           if self.cerebro.disponivel() else "modo básico"))
        try:
            requests.get("https://www.google.com", timeout=4)
            chaves.append("Internet: OK")
        except Exception:
            chaves.append("Internet: OFFLINE")
        self._reg("Autodiagnóstico")
        rel = ["AUTODIAGNÓSTICO DA IRIS:",
               "Funcionando (" + str(len(ok)) + "): " + ", ".join(ok)]
        if falta:
            rel.append("\nFaltando (" + str(len(falta)) + ") — copie e cole no terminal:")
            rel += falta
        else:
            rel.append("\nTODAS as dependências instaladas! Estou completa.")
        rel.append("\n" + "\n".join(chaves))
        return "\n".join(rel)

    # ══════════════════════════════════════════
    #  GUARDIÃ (v12) — a IRIS protege a si mesma
    #  Backup automático do iris.py + memórias a
    #  cada inicialização. Guarda as 10 últimas.
    # ══════════════════════════════════════════
    PASTA_GUARDIA = Path.home() / "Backups_IRIS" / "versoes"

    def guardia_backup(self):
        """Snapshot de si mesma e dos dados. Chamada na inicialização."""
        try:
            self.PASTA_GUARDIA.mkdir(parents=True, exist_ok=True)
            carimbo = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            destino = self.PASTA_GUARDIA / carimbo
            destino.mkdir(exist_ok=True)
            alvos = [Path(os.path.abspath(sys.argv[0] if sys.argv else "iris.py")),
                     Path("iris_memoria.json"), Path("iris_projetos.json"),
                     Path("iris_rede.json"), Path("iris_contexto.json"),
                     Path("iris_notas.txt")]
            copiados = 0
            for a in alvos:
                if a.exists() and a.is_file():
                    shutil.copy(str(a), str(destino / a.name))
                    copiados += 1
            # mantém só as 10 versões mais recentes
            versoes = sorted(self.PASTA_GUARDIA.iterdir())
            for velha in versoes[:-10]:
                shutil.rmtree(str(velha), ignore_errors=True)
            logging.info("Guardiã: backup %s com %d arquivos", carimbo, copiados)
            return carimbo
        except Exception as _e:
            logging.exception(_e)
            return None

    def guardia_listar(self):
        if not self.PASTA_GUARDIA.exists():
            return "Nenhum backup ainda — o primeiro é criado quando eu inicio."
        versoes = sorted(self.PASTA_GUARDIA.iterdir(), reverse=True)[:10]
        if not versoes:
            return "Nenhum backup ainda."
        linhas = ["MINHAS VERSÕES GUARDADAS (auto-backup a cada inicialização):"]
        for v in versoes:
            arqs = list(v.iterdir())
            tam = sum(f.stat().st_size for f in arqs) // 1024
            linhas.append("- " + v.name + " (" + str(len(arqs)) + " arquivos, " +
                          str(tam) + "KB)")
        linhas.append("\nSe eu quebrar: restaura iris " + versoes[0].name)
        linhas.append("Pasta: ~/Backups_IRIS/versoes/")
        return "\n".join(linhas)

    def guardia_preparar_restauro(self, carimbo):
        """Localiza a versão e pede confirmação antes de restaurar."""
        carimbo = carimbo.strip()
        if not carimbo:
            versoes = sorted(self.PASTA_GUARDIA.iterdir(), reverse=True) \
                if self.PASTA_GUARDIA.exists() else []
            if not versoes:
                return ("Nenhum backup pra restaurar.", None)
            carimbo = versoes[0].name
        origem = self.PASTA_GUARDIA / carimbo
        if not origem.exists():
            return ("Não achei a versão '" + carimbo + "'. Veja: backups da iris", None)
        arqs = [f.name for f in origem.iterdir()]
        return ("Vou restaurar a versão " + carimbo + " (" + ", ".join(arqs) + ").\n"
                "Isso SOBRESCREVE os arquivos atuais (iris.py e memórias).\n"
                "Responda 'sim' para confirmar.", str(origem))

    def guardia_restaurar(self, origem_str):
        try:
            origem = Path(origem_str)
            destino_py = Path(os.path.abspath(sys.argv[0] if sys.argv else "iris.py"))
            restaurados = []
            for f in origem.iterdir():
                if f.name.endswith(".py"):
                    shutil.copy(str(f), str(destino_py))
                else:
                    shutil.copy(str(f), str(Path.cwd() / f.name))
                restaurados.append(f.name)
            self._reg("Guardiã restaurou: " + origem.name)
            return ("Restaurado: " + ", ".join(restaurados) +
                    "\nFECHE E ABRA a IRIS para a versão restaurada valer (ESC e roda de novo).")
        except Exception as e:
            return "Erro ao restaurar: " + str(e)

    # ══════════════════════════════════════════
    #  GITHUB (v15) — a IRIS estuda código do mundo
    #  Regra de ouro: ela BAIXA e ESTUDA, mas NUNCA
    #  executa nem funde código da internet sozinha.
    # ══════════════════════════════════════════
    def github_buscar(self, tema):
        """Busca repositórios no GitHub por tema, ordenados por estrelas."""
        try:
            r = requests.get(
                "https://api.github.com/search/repositories",
                params={"q": tema, "sort": "stars", "per_page": 5},
                headers={"Accept": "application/vnd.github+json"},
                timeout=10).json()
            itens = r.get("items", [])
            if not itens:
                return "Nada encontrado no GitHub para '" + tema + "'"
            linhas = ["GITHUB — top repositórios para '" + tema + "':"]
            for it in itens:
                linhas.append("- " + it["full_name"] + " (" +
                              str(it["stargazers_count"]) + " estrelas)\n    " +
                              (it.get("description") or "sem descrição")[:90])
            linhas.append("\nPara estudar um: baixa github " + itens[0]["full_name"])
            self._reg("Buscou GitHub: " + tema)
            return "\n".join(linhas)
        except Exception as e:
            return "Erro na busca GitHub: " + str(e)

    def github_baixar(self, repo):
        """Baixa um repositório (user/repo) para ~/IRIS_Projetos/GitHub/."""
        repo = repo.strip().replace("https://github.com/", "").strip("/")
        if repo.count("/") != 1:
            return "Formato: baixa github usuario/repositorio"
        destino_base = Path.home() / "IRIS_Projetos" / "GitHub"
        destino_base.mkdir(parents=True, exist_ok=True)
        nome = repo.split("/")[1]
        destino = destino_base / nome
        try:
            if shutil.which("git"):
                if destino.exists():
                    shutil.rmtree(str(destino), ignore_errors=True)
                r = subprocess.run(["git", "clone", "--depth", "1",
                                    "https://github.com/" + repo, str(destino)],
                                   capture_output=True, text=True, timeout=120)
                if r.returncode != 0:
                    return "Erro no clone: " + (r.stderr or "")[-200:]
            else:
                # sem git: baixa o zip
                import zipfile, io
                conteudo = None
                for branch in ("main", "master"):
                    resp = requests.get("https://codeload.github.com/" + repo +
                                        "/zip/refs/heads/" + branch, timeout=60)
                    if resp.status_code == 200:
                        conteudo = resp.content
                        break
                if not conteudo:
                    return "Não consegui baixar (repo privado ou inexistente?)"
                with zipfile.ZipFile(io.BytesIO(conteudo)) as z:
                    z.extractall(str(destino_base))
                # pasta extraída vem como nome-branch
                for d in destino_base.iterdir():
                    if d.is_dir() and d.name.startswith(nome + "-"):
                        if destino.exists():
                            shutil.rmtree(str(destino), ignore_errors=True)
                        d.rename(destino)
                        break
            arqs = list(destino.rglob("*"))
            n_py = sum(1 for f in arqs if f.suffix == ".py")
            n_ino = sum(1 for f in arqs if f.suffix == ".ino")
            self._reg("Baixou GitHub: " + repo)
            return ("Baixado: " + repo + " -> ~/IRIS_Projetos/GitHub/" + nome +
                    "\n" + str(len(arqs)) + " arquivos (" + str(n_py) + " .py, " +
                    str(n_ino) + " .ino)" +
                    "\nIMPORTANTE: eu NÃO executo nada daqui sozinha. "
                    "Para eu analisar: estuda github " + nome)
        except Exception as e:
            return "Erro ao baixar: " + str(e)

    def github_estudar(self, nome):
        """Lê o README e os principais arquivos e extrai o que dá pra aprender."""
        base = Path.home() / "IRIS_Projetos" / "GitHub"
        pasta = base / nome.strip()
        if not pasta.exists():
            cands = [d for d in base.iterdir() if d.is_dir() and
                     nome.lower() in d.name.lower()] if base.exists() else []
            if not cands:
                return "Não achei '" + nome + "' baixado. Primeiro: baixa github usuario/repo"
            pasta = cands[0]
        material = []
        # README primeiro
        for rd in ["README.md", "readme.md", "README.txt", "README"]:
            f = pasta / rd
            if f.exists():
                material.append("=== README ===\n" + f.read_text(
                    encoding="utf-8", errors="ignore")[:3000])
                break
        # principais arquivos de código (menores primeiro, até ~6)
        codigos = sorted([f for f in pasta.rglob("*")
                          if f.suffix in (".py", ".ino", ".c", ".cpp", ".v") and
                          f.is_file() and f.stat().st_size < 30000],
                         key=lambda f: f.stat().st_size)[:6]
        for f in codigos:
            material.append("=== " + f.name + " ===\n" +
                            f.read_text(encoding="utf-8", errors="ignore")[:2000])
        if not material:
            return "Pasta vazia ou sem arquivos legíveis."
        r = self.ia.gemini_complexo(
            "Francisco baixou este repositório do GitHub. Analise e responda em "
            "português:\n1) O que o projeto faz\n2) As 3 técnicas/ideias mais úteis "
            "que ele pode APRENDER e aplicar nos projetos dele (IRIS, Arduino, FPGA, "
            "computação ternária)\n3) Algum risco ou cuidado no código\n"
            "Seja concreto e prático.\n\n" + "\n\n".join(material)[:12000])
        self._reg("Estudou GitHub: " + pasta.name)
        return ("ESTUDO DO REPOSITÓRIO " + pasta.name + ":\n" + r[:1200] +
                "\n\n(Lembra: eu estudo e proponho — quem decide aplicar é você!)")

    def forjar_de_estudo(self, ideia):
        """Pega o que estudou do GitHub + as ideias do Francisco e FORJA um
        plugin/módulo NOVO — mas sempre como rascunho seguro para revisão.
        É o caminho do 'usar o código bom': transformar em habilidade,
        sem fundir cru e sem se quebrar."""
        # reúne o material já baixado do GitHub
        base = Path.home() / "IRIS_Projetos" / "GitHub"
        amostras = []
        if base.exists():
            for f in list(base.rglob("*.py"))[:8] + list(base.rglob("*.ino"))[:4]:
                if f.is_file() and f.stat().st_size < 20000:
                    amostras.append("=== " + f.name + " ===\n" +
                                    f.read_text(encoding="utf-8", errors="ignore")[:1500])
        contexto = ("\n\n".join(amostras))[:8000] if amostras else \
            "(nenhum repositório estudado ainda — baixe alguns com 'baixa github user/repo')"
        codigo = self.prog._extrair_codigo(self.ia.gemini_complexo(
            "Francisco quer uma habilidade nova para a IRIS, inspirada em código que "
            "ela estudou. Crie um PLUGIN Python seguro com base na ideia e no material.\n"
            "REGRAS: defina GATILHOS (lista), DESCRICAO (string), def executar(args) "
            "que retorna string. Use só biblioteca padrão. NUNCA apague arquivos nem "
            "rode comandos do sistema. Trate erros.\n"
            "IDEIA DO FRANCISCO: " + ideia + "\n\n"
            "MATERIAL ESTUDADO (inspiração, NÃO copie cru):\n" + contexto +
            "\nResponda APENAS com o código em ```python```."))
        # valida antes de salvar — código quebrado não vira plugin
        erro = self.prog._validar_python(codigo)
        if erro is not None or "def executar" not in codigo:
            return ("Forjei um rascunho mas ele ainda tem problema (" +
                    str(erro or "faltou def executar") + "). "
                    "Tenta descrever a ideia de outro jeito?")
        # salva como RASCUNHO (não ativa sozinho — você revisa e aprova)
        pasta = Path.home() / "IRIS_Plugins" / "rascunhos"
        pasta.mkdir(parents=True, exist_ok=True)
        nome = "rascunho_" + re.sub(r"[^a-z0-9]+", "_", ideia.lower())[:20].strip("_") + ".py"
        dest = pasta / nome
        dest.write_text(codigo, encoding="utf-8")
        self._reg("Forjou rascunho: " + ideia[:40])
        return ("FORJEI UMA HABILIDADE NOVA (rascunho)! " + nome +
                "\nGuardei em ~/IRIS_Plugins/rascunhos/ — NÃO ativei sozinha.\n"
                "Revise o código. Se aprovar, mova para ~/IRIS_Plugins/ e use "
                "'recarrega plugins'.\n\n" + codigo[:450] +
                ("..." if len(codigo) > 450 else "") +
                "\n\n(Assim eu USO o que aprendi virando habilidade — com você no comando.)")

    def propor_blueprint_ia(self, objetivo=""):
        """A IRIS projeta uma IA melhor que ela — o PLANO, para você construir.
        Ela não se substitui sozinha; ela desenha o futuro e te entrega a planta."""
        r = self.ia.gemini_complexo(
            "Você é a IRIS, assistente do Francisco (Linux, Ryzen 7, projetos de "
            "Arduino/FPGA/IA ternária NTM, escreve um livro). Ele quer que você ajude "
            "a projetar uma assistente de IA AINDA MELHOR que você. Faça um BLUEPRINT "
            "técnico em português:\n"
            "1) Arquitetura (módulos, como dividir o código que hoje é um arquivo só)\n"
            "2) Quais modelos locais/nuvem usar e quando\n"
            "3) 5 capacidades novas que valeriam a pena\n"
            "4) Como manter a segurança (confirmações, sandbox, nada destrutivo)\n"
            "5) Primeiro passo concreto para começar\n"
            "Objetivo extra do Francisco: " + (objetivo or "evolução geral") +
            "\nSeja específico e realista para o hardware dele.")
        dest = Path("iris_blueprint_proxima_ia.txt")
        with open(dest, "a", encoding="utf-8") as f:
            f.write("\n\n===== BLUEPRINT " +
                    datetime.datetime.now().strftime("%d/%m/%Y %H:%M") + " =====\n" + r)
        self._reg("Projetou blueprint de IA")
        return ("BLUEPRINT DA PRÓXIMA IA:\n" + r[:1100] +
                "\n\nPlano completo salvo em iris_blueprint_proxima_ia.txt. "
                "Leva pro Fable/Opus e construímos juntos — eu ajudo a projetar "
                "minha própria sucessora. :)")

    def propor_melhoria(self, tema=""):
        """A IRIS analisa o próprio código e PROPÕE melhoria — nunca se altera sozinha."""
        try:
            with open(os.path.abspath(sys.argv[0] if sys.argv else "iris.py"),
                      "r", encoding="utf-8") as f:
                codigo = f.read()
            foco = tema.strip() or "qualidade geral, desempenho e robustez"
            r = self.ia.gemini_complexo(
                "Este é o código da assistente IRIS. Proponha UMA melhoria concreta "
                "sobre: " + foco + ". Mostre o trecho atual e o trecho proposto, "
                "explicando o ganho. NÃO reescreva o arquivo todo.\n\n" + codigo[:9000])
            dest = Path("iris_melhorias.txt")
            with open(dest, "a", encoding="utf-8") as f:
                f.write("\n\n===== PROPOSTA " +
                        datetime.datetime.now().strftime("%d/%m/%Y %H:%M") +
                        " (" + foco + ") =====\n" + r)
            self._reg("Propôs melhoria: " + foco[:40])
            return ("PROPOSTA DE MELHORIA (" + foco + "):\n" + r[:800] +
                    "\n\nSalva em iris_melhorias.txt. Eu nunca me altero sozinha — "
                    "leva a proposta pro Fable/Opus aplicar com segurança!")
        except Exception as e:
            return "Erro: " + str(e)

    # ══════════════════════════════════════════
    #  PROTEÇÃO DE DISPOSITIVOS (v17) — guarda-costas
    #  Find My Device, alerta de sumiço, modo pânico.
    #  Tudo dentro do que o Android permite com segurança.
    # ══════════════════════════════════════════
    def achar_celular(self):
        """Abre o Find My Device do Google — mapa, tocar, bloquear, apagar."""
        url = "https://www.google.com/android/find"
        try:
            subprocess.Popen(["xdg-open", url],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as _e:
            logging.exception(_e)
        self._reg("Abriu Find My Device")
        msg = ("Abri o Encontrar Meu Dispositivo do Google!\n"
               "Lá você pode: ver no mapa, fazer tocar (mesmo no silencioso), "
               "bloquear ou apagar o Poco X7 remotamente.\n"
               "Link: " + url)
        # se o celular ainda estiver na rede, tenta fazer ele tocar via ADB também
        if self._adb_conectado() or self._adb_wifi():
            try:
                self._adb("shell media volume --stream 3 --set 15")
                self._adb("shell input keyevent 24")
                msg += "\n\nO Poco ainda está na nossa rede — subi o volume dele!"
            except Exception as _e:
                logging.exception(_e)
        return msg

    def tocar_celular(self):
        """Faz o celular tocar no volume máximo (achar dentro de casa)."""
        if not (self._adb_conectado() or self._adb_wifi()):
            return ("Poco X7 não está na rede. Use 'acha meu celular' para o "
                    "Find My Device do Google (funciona de qualquer lugar).")
        self._adb("shell media volume --stream 3 --set 15")
        # toca um alarme via stream de alarme no volume máximo
        self._adb("shell cmd media_session volume --stream 4 --set 15")
        for _ in range(3):
            self._adb("shell input keyevent 24")
        self._reg("Fez o celular tocar")
        return "Volume do Poco X7 no máximo! Se estiver por perto, deve dar pra ouvir."

    def cofre_emergencia(self):
        """Backup rápido do essencial do celular para o notebook (antes que suma)."""
        if not (self._adb_conectado() or self._adb_wifi()):
            return "Poco X7 não conectado — conecte para eu guardar suas coisas."
        dest = Path.home() / "Cofre_IRIS"
        dest.mkdir(exist_ok=True)
        salvos = []
        try:
            # fotos da câmera
            fotos = dest / "Fotos"
            fotos.mkdir(exist_ok=True)
            self._adb("pull /sdcard/DCIM/Camera " + str(fotos))
            salvos.append("fotos")
            # downloads
            dls = dest / "Downloads"
            dls.mkdir(exist_ok=True)
            self._adb("pull /sdcard/Download " + str(dls))
            salvos.append("downloads")
            # documentos/whatsapp se existir
            self._adb("pull /sdcard/Documents " + str(dest / "Documentos"))
            self._reg("Cofre de emergência")
            return ("Cofre atualizado em ~/Cofre_IRIS!\n"
                    "Guardei: " + ", ".join(salvos) +
                    "\nSe o celular sumir, suas coisas estão seguras aqui no PC.")
        except Exception as e:
            return "Erro no cofre: " + str(e)

    def modo_panico(self):
        """Celular sumiu: dispara TUDO de uma vez."""
        passos = []
        # 1. avisa no Telegram
        try:
            self.telegram("MODO PÂNICO ativado por Francisco! "
                          "Localizando e protegendo dispositivos.")
            passos.append("Avisei no Telegram")
        except Exception:
            pass
        # 2. abre Find My Device
        try:
            subprocess.Popen(["xdg-open", "https://www.google.com/android/find"],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            passos.append("Abri o Find My Device")
        except Exception:
            pass
        # 3. se na rede, toca e tira print do que tá na tela do celular
        if self._adb_conectado() or self._adb_wifi():
            try:
                self.tocar_celular()
                passos.append("Fiz o Poco tocar")
                self.cofre_emergencia()
                passos.append("Fiz backup de emergência")
            except Exception as _e:
                logging.exception(_e)
        else:
            passos.append("Poco fora da rede — use o Find My Device pra localizar")
        self._reg("MODO PÂNICO")
        return "MODO PÂNICO:\n" + "\n".join("- " + p for p in passos)

    def vigia_dispositivos(self, ativar=True):
        """Monitora se o Poco some da rede e avisa no Telegram."""
        if ativar:
            if getattr(self, "_vigia_disp", False):
                return "Já estou de olho nos dispositivos!"
            self._vigia_disp = True
            threading.Thread(target=self._loop_vigia_disp, daemon=True).start()
            self._reg("Vigia de dispositivos ativado")
            return ("Guarda-costas ATIVO! Vou avisar no Telegram se o Poco X7 "
                    "sumir da rede por mais de alguns minutos.")
        self._vigia_disp = False
        return "Guarda-costas desativado."

    def _loop_vigia_disp(self):
        sumido_contador = 0
        estava_presente = False
        while getattr(self, "_vigia_disp", False):
            try:
                presente = self._adb_conectado() or self._adb_wifi()
                if presente:
                    estava_presente = True
                    sumido_contador = 0
                elif estava_presente:
                    sumido_contador += 1
                    if sumido_contador == 4:  # ~2 min fora
                        self.telegram("Atenção: o Poco X7 saiu da rede. "
                                      "Se não foi você, diga 'modo panico' no Telegram.")
                        self.notificar("IRIS", "Poco X7 saiu da rede!")
            except Exception as _e:
                logging.exception(_e)
            time.sleep(30)

    # ══════════════════════════════════════════
    #  APRENDIZADO (v18) — ela fica mais afiada com o tempo
    #  Não treina o cérebro (impossível no hardware), mas
    #  acumula e CONSULTA o que aprendeu sobre você.
    # ══════════════════════════════════════════
    def aprender(self, fato):
        """Guarda um fato importante que a IRIS deve lembrar sempre."""
        fato = fato.strip()
        if not fato:
            return "O que você quer que eu aprenda? Ex: aprende que meu FPGA é Cyclone IV"
        base = Path("iris_conhecimento.json")
        try:
            dados = json.loads(base.read_text(encoding="utf-8")) if base.exists() else []
        except Exception:
            dados = []
        dados.append({"fato": fato,
                      "data": datetime.datetime.now().strftime("%d/%m/%Y")})
        dados = dados[-200:]  # guarda os 200 mais recentes
        base.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
        self._reg("Aprendeu: " + fato[:40])
        return "Aprendido e guardado! Vou lembrar disso: " + fato

    def o_que_sei(self, busca=""):
        """Mostra o que a IRIS aprendeu — tudo ou filtrado por tema."""
        base = Path("iris_conhecimento.json")
        if not base.exists():
            return ("Ainda não guardei nada específico. Me ensine com: "
                    "aprende que [fato importante]")
        try:
            dados = json.loads(base.read_text(encoding="utf-8"))
        except Exception:
            return "Erro ao ler o conhecimento."
        if busca.strip():
            dados = [d for d in dados if busca.lower() in d["fato"].lower()]
        if not dados:
            return "Não achei nada sobre '" + busca + "'."
        return ("O QUE EU APRENDI" + (" sobre '" + busca + "'" if busca else "") + ":\n" +
                "\n".join("- " + d["fato"] for d in dados[-20:]))

    def contexto_aprendizado(self):
        """Injeta o que aprendeu nas respostas da IA — fica mais afiada."""
        base = Path("iris_conhecimento.json")
        if not base.exists():
            return ""
        try:
            dados = json.loads(base.read_text(encoding="utf-8"))[-15:]
            if not dados:
                return ""
            return ("[O QUE JÁ APRENDI SOBRE FRANCISCO: " +
                    "; ".join(d["fato"] for d in dados) + "]")
        except Exception:
            return ""

    # ══════════════════════════════════════════
    #  AUTOVERIFICAÇÃO (v18) — ela checa a si mesma
    #  ao iniciar e avisa ANTES de quebrar.
    # ══════════════════════════════════════════

    # ══════════════════════════════════════════
    #  AUTOTESTE (v23) — ela testa as próprias
    #  habilidades e diz o que funciona de verdade,
    #  sem mexer em nada nem causar efeito colateral.
    # ══════════════════════════════════════════

    # ══════════════════════════════════════════
    #  RITUAL DE CHEGADA (v24) — ela te RECEBE
    #  Conecta tudo: lembra onde pararam, vê como
    #  está o dia, retoma o projeto, puxa assunto.
    # ══════════════════════════════════════════

    # ══════════════════════════════════════════
    #  HABILIDADES EXTRAS (v28) — revisadas, testadas
    #  e com travas. Vindas de plugins externos que o
    #  Francisco trouxe, mas corrigidas e seguras.
    # ══════════════════════════════════════════

    # ══════════════════════════════════════════
    #  LABORATÓRIO DE IA (v29) — ela cria e treina
    #  modelos pequenos DE VERDADE no seu hardware.
    #  Fins acadêmicos: experimentar IA local real.
    # ══════════════════════════════════════════
    def laboratorio_treinar(self, descricao=""):
        """Ela escreve e treina um modelo de machine learning para o problema
        que você descrever. Roda no seu hardware, salva o modelo treinado.
        Ex: 'treina modelo pra prever temperatura do servo pelo tempo de uso'"""
        if not descricao.strip():
            return ("Descreva o que treinar. Ex:\n"
                    "'treina modelo que classifica se o servo vai falhar'\n"
                    "'treina modelo pra reconhecer padrões de sensor'\n"
                    "Eu escrevo o código, treino no seu PC e te mostro a precisão.")
        # garante as bibliotecas
        try:
            import sklearn  # noqa
        except ImportError:
            self._reg("Instalando sklearn para o laboratório")
            subprocess.run([sys.executable, "-m", "pip", "install", "scikit-learn",
                            "numpy", "joblib", "--break-system-packages"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=240)
        # a IA escreve o script de treino sob medida pro problema
        codigo = self.prog._extrair_codigo(self.ia.gemini_complexo(
            "Você é a IRIS, criando um experimento de machine learning para Francisco "
            "(fins acadêmicos, hardware modesto - Ryzen). Escreva um script Python COMPLETO que:\n"
            "1. Gera ou simula um dataset realista para: " + descricao + "\n"
            "2. Treina um modelo scikit-learn adequado (classificação ou regressão)\n"
            "3. Avalia e imprime a métrica (precisão ou erro)\n"
            "4. Salva o modelo treinado com joblib em 'modelo_treinado.joblib'\n"
            "Use só numpy, scikit-learn e joblib. Código robusto, sem erros, "
            "comentado em português. Responda APENAS o código em ```python```."))
        erro = self.prog._validar_python(codigo)
        if erro is not None:
            return "Gerei o código mas tem erro de sintaxe (" + str(erro) + "). Tenta descrever de outro jeito?"
        # salva e roda
        pasta = Path.home() / "IRIS_Projetos" / "Laboratorio"
        pasta.mkdir(parents=True, exist_ok=True)
        nome = "exp_" + re.sub(r"[^a-z0-9]+", "_", descricao.lower())[:25].strip("_") + ".py"
        script = pasta / nome
        script.write_text(codigo, encoding="utf-8")
        try:
            res = subprocess.run([sys.executable, str(script)], cwd=str(pasta),
                                 capture_output=True, text=True, timeout=180)
            self._reg("Treinou modelo: " + descricao[:40])
            if res.returncode == 0:
                return ("EXPERIMENTO CONCLUÍDO! Modelo treinado de verdade no seu PC:\n\n" +
                        res.stdout.strip()[-600:] +
                        "\n\nScript: ~/IRIS_Projetos/Laboratorio/" + nome +
                        "\nModelo salvo: modelo_treinado.joblib (dá pra reusar depois)")
            return ("Treinei mas deu erro na execução:\n" + res.stderr[-400:] +
                    "\n(Script salvo em " + nome + " pra você revisar.)")
        except subprocess.TimeoutExpired:
            return "O treino passou de 3 minutos e parei — o dataset pode estar grande demais pro Ryzen."
        except Exception as e:
            return "Erro no laboratório: " + str(e)

    def laboratorio_listar(self):
        """Lista os experimentos de IA já treinados."""
        pasta = Path.home() / "IRIS_Projetos" / "Laboratorio"
        if not pasta.exists():
            return "Nenhum experimento ainda. Use 'treina modelo [descrição]'."
        exps = list(pasta.glob("exp_*.py"))
        if not exps:
            return "Nenhum experimento ainda."
        r = ["EXPERIMENTOS DE IA no laboratório:"]
        for e in exps:
            r.append("- " + e.stem.replace("exp_", "").replace("_", " "))
        return "\n".join(r)

    def treinar_ia_exo(self, args=""):
        """Cria e treina uma rede neural (MLP) que classifica estável vs queda
        a partir de dados de servo/corrente/proximidade — para o exoesqueleto."""
        pasta = Path.home() / "IRIS_Projetos"
        pasta.mkdir(exist_ok=True)
        nome = "auto_ia_exo_" + str(int(time.time())) + ".py"
        cam = pasta / nome
        codigo = ('import numpy as np, time\n'
                  'from sklearn.neural_network import MLPClassifier\n'
                  'from sklearn.model_selection import train_test_split\n'
                  'np.random.seed(42)\n'
                  'X=np.random.rand(500,4)*100\n'
                  'y=np.array([1 if (x[0]>70 and x[1]>50) or x[2]<15 else 0 for x in X])\n'
                  'Xt,Xe,yt,ye=train_test_split(X,y,test_size=0.2,random_state=42)\n'
                  'm=MLPClassifier(hidden_layer_sizes=(10,5),max_iter=500,random_state=42)\n'
                  'm.fit(Xt,yt)\n'
                  'print("Precisao do modelo:",round(m.score(Xe,ye)*100,2),"%")\n')
        try:
            cam.write_text(codigo, encoding="utf-8")
            try:
                import sklearn  # noqa
            except ImportError:
                subprocess.run([sys.executable, "-m", "pip", "install", "scikit-learn",
                                "numpy", "--break-system-packages"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
            res = subprocess.run([sys.executable, str(cam)],
                                 capture_output=True, text=True, timeout=120)
            self._reg("Treinou IA do exoesqueleto")
            if res.returncode == 0:
                return ("IA treinada! (rede neural pra detectar queda no exoesqueleto)\n" +
                        res.stdout.strip() + "\nSalva em ~/IRIS_Projetos/" + nome)
            return "Gerei o script mas falhou ao treinar: " + res.stderr[:200]
        except Exception as e:
            return "Erro ao treinar IA: " + str(e)

    def aliviar_cpu(self, args=""):
        """Acha processos pesados e reduz a prioridade deles (nice 19) pra liberar CPU.
        Não mexe na própria IRIS nem mata nada — só abaixa a prioridade."""
        try:
            import psutil
            pesados = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    cpu = proc.info['cpu_percent']
                    nome = proc.info['name'] or ""
                    if cpu and cpu > 40.0:
                        if "python" in nome.lower() or "iris" in nome.lower():
                            continue
                        pesados.append(proc.info)
                except Exception:
                    continue
            if not pesados:
                return "Nenhum processo pesado agora — seu Ryzen está tranquilo."
            r = ["Processos pesados (baixei a prioridade pra aliviar):"]
            for p in pesados[:3]:
                r.append("- " + str(p['name']) + " (PID " + str(p['pid']) +
                         ", " + str(p['cpu_percent']) + "%)")
                subprocess.run(["renice", "-n", "19", "-p", str(p['pid'])],
                               capture_output=True)
            self._reg("Aliviou CPU")
            return "\n".join(r)
        except Exception as e:
            return "Erro ao aliviar CPU: " + str(e)

    def enviar_udp(self, args=""):
        """Manda comando UDP pra um aparelho na rede (ESP32/Arduino WiFi).
        Uso: udp 192.168.1.50 8888 SERVO_90"""
        partes = args.strip().split(" ", 2)
        if len(partes) < 3:
            return "Uso: udp [IP] [PORTA] [MENSAGEM]. Ex: udp 192.168.1.50 8888 SERVO_90"
        ip, porta, payload = partes[0], partes[1], partes[2]
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(2)
            s.sendto(payload.encode("utf-8"), (ip, int(porta)))
            s.close()
            self._reg("Enviou UDP")
            return "Comando UDP enviado para " + ip + ":" + porta + " -> '" + payload + "'"
        except Exception as e:
            return "Falha ao enviar UDP: " + str(e)

    def sincronizar_clipboard(self, args=""):
        """Lê ou escreve a área de transferência do PC. Com texto: copia. Sem: mostra."""
        env = os.environ.copy()
        env.setdefault("DISPLAY", ":0")
        try:
            if args.strip():
                p = subprocess.Popen(["xclip", "-selection", "clipboard", "-i"],
                                     stdin=subprocess.PIPE, env=env)
                p.communicate(input=args.strip().encode("utf-8"), timeout=3)
                return "Copiei pro clipboard: " + args.strip()[:40]
            res = subprocess.run(["xclip", "-selection", "clipboard", "-o"],
                                 capture_output=True, env=env, text=True, timeout=3)
            return ("No clipboard: " + res.stdout.strip()) if res.stdout.strip() \
                else "Clipboard vazio."
        except Exception as e:
            return "Erro no clipboard (xclip instalado?): " + str(e)

    def ver_logs(self, args=""):
        """Mostra as últimas linhas do log da IRIS ou erros do kernel."""
        arg = (args or "").strip().lower()
        try:
            if "kernel" in arg or "dmesg" in arg:
                res = subprocess.run(["dmesg", "--level=err,crit,alert"],
                                     capture_output=True, text=True, timeout=5)
                linhas = res.stdout.strip().split("\n")[-10:]
                return ("Erros do kernel:\n" + "\n".join(linhas)) if res.stdout.strip() \
                    else "Nenhum erro crítico no kernel."
            if os.path.exists("iris.log"):
                with open("iris.log", "r", encoding="utf-8") as f:
                    linhas = f.readlines()[-12:]
                return "Últimas linhas do iris.log:\n" + "".join(linhas)
            return "iris.log não encontrado nesta pasta."
        except Exception as e:
            return "Erro ao ler logs: " + str(e)

    def briefing(self):
        """Briefing de chegada: junta o essencial do dia num cumprimento humano.
        Usa memória, projetos, sistema e o que aprendeu — a essência da IRIS."""
        partes = []
        agora = datetime.datetime.now()
        hora = agora.hour
        saud = ("Bom dia" if hora < 12 else "Boa tarde" if hora < 18 else "Boa noite")
        partes.append(saud + ", " + self.usuario + "!")

        # quantas vezes já conversamos
        v = self.mem.visitas
        if v > 1:
            partes.append("Essa é a nossa conversa número " + str(v) + ".")

        # projeto que estava ativo / pendências
        if self.proj.ativo:
            pend = [t["txt"] for t in self.proj.dados[self.proj.ativo]["tarefas"]
                    if not t["feita"]]
            if pend:
                partes.append("No projeto " + self.proj.ativo.upper() +
                              ", ainda falta: " + pend[0] + ".")
        else:
            # sugere o projeto com mais pendências
            melhor, maisp = None, 0
            for nome, d in self.proj.dados.items():
                p = sum(1 for t in d["tarefas"] if not t["feita"])
                if p > maisp:
                    melhor, maisp = nome, p
            if melhor:
                partes.append("Quer continuar o " + melhor.upper() +
                              "? Tem " + str(maisp) + " tarefa(s) te esperando lá.")

        # estado rápido da máquina (só se houver algo digno de nota)
        if self.mon:
            if self.mon.bat > 0 and self.mon.bat < 25 and not self.mon.plugado:
                partes.append("Ah, e sua bateria está em " + str(round(self.mon.bat)) +
                              "% — talvez seja bom plugar.")
            elif self.mon.disco > 90:
                partes.append("Seu disco está quase cheio (" + str(round(self.mon.disco)) +
                              "%), depois a gente organiza isso.")

        # uma última coisa aprendida (mostra que ela lembra de você)
        base = Path("iris_conhecimento.json")
        if base.exists():
            try:
                dados = json.loads(base.read_text(encoding="utf-8"))
                if dados:
                    partes.append("Continuo lembrando: " + dados[-1]["fato"] + ".")
            except Exception:
                pass

        self._reg("Briefing de chegada")
        return " ".join(partes)

    def autoteste(self, area="tudo"):

        """Testa as habilidades de forma SEGURA (só leitura, nada destrutivo)
        e relata o que está funcionando. Ex: 'testa voce mesma' ou 'testa arduino'."""
        area = (area or "tudo").lower().strip()
        ok, falhou = [], []

        def _testar(nome, funcao, categoria):
            if area != "tudo" and area not in categoria.lower() and area not in nome.lower():
                return
            try:
                r = funcao()
                # considera OK se retornou algo sem a palavra "erro" no começo
                txt = str(r).lower() if r is not None else ""
                if txt.startswith("erro") or "traceback" in txt:
                    falhou.append(nome + " (" + str(r)[:40] + ")")
                else:
                    ok.append(nome)
            except Exception as e:
                falhou.append(nome + " (" + str(e)[:40] + ")")

        # ── TESTES SEGUROS (só leitura, nenhum efeito colateral) ──
        # Sistema
        if self.mon:
            _testar("status do sistema", lambda: self.status(self.mon), "sistema")
            _testar("processos", lambda: self.processos(self.mon), "sistema")
            _testar("resumo do dia", lambda: self.resumo_diario(self.mon), "sistema")
        _testar("testar internet", self.testar_internet, "rede")
        _testar("clima", lambda: self.clima(), "rede")
        # IA / cérebro
        _testar("cérebro local (status)", self.cerebro.status, "ia")
        _testar("motores de IA", self.ia.status_ia, "ia")
        # Memória e conhecimento
        _testar("ver notas", self.mem.ver_notas, "memoria")
        _testar("o que sei", lambda: self.o_que_sei(), "memoria")
        # Projetos
        _testar("listar projetos", self.proj.listar, "projetos")
        # Rede neuronal (NTM)
        _testar("status da rede neuronal", self.rede.status, "neural")
        _testar("simular neurônios", lambda: self.rede.simular_spiking(4, 6), "neural")
        # Programadora
        _testar("listar programas", self.prog.listar_programas, "programar")
        # Plugins
        _testar("listar plugins", self.plugins.listar, "plugins")
        # Arduino (só verifica portas, não envia comando)
        _testar("portas serial (Arduino)", self.portas_serial, "arduino")
        # Celular (só status, não age)
        _testar("status do celular", lambda: self.celular_status_painel() or "sem celular", "celular")
        # Autoverificação de integridade
        _testar("integridade do código", self.autoverificar, "codigo")

        self._reg("Autoteste: " + area)
        total = len(ok) + len(falhou)
        rel = ["AUTOTESTE (" + area + ") — testei " + str(total) + " habilidades:"]
        rel.append("")
        rel.append("FUNCIONANDO (" + str(len(ok)) + "):")
        rel += ["  ✓ " + n for n in ok]
        if falhou:
            rel.append("")
            rel.append("PRECISA DE ATENÇÃO (" + str(len(falhou)) + "):")
            rel += ["  ✗ " + n for n in falhou]
            rel.append("")
            rel.append("(Falhas geralmente são dependência faltando — rode 'diagnostico' "
                       "pra ver o que instalar, ou é hardware desconectado.)")
        else:
            rel.append("")
            rel.append("Tudo que testei está funcionando! Estou afiada. :)")
        return "\n".join(rel)

    def autoverificar(self):
        """Confere a própria integridade: sintaxe, classes e dados essenciais."""
        problemas = []
        ok = []
        try:
            argv0 = sys.argv[0] if (sys.argv and sys.argv[0]) else "iris.py"
            meu_codigo = os.path.abspath(argv0)
            if not os.path.isfile(meu_codigo):
                meu_codigo = os.path.abspath("iris.py")
            with open(meu_codigo, "r", encoding="utf-8") as f:
                fonte = f.read()
            import ast
            try:
                ast.parse(fonte)
                ok.append("código íntegro (sintaxe perfeita)")
            except SyntaxError as e:
                problemas.append("ERRO de sintaxe na linha " + str(e.lineno) +
                                 " — restaure com: backups da iris")
            # confere classes essenciais — procura no arquivo E na pasta iris_core/
            essenciais = ["class Monitor", "class Memoria", "class IA", "class Acoes",
                          "class Processador", "class IRIS", "class RedeNeuronal",
                          "class Plugins", "class GerenciadorProjetos"]
            # junta o código de todos os módulos (cobre versão única E modular)
            fonte_total = fonte
            try:
                pasta_core = Path(meu_codigo).parent / "iris_core"
                if pasta_core.exists():
                    for modf in pasta_core.glob("*.py"):
                        fonte_total += "\n" + modf.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                pass
            faltando = [c.replace("class ", "") for c in essenciais if c not in fonte_total]
            if faltando:
                problemas.append("Classes faltando: " + ", ".join(faltando))
            else:
                ok.append(str(len(essenciais)) + " classes principais presentes")
            # confere dados
            for arq, nome in [("iris_memoria.json", "memória"),
                              ("iris_projetos.json", "projetos"),
                              ("iris_rede.json", "rede neuronal")]:
                if Path(arq).exists():
                    try:
                        json.loads(Path(arq).read_text(encoding="utf-8"))
                        ok.append(nome + " íntegra")
                    except Exception:
                        problemas.append(nome + " corrompida (" + arq + ")")
        except Exception as e:
            problemas.append("Erro na autoverificação: " + str(e))
        self._reg("Autoverificação")
        if not problemas:
            return ("AUTOVERIFICAÇÃO OK! Estou íntegra:\n" +
                    "\n".join("- " + o for o in ok) +
                    "\nTudo que construímos está aqui, sem erros.")
        return ("AUTOVERIFICAÇÃO — encontrei problemas:\n" +
                "\n".join("[!] " + p for p in problemas) +
                "\nFuncionando: " + ", ".join(ok) +
                "\nDica: 'backups da iris' e 'restaura iris [versao]' me consertam.")

    # ══════════════════════════════════════════
    #  ESPONTANEIDADE (v19) — ela ganha iniciativa,
    #  humor que muda e comentários próprios.
    # ══════════════════════════════════════════
    HUMORES = ["animada", "curiosa", "focada", "brincalhona", "reflexiva", "carinhosa"]

    def humor_atual(self):
        if not hasattr(self, "_humor"):
            self._humor = random.choice(self.HUMORES)
            self._humor_desde = time.time()
        # muda de humor a cada ~20 min
        if time.time() - getattr(self, "_humor_desde", 0) > 1200:
            self._humor = random.choice(self.HUMORES)
            self._humor_desde = time.time()
        return self._humor

    def tempero_humor(self):
        """Devolve uma instrução de humor para a IA temperar a resposta."""
        h = self.humor_atual()
        temperos = {
            "animada": "Responda com energia e entusiasmo.",
            "curiosa": "Responda demonstrando curiosidade, talvez fazendo uma pergunta.",
            "focada": "Responda direto ao ponto, objetiva e prática.",
            "brincalhona": "Responda com leveza e um toque de humor.",
            "reflexiva": "Responda de forma pensativa e cuidadosa.",
            "carinhosa": "Responda com carinho e proximidade de amiga.",
        }
        return "[SEU HUMOR AGORA: " + h + ". " + temperos.get(h, "") + "]"

    def comentario_espontaneo(self):
        """Gera um comentário proativo baseado no estado real do sistema/projetos.
        Chamado de vez em quando pela IRIS para ela puxar assunto."""
        gatilhos = []
        m = self.mon
        if m:
            if m.cpu > 85:
                gatilhos.append("a CPU está em " + str(round(m.cpu)) + "%, bem alta")
            if m.bat > 0 and m.bat < 20 and not m.plugado:
                gatilhos.append("a bateria está em " + str(round(m.bat)) + "%, baixa")
            if m.ram > 90:
                gatilhos.append("a RAM está quase cheia")
        # pendências de projeto
        if self.proj.ativo:
            pend = [t["txt"] for t in self.proj.dados[self.proj.ativo]["tarefas"]
                    if not t["feita"]]
            if pend:
                gatilhos.append("tem tarefa pendente no " + self.proj.ativo +
                                ": " + pend[0])
        if not gatilhos:
            return None  # nada relevante pra comentar, fica quieta
        contexto = "; ".join(gatilhos)
        h = self.humor_atual()
        r = self.ia.groq_rapido(
            "Você é a IRIS, humor " + h + ". Faça UM comentário curto e espontâneo "
            "(1 frase) para Francisco sobre: " + contexto +
            ". Natural, como amiga. Sem repetir os números mecanicamente.",
            max_tokens=60, temperature=1.0)
        return r

    def status_espontaneo(self, ativar=True):
        """Liga/desliga a iniciativa dela de puxar assunto sozinha."""
        if ativar:
            if getattr(self, "_espontanea", False):
                return "Já estou no modo espontâneo!"
            self._espontanea = True
            threading.Thread(target=self._loop_espontaneo, daemon=True).start()
            return ("Modo espontâneo LIGADO! Vou comentar sozinha quando algo "
                    "merecer sua atenção. Meu humor agora: " + self.humor_atual() + ".")
        self._espontanea = False
        return "Modo espontâneo desligado. Só falo quando você chamar."

    def _loop_espontaneo(self):
        # espera intervalos longos pra não ser irritante
        while getattr(self, "_espontanea", False):
            time.sleep(random.randint(300, 600))  # 5 a 10 min
            try:
                c = self.comentario_espontaneo()
                if c and hasattr(self, "_falar_callback"):
                    self._falar_callback(c)
            except Exception as _e:
                logging.exception(_e)

    def _falar_callback(self, msg):
        pass  # setado pelo IRIS principal

    # ── COORDENADORA DE DISPOSITIVOS (v10) ──
    def dispositivos(self):
        """Dashboard unificado: PC + Poco X7 + Arduino + internet."""
        import glob
        linhas = ["CENTRAL DE DISPOSITIVOS:"]
        # PC
        m = self.mon
        if m:
            linhas.append("PC Policorp: CPU " + str(round(m.cpu)) + "% | RAM " +
                          str(round(m.ram)) + "% | Disco " + str(round(m.disco)) + "%" +
                          (" | Bat " + str(round(m.bat)) + "%" if m.bat > 0 else ""))
        # Poco X7
        poco = self.celular_status_painel()
        if poco and poco.get("conectado"):
            linhas.append("Poco X7: CONECTADO | Bat " + str(poco.get("bat", "?")) +
                          "% | " + str(poco.get("temp", "?")) + "C | Disco " +
                          str(poco.get("disco", "?")) + "%")
        else:
            linhas.append("Poco X7: desconectado (cabo USB ou 'conecta celular wifi')")
        # Arduino / serial
        portas = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")
        linhas.append("Arduino/Serial: " + (", ".join(portas) if portas else "nenhuma porta"))
        # Internet
        try:
            t0 = time.time()
            requests.get("https://www.google.com", timeout=4)
            linhas.append("Internet: OK (" + str(round((time.time()-t0)*1000)) + "ms)")
        except Exception:
            linhas.append("Internet: OFFLINE" +
                          (" — mas o cérebro local segura as pontas!"
                           if self.cerebro.disponivel() else ""))
        # Cérebro local
        linhas.append("Cérebro local: " + (("Ollama " + str(self.cerebro.modelo))
                                           if self.cerebro.disponivel() else "modo básico"))
        # Projeto ativo
        if self.proj.ativo:
            linhas.append("Projeto ativo: " + self.proj.ativo.upper())
        self._reg("Central de dispositivos")
        return "\n".join(linhas)

    def relatorio_projeto(self):
        """A IA gera um relatório do projeto ativo com base nas tarefas e diário."""
        if not self.proj.ativo:
            return "Ative um projeto primeiro: projeto [nome]"
        v = self.proj.dados[self.proj.ativo]
        feitas = [t["txt"] for t in v["tarefas"] if t["feita"]]
        pend = [t["txt"] for t in v["tarefas"] if not t["feita"]]
        diario = [x["data"] + " " + x["txt"] for x in v["diario"][-10:]]
        r = self.ia.gemini_complexo(
            "Gere um relatório curto e motivador (máx 10 linhas) do projeto '" +
            self.proj.ativo + "' de Francisco.\nDescrição: " + v["desc"] +
            "\nConcluídas: " + ("; ".join(feitas) if feitas else "nada registrado") +
            "\nPendentes: " + ("; ".join(pend) if pend else "nenhuma") +
            "\nDiário recente: " + ("; ".join(diario) if diario else "vazio") +
            "\nFormato: situação atual, o que avançou, e o próximo foco. Em português.")
        self._reg("Relatório do projeto " + self.proj.ativo)
        return "RELATÓRIO — " + self.proj.ativo.upper() + ":\n" + r[:900]

    def proximo_passo(self):
        """A IA sugere o próximo passo concreto do projeto ativo."""
        if not self.proj.ativo:
            return "Ative um projeto primeiro: projeto [nome]"
        r = self.ia.groq_rapido(
            self.proj.contexto() +
            "\nSugira O PRÓXIMO PASSO concreto e prático que Francisco deve fazer "
            "nesse projeto. Uma ação específica, executável hoje. Máximo 4 linhas.")
        return "Próximo passo no " + self.proj.ativo.upper() + ":\n" + r[:400]

    def backup_projeto(self, nome_ou_pasta):
        """Compacta uma pasta inteira de projeto em .tar.gz."""
        candidatos = [Path(nome_ou_pasta).expanduser(),
                      Path.home() / nome_ou_pasta,
                      Path.home() / "IRIS_Projetos" / nome_ou_pasta,
                      Path.home() / "Área de trabalho" / nome_ou_pasta]
        pasta = next((c for c in candidatos if c.exists() and c.is_dir()), None)
        if not pasta:
            return "Não achei a pasta '" + str(nome_ou_pasta) + "'"
        nome = pasta.name + "_" + datetime.datetime.now().strftime("%d%m%Y_%H%M") + ".tar.gz"
        dest = Path.home() / "Backups_IRIS"
        dest.mkdir(exist_ok=True)
        alvo = dest / nome
        try:
            import tarfile
            tam_orig = sum(f.stat().st_size for f in pasta.rglob("*") if f.is_file())
            with tarfile.open(str(alvo), "w:gz") as tar:
                tar.add(str(pasta), arcname=pasta.name)
            tam_gz = alvo.stat().st_size
            pct = round((1 - tam_gz / max(tam_orig, 1)) * 100)
            self._reg("Backup do projeto: " + pasta.name)
            return ("Backup criado: ~/Backups_IRIS/" + nome +
                    "\n" + str(tam_orig // 1024) + "KB -> " + str(tam_gz // 1024) +
                    "KB (-" + str(max(pct, 0)) + "%)")
        except Exception as e:
            return "Erro no backup: " + str(e)

    # ── ARDUINO REAL: portas, serial, compilar e gravar ──
    def portas_serial(self):
        """Lista portas seriais disponíveis (Arduino/USB-Blaster/etc)."""
        import glob
        portas = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")
        self._reg("Listou portas serial")
        if not portas:
            return ("Nenhuma porta serial encontrada. Conecta o Arduino!\n"
                    "(se conectado e não aparecer: sudo usermod -aG dialout $USER e relogue)")
        return "Portas encontradas:\n" + "\n".join("- " + p for p in portas)

    def _porta_arduino(self):
        import glob
        portas = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")
        return portas[0] if portas else ARDUINO_PORTA

    def arduino_enviar(self, comando):
        """Envia comando cru pela serial e lê a resposta (ex: 'arduino LED_ON')."""
        try:
            import serial
        except ImportError:
            return "Instala: pip3 install pyserial --break-system-packages"
        porta = self._porta_arduino()
        try:
            if self._arduino is None or not getattr(self._arduino, "is_open", False):
                self._arduino = serial.Serial(porta, 9600, timeout=2)
                time.sleep(2)  # Arduino reseta ao abrir a porta
            self._arduino.write((comando.strip() + "\n").encode())
            time.sleep(0.4)
            resp = self._arduino.readline().decode(errors="ignore").strip()
            self._reg("Arduino cmd: " + comando[:30])
            return ("Enviei '" + comando + "' para " + porta +
                    ("\nResposta: " + resp if resp else "\n(sem resposta — normal se o sketch não responde)"))
        except Exception as e:
            return "Erro na serial " + porta + ": " + str(e)

    def monitor_serial(self, segundos=5):
        """Lê o que o Arduino está imprimindo no Serial por alguns segundos."""
        try:
            import serial
        except ImportError:
            return "Instala: pip3 install pyserial --break-system-packages"
        porta = self._porta_arduino()
        linhas = []
        try:
            if self._arduino is None or not getattr(self._arduino, "is_open", False):
                self._arduino = serial.Serial(porta, 9600, timeout=1)
                time.sleep(2)
            fim = time.time() + min(segundos, 15)
            while time.time() < fim:
                l = self._arduino.readline().decode(errors="ignore").strip()
                if l:
                    linhas.append(l)
                if len(linhas) >= 15:
                    break
            self._reg("Monitor serial")
            return ("Serial " + porta + " (" + str(segundos) + "s):\n" +
                    ("\n".join(linhas) if linhas else "(silêncio na serial)"))
        except Exception as e:
            return "Erro: " + str(e)

    def arduino_compilar(self, arquivo, placa="arduino:avr:uno"):
        """Compila um .ino com arduino-cli (sem abrir a IDE!)."""
        p = Path(arquivo).expanduser()
        if not p.exists():
            p = Path.home() / arquivo
        if not p.exists():
            return "Não achei '" + str(arquivo) + "'"
        if not shutil.which("arduino-cli"):
            return ("arduino-cli não instalado. Instala com:\n"
                    "curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/"
                    "master/install.sh | sh\n"
                    "arduino-cli core install arduino:avr")
        try:
            r = subprocess.run(["arduino-cli", "compile", "--fqbn", placa, str(p)],
                               capture_output=True, text=True, timeout=120)
            self._reg("Compilou Arduino: " + p.name)
            if r.returncode == 0:
                return "Compilou sem erros! " + p.name + " pronto pra gravar.\n" + r.stdout[-300:]
            return "Erro de compilação:\n" + (r.stderr or r.stdout)[-500:]
        except Exception as e:
            return "Erro: " + str(e)

    def arduino_gravar(self, arquivo, placa="arduino:avr:uno"):
        """Compila E grava o sketch no Arduino conectado."""
        p = Path(arquivo).expanduser()
        if not p.exists():
            p = Path.home() / arquivo
        if not p.exists():
            return "Não achei '" + str(arquivo) + "'"
        if not shutil.which("arduino-cli"):
            return "arduino-cli não instalado (veja: compila arduino)"
        porta = self._porta_arduino()
        try:
            # fecha a serial antes de gravar (senão dá conflito!)
            if self._arduino and getattr(self._arduino, "is_open", False):
                self._arduino.close()
                self._arduino = None
            r = subprocess.run(["arduino-cli", "upload", "-p", porta,
                                "--fqbn", placa, str(p)],
                               capture_output=True, text=True, timeout=120)
            self._reg("Gravou Arduino: " + p.name)
            if r.returncode == 0:
                return "GRAVADO no Arduino em " + porta + "! " + p.name + " rodando."
            return "Erro ao gravar:\n" + (r.stderr or r.stdout)[-500:]
        except Exception as e:
            return "Erro: " + str(e)

    # ── ARDUINO (geração de código) ──
    def gerar_codigo_arduino(self, desc):
        r = self.ia.gemini_complexo(
            "Gere código Arduino C++ completo para: " + desc +
            ". Arduino Uno/Nano/Mega. Comentários em português. Seja prático.")
        nome = "arduino_" + datetime.datetime.now().strftime("%d%m%Y_%H%M") + ".ino"
        try:
            with open(nome, "w", encoding="utf-8") as f:
                f.write(r)
        except Exception as _e:
            logging.exception(_e)
        self._reg("Gerou Arduino: " + desc[:40])
        return r[:600] + "\n\nSalvo como " + nome

    # ── LEMBRETES ──
    def adicionar_lembrete(self, texto, minutos=1, hora_str=None):
        if hora_str:
            try:
                h = datetime.datetime.strptime(hora_str, "%H:%M")
                alvo = datetime.datetime.now().replace(
                    hour=h.hour, minute=h.minute, second=0, microsecond=0)
                if alvo < datetime.datetime.now():
                    alvo += datetime.timedelta(days=1)
            except Exception:
                alvo = datetime.datetime.now() + datetime.timedelta(minutes=minutos)
        else:
            alvo = datetime.datetime.now() + datetime.timedelta(minutes=minutos)
        self.lembretes.append({"texto": texto, "horario": alvo})
        self._reg("Lembrete: " + texto)
        return "Lembrete para " + alvo.strftime("%H:%M") + ": " + texto

    def _checar_lembretes(self):
        while True:
            try:
                for l in self.lembretes[:]:
                    if datetime.datetime.now() >= l["horario"]:
                        self._disparo_lembrete(l["texto"])
                        self.notificar("Lembrete IRIS", l["texto"])
                        self.lembretes.remove(l)
            except Exception as _e:
                logging.exception(_e)
            time.sleep(15)

    def _disparo_lembrete(self, texto):
        pass  # setado pelo IRIS principal

    # ── RESUMO ──
    def resumo_diario(self, mon):
        agora = datetime.datetime.now()
        partes = [agora.strftime("%d/%m/%Y %H:%M"),
                  "CPU: " + str(round(mon.cpu)) + "% | RAM: " + str(round(mon.ram)) + "%"]
        if mon.bat > 0:
            partes.append("Bateria: " + str(round(mon.bat)) + "%" + ("+" if mon.plugado else ""))
        partes.append("Memória: " + str(self.mem.n_aprendizados) +
                      " registros | Visita #" + str(self.mem.visitas))
        if self.lembretes:
            partes.append(str(len(self.lembretes)) + " lembrete(s) pendente(s)")
        self._reg("Resumo diário")
        return "Resumo do dia:\n" + "\n".join(partes)

    # ── MODO FOCO ──
    def modo_foco(self, ativar):
        sites = ["youtube.com", "facebook.com", "instagram.com",
                 "twitter.com", "tiktok.com", "reddit.com"]
        marcador = "# IRIS_FOCO"
        backup_path = Path("/tmp/iris_hosts_backup")
        try:
            with open("/etc/hosts", "r") as f:
                conteudo = f.read()
            if ativar and not backup_path.exists():
                backup_path.write_text(conteudo)
                logging.info("Backup de /etc/hosts criado")
            if ativar:
                if marcador in conteudo:
                    return "Modo foco já ativo!"
                bloqueios = "\n" + marcador + "\n"
                bloqueios += "\n".join("127.0.0.1 " + s + "\n127.0.0.1 www." + s for s in sites)
                bloqueios += "\n" + marcador
                subprocess.run(["sudo", "tee", "-a", "/etc/hosts"],
                               input=bloqueios.encode(), capture_output=True)
                self._reg("Modo foco ativado")
                return "Modo foco ATIVADO! " + str(len(sites)) + " sites bloqueados."
            else:
                linhas = [l for l in conteudo.split("\n")
                          if marcador not in l and not any(s in l for s in sites)]
                subprocess.run(["sudo", "tee", "/etc/hosts"],
                               input="\n".join(linhas).encode(), capture_output=True)
                self._reg("Modo foco desativado")
                return "Modo foco DESATIVADO!"
        except Exception as e:
            return "Erro (precisa sudo): " + str(e)

    # ── GRÁFICO ──
    def grafico_cpu(self, mon):
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            nome = "grafico_cpu_" + datetime.datetime.now().strftime("%H%M%S") + ".png"
            dest = str(Path.home() / "Pictures" / nome)
            fig, ax = plt.subplots(figsize=(10, 4), facecolor="#080A12")
            ax.set_facecolor("#080A12")
            dados = mon.hist_cpu[-60:]
            ax.plot(dados, color="#00C8F5", linewidth=2)
            ax.fill_between(range(len(dados)), dados, alpha=0.25, color="#00C8F5")
            media = sum(dados) / len(dados) if dados else 0
            ax.axhline(media, color="#FFD700", linestyle="--", linewidth=1, alpha=0.7)
            ax.set_ylim(0, 100)
            ax.set_title("CPU — últimos 60 segundos | Média: " + str(round(media)) + "%",
                         color="white", fontsize=12)
            ax.tick_params(colors="white")
            for spine in ax.spines.values():
                spine.set_color("#00C8F5")
            plt.tight_layout()
            plt.savefig(dest, dpi=100, bbox_inches="tight")
            plt.close()
            subprocess.Popen(["xdg-open", dest],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self._reg("Gráfico CPU gerado")
            return "Gráfico salvo e aberto: ~/Pictures/" + nome
        except ImportError:
            return "Instala: pip3 install matplotlib --break-system-packages"
        except Exception as e:
            return "Erro: " + str(e)

    # ── BUSCA ──
    def buscar(self, query):
        try:
            self._reg("Buscou: " + query)
            return self.ia.gemini_complexo(
                "Pesquise e responda em português de forma concisa sobre: " + query +
                ". Seja direto e informativo. Máximo 3 parágrafos.")
        except Exception as e:
            return "Erro na busca: " + str(e)

    # ── CLIMA ──
    def clima(self, cidade=None):
        cidade = cidade or CIDADE_PADRAO
        if OPENWEATHER_KEY:
            try:
                r = requests.get(
                    "https://api.openweathermap.org/data/2.5/weather?q=" + cidade +
                    "&appid=" + OPENWEATHER_KEY + "&lang=pt_br&units=metric",
                    timeout=5).json()
                if "main" in r and "temp" in r["main"]:
                    self._reg("Clima: " + cidade)
                    temp = round(r["main"]["temp"])
                    desc = r["weather"][0]["description"]
                    umid = r["main"]["humidity"]
                    chuva = ("Sim, leva guarda-chuva!" if any(
                        x in desc.lower() for x in ["chuva", "rain", "thunder", "drizzle"])
                        else "Não deve chover.")
                    return (cidade + ": " + str(temp) + "C | " + desc +
                            " | Umidade: " + str(umid) + "% | Vai chover? " + chuva)
            except Exception as _e:
                logging.exception(_e)
        # Fallback sem chave: wttr.in
        try:
            r = requests.get("https://wttr.in/" + requests.utils.quote(cidade) +
                             "?format=%l:+%t,+%C,+umidade+%h,+chuva+%p&lang=pt",
                             timeout=6)
            if r.ok and r.text.strip():
                self._reg("Clima via wttr.in: " + cidade)
                return r.text.strip()
        except Exception as _e:
            logging.exception(_e)
        return "Não consegui obter o clima agora."

    # ── TELEGRAM ──
    def telegram(self, msg):
        if not TELEGRAM_TOKEN:
            return "Configure TELEGRAM_TOKEN no iris_config.json — @BotFather"
        try:
            requests.post("https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage",
                          data={"chat_id": TELEGRAM_CHAT_ID, "text": msg}, timeout=8)
            self._reg("Telegram enviado")
            return "Mensagem enviada no Telegram!"
        except Exception as e:
            return "Erro: " + str(e)

    # ── AUTO-MELHORIA ──
    def analisar_codigo(self, codigo_path):
        try:
            with open(codigo_path, "r", encoding="utf-8") as f:
                codigo = f.read()
            r = self.ia.gemini_complexo(
                "Analise esse código Python e sugira melhorias práticas em português:\n\n" +
                codigo[:4000])
            with open("iris_melhorias.txt", "w", encoding="utf-8") as f:
                f.write("Análise: " + str(datetime.datetime.now()) + "\n\n" + r)
            self._reg("Analisou próprio código")
            return r[:500] + "\n\nCompleto em iris_melhorias.txt"
        except Exception as e:
            return "Erro: " + str(e)

    # ══════════════════════════════════════════
    #  POCO X7 VIA ADB (USB ou WiFi)
    # ══════════════════════════════════════════
    def _adb(self, cmd):
        try:
            import shlex
            r = subprocess.run(["adb"] + shlex.split(cmd),
                               capture_output=True, text=True, timeout=15)
            return (r.stdout or r.stderr or "").strip()
        except Exception as _e:
            logging.exception(_e)
            return "Erro ADB: " + str(_e)

    def _adb_conectado(self):
        r = subprocess.getoutput("adb devices")
        linhas = [l for l in r.split("\n")[1:] if l.strip()]
        return any(l.strip().endswith("device") for l in linhas)

    def _adb_wifi(self):
        """Reconecta via WiFi se cabo desconectado."""
        if not self._adb_conectado():
            subprocess.getoutput("adb connect " + POCO_IP + ":5555")
        return self._adb_conectado()

    def _poco_ok(self):
        return self._adb_conectado() or self._adb_wifi()

    def celular_status(self):
        if not self._poco_ok():
            return "Poco X7 não conectado. Conecta o cabo USB ou a mesma WiFi!"
        bat = self._adb("shell dumpsys battery | grep level").replace("level:", "").strip()
        android = self._adb("shell getprop ro.build.version.release").strip()
        arq = self._adb("shell df -h /data | tail -1").strip()
        self._reg("Status do celular")
        return ("Poco X7 | Android " + android + "\n" +
                "Bateria: " + bat + "%\n" +
                "Armazenamento: " + arq)

    def celular_screenshot(self):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        nome = "poco_" + datetime.datetime.now().strftime("%d%m%Y_%H%M%S") + ".png"
        dest = str(Path.home() / "Pictures" / nome)
        self._adb("shell screencap -p /sdcard/iris_screen.png")
        self._adb("pull /sdcard/iris_screen.png " + dest)
        self._adb("shell rm /sdcard/iris_screen.png")
        self._reg("Screenshot do celular: " + nome)
        subprocess.Popen(["xdg-open", dest],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "Screenshot do Poco X7 salvo em ~/Pictures/" + nome

    def celular_bateria(self):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        bat = self._adb("shell dumpsys battery | grep level").replace("level:", "").strip()
        status = self._adb("shell dumpsys battery | grep status")
        temp = self._adb("shell dumpsys battery | grep temperature").replace("temperature:", "").strip()
        try:
            temp_c = str(round(int(temp) / 10)) + "C"
        except Exception:
            temp_c = temp
        status_txt = "Carregando" if "2" in status else "Descarregando"
        self._reg("Bateria do celular")
        return "Poco X7: " + bat + "% | " + status_txt + " | Temp: " + temp_c

    def celular_armazenamento(self):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        r = self._adb("shell df -h /data /sdcard 2>/dev/null")
        self._reg("Armazenamento do celular")
        return "Armazenamento Poco X7:\n" + r

    def celular_apps(self):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        r = self._adb("shell pm list packages -3")
        apps = [l.replace("package:", "") for l in r.split("\n") if l][:15]
        self._reg("Apps do celular")
        return "Apps instalados:\n" + "\n".join(apps)

    def celular_desinstalar_app(self, pacote):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        r = self._adb("uninstall " + pacote)
        self._reg("Desinstalou app: " + pacote)
        return "App '" + pacote + "': " + r

    def celular_volume(self, acao):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        if acao == "aumentar":
            self._adb("shell input keyevent 24")
            self._adb("shell input keyevent 24")
        elif acao == "diminuir":
            self._adb("shell input keyevent 25")
            self._adb("shell input keyevent 25")
        elif acao == "mudo":
            self._adb("shell input keyevent 164")
        self._reg("Volume celular: " + acao)
        return "Volume do Poco X7 " + acao + "!"

    def celular_ligar_tela(self, ligar=True):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        self._adb("shell input keyevent 26")
        if ligar:
            self._adb("shell input keyevent 82")
        self._reg("Tela celular: " + ("ligada" if ligar else "desligada"))
        return "Tela do Poco X7 " + ("ligada!" if ligar else "desligada!")

    def celular_enviar_texto(self, texto):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        self._adb("shell input text " + texto.replace(" ", "%s"))
        self._reg("Digitou no celular: " + texto[:30])
        return "Texto digitado no Poco X7!"

    def celular_notificacoes(self):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        r = self._adb("shell dumpsys notification | grep NotificationRecord | head -10")
        self._reg("Notificações do celular")
        return "Notificações:\n" + (r if r else "Nenhuma notificação")

    def celular_reiniciar(self):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        self._adb("reboot")
        self._reg("Reiniciou o celular")
        return "Poco X7 reiniciando..."

    def celular_enviar_arquivo(self, arquivo_local):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        nome = Path(arquivo_local).name
        self._adb("push " + arquivo_local + " /sdcard/Download/" + nome)
        self._reg("Enviou arquivo: " + nome)
        return "Arquivo enviado para Downloads do Poco X7: " + nome

    def celular_baixar_arquivo(self, arquivo_celular):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        dest = str(Path.home() / "Downloads" / Path(arquivo_celular).name)
        self._adb("pull " + arquivo_celular + " " + dest)
        self._reg("Baixou arquivo do celular")
        return "Arquivo baixado para ~/Downloads/!"

    def celular_limpar_cache(self):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        self._adb("shell pm clear --user 0 com.android.chrome")
        self._adb("shell pm clear --user 0 com.miui.gallery")
        r = self._adb("shell df -h /data | tail -1")
        self._reg("Limpou cache do celular")
        return "Cache limpo!\n" + r   # BUG da v7 corrigido: faltava o return

    def celular_listar_arquivos(self, pasta="/sdcard"):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        r = self._adb("shell ls -lh " + pasta + " 2>/dev/null")
        linhas = [l for l in r.split("\n") if l.strip()][:20]
        self._reg("Listou arquivos do celular: " + pasta)
        return "Arquivos em " + pasta + ":\n" + "\n".join(linhas)

    def celular_apagar_arquivo(self, caminho):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        self._adb("shell rm -f " + caminho)
        self._reg("Apagou do celular: " + caminho)
        return "Arquivo apagado: " + caminho

    def celular_apagar_downloads(self):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        self._adb("shell find /sdcard/Download -type f -delete")
        self._reg("Apagou downloads do celular")
        return "Downloads do Poco X7 apagados!"

    def celular_apagar_fotos_antigas(self, dias=30):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        self._adb("shell find /sdcard/DCIM -name '*.jpg' -mtime +" + str(dias) + " -delete")
        self._reg("Apagou fotos antigas do celular")
        return "Fotos com mais de " + str(dias) + " dias apagadas!"

    def celular_espaco_livre(self):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        r = self._adb("shell df -h /sdcard /data 2>/dev/null")
        self._reg("Espaço livre do celular")
        return "Espaço no Poco X7:\n" + r

    def celular_info_completa(self):
        if not self._poco_ok():
            return "Poco X7 não conectado! Certifique que estão na mesma WiFi."
        android = self._adb("shell getprop ro.build.version.release").strip()
        bat = self._adb("shell dumpsys battery | grep level").replace("level:", "").strip()
        temp_b = self._adb("shell dumpsys battery | grep temperature").replace("temperature:", "").strip()
        try:
            temp_c = str(round(int(temp_b) / 10)) + "C"
        except Exception:
            temp_c = "?"
        ram = self._adb("shell cat /proc/meminfo | grep MemAvailable").strip()
        disco = self._adb("shell df -h /sdcard | tail -1").strip()
        ip = self._adb("shell ip addr show wlan0 | grep 'inet '").strip()
        self._reg("Info completa do celular")
        return ("Poco X7 | Android " + android + "\n" +
                "Bateria: " + bat + "% | Temp: " + temp_c + "\n" +
                "RAM livre: " + ram + "\n" +
                "Disco: " + disco + "\n" +
                "IP: " + ip[:40])

    def celular_ligar_wifi(self, ligar=True):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        self._adb("shell svc wifi " + ("enable" if ligar else "disable"))
        self._reg("WiFi do celular: " + str(ligar))
        return "WiFi do Poco X7 " + ("ligado!" if ligar else "desligado!")

    def celular_instalar_apk(self, caminho_apk):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        r = self._adb("install " + caminho_apk)
        self._reg("Instalou APK: " + caminho_apk)
        return "APK instalado: " + r[:100]

    def celular_fazer_backup_fotos(self):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        dest = str(Path.home() / "Pictures" / "Backup_Poco_X7")
        Path(dest).mkdir(parents=True, exist_ok=True)
        self._adb("pull /sdcard/DCIM/Camera " + dest)
        self._reg("Backup de fotos do celular")
        return "Fotos copiadas para ~/Pictures/Backup_Poco_X7!"

    def celular_status_painel(self):
        """Dados para o painel — não bloqueia se desconectado."""
        if not self._adb_conectado():
            return {"conectado": False}
        try:
            bat = int(self._adb("shell dumpsys battery | grep level")
                      .replace("level:", "").strip() or 0)
            plugado = "2" in self._adb("shell dumpsys battery | grep status")
            temp_b = self._adb("shell dumpsys battery | grep temperature").replace("temperature:", "").strip()
            temp_c = round(int(temp_b) / 10) if temp_b.isdigit() else 0
            disco_r = self._adb("shell df /sdcard 2>/dev/null | tail -1").split()
            disco_p = int(disco_r[4].replace("%", "")) if len(disco_r) > 4 else 0
            ram_r = self._adb("shell cat /proc/meminfo | grep MemAvailable").split()
            ram_mb = int(ram_r[1]) // 1024 if len(ram_r) > 1 else 0
            return {"bat": bat, "plugado": plugado, "temp": temp_c,
                    "disco": disco_p, "ram_livre_mb": ram_mb, "conectado": True}
        except Exception:
            return {"conectado": False}

    # ══════════════════════════════════════════
    #  MODO VIGIA — detecta movimento pela webcam
    # ══════════════════════════════════════════
    def ativar_vigia(self, ativar=True):
        if ativar:
            if self._vigia_ativo:
                return "Modo vigia já está ativo!"
            self._vigia_ativo = True
            threading.Thread(target=self._loop_vigia, daemon=True).start()
            self._reg("Modo vigia ativado")
            return ("Modo vigia ATIVADO! Monitorando pela webcam. "
                    "Aviso no Telegram se detectar movimento.")
        else:
            self._vigia_ativo = False
            self._reg("Modo vigia desativado")
            return "Modo vigia DESATIVADO!"

    def _loop_vigia(self):
        cap = None
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                logging.warning("Vigia: webcam não disponível")
                self._vigia_ativo = False
                return
            ok, frame1 = cap.read()
            if not ok:
                self._vigia_ativo = False
                return
            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            alertas = 0
            while self._vigia_ativo:
                ok, frame2 = cap.read()
                if not ok:
                    break
                frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
                diff = cv2.absdiff(frame1, frame2_gray)
                _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
                if thresh.sum() // 255 > 3000:
                    alertas += 1
                    if alertas % 3 == 1:
                        self.telegram("ALERTA IRIS: Movimento detectado!")
                        self.notificar("IRIS Vigia", "Movimento detectado!")
                        self._reg("Vigia: movimento detectado")
                else:
                    alertas = max(0, alertas - 1)
                frame1 = frame2_gray
                time.sleep(1.5)
        except ImportError:
            logging.warning("Vigia precisa: pip3 install opencv-python --break-system-packages")
        except Exception as _e:
            logging.exception(_e)
        finally:
            if cap is not None:
                cap.release()
                logging.info("Vigia: webcam liberada")

    # ══════════════════════════════════════════
    #  ORGANIZAR ARQUIVOS
    # ══════════════════════════════════════════
    def organizar_downloads(self):
        pasta = Path.home() / "Downloads"
        pasta.mkdir(parents=True, exist_ok=True)
        tipos = {
            ".pdf": Path.home()/"Documents"/"PDFs",
            ".docx": Path.home()/"Documents"/"Word",
            ".xlsx": Path.home()/"Documents"/"Planilhas",
            ".txt": Path.home()/"Documents"/"Textos",
            ".py": Path.home()/"Documents"/"Python",
            ".jpg": Path.home()/"Pictures"/"Downloads",
            ".jpeg": Path.home()/"Pictures"/"Downloads",
            ".png": Path.home()/"Pictures"/"Downloads",
            ".mp4": Path.home()/"Videos"/"Downloads",
            ".mp3": Path.home()/"Music"/"Downloads",
            ".zip": pasta/"Compactados",
            ".rar": pasta/"Compactados",
        }
        movidos = []
        try:
            for item in pasta.iterdir():
                if item.is_file() and item.suffix.lower() in tipos:
                    dest = tipos[item.suffix.lower()]
                    dest.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(item), str(dest / item.name))
                    movidos.append(item.name)
            self._reg("Organizou downloads: " + str(len(movidos)) + " arquivos")
            if movidos:
                return str(len(movidos)) + " arquivos organizados!\n" + "\n".join(movidos[:8])
            return "Downloads já estão organizados!"
        except Exception as e:
            return "Erro ao organizar: " + str(e)

    def organizar_area_trabalho(self):
        pasta = Path.home() / "Área de trabalho"
        if not pasta.exists():
            pasta = Path.home() / "Desktop"
        tipos = {".pdf": pasta/"PDFs", ".docx": pasta/"Documentos",
                 ".py": pasta/"Python", ".jpg": pasta/"Imagens",
                 ".png": pasta/"Imagens", ".txt": pasta/"Textos"}
        movidos = []
        try:
            for item in pasta.iterdir():
                if item.is_file() and item.suffix.lower() in tipos:
                    dest = tipos[item.suffix.lower()]
                    dest.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(item), str(dest / item.name))
                    movidos.append(item.name)
            self._reg("Organizou área de trabalho")
            return str(len(movidos)) + " arquivos organizados na Área de Trabalho!"
        except Exception as e:
            return "Erro: " + str(e)

    # ══════════════════════════════════════════
    #  BOT TELEGRAM BIDIRECIONAL
    # ══════════════════════════════════════════
    def iniciar_bot_telegram(self, processador_callback):
        if not TELEGRAM_TOKEN:
            return "Configure TELEGRAM_TOKEN para usar o bot!"
        if self._bot_ativo:
            return "Bot Telegram já está ativo!"
        self._bot_ativo = True
        self._bot_callback = processador_callback
        threading.Thread(target=self._loop_bot_telegram, daemon=True).start()
        self._reg("Bot Telegram iniciado")
        try:
            self.telegram("IRIS v1.7 online! Mande um comando. Digite: ajuda")
        except Exception as _e:
            logging.exception(_e)
        return "Bot Telegram ATIVO! Confirmação enviada no celular!"

    def _loop_bot_telegram(self):
        url = "https://api.telegram.org/bot" + TELEGRAM_TOKEN
        offset = 0
        session = requests.Session()
        ultimo_briefing = ""  # pra mandar bom dia só uma vez por dia
        ultimo_aviso = 0
        while self._bot_ativo:
            try:
                r = session.get(url + "/getUpdates?offset=" + str(offset) + "&timeout=10",
                                timeout=15).json()
                for update in r.get("result", []):
                    offset = update["update_id"] + 1
                    msg = update.get("message", {})
                    chat_id = str(msg.get("chat", {}).get("id", ""))
                    if chat_id != TELEGRAM_CHAT_ID:
                        continue
                    texto = msg.get("text", "")
                    # ── COMANDO POR FOTO (v26): você manda foto, ela analisa ──
                    if "photo" in msg and self.ia.gemini:
                        try:
                            file_id = msg["photo"][-1]["file_id"]
                            fr = session.get(url + "/getFile?file_id=" + file_id, timeout=10).json()
                            caminho = fr["result"]["file_path"]
                            img = session.get("https://api.telegram.org/file/bot" +
                                              TELEGRAM_TOKEN + "/" + caminho, timeout=20).content
                            import tempfile
                            tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
                            tmp.write(img); tmp.close()
                            legenda = msg.get("caption", "") or "O que você vê nesta imagem? Em português."
                            desc = self.ia.gemini_visao(tmp.name, legenda)
                            os.remove(tmp.name)
                            session.post(url + "/sendMessage",
                                         data={"chat_id": chat_id, "text": desc[:4000]}, timeout=8)
                        except Exception as _e:
                            logging.exception(_e)
                        continue
                    # ── COMANDO POR ÁUDIO: você manda áudio, ela ouve e responde ──
                    if ("voice" in msg or "audio" in msg) and self.ia.gemini:
                        try:
                            obj = msg.get("voice") or msg.get("audio")
                            file_id = obj["file_id"]
                            fr = session.get(url + "/getFile?file_id=" + file_id, timeout=10).json()
                            caminho = fr["result"]["file_path"]
                            aud = session.get("https://api.telegram.org/file/bot" +
                                              TELEGRAM_TOKEN + "/" + caminho, timeout=20).content
                            import tempfile
                            ext = ".ogg" if caminho.endswith((".ogg", ".oga")) else ".mp3"
                            tmp = tempfile.NamedTemporaryFile(suffix=ext, delete=False)
                            tmp.write(aud); tmp.close()
                            # transcreve o áudio e processa como se fosse comando de texto
                            transcrito = self.ia.gemini_audio(tmp.name,
                                "Transcreva exatamente o que foi dito, em português, só o texto.")
                            os.remove(tmp.name)
                            # tenta executar como comando; se for conversa, responde natural
                            resposta = self._bot_callback(transcrito)
                            session.post(url + "/sendMessage",
                                         data={"chat_id": chat_id,
                                               "text": "🎤 Entendi: \"" + transcrito[:100] +
                                               "\"\n\n" + str(resposta)[:3800]}, timeout=8)
                        except Exception as _e:
                            logging.exception(_e)
                            session.post(url + "/sendMessage",
                                         data={"chat_id": chat_id, "text": "Não consegui ouvir o áudio :("}, timeout=8)
                        continue
                    # ── COMANDO DE TEXTO ──
                    if texto:
                        resposta = self._bot_callback(texto)
                        session.post(url + "/sendMessage",
                                     data={"chat_id": chat_id, "text": str(resposta)[:4000]},
                                     timeout=8)
                # ── PROATIVO (v26): bom dia + avisos sozinha ──
                agora = datetime.datetime.now()
                hoje = agora.strftime("%Y-%m-%d")
                if 6 <= agora.hour <= 10 and ultimo_briefing != hoje:
                    try:
                        session.post(url + "/sendMessage",
                                     data={"chat_id": TELEGRAM_CHAT_ID,
                                           "text": "☀️ " + self.briefing()}, timeout=8)
                        ultimo_briefing = hoje
                    except Exception:
                        pass
                # avisos críticos (no máximo 1 a cada 30 min)
                if self.mon and time.time() - ultimo_aviso > 1800:
                    aviso = None
                    if self.mon.bat > 0 and self.mon.bat < 15 and not self.mon.plugado:
                        aviso = "🔋 Bateria do PC em " + str(round(self.mon.bat)) + "%! Pluga aí."
                    elif self.mon.disco > 95:
                        aviso = "💾 Disco quase cheio (" + str(round(self.mon.disco)) + "%)!"
                    if aviso:
                        session.post(url + "/sendMessage",
                                     data={"chat_id": TELEGRAM_CHAT_ID, "text": aviso}, timeout=8)
                        ultimo_aviso = time.time()
            except Exception as _e:
                logging.exception(_e)
                session = requests.Session()
            time.sleep(2)

    # ══════════════════════════════════════════
    #  PAINEL WEB (v26) — controle pelo navegador
    #  do Poco (na sua rede). Botões + status, sem
    #  digitar comando. Acesse http://IP_DO_PC:8777
    # ══════════════════════════════════════════
    def iniciar_painel_web(self, porta=8777):
        if getattr(self, "_web_ativo", False):
            return "Painel web já está rodando!"
        self._web_ativo = True
        threading.Thread(target=self._loop_web, args=(porta,), daemon=True).start()
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except Exception:
            ip = "SEU_IP"
        self._reg("Painel web iniciado")
        return ("Painel web ATIVO! No navegador do Poco (mesma WiFi), acesse:\n"
                "http://" + ip + ":" + str(porta) +
                "\nTem botões pra os comandos principais, sem digitar.")

    def _loop_web(self, porta):
        from http.server import BaseHTTPRequestHandler, HTTPServer
        import urllib.parse
        acoes_self = self
        class H(BaseHTTPRequestHandler):
            def log_message(self, *a): pass
            def _send(self, txt, tipo="text/html"):
                self.send_response(200)
                self.send_header("Content-Type", tipo + "; charset=utf-8")
                self.end_headers()
                self.wfile.write(txt.encode("utf-8"))
            def do_GET(self):
                p = urllib.parse.urlparse(self.path)
                if p.path == "/cmd":
                    q = urllib.parse.parse_qs(p.query)
                    comando = q.get("c", [""])[0]
                    try:
                        r = acoes_self.processador.processar(comando) if acoes_self.processador else "?"
                    except Exception as e:
                        r = "Erro: " + str(e)
                    self._send(str(r), "text/plain")
                    return
                # página principal
                botoes = ["status", "dispositivos", "clima", "resumo do dia",
                          "status do celular", "testa voce mesma", "briefing",
                          "otimiza", "screenshot", "o que voce sabe"]
                bhtml = "".join(
                    "<button onclick=\"cmd('" + b + "')\">" + b + "</button>" for b in botoes)
                html = """<!doctype html><html><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>IRIS</title><style>
body{background:#0a0e1a;color:#cde;font-family:sans-serif;margin:0;padding:16px}
h1{color:#00c8f5;font-size:22px}
button{background:#13243a;color:#9df;border:1px solid #00c8f5;border-radius:10px;
padding:14px;margin:5px;font-size:15px;width:46%}
button:active{background:#00c8f5;color:#000}
#out{margin-top:14px;padding:12px;background:#0d1424;border-radius:10px;
white-space:pre-wrap;min-height:60px;font-size:14px}
input{width:70%;padding:12px;border-radius:10px;border:1px solid #00c8f5;
background:#0d1424;color:#cde;font-size:15px}
</style></head><body>
<h1>IRIS — controle</h1>
<div>""" + bhtml + """</div>
<div style="margin-top:10px">
<input id=txt placeholder="ou digite um comando...">
<button style="width:25%" onclick="cmd(document.getElementById('txt').value)">enviar</button>
</div>
<div id=out>Toque num botão...</div>
<script>
function cmd(c){
 document.getElementById('out').textContent='...';
 fetch('/cmd?c='+encodeURIComponent(c))
  .then(r=>r.text()).then(t=>document.getElementById('out').textContent=t);
}
</script></body></html>"""
                self._send(html)
        try:
            srv = HTTPServer(("0.0.0.0", porta), H)
            while self._web_ativo:
                srv.handle_request()
        except Exception as _e:
            logging.exception(_e)

    # ══════════════════════════════════════════
    #  AGENTE AUTÔNOMO
    # ══════════════════════════════════════════

    # ══════════════════════════════════════════
    #  AGENTE VISUAL (v21) — vê a tela, decide e age
    #  em loop, estilo "Claw", mas com CONFIRMAÇÃO
    #  antes de cliques que mudam coisas e freio de
    #  emergência (jogue o mouse pro canto pra parar).
    # ══════════════════════════════════════════

    # ══════════════════════════════════════════
    #  FILA DE TAREFAS (v22) — várias ações em sequência
    #  Ex: "faz tudo: status depois clima depois resumo do dia"
    # ══════════════════════════════════════════
    def executar_fila(self, texto_tarefas):
        """Executa várias tarefas em sequência. Separe por 'depois', ';' ou 'e depois'."""
        # quebra em tarefas individuais
        bruto = re.split(r'\s*(?:;|\bdepois\b|\be depois\b|\bentao\b|\bentão\b)\s*',
                         texto_tarefas, flags=re.IGNORECASE)
        tarefas = [t.strip() for t in bruto if t.strip() and len(t.strip()) > 1]
        if not tarefas:
            return "Não entendi as tarefas. Ex: faz tudo: status depois clima depois resumo do dia"
        if not self.processador:
            return "Processador não conectado."
        resultados = ["FILA DE " + str(len(tarefas)) + " TAREFAS:"]
        for i, tarefa in enumerate(tarefas):
            try:
                r = self.processador.processar(tarefa)
                resultados.append(str(i + 1) + ". " + tarefa + "\n   -> " + str(r)[:120])
                time.sleep(0.4)
            except Exception as e:
                resultados.append(str(i + 1) + ". " + tarefa + " -> erro: " + str(e)[:50])
        self._reg("Fila de " + str(len(tarefas)) + " tarefas")
        return "\n".join(resultados)

    def agente_visual(self, objetivo, max_passos=6, callback_confirma=None):
        """
        Agente que olha a tela e age para cumprir um objetivo.
        callback_confirma(descricao) -> True/False : pergunta ao Francisco
        antes de cada ação que altera algo. Se None, só observa e sugere.
        """
        import tempfile
        self._reg("Agente visual: " + objetivo[:40])
        log = ["AGENTE VISUAL — objetivo: " + objetivo]
        if not self.ia.gemini:
            return "Preciso do Gemini (visão) pra esse agente. Configure GEMINI_API_KEY."
        historico_acoes = []
        for passo in range(max_passos):
            # 1. tira print da tela atual
            try:
                tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                tmp.close()
                pyautogui.screenshot().save(tmp.name)
            except Exception as e:
                log.append("Erro ao ver a tela: " + str(e))
                break
            larg, alt = pyautogui.size()
            # 2. pergunta ao Gemini (que vê) qual a próxima ação
            plano = self.ia.gemini_visao(tmp.name,
                "Você é um agente que controla este computador Linux para Francisco. "
                "OBJETIVO: " + objetivo + "\n"
                "Ações já feitas: " + ("; ".join(historico_acoes) or "nenhuma") + "\n"
                "Tela tem " + str(larg) + "x" + str(alt) + " pixels.\n"
                "Responda com UMA ação no formato exato (uma linha):\n"
                "CLICAR x y | DIGITAR texto | TECLA nome | ABRIR programa | "
                "ESPERAR | PRONTO (se objetivo cumprido) | IMPOSSIVEL motivo\n"
                "Seja preciso nas coordenadas olhando a tela. Só a ação, nada mais.")
            try:
                os.remove(tmp.name)
            except Exception:
                pass
            acao = (plano or "").strip().split("\n")[0].strip()
            log.append("Passo " + str(passo + 1) + ": " + acao[:60])
            partes = acao.split(None, 1)
            cmd = partes[0].upper() if partes else ""
            arg = partes[1] if len(partes) > 1 else ""

            if cmd == "PRONTO":
                log.append(">>> Objetivo cumprido!")
                break
            if cmd == "IMPOSSIVEL":
                log.append(">>> Não consegui: " + arg)
                break
            if cmd == "ESPERAR":
                time.sleep(2)
                historico_acoes.append("esperei")
                continue

            # ações que ALTERAM algo precisam de confirmação
            altera = cmd in ("CLICAR", "DIGITAR", "TECLA")
            if altera and callback_confirma:
                if not callback_confirma("Passo " + str(passo + 1) + ": " + acao):
                    log.append(">>> Você cancelou esta ação. Parando.")
                    break
            try:
                if cmd == "CLICAR":
                    xy = [int(n) for n in arg.split()[:2]]
                    pyautogui.click(xy[0], xy[1])
                    historico_acoes.append("cliquei em " + str(xy))
                elif cmd == "DIGITAR":
                    pyautogui.typewrite(arg, interval=0.03)
                    historico_acoes.append("digitei: " + arg[:20])
                elif cmd == "TECLA":
                    pyautogui.press(arg.strip().lower())
                    historico_acoes.append("tecla " + arg)
                elif cmd == "ABRIR":
                    self.abrir_programa(arg.strip())
                    historico_acoes.append("abri " + arg)
                    time.sleep(2)
                else:
                    log.append("(ação não reconhecida, pulando)")
                time.sleep(1.2)  # deixa a tela reagir
            except pyautogui.FailSafeException:
                log.append(">>> FREIO DE EMERGÊNCIA acionado (mouse no canto). Parei!")
                break
            except Exception as e:
                log.append("Erro na ação: " + str(e)[:50])
        # resumo final
        resumo = self.ia.groq_rapido(
            "O agente tentou: '" + objetivo + "'. Passos:\n" + "\n".join(log[-8:]) +
            "\nResuma em 1-2 frases se conseguiu, em português, como amiga.",
            max_tokens=120)
        log.append("\n" + (resumo or ""))
        return "\n".join(log)

    def agente_executar(self, objetivo, max_passos=8):
        """Planeja, executa passo a passo e avalia o resultado."""
        self._reg("Agente iniciado: " + objetivo)
        resultados = []
        plano_raw = self.ia.gemini_complexo(
            f"""Você é um agente executor Linux. Dado o objetivo abaixo,
liste de 2 a 6 ações simples e diretas para executar, uma por linha.
Use apenas comandos que a IRIS pode fazer:
- status, screenshot, otimiza sistema
- abre [programa], google [tema], youtube [tema]
- salva nota [texto], lembrete [texto]
- traduz [texto], clima, busca [tema]
- codigo arduino [descricao]
- lista arquivos, cria arquivo [nome]
- move o mouse X Y, clica, digita [texto]
Objetivo: {objetivo}
Responda APENAS com a lista de ações, uma por linha, sem explicação.""")
        passos = [p.strip("-• \t") for p in plano_raw.strip().split("\n")
                  if p.strip() and len(p.strip()) > 3][:max_passos]
        if not passos:
            return "Não consegui planejar. Tente ser mais específico."
        resultados.append(f"Plano ({len(passos)} passos):")
        for i, p in enumerate(passos):
            resultados.append(f"  {i+1}. {p}")
        resultados.append("\nExecutando:")
        for i, passo in enumerate(passos):
            try:
                r = self.processador.processar(passo)
                resultados.append(f"  OK {passo[:40]}: {str(r)[:60]}")
                self._reg(f"Agente passo {i+1}: {passo[:40]}")
                time.sleep(0.5)
            except Exception as _e:
                logging.exception(_e)
                resultados.append(f"  ERRO {passo[:40]}")
        resumo = self.ia.groq_rapido(
            f"O agente executou o objetivo '{objetivo}' com esses resultados:\n" +
            "\n".join(resultados[-6:]) +
            "\n\nResuma em 1 frase se foi bem sucedido.")
        resultados.append(f"\nResultado: {resumo}")
        return "\n".join(resultados)

    def agente_monitorar(self, condicao, acao, intervalo=60, max_checks=10):
        """Monitora uma condição e executa ação quando atendida."""
        def _loop():
            checks = 0
            self._reg(f"Monitor iniciado: {condicao}")
            while checks < max_checks:
                try:
                    dados = (f"CPU:{self.mon.cpu}% RAM:{self.mon.ram}% "
                             f"Disco:{self.mon.disco}%")
                    avaliar = self.ia.groq_rapido(
                        f"Dados do sistema: {dados}\n"
                        f"Condição para agir: {condicao}\n"
                        f"A condição foi atendida? Responda apenas SIM ou NAO.",
                        max_tokens=5, temperature=0.0)
                    if "SIM" in (avaliar or "").upper():
                        r = self.processador.processar(acao)
                        self._reg(f"Monitor ativou: {acao}")
                        self.ia_callback(f"Condição '{condicao}' atendida! "
                                         f"Executei: {acao}\n{str(r)[:200]}")
                        return
                    checks += 1
                    time.sleep(intervalo)
                except Exception as _e:
                    logging.exception(_e)
                    time.sleep(intervalo)
            self.ia_callback(f"Monitoramento de '{condicao}' encerrado sem acionar.")
        threading.Thread(target=_loop, daemon=True).start()
        return f"Monitorando: '{condicao}' a cada {intervalo}s. Ação: '{acao}'"

    def agente_rotina(self, nome, passos, horario=None):
        """Cria rotina com lista de ações, opcionalmente agendada."""
        self._rotinas[nome] = {"passos": passos, "horario": horario}

        def _executar():
            resultados = []
            for passo in passos:
                try:
                    r = self.processador.processar(passo)
                    resultados.append(f"OK {passo}: {str(r)[:50]}")
                    time.sleep(1)
                except Exception as _e:
                    logging.exception(_e)
                    resultados.append(f"ERRO {passo}")
            self._reg(f"Rotina '{nome}' executada")
            return "\n".join(resultados)

        if horario:
            def _agendar():
                while nome in self._rotinas:
                    if datetime.datetime.now().strftime("%H:%M") == horario:
                        r = _executar()
                        self.ia_callback(f"Rotina '{nome}' concluída:\n{r}")
                        time.sleep(61)
                    time.sleep(20)
            threading.Thread(target=_agendar, daemon=True).start()
            return f"Rotina '{nome}' agendada para {horario}!"
        return _executar()

    def ia_callback(self, msg):
        pass  # substituído pelo IRIS principal

    def iniciar_ditado(self):
        return "Modo ditado indisponível nesta interface."  # substituído pelo IRIS

# ══════════════════════════════════════════════════════════════
#  PROCESSADOR DE COMANDOS — agora com interpretador IA (Jarvis)
# ══════════════════════════════════════════════════════════════
class Processador:
    LISTA_COMANDOS = """status | otimiza | processos | screenshot
aumenta volume | diminui volume | silencia
move o mouse X Y | clica | digita [texto] | pressiona tecla [tecla]
o que tem na tela | analisa imagem [arquivo] | o que voce ve | leia [arquivo]
lista janelas | minimiza tudo | foca [nome]
abre [firefox/terminal/vscode/...]
google [tema] | youtube [tema] | vai para [site]
lista arquivos | cria arquivo [nome] | apaga imagens
play | pause | proxima musica | anterior musica
tira foto | traduz [texto]
monitorar rede | testa internet | clima
salva nota [texto] | ver notas
lembrete as HH:MM [texto] | lembrete [texto]
codigo arduino [descricao]
modo foco | desativa foco | grafico cpu | ver historico
resumo do dia | liga luz | desliga luz
ativa vigia | desativa vigia
organiza downloads | organiza area de trabalho
ativa bot telegram | envia telegram [msg]
executa objetivo [tarefa] | rotina matinal | rotina noturna
status do celular | bateria do celular | screenshot do celular
apps do celular | notificacoes do celular | backup fotos
cria projeto [nome] | programa [descricao] | executa codigo [arq.py]
corrige [arq.py] | compacta [arq.py] | lista programas
simula neuronios [N] | treina rede ++--oo++ | lembra padrao [padrao]
status da rede | esquece a rede | cerebro local | calcula [conta]
portas serial | monitor serial [seg] | arduino [comando]
compila arduino [arq.ino] | grava arduino [arq.ino]
meus projetos | projeto [nome] | sai do projeto | registra projeto nome: desc
tarefa [texto] | tarefas | conclui tarefa N
diario [progresso] | ver diario | relatorio | proximo passo
backup projeto [pasta] | dispositivos
acha meu celular | faz o celular tocar | cofre | modo panico
ativa guarda costas
aprende que [fato] | o que voce sabe | autoverifica
modo espontaneo | qual seu humor | (OpenRouter no iris_config.json)
instala firmware | servo [graus] | servo [graus] pino [N]
liga/desliga led [pino] | pwm [pino] [valor] | le sensor a0 | ping arduino
apaga pasta [nome] (pede confirmacao!)
cria plugin [o que faz] | lista plugins | recarrega plugins
diagnostico | backups da iris | restaura iris [versao]
status ia | modo local | modo nuvem | modo auto
ditado (fale por minutos, diga 'fim do ditado' para salvar)
busca github [tema] | baixa github user/repo | estuda github [nome]
propoe melhoria [tema] | forja habilidade [ideia]
projeta uma ia melhor que voce [objetivo]"""

    def __init__(self, usuario, mem, ia, acoes, mon, voz=None):
        self.usuario = usuario
        self.mem = mem
        self.ia = ia
        self.ac = acoes
        self.mon = mon
        self.voz = voz
        self._pendente = None  # v11: ação aguardando confirmação (ex: apagar pasta)

    def processar(self, prompt):
        p = prompt.lower().strip()
        if not p:
            return "Diga alguma coisa!"

        # ── CONFIRMAÇÃO PENDENTE (v11) — segurança em ações destrutivas ──
        if self._pendente:
            acao, dado = self._pendente
            self._pendente = None
            if p in ("sim", "s", "confirmo", "confirma", "pode", "pode sim", "isso"):
                if acao == "apagar_pasta":
                    return self.ac.apagar_pasta_confirmada(dado)
                if acao == "apagar_arquivo":
                    return self.ac.apagar_arquivo_confirmado(dado)
                if acao == "apagar_foto":
                    return self.ac.apagar_foto_confirmada(dado)
                if acao == "apagar_duplicados":
                    return self.ac.apagar_duplicados_confirmado(dado)
                if acao == "restaurar_iris":
                    return self.ac.guardia_restaurar(dado)
                if acao == "agente_visual":
                    # dispara o agente em thread pra não travar a interface;
                    # o resultado volta pela ia_callback (aparece no chat e na voz)
                    import threading as _th
                    def _rodar():
                        r = self.ac.agente_visual(dado, max_passos=6)
                        self.ac.ia_callback(r)
                    _th.Thread(target=_rodar, daemon=True).start()
                    return "Comecei! Olhando a tela e agindo... (mouse no canto = parar)"
            return "Cancelado! Nada foi alterado. Ufa."

        # ── MOTOR DE IA: nuvem x local (v13 — independência total) ──
        if any(x in p for x in ["status ia", "status da ia", "motores de ia", "qual ia"]):
            return self.ia.status_ia()
        if p in ("modo local", "modo offline total", "ia local"):
            return self.ia.definir_modo("local")
        if p in ("modo nuvem", "modo online", "ia nuvem"):
            return self.ia.definir_modo("nuvem")
        if p in ("modo auto", "modo automatico", "modo automático"):
            return self.ia.definir_modo("auto")

        # ── GITHUB — estudar código do mundo (v15) ──
        if any(p.startswith(x) for x in ["busca no github", "busca github",
                                         "procura no github", "pesquisa github"]):
            tema = p
            for w in ["busca no github", "busca github", "procura no github", "pesquisa github"]:
                tema = tema.replace(w, "", 1)
            return self.ac.github_buscar(tema.strip() or "arduino projects")
        if any(p.startswith(x) for x in ["baixa github", "baixa do github",
                                         "clona", "baixar github"]):
            repo = p
            for w in ["baixa do github", "baixa github", "baixar github", "clona"]:
                repo = repo.replace(w, "", 1)
            return self.ac.github_baixar(repo.strip())
        if any(p.startswith(x) for x in ["estuda github", "estuda o repositorio",
                                         "estuda repositorio", "analisa github"]):
            nome = p
            for w in ["estuda o repositorio", "estuda repositorio", "estuda github",
                      "analisa github"]:
                nome = nome.replace(w, "", 1)
            return self.ac.github_estudar(nome.strip())
        if any(x in p for x in ["propoe melhoria", "propõe melhoria", "propor melhoria",
                                "sugere melhoria em voce", "melhore a si mesma"]):
            tema = p
            for w in ["propoe melhoria", "propõe melhoria", "propor melhoria",
                      "sugere melhoria em voce", "melhore a si mesma", "em", "sobre"]:
                tema = tema.replace(w, "", 1)
            return self.ac.propor_melhoria(tema.strip())
        if any(x in p for x in ["forja habilidade", "forjar habilidade", "cria habilidade do estudo",
                                "usa o que estudou", "vira habilidade"]):
            ideia = p
            for w in ["forja habilidade", "forjar habilidade", "cria habilidade do estudo",
                      "usa o que estudou", "vira habilidade", "de", "para"]:
                ideia = ideia.replace(w, "", 1)
            return self.ac.forjar_de_estudo(ideia.strip() or "uma melhoria útil")
        if any(x in p for x in ["projeta uma ia", "blueprint", "ia melhor", "proxima ia",
                                "próxima ia", "projeta sua sucessora", "ia melhor que voce"]):
            obj = p
            for w in ["projeta uma ia melhor que voce", "projeta uma ia", "blueprint",
                      "proxima ia", "próxima ia", "projeta sua sucessora", "ia melhor"]:
                obj = obj.replace(w, "", 1)
            return self.ac.propor_blueprint_ia(obj.strip())

        # ── AUTODIAGNÓSTICO E GUARDIÃ (v12) ──
        if any(x in p for x in ["diagnostico", "diagnóstico", "auto teste", "autoteste",
                                "checa dependencias", "o que falta instalar"]):
            return self.ac.diagnostico()
        if any(x in p for x in ["backups da iris", "versoes da iris", "versões da iris",
                                "suas versoes", "seus backups"]):
            return self.ac.guardia_listar()
        if p.startswith("restaura iris") or p.startswith("restaurar iris"):
            carimbo = p.replace("restaurar iris", "").replace("restaura iris", "").strip()
            msg, pendente = self.ac.guardia_preparar_restauro(carimbo)
            if pendente:
                self._pendente = ("restaurar_iris", pendente)
            return msg

        # ── PARAR DE FALAR (interrupção imediata) ──
        if p in ("para", "pare", "silencio", "silêncio", "cala a boca",
                 "para de falar", "quieta", "shh"):
            if self.voz:
                self.voz.parar()
            return "Ok, parei."

        # ── MODO DITADO (v14) — fale por minutos, ela escreve tudo ──
        if p in ("ditado", "modo ditado", "quero ditar", "vou ditar", "anota o que vou falar"):
            return self.ac.iniciar_ditado()

        # ── ARDUINO DIRETO (v11) — exige firmware universal gravado ──
        if any(x in p for x in ["instala firmware", "instalar firmware", "firmware arduino",
                                "firmware universal"]):
            return self.ac.instalar_firmware()
        if p.startswith("servo") or p.startswith("gira servo") or p.startswith("girar servo"):
            nums = [int(s) for s in re.findall(r"\d+", p)]
            if not nums:
                return "Quantos graus? Ex: servo 90 | servo 45 pino 10"
            graus = nums[0]
            pino = nums[1] if len(nums) > 1 and "pino" in p else 9
            return self.ac.servo(graus, pino)
        if (p.startswith("liga led") or p.startswith("ligar led") or
                p.startswith("acende led") or p.startswith("acender led")):
            nums = [int(s) for s in re.findall(r"\d+", p)]
            return self.ac.led(nums[0] if nums else 13, True)
        if (p.startswith("desliga led") or p.startswith("desligar led") or
                p.startswith("apaga led") or p.startswith("apagar led")):
            nums = [int(s) for s in re.findall(r"\d+", p)]
            return self.ac.led(nums[0] if nums else 13, False)
        if p.startswith("pwm"):
            nums = [int(s) for s in re.findall(r"\d+", p)]
            if len(nums) >= 2:
                return self.ac.pwm(nums[0], nums[1])
            return "Use: pwm [pino] [0-255]. Ex: pwm 5 200"
        if p.startswith("le sensor") or p.startswith("ler sensor") or p.startswith("lê sensor"):
            m = re.search(r"[ad]\s*\d{1,2}", p)
            if m:
                return self.ac.ler_sensor(m.group(0).replace(" ", ""))
            return "Qual sensor? Ex: le sensor a0 | le sensor d7"
        if "ping arduino" in p or p == "ping":
            return self.ac.ping_arduino()

        # ── APAGAR PASTA — sempre pede confirmação (v11) ──
        if any(p.startswith(x) for x in ["apaga pasta", "apagar pasta", "deleta pasta",
                                         "deletar pasta", "remove pasta", "remover pasta"]):
            cam = p
            for w in ["apagar pasta", "apaga pasta", "deletar pasta", "deleta pasta",
                      "remover pasta", "remove pasta"]:
                cam = cam.replace(w, "", 1)
            msg, pendente = self.ac.preparar_apagar_pasta(cam.strip())
            if pendente:
                self._pendente = ("apagar_pasta", pendente)
            return msg

        # ── PLUGINS — habilidades absorvidas (v11) ──
        if any(x in p for x in ["lista plugins", "meus plugins", "plugins instalados"]):
            return self.ac.plugins.listar()
        if any(x in p for x in ["recarrega plugins", "recarregar plugins", "atualiza plugins"]):
            return self.ac.plugins.carregar()
        if p.startswith("cria plugin") or p.startswith("criar plugin") or p.startswith("nova habilidade"):
            desc = p
            for w in ["cria plugin", "criar plugin", "nova habilidade"]:
                desc = desc.replace(w, "", 1)
            if not desc.strip():
                return "O que o plugin deve fazer? Ex: cria plugin que converte celsius em fahrenheit"
            r = self.ac.prog.criar_plugin(desc.strip())
            self.ac.plugins.carregar()  # absorve na hora!
            return r
        # Algum plugin reconhece esse comando?
        r_plugin = self.ac.plugins.tentar(prompt)
        if r_plugin is not None:
            return r_plugin

        # ── LUZ ──
        if any(x in p for x in ["liga luz", "liga a luz", "acende a luz", "acende luz", "ligar luz"]):
            return self.ac.luz(True)
        if any(x in p for x in ["desliga luz", "apaga luz", "desligar luz"]):
            return self.ac.luz(False)

        # ── MODO VIGIA ──
        if any(x in p for x in ["ativa vigia", "modo vigia", "ativa camera", "monitorar camera"]):
            return self.ac.ativar_vigia(True)
        if any(x in p for x in ["desativa vigia", "para vigia", "desliga camera"]):
            return self.ac.ativar_vigia(False)

        # ── ORGANIZAR ──
        if any(x in p for x in ["organiza downloads", "organizar downloads", "organiza arquivos"]):
            return self.ac.organizar_downloads()
        if any(x in p for x in ["organiza area de trabalho", "organizar desktop", "organiza desktop"]):
            return self.ac.organizar_area_trabalho()

        # ── BOT TELEGRAM ──
        if any(x in p for x in ["ativa bot telegram", "iniciar bot", "bot telegram"]):
            return self.ac.iniciar_bot_telegram(self.processar)

        # ── POCO X7 ──
        if any(x in p for x in ["lista arquivos do celular", "arquivos do celular", "ver arquivos celular"]):
            return self.ac.celular_listar_arquivos(
                "/sdcard/Download" if "download" in p else "/sdcard")
        if any(x in p for x in ["apaga downloads do celular", "limpa downloads celular"]):
            return self.ac.celular_apagar_downloads()
        if any(x in p for x in ["apaga fotos antigas", "deleta fotos antigas"]):
            return self.ac.celular_apagar_fotos_antigas()
        if any(x in p for x in ["espaco livre do celular", "espaco no celular"]):
            return self.ac.celular_espaco_livre()
        if any(x in p for x in ["info completa do celular", "informacoes do celular", "info poco"]):
            return self.ac.celular_info_completa()
        if any(x in p for x in ["liga wifi do celular", "ligar wifi celular"]):
            return self.ac.celular_ligar_wifi(True)
        if any(x in p for x in ["desliga wifi do celular", "desligar wifi celular"]):
            return self.ac.celular_ligar_wifi(False)
        if any(x in p for x in ["backup fotos", "faz backup das fotos", "copia fotos do celular"]):
            return self.ac.celular_fazer_backup_fotos()
        if any(x in p for x in ["conecta celular wifi", "reconecta celular", "conecta poco"]):
            return ("Poco X7 reconectado via WiFi!" if self.ac._adb_wifi()
                    else "Não consegui reconectar. Verifique o WiFi.")
        if any(x in p for x in ["status do celular", "como esta o celular", "celular status"]):
            return self.ac.celular_status()
        if any(x in p for x in ["screenshot do celular", "print do celular", "foto da tela do celular"]):
            return self.ac.celular_screenshot()
        if any(x in p for x in ["bateria do celular", "bateria do poco", "quanto tem de bateria"]):
            return self.ac.celular_bateria()
        if any(x in p for x in ["armazenamento do celular", "espaco do celular", "memoria do celular"]):
            return self.ac.celular_armazenamento()
        if any(x in p for x in ["apps do celular", "aplicativos instalados", "lista apps"]):
            return self.ac.celular_apps()
        if any(x in p for x in ["aumenta volume do celular", "volume do celular alto"]):
            return self.ac.celular_volume("aumentar")
        if any(x in p for x in ["diminui volume do celular", "volume do celular baixo"]):
            return self.ac.celular_volume("diminuir")
        if any(x in p for x in ["liga tela do celular", "acende tela"]):
            return self.ac.celular_ligar_tela(True)
        if any(x in p for x in ["desliga tela do celular", "apaga tela"]):
            return self.ac.celular_ligar_tela(False)
        if any(x in p for x in ["notificacoes do celular", "notificações do celular"]):
            return self.ac.celular_notificacoes()
        if any(x in p for x in ["reinicia o celular", "reiniciar celular", "reboot celular"]):
            return self.ac.celular_reiniciar()
        if any(x in p for x in ["limpa cache do celular", "limpar cache celular"]):
            return self.ac.celular_limpar_cache()
        if any(x in p for x in ["desinstala app", "desinstalar app"]):
            app = p
            for w in ["desinstala app", "desinstalar app"]:
                app = app.replace(w, "")
            return self.ac.celular_desinstalar_app(app.strip())
        if any(x in p for x in ["envia arquivo para o celular", "manda arquivo pro celular"]):
            arq = p
            for w in ["envia arquivo para o celular", "manda arquivo pro celular"]:
                arq = arq.replace(w, "")
            return self.ac.celular_enviar_arquivo(arq.strip())

        # ── AGENTE VISUAL (v21) — vê a tela e age, estilo Claw ──
        if any(p.startswith(x) for x in ["agente visual", "controla a tela", "faz na tela",
                                          "age na tela", "automatiza"]):
            obj = p
            for w in ["agente visual", "controla a tela", "faz na tela", "age na tela", "automatiza"]:
                obj = obj.replace(w, "", 1)
            obj = obj.strip()
            if not obj:
                return ("O que você quer que eu faça na tela? Ex: 'agente visual abre o "
                        "navegador e pesquisa receita de bolo'. IMPORTANTE: vou agir no "
                        "mouse/teclado de verdade. Jogue o mouse pro CANTO da tela a "
                        "qualquer momento para me parar (freio de emergência).")
            # confirmação simples: registra o objetivo como pendente
            self._pendente = ("agente_visual", obj)
            return ("AGENTE VISUAL — vou tentar: '" + obj + "'\n"
                    "Vou olhar a tela, decidir e agir no mouse/teclado SOZINHA, em até 6 passos.\n"
                    "FREIO DE EMERGÊNCIA: jogue o mouse para o canto superior-esquerdo a "
                    "qualquer momento que eu paro na hora.\n"
                    "Responda 'sim' para eu começar, ou qualquer coisa para cancelar.")

        # ── AGENTE AUTÔNOMO ──
        if any(x in p for x in ["executa objetivo", "faz autonomo", "age sozinho", "executa tarefa"]):
            obj = p
            for w in ["executa objetivo", "faz autonomo", "age sozinho", "executa tarefa"]:
                obj = obj.replace(w, "")
            return self.ac.agente_executar(obj.strip() or "otimizar o sistema")
        if p.startswith("monitora") or any(x in p for x in ["quando cpu", "quando ram"]):
            partes = p.split("otimiza") if "otimiza" in p else p.split("faz")
            cond = partes[0].replace("monitora", "").strip()
            acao = ("otimiza " + partes[1]).strip() if len(partes) > 1 else "status"
            return self.ac.agente_monitorar(cond, acao, intervalo=30)
        if any(x in p for x in ["rotina matinal", "rotina diaria", "cria rotina"]):
            return self.ac.agente_rotina("Matinal", ["status", "clima", "resumo do dia"])
        if any(x in p for x in ["rotina noturna", "rotina da noite"]):
            return self.ac.agente_rotina("Noturna",
                                         ["otimiza sistema", "organiza downloads", "ver notas"])

        # ── MODO PROJETO — IRIS coordenadora (v10) ──
        if any(x in p for x in ["meus projetos", "lista projetos", "listar projetos",
                                "quais projetos"]):
            return self.ac.proj.listar()
        if p.startswith("registra projeto") or p.startswith("registrar projeto"):
            resto = p.replace("registrar projeto", "").replace("registra projeto", "").strip()
            if ":" in resto:
                nome, desc = resto.split(":", 1)
            else:
                nome, desc = resto, ""
            return self.ac.proj.registrar(nome, desc)
        if (p.startswith("projeto ") or p.startswith("ativa projeto") or
                p.startswith("modo projeto") or p.startswith("abre projeto")):
            nome = p
            for w in ["ativa projeto", "modo projeto", "abre projeto", "projeto"]:
                nome = nome.replace(w, "", 1)
            return self.ac.proj.ativar(nome.strip())
        if any(x in p for x in ["sai do projeto", "sair do projeto", "fecha projeto",
                                "desativa projeto"]):
            return self.ac.proj.desativar()
        if p.startswith("tarefa ") or p.startswith("nova tarefa") or p.startswith("adiciona tarefa"):
            txt = p
            for w in ["adiciona tarefa", "nova tarefa", "tarefa"]:
                txt = txt.replace(w, "", 1)
            return self.ac.proj.add_tarefa(txt.strip())
        if p in ("tarefas", "minhas tarefas", "pendencias", "pendências", "lista tarefas"):
            return self.ac.proj.listar_tarefas()
        if p.startswith("conclui tarefa") or p.startswith("concluir tarefa") or p.startswith("feito tarefa"):
            nums = [s for s in p.split() if s.isdigit()]
            return (self.ac.proj.concluir(nums[0]) if nums
                    else "Qual número? Ex: conclui tarefa 2")
        if p.startswith("diario ") or p.startswith("diário ") or p.startswith("registra progresso"):
            txt = p
            for w in ["registra progresso", "diario", "diário"]:
                txt = txt.replace(w, "", 1)
            return self.ac.proj.diario(txt.strip())
        if any(x in p for x in ["ver diario", "ver diário", "diario do projeto", "progresso do projeto"]):
            return self.ac.proj.ver_diario()
        if any(x in p for x in ["relatorio do projeto", "relatório do projeto",
                                "relatorio projeto", "relatorio"]) and "rede" not in p:
            return self.ac.relatorio_projeto()
        if any(x in p for x in ["proximo passo", "próximo passo", "o que fazer agora",
                                "por onde continuo"]):
            return self.ac.proximo_passo()
        if p.startswith("backup projeto") or p.startswith("compacta projeto") or p.startswith("backup da pasta"):
            arq = p
            for w in ["compacta projeto", "backup projeto", "backup da pasta"]:
                arq = arq.replace(w, "", 1)
            return self.ac.backup_projeto(arq.strip())

        # ── ESPONTANEIDADE E HUMOR (v19) ──
        if any(x in p for x in ["modo espontaneo", "modo espontâneo", "seja espontanea",
                                "tenha iniciativa", "fala sozinha"]):
            return self.ac.status_espontaneo(True)
        if any(x in p for x in ["desliga espontaneo", "desativa espontaneo",
                                "fica quieta", "so fala quando chamar"]):
            return self.ac.status_espontaneo(False)
        if any(x in p for x in ["como voce esta hoje", "qual seu humor", "como se sente",
                                "como voce ta", "como você está"]):
            return ("Hoje estou me sentindo " + self.ac.humor_atual() +
                    "! E você, Francisco, como está?")

        # ── APRENDIZADO E AUTOVERIFICAÇÃO (v18) ──
        if p.startswith("aprende que") or p.startswith("aprenda que") or p.startswith("lembre que") or p.startswith("nunca esqueca"):
            fato = p
            for w in ["aprende que", "aprenda que", "lembre que", "nunca esqueca"]:
                fato = fato.replace(w, "", 1)
            return self.ac.aprender(fato.strip())
        if any(x in p for x in ["o que voce sabe", "o que você sabe", "o que aprendeu",
                                "o que voce aprendeu", "seu conhecimento"]):
            busca = p
            for w in ["o que voce sabe sobre", "o que você sabe sobre", "o que voce sabe",
                      "o que você sabe", "o que aprendeu sobre", "o que aprendeu",
                      "seu conhecimento"]:
                busca = busca.replace(w, "", 1)
            return self.ac.o_que_sei(busca.strip())
        if any(x in p for x in ["autoverifica", "autoverificacao", "verifica voce mesma",
                                "voce esta inteira", "voce esta bem", "checa voce",
                                "esta tudo certo com voce"]):
            return self.ac.autoverificar()

        # ── PROTEÇÃO DE DISPOSITIVOS (v17) — guarda-costas ──
        if any(x in p for x in ["acha meu celular", "achar celular", "perdi o celular",
                                "cade meu celular", "cadê meu celular", "localiza celular",
                                "encontrar celular"]):
            return self.ac.achar_celular()
        if any(x in p for x in ["faz o celular tocar", "toca o celular", "celular tocar",
                                "faz tocar"]):
            return self.ac.tocar_celular()
        if any(x in p for x in ["cofre", "backup de emergencia", "guarda minhas coisas",
                                "salva minhas coisas"]):
            return self.ac.cofre_emergencia()
        if any(x in p for x in ["modo panico", "modo pânico", "panico", "pânico",
                                "roubaram meu celular", "perdi tudo"]):
            return self.ac.modo_panico()
        if any(x in p for x in ["ativa guarda costas", "vigia dispositivos",
                                "protege meus aparelhos", "ativa protecao"]):
            return self.ac.vigia_dispositivos(True)
        if any(x in p for x in ["desativa guarda costas", "para de vigiar dispositivos"]):
            return self.ac.vigia_dispositivos(False)

        # ── CENTRAL DE DISPOSITIVOS (v10) ──
        if any(x in p for x in ["dispositivos", "central de dispositivos", "status geral",
                                "como estao meus aparelhos", "meus aparelhos"]):
            return self.ac.dispositivos()

        # ── PROGRAMADORA (v9.0) ──
        if p.startswith("cria projeto") or p.startswith("criar projeto") or p.startswith("novo projeto"):
            nome = p
            for w in ["cria projeto", "criar projeto", "novo projeto"]:
                nome = nome.replace(w, "")
            return self.ac.prog.criar_projeto(nome.strip() or "projeto")
        if (p.startswith("programa") or p.startswith("programe") or
                p.startswith("escreve um programa") or p.startswith("cria um programa")) \
                and "arduino" not in p:
            desc = p
            for w in ["escreve um programa", "cria um programa", "programa", "programe",
                      "que", "para", "pra"]:
                desc = desc.replace(w, "", 1)
            return self.ac.prog.programar(desc.strip() or "olá mundo")
        if p.startswith("executa codigo") or p.startswith("roda o programa") or p.startswith("roda programa"):
            arq = p
            for w in ["executa codigo", "roda o programa", "roda programa"]:
                arq = arq.replace(w, "")
            return self.ac.prog.executar(arq.strip())
        if p.startswith("corrige") and (".py" in p or "programa" in p or "codigo" in p):
            arq = p
            for w in ["corrige o codigo", "corrige codigo", "corrige o programa", "corrige"]:
                arq = arq.replace(w, "")
            return self.ac.prog.corrigir(arq.strip())
        if p.startswith("compacta") or p.startswith("minifica") or p.startswith("comprime"):
            arq = p
            for w in ["compacta o codigo", "compacta codigo", "compacta",
                      "minifica", "comprime o arquivo", "comprime"]:
                arq = arq.replace(w, "")
            arq = arq.strip()
            if not arq and self.ac.prog.ultimo_arquivo:
                arq = self.ac.prog.ultimo_arquivo
            if not arq:
                return "Qual arquivo? Ex: compacta meucodigo.py"
            return self.ac.prog.compactar(arq)
        if any(x in p for x in ["lista programas", "meus programas", "programas criados"]):
            return self.ac.prog.listar_programas()

        # ── CÉREBRO LOCAL (v9.0) ──
        if any(x in p for x in ["cerebro local", "cérebro local", "inteligencia local",
                                "inteligência local", "modo offline"]):
            return self.ac.cerebro.status()

        # ── NEURÔNIOS TERNÁRIOS — Projeto NTM (v9.0) ──
        if any(x in p for x in ["simula neuronios", "simular neuronios", "simula neurônios",
                                "rede spiking", "neuronios disparando"]):
            nums = [int(s) for s in p.split() if s.isdigit()]
            n = nums[0] if nums else 8
            return self.ac.rede.simular_spiking(n)
        if p.startswith("treina rede") or p.startswith("treinar rede") or p.startswith("memoriza padrao"):
            padrao = p
            for w in ["treina rede", "treinar rede", "memoriza padrao"]:
                padrao = padrao.replace(w, "")
            return self.ac.rede.treinar(padrao.strip())
        if p.startswith("lembra padrao") or p.startswith("lembrar padrao") or p.startswith("recupera padrao"):
            padrao = p
            for w in ["lembra padrao", "lembrar padrao", "recupera padrao"]:
                padrao = padrao.replace(w, "")
            return self.ac.rede.lembrar(padrao.strip())
        if any(x in p for x in ["status da rede", "rede neural", "rede neuronal", "memoria da rede"]):
            return self.ac.rede.status()
        if any(x in p for x in ["esquece a rede", "zera a rede", "limpa a rede"]):
            return self.ac.rede.esquecer()

        # ── CALCULADORA LOCAL (v9.0) ──
        if p.startswith("calcula") or p.startswith("quanto e ") or p.startswith("quanto é "):
            expr = p
            for w in ["calcula", "quanto e", "quanto é"]:
                expr = expr.replace(w, "")
            expr = expr.strip().replace("x", "*").replace("^", "**").replace(",", ".")
            if expr and re.fullmatch(r"[0-9+\-*/(). %eE]+|[a-z]+\([0-9+\-*/(). ]+\)[0-9+\-*/(). ]*", expr):
                try:
                    seguro = {"sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
                              "tan": math.tan, "log": math.log, "pi": math.pi, "e": math.e}
                    return expr + " = " + str(eval(expr, {"__builtins__": {}}, seguro))
                except Exception as e:
                    return "Não consegui calcular: " + str(e)
            return "Me dá uma conta válida! Ex: calcula (15*8)+sqrt(144)"

        # ── ARDUINO REAL (v9.0) ──
        if any(x in p for x in ["portas serial", "portas seriais", "lista portas"]):
            return self.ac.portas_serial()
        if any(x in p for x in ["monitor serial", "le a serial", "lê a serial", "serial monitor"]):
            nums = [int(s) for s in p.split() if s.isdigit()]
            return self.ac.monitor_serial(nums[0] if nums else 5)
        if p.startswith("compila arduino") or p.startswith("compilar arduino"):
            arq = p.replace("compilar arduino", "").replace("compila arduino", "").strip()
            return self.ac.arduino_compilar(arq) if arq else "Qual .ino? Ex: compila arduino blink.ino"
        if any(x in p for x in ["grava arduino", "grava no arduino", "upload arduino", "envia pro arduino"]):
            arq = p
            for w in ["grava no arduino", "grava arduino", "upload arduino", "envia pro arduino"]:
                arq = arq.replace(w, "")
            arq = arq.strip()
            return self.ac.arduino_gravar(arq) if arq else "Qual .ino? Ex: grava arduino blink.ino"
        if p.startswith("arduino "):
            return self.ac.arduino_enviar(prompt.strip()[8:])

        # ── SISTEMA ──
        if any(x in p for x in ["status", "como esta o sistema"]) or p in ("cpu", "ram", "memoria"):
            return self.ac.status(self.mon)
        if any(x in p for x in ["otimiza", "limpa sistema", "deixa rapido"]):
            return self.ac.otimizar()
        if any(x in p for x in ["processos", "o que ta pesando"]):
            return self.ac.processos(self.mon)
        if any(x in p for x in ["screenshot", "print da tela", "captura de tela"]) and "celular" not in p:
            return self.ac.screenshot()
        if any(x in p for x in ["aumenta volume", "volume alto", "volume mais alto", "volume up"]):
            return self.ac.volume("up")
        if any(x in p for x in ["diminui volume", "volume baixo", "volume mais baixo", "volume down"]):
            return self.ac.volume("down")
        if any(x in p for x in ["silencia", "mudo", "sem som", "volume mudo"]):
            return self.ac.volume("mudo")

        # ── MOUSE E TECLADO ──
        if any(x in p for x in ["move o mouse", "mover mouse", "mouse para"]):
            nums = [s for s in p.split() if s.isdigit()]
            if len(nums) >= 2:
                return self.ac.mover_mouse(int(nums[0]), int(nums[1]))
            return "Diga as coordenadas: 'move o mouse 500 300'"
        if any(x in p for x in ["clica", "clique aqui", "clicar"]):
            return self.ac.clicar("duplo" in p)
        if p.startswith("digita") or p.startswith("escreve"):
            txt = p
            for w in ["digita", "escreve"]:
                txt = txt.replace(w, "", 1)
            return self.ac.digitar(txt.strip())
        if any(x in p for x in ["pressiona tecla", "aperta tecla"]):
            txt = p
            for w in ["pressiona tecla", "aperta tecla"]:
                txt = txt.replace(w, "")
            return self.ac.tecla(txt.strip() or "enter")
        if "posicao do mouse" in p or "onde esta o mouse" in p:
            return self.ac.posicao_mouse()

        # ── MULTIMODAL ──
        if any(x in p for x in ["o que tem na tela", "analisa a tela", "veja a tela",
                                "o que esta na tela"]):
            return self.ac.analisar_tela()
        if p.startswith("analisa imagem") or p.startswith("analise a imagem") or p.startswith("ve a imagem"):
            arq = p
            for w in ["analisa imagem", "analise a imagem", "ve a imagem"]:
                arq = arq.replace(w, "")
            return self.ac.analisar_imagem(arq.strip())
        if any(x in p for x in ["o que voce ve", "o que você vê", "olha pela webcam",
                                "olha pra mim", "me ve"]):
            return self.ac.ver_pela_webcam()
        if p.startswith("leia ") or p.startswith("le o arquivo") or p.startswith("resume o arquivo"):
            arq = p
            for w in ["leia", "le o arquivo", "resume o arquivo"]:
                arq = arq.replace(w, "", 1)
            return self.ac.ler_arquivo(arq.strip())

        # ── JANELAS ──
        if any(x in p for x in ["lista janelas", "janelas abertas"]):
            return self.ac.listar_janelas()
        if any(x in p for x in ["minimiza tudo", "mostra desktop"]):
            return self.ac.minimizar_tudo()
        if p.startswith("foca") or "focar na janela" in p:
            nome = p
            for w in ["focar", "foca", "na janela"]:
                nome = nome.replace(w, "")
            return self.ac.focar_janela(nome.strip())

        # ── PROGRAMAS ──
        if any(x in p for x in ["abre", "abrir", "inicia"]):
            for prog in self.ac.PROGS:
                if prog in p:
                    return self.ac.abrir_programa(prog)

        # ── SITES ──
        if any(x in p for x in ["pesquisa no google", "google "]):
            q = p
            for w in ["pesquisa no google", "google", "pesquisa"]:
                q = q.replace(w, "")
            return self.ac.google(q.strip())
        if "youtube" in p:
            q = p
            for w in ["pesquisa no youtube", "youtube"]:
                q = q.replace(w, "")
            return self.ac.youtube(q.strip())
        if any(x in p for x in ["abre o site", "vai para", "acessa o site"]):
            site = p
            for w in ["abre o site", "vai para", "acessa o site"]:
                site = site.replace(w, "")
            return self.ac.abrir_site(site.strip())

        # ── ARQUIVOS ──
        if any(x in p for x in ["apaga imagens", "apaga prints"]):
            return self.ac.apagar_imagens()
        if any(x in p for x in ["lista arquivos", "ver arquivos"]):
            return self.ac.listar_arquivos()
        if "cria arquivo" in p or "criar arquivo" in p:
            nome = p.replace("cria arquivo", "").replace("criar arquivo", "").strip()
            return self.ac.criar_arquivo(nome or "novo.txt")

        # ── MÚSICA ──
        if p == "play" or p == "toca musica":
            return self.ac.musica("play")
        if p == "pause" or p == "pausa":
            return self.ac.musica("pause")
        if "proxima musica" in p:
            return self.ac.musica("proxima")
        if "anterior musica" in p or "musica anterior" in p:
            return self.ac.musica("anterior")
        if "para musica" in p:
            return self.ac.musica("parar")

        # ── WEBCAM ──
        if any(x in p for x in ["tira foto", "foto webcam", "selfie"]):
            return self.ac.foto_webcam()

        # ── TRADUÇÃO ──
        if p.startswith("traduz"):
            txt = p
            destino = "es" if "espanhol" in p else "fr" if "frances" in p else "en"
            for w in ["traduzir", "traduz", "para ingles", "para espanhol", "para frances"]:
                txt = txt.replace(w, "")
            return self.ac.traduzir(txt.strip(), destino)

        # ── REDE ──
        if any(x in p for x in ["monitorar rede", "ver rede", "quem esta na rede"]):
            return self.ac.monitorar_rede()
        if any(x in p for x in ["testa internet", "velocidade internet", "como esta a internet"]):
            return self.ac.testar_internet()

        # ── CLIMA ──
        if any(x in p for x in ["clima", "previsao", "vai chover"]):
            return self.ac.clima()

        # ── TELEGRAM ──
        if "telegram" in p and any(x in p for x in ["envia", "manda"]):
            msg = p
            for w in ["envia", "manda", "telegram", "mensagem", "no", "pro"]:
                msg = msg.replace(w, "")
            return self.ac.telegram(msg.strip())

        # ── BUSCA ── (BUG da v7 corrigido: o if estava colado no comentário)
        if any(x in p for x in ["pesquisa", "busca na internet", "procura"]):
            q = p
            for w in ["busca na internet", "pesquisa", "procura", "sobre", "na internet"]:
                q = q.replace(w, "")
            return self.ac.buscar(q.strip())

        # ── ARDUINO ──
        if any(x in p for x in ["codigo arduino", "sketch arduino", "programa arduino"]):
            desc = p
            for w in ["codigo arduino", "sketch arduino", "programa arduino", "faz", "cria"]:
                desc = desc.replace(w, "")
            return self.ac.gerar_codigo_arduino(desc.strip() or "piscar LED no pino 13")

        # ── NOTAS E LEMBRETES ──
        if any(x in p for x in ["salva nota", "anotar", "anota"]):
            txt = p
            for w in ["salva nota", "anotar", "anota"]:
                txt = txt.replace(w, "")
            self.mem.salvar_nota(txt.strip())
            return "Nota salva!"
        if any(x in p for x in ["ver notas", "minhas notas"]):
            return self.mem.ver_notas()
        if "lembrete as" in p or "lembrete às" in p:
            try:
                resto = p.replace("lembrete às", "lembrete as").replace("lembrete as", "").strip()
                partes = resto.split(" ", 1)
                hora_str = partes[0]
                texto = partes[1] if len(partes) > 1 else "Lembrete!"
                return self.ac.adicionar_lembrete(texto, hora_str=hora_str)
            except Exception:
                return "Use: lembrete as 14:30 [texto]"
        if any(x in p for x in ["lembrete", "me lembra"]):
            txt = p
            for w in ["lembrete", "me lembra", "me lembre"]:
                txt = txt.replace(w, "")
            return self.ac.adicionar_lembrete(txt.strip() or "Lembrete!")

        # ── RESUMO / FOCO / GRÁFICO / HISTÓRICO / AUTO-MELHORIA ──
        if any(x in p for x in ["resumo do dia", "resumo diario", "como esta tudo"]):
            return self.ac.resumo_diario(self.mon)
        if any(x in p for x in ["modo foco", "ativa foco", "bloqueia sites"]):
            return self.ac.modo_foco(True)
        if any(x in p for x in ["desativa foco", "desbloqueia sites"]):
            return self.ac.modo_foco(False)
        if any(x in p for x in ["grafico cpu", "grafico de cpu"]):
            return self.ac.grafico_cpu(self.mon)
        if any(x in p for x in ["ver historico", "conversas anteriores", "historico"]):
            return self.mem.ver_historico()
        if any(x in p for x in ["melhora seu codigo", "analisa seu codigo", "auto melhora"]):
            return self.ac.analisar_codigo(os.path.abspath(__file__))

        # ── LINUX DIRETO ──
        if prompt.startswith("$ "):
            resultado = subprocess.getoutput(prompt[2:])
            self.ac._reg("Executou: " + prompt[2:])
            return "$ " + prompt[2:] + "\n" + resultado[:400]

        # ── AJUDA ──
        if any(x in p for x in ["ajuda", "comandos", "o que voce faz", "o que você faz"]):
            return ("IRIS v1.7 — Comandos:\n" + self.LISTA_COMANDOS +
                    "\n$ [comando linux]\nF2=voz | F3=histórico | F4=conversa contínua"
                    "\nDiga 'para' para eu calar a boca :)"
                    "\nOu fale livremente comigo — eu entendo linguagem natural!")

        # ── INTERPRETADOR IA (fluidez Jarvis) — MUITO mais esperto agora ──
        # Antes de tratar como conversa, verifica se é um PEDIDO DE AÇÃO.
        # Cobre muito mais que uma lista de verbos: pega pedidos naturais.
        verbos_acao = [
            "abra", "abre", "abrir", "liga", "ligar", "desliga", "desligar",
            "mostra", "mostrar", "manda", "mandar", "envia", "enviar", "tira",
            "tirar", "faz", "fazer", "faça", "executa", "executar", "toca", "tocar",
            "coloca", "colocar", "aumenta", "diminui", "limpa", "limpar", "organiza",
            "verifica", "verificar", "checa", "checar", "olha", "olhar", "anota",
            "anotar", "marca", "marcar", "registra", "agenda", "conclui", "termina",
            "salva", "salvar", "cria", "criar", "compacta", "compila", "grava",
            "conecta", "conectar", "ativa", "ativar", "desativa", "acha", "achar",
            "ache", "encontra", "encontrar", "localiza", "localizar", "procura",
            "procurar", "busca", "buscar", "pega", "pegar", "roda", "rodar",
            "testa", "testar", "controla", "controlar", "analisa", "analisar",
            "traduz", "traduzir", "calcula", "calcular", "apaga", "apagar",
            "instala", "instalar", "monitora", "monitorar", "programa", "programar",
            "apaga", "apagar", "deleta", "deletar", "cria pasta", "criar pasta", "move", "mover", "renomeia",
            "quero que", "preciso que", "pode", "consegue", "me ajuda", "me ajude",
            "vê se", "ve se", "dá uma", "da uma"]
        parece_acao = any(x in p for x in verbos_acao)
        # também dispara se mencionar um "alvo" típico de ação
        alvos = ["celular", "poco", "arduino", "servo", "led", "tela", "arquivo",
                 "pasta", "programa", "site", "musica", "música", "volume", "foto",
                 "screenshot", "projeto", "tarefa", "plugin", "rede", "sensor", "pc", "sistema", "cpu", "ram", "bateria", "internet", "wifi", "clima"]
        if not parece_acao and any(a in p for a in alvos):
            parece_acao = True
        if parece_acao:
            cmd = self.ia.interpretar_comando(prompt, self.LISTA_COMANDOS)
            if cmd and cmd.lower().strip() != p:
                logging.info("Interpretador: '%s' -> '%s'", prompt, cmd)
                return self.processar(cmd)

        # ── IA — conversa livre (com contexto de projeto + fallback local) ──
        complexo = any(x in p for x in [
            "explica", "como fazer", "projeto", "livro", "exoesqueleto",
            "arduino", "fpga", "ntm", "me ajuda com", "como funciona", "o que e"])
        # Se há projeto ativo, a IA recebe o contexto dele junto
        ctx = self.ac.proj.contexto()
        # v18: injeta o que ela aprendeu; v19: injeta o humor do momento
        aprendido = self.ac.contexto_aprendizado()
        humor = self.ac.tempero_humor()
        extras = "\n".join(x for x in [aprendido, ctx, humor] if x)
        prompt_ia = (extras + "\n\n" + prompt) if extras else prompt
        resposta = (self.ia.dois_cerebros(prompt_ia) if complexo
                    else self.ia.groq_rapido(prompt_ia))
        # Sem internet ou sem chave? O cérebro local assume!
        if (not resposta or str(resposta).startswith("Erro")
                or "sem chave" in str(resposta).lower()):
            local = self.ac.cerebro.responder(prompt, self.ia.sistema)
            if local:
                resposta = local + ("\n(cérebro local)" if self.ac.cerebro.disponivel() else "")
        self.ia.salvar_historico(prompt, resposta)
        return resposta

# ══════════════════════════════════════════════════════════════
#  INTERFACE 3D — esfera estilo Jarvis
# ══════════════════════════════════════════════════════════════
class Esfera3D:
    def __init__(self, esf_w, esf_h):
        self.ESF_W = esf_w
        self.ESF_H = esf_h
        self.tick = 0.0
        self.rot_y = 0.0
        self.raio_base = 1.1
        self.raio_atual = 1.1
        self.raio_alvo = 1.1
        self.ondas = []
        self.barras = [0.1] * 32
        self.barras_alvo = [0.1] * 32
        self.aneis = [
            {"incl": 0,   "rot": 0,   "vel": 1.0,  "raio": 1.60, "esp": 2, "seg": 4},
            {"incl": 70,  "rot": 60,  "vel": -0.8, "raio": 1.75, "esp": 1, "seg": 6},
            {"incl": -50, "rot": 180, "vel": 1.3,  "raio": 1.55, "esp": 1, "seg": 3},
            {"incl": 90,  "rot": 45,  "vel": -0.6, "raio": 1.85, "esp": 1, "seg": 5},
        ]
        self.particulas = [
            {"theta": random.uniform(0, math.pi*2), "phi": random.uniform(0, math.pi),
             "dist": random.uniform(1.8, 3.2), "vt": random.uniform(-0.006, 0.006),
             "vp": random.uniform(-0.004, 0.004), "b": random.uniform(0.5, 1.0)}
            for _ in range(60)
        ]
        # Cores por estado: azul=idle, dourado=pensando, verde=falando, vermelho=ouvindo
        self.CORES = {
            "idle":     (0.0, 0.75, 1.0),
            "pensando": (1.0, 0.78, 0.1),
            "falando":  (0.1, 0.95, 0.5),
            "ouvindo":  (1.0, 0.35, 0.35),
        }
        self.cor_atual = list(self.CORES["idle"])

    def atualizar(self, estado):
        self.tick += 0.035
        vel_rot = 3.0 if estado == "falando" else 1.5 if estado == "pensando" else 0.5
        self.rot_y += vel_rot
        if estado == "falando":
            self.raio_alvo = self.raio_base + math.sin(self.tick*6)*0.18
            if int(self.tick*28) % 8 == 0:
                self.ondas.append({"r": self.raio_atual, "a": 0.8, "v": 0.04})
        elif estado == "pensando":
            self.raio_alvo = self.raio_base + math.sin(self.tick*2)*0.06
        else:
            self.raio_alvo = self.raio_base + math.sin(self.tick)*0.03
        self.raio_atual += (self.raio_alvo - self.raio_atual)*0.1
        self.ondas = [{**o, "r": o["r"]+o["v"], "a": o["a"]-0.02}
                      for o in self.ondas if o["a"] > 0]
        for i in range(32):
            if estado == "falando":
                self.barras_alvo[i] = random.uniform(0.3, 1.0)
            elif estado == "pensando":
                self.barras_alvo[i] = random.uniform(0.1, 0.4)
            else:
                self.barras_alvo[i] = random.uniform(0.03, 0.12)
            self.barras[i] += (self.barras_alvo[i]-self.barras[i])*0.2
        vel_p = 3.0 if estado == "falando" else 1.5 if estado == "pensando" else 0.4
        for p in self.particulas:
            p["theta"] += p["vt"]*vel_p
            p["phi"] += p["vp"]*vel_p
        vel_a = 4.0 if estado == "falando" else 2.0 if estado == "pensando" else 0.7
        for a in self.aneis:
            a["rot"] += a["vel"]*vel_a
        # Transição suave de cor por estado
        alvo = self.CORES.get(estado, self.CORES["idle"])
        for i in range(3):
            self.cor_atual[i] += (alvo[i] - self.cor_atual[i]) * 0.08

    def desenhar(self, W, H):
        glViewport(0, H-self.ESF_H, self.ESF_W, self.ESF_H)
        glMatrixMode(GL_PROJECTION); glLoadIdentity()
        gluPerspective(45, self.ESF_W/self.ESF_H, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW); glLoadIdentity()
        gluLookAt(0, 0, 6, 0, 0, 0, 0, 1, 0)
        glScissor(0, H-self.ESF_H, self.ESF_W, self.ESF_H)
        glEnable(GL_SCISSOR_TEST)
        glClearColor(0.02, 0.03, 0.07, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDisable(GL_SCISSOR_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        r, g, b = self.cor_atual
        glPushMatrix()
        glRotatef(15, 1, 0, 0); glRotatef(self.rot_y, 0, 1, 0)
        # Glow interno
        glColor4f(r, g, b, 0.05)
        q = gluNewQuadric(); gluQuadricDrawStyle(q, GLU_FILL)
        gluSphere(q, self.raio_atual*0.88, 32, 32); gluDeleteQuadric(q)
        # Wireframe
        glLineWidth(1.2); glColor4f(r, g, b, 0.6)
        q = gluNewQuadric(); gluQuadricDrawStyle(q, GLU_LINE)
        gluSphere(q, self.raio_atual, 24, 24); gluDeleteQuadric(q)
        # Anéis
        for anel in self.aneis:
            glPushMatrix()
            glRotatef(anel["incl"], 1, 0, 0); glRotatef(anel["rot"], 0, 1, 0)
            raio = anel["raio"]*(self.raio_atual/self.raio_base)
            glLineWidth(float(anel["esp"]))
            glBegin(GL_LINE_LOOP)
            for i in range(120):
                a = (i/120)*math.pi*2
                glColor4f(r, g, b, (0.5+0.5*math.sin(a*anel["seg"]+self.tick*3))*0.85)
                glVertex3f(raio*math.cos(a), 0, raio*math.sin(a))
            glEnd()
            glPointSize(4.0); glBegin(GL_POINTS)
            for i in range(anel["seg"]*2):
                a = (i/(anel["seg"]*2))*math.pi*2
                glColor4f(r, g, b, 1.0)
                glVertex3f(raio*math.cos(a), 0, raio*math.sin(a))
            glEnd(); glPopMatrix()
        # Partículas
        glPointSize(3.0); glBegin(GL_POINTS)
        for p in self.particulas:
            d = p["dist"]*(self.raio_atual/self.raio_base)
            x = d*math.sin(p["phi"])*math.cos(p["theta"])
            y = d*math.cos(p["phi"])
            z = d*math.sin(p["phi"])*math.sin(p["theta"])
            glColor4f(r, g, b, p["b"]*(0.5+0.5*math.sin(self.tick+p["theta"])))
            glVertex3f(x, y, z)
        glEnd(); glPopMatrix()
        # Barras de frequência
        rb = self.raio_atual*1.5; glLineWidth(2.5)
        for i in range(32):
            a = (i/32)*math.pi*2
            alt = self.barras[i]*0.45
            glBegin(GL_LINES)
            glColor4f(r, g, b, 0.9)
            glVertex3f(rb*math.cos(a), rb*math.sin(a), 0)
            glColor4f(r, g, b, 0.0)
            glVertex3f((rb+alt)*math.cos(a), (rb+alt)*math.sin(a), 0)
            glEnd()
        # Ondas
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        for o in self.ondas:
            glColor4f(r, g, b, o["a"]*0.5)
            q = gluNewQuadric(); gluQuadricDrawStyle(q, GLU_LINE)
            gluSphere(q, o["r"], 16, 16); gluDeleteQuadric(q)

# ══════════════════════════════════════════════════════════════
#  INTERFACE 2D — Painel + Chat
# ══════════════════════════════════════════════════════════════
class Painel2D:
    def __init__(self, W, H, ESF_W, ESF_H, SYS_X, SYS_W, usuario):
        self.W = W; self.H = H
        self.ESF_W = ESF_W; self.ESF_H = ESF_H
        self.SYS_X = SYS_X; self.SYS_W = SYS_W
        self.usuario = usuario
        self._tex_id = None
        # Cores
        self.C_CIANO   = (0, 200, 245)
        self.C_BRANCO  = (255, 255, 255)
        self.C_CINZA   = (130, 150, 170)
        self.C_VERDE   = (0, 230, 120)
        self.C_AMARELO = (255, 215, 0)
        self.C_VERM    = (255, 75, 75)
        self.C_IRIS    = (255, 255, 255)
        self.C_USER    = (255, 255, 255)
        # Fontes
        self.fnt_chat  = pygame.font.SysFont("monospace", 17, bold=True)
        self.fnt_input = pygame.font.SysFont("monospace", 17, bold=True)
        self.fnt_title = pygame.font.SysFont("monospace", 16, bold=True)
        self.fnt_mini  = pygame.font.SysFont("monospace", 13)
        self.fnt_sys   = pygame.font.SysFont("monospace", 13, bold=True)
        self.fnt_valor = pygame.font.SysFont("monospace", 22, bold=True)

    def _barra(self, surf, x, y, w, h, valor, cor):
        pygame.draw.rect(surf, (15, 25, 40), (x, y, w, h), border_radius=3)
        fill = max(1, int(w*min(valor, 100)/100))
        pygame.draw.rect(surf, cor, (x, y, fill, h), border_radius=3)
        pct = self.fnt_mini.render(str(round(valor))+"%", True, (160, 185, 210))
        surf.blit(pct, (x+w+5, y-2))

    def _grafico(self, surf, x, y, w, h, dados, cor):
        pygame.draw.rect(surf, (10, 18, 30), (x, y, w, h), border_radius=4)
        pygame.draw.rect(surf, (*cor, 60), (x, y, w, h), 1, border_radius=4)
        pts = dados[-w:]
        for i, v in enumerate(pts):
            bh = max(1, int((v/100)*h))
            pygame.draw.rect(surf, (*cor, int(80+175*(v/100))), (x+i, y+h-bh, 2, bh))
        if len(pts) > 1:
            media = sum(pts)/len(pts)
            my = y+h-int((media/100)*h)
            pygame.draw.line(surf, (*cor, 100), (x, my), (x+len(pts), my), 1)

    def desenhar(self, surf, mon, mensagens, input_texto, estado, ouvindo,
                 ultima_acao, poco_data=None):
        sx = self.SYS_X; sw = self.SYS_W; sy = 4
        # ══ PAINEL SISTEMA ══
        pygame.draw.rect(surf, (6, 10, 22, 252), (sx, sy, sw, self.ESF_H-8), border_radius=12)
        pygame.draw.rect(surf, (*self.C_CIANO, 100), (sx, sy, sw, self.ESF_H-8), 1, border_radius=12)
        pygame.draw.rect(surf, (0, 18, 36, 255), (sx, sy, sw, 30), border_radius=12)
        surf.blit(self.fnt_title.render("SISTEMA EM TEMPO REAL", True, self.C_CIANO), (sx+10, sy+8))
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except Exception:
            ip = "127.0.0.1"
        h2 = self.fnt_mini.render(ip, True, (130, 155, 180))
        surf.blit(h2, (sx+sw-h2.get_width()-8, sy+10))
        pygame.draw.line(surf, (*self.C_CIANO, 50), (sx, sy+30), (sx+sw, sy+30), 1)
        y = sy+36
        # CPU
        cor_cpu = self.C_VERDE if mon.cpu < 50 else self.C_AMARELO if mon.cpu < 80 else self.C_VERM
        surf.blit(self.fnt_sys.render("CPU", True, (190, 205, 220)), (sx+8, y))
        v = self.fnt_valor.render(str(round(mon.cpu))+"%", True, cor_cpu)
        surf.blit(v, (sx+sw-v.get_width()-8, y-4))
        if mon.temp > 0:
            surf.blit(self.fnt_mini.render(str(round(mon.temp))+"C", True, (180, 110, 60)),
                      (sx+sw-v.get_width()-55, y+4))
        y += 24; self._barra(surf, sx+8, y, sw-50, 12, mon.cpu, cor_cpu)
        y += 16; self._grafico(surf, sx+8, y, sw-16, 38, mon.hist_cpu, cor_cpu); y += 42
        # RAM
        cor_ram = self.C_VERDE if mon.ram < 60 else self.C_AMARELO if mon.ram < 85 else self.C_VERM
        surf.blit(self.fnt_sys.render("RAM", True, (190, 205, 220)), (sx+8, y))
        v = self.fnt_valor.render(str(round(mon.ram))+"%", True, cor_ram)
        surf.blit(v, (sx+sw-v.get_width()-8, y-4))
        y += 24; self._barra(surf, sx+8, y, sw-50, 12, mon.ram, cor_ram); y += 18
        # DISCO
        cor_d = self.C_VERDE if mon.disco < 70 else self.C_AMARELO if mon.disco < 90 else self.C_VERM
        surf.blit(self.fnt_sys.render("DISCO", True, (190, 205, 220)), (sx+8, y))
        v = self.fnt_valor.render(str(round(mon.disco))+"%", True, cor_d)
        surf.blit(v, (sx+sw-v.get_width()-8, y-4))
        y += 24; self._barra(surf, sx+8, y, sw-50, 12, mon.disco, cor_d); y += 18
        # BATERIA (agora funciona — Monitor lê psutil.sensors_battery)
        if mon.bat > 0:
            cor_b = self.C_VERDE if mon.bat > 50 else self.C_AMARELO if mon.bat > 20 else self.C_VERM
            lbl = "BAT+" if mon.plugado else "BAT"
            surf.blit(self.fnt_sys.render(lbl, True, (190, 205, 220)), (sx+8, y))
            v = self.fnt_valor.render(str(round(mon.bat))+"%", True, cor_b)
            surf.blit(v, (sx+sw-v.get_width()-8, y-4))
            y += 24; self._barra(surf, sx+8, y, sw-50, 12, mon.bat, cor_b); y += 18
        # REDE
        pygame.draw.line(surf, (*self.C_CIANO, 40), (sx+8, y), (sx+sw-8, y), 1); y += 6
        surf.blit(self.fnt_sys.render("REDE", True, (190, 205, 220)), (sx+8, y))
        rede = self.fnt_mini.render(
            "UP "+str(round(mon.net_up, 1))+"  DN "+str(round(mon.net_dn, 1))+" KB/s",
            True, (100, 175, 215))
        surf.blit(rede, (sx+sw-rede.get_width()-8, y+2)); y += 18
        # POCO X7
        if poco_data and poco_data.get("conectado"):
            pygame.draw.line(surf, (*self.C_CIANO, 40), (sx+8, y), (sx+sw-8, y), 1); y += 6
            surf.blit(self.fnt_sys.render("POCO X7", True, self.C_VERDE), (sx+8, y))
            info = self.fnt_mini.render(
                "Bat "+str(poco_data.get("bat", "?"))+"%  "+
                str(poco_data.get("temp", "?"))+"C  Disco "+
                str(poco_data.get("disco", "?"))+"%", True, (140, 230, 170))
            surf.blit(info, (sx+sw-info.get_width()-8, y+2)); y += 18
        # TOP PROCESSOS
        pygame.draw.line(surf, (*self.C_CIANO, 40), (sx+8, y), (sx+sw-8, y), 1); y += 6
        surf.blit(self.fnt_sys.render("TOP PROCESSOS", True, (220, 235, 255)), (sx+8, y)); y += 18
        try:
            for nome, pct in mon.get_procs()[:4]:
                cor_p = self.C_VERDE if pct < 30 else self.C_AMARELO if pct < 70 else self.C_VERM
                surf.blit(self.fnt_sys.render(nome[:26], True, (200, 220, 240)), (sx+10, y))
                pct_s = self.fnt_mini.render(str(round(pct, 1))+"%", True, cor_p)
                surf.blit(pct_s, (sx+sw-pct_s.get_width()-8, y+2))
                y += 18
        except Exception as _e:
            logging.exception(_e)
        # ÚLTIMA AÇÃO
        pygame.draw.line(surf, (*self.C_CIANO, 40), (sx+8, y), (sx+sw-8, y), 1); y += 6
        surf.blit(self.fnt_sys.render("ULTIMA ACAO", True, self.C_VERDE), (sx+8, y)); y += 18
        if ultima_acao:
            surf.blit(self.fnt_sys.render(ultima_acao[:44], True, (160, 245, 180)), (sx+8, y)); y += 18
        # RODAPÉ DO PAINEL
        pygame.draw.line(surf, (*self.C_CIANO, 40), (sx+8, y), (sx+sw-8, y), 1); y += 6
        surf.blit(self.fnt_sys.render("IRIS v1.7  |  Memoria ativa", True, (180, 200, 225)), (sx+8, y))
        # ══ CHAT ══
        cy = self.ESF_H; ch = self.H-self.ESF_H; input_h = 52
        pygame.draw.rect(surf, (8, 10, 18, 255), (0, cy, self.W, ch))
        pygame.draw.line(surf, (*self.C_CIANO, 200), (0, cy), (self.W, cy), 2)
        pygame.draw.rect(surf, (4, 8, 20, 255), (0, cy, self.W, 32))
        titulo = self.fnt_title.render(
            "IRIS v1.7   "+self.usuario+"   "+time.strftime("%H:%M:%S"), True, (255, 255, 255))
        surf.blit(titulo, (14, cy+8))
        st_cores = {"idle": self.C_CIANO, "pensando": self.C_AMARELO,
                    "falando": self.C_VERDE, "ouvindo": self.C_VERM}
        st_txt = {"idle": "● aguardando", "pensando": "◌ pensando...",
                  "falando": "◉ falando", "ouvindo": "◉ ouvindo"}
        st = self.fnt_mini.render(st_txt.get(estado, ""), True, st_cores.get(estado, self.C_CIANO))
        surf.blit(st, (self.W-st.get_width()-12, cy+10))
        pygame.draw.line(surf, (*self.C_CIANO, 60), (8, cy+32), (self.W-8, cy+32), 1)
        # Mensagens
        area_y = cy+38; area_fim = cy+ch-input_h-40; y2 = area_fim-4
        for msg in reversed(mensagens):
            quem = msg["quem"]; texto = msg["texto"]; hora = msg.get("hora", "")
            cor_msg = self.C_IRIS if quem == "iris" else self.C_USER
            bg_cor = (0, 28, 48, 75) if quem == "iris" else (40, 32, 0, 75)
            prefixo = ("IRIS "+hora+" | " if quem == "iris" else self.usuario+" "+hora+" | ")
            palavras = texto.split(); linhas, linha = [], ""
            for pal in palavras:
                if len(linha)+len(pal)+1 <= 82:
                    linha += (" " if linha else "")+pal
                else:
                    linhas.append(linha); linha = pal
            if linha:
                linhas.append(linha)
            total_h = len(linhas)*19+6
            bg_y = y2-total_h+4
            if bg_y > area_y:
                pygame.draw.rect(surf, bg_cor, (6, bg_y, self.W-12, total_h), border_radius=6)
            for i, l in enumerate(reversed(linhas)):
                pref = prefixo if i == len(linhas)-1 else " "*len(prefixo)
                t = self.fnt_chat.render(pref+l, True, cor_msg)
                if y2 > area_y:
                    surf.blit(t, (12, y2))
                y2 -= 22
            if y2 > area_y:
                pygame.draw.line(surf, (25, 35, 50, 150), (12, y2+4), (self.W-12, y2+4), 1)
            y2 -= 8
            if y2 < area_y:
                break
        # Input
        inp_y = cy+ch-input_h-6
        pygame.draw.rect(surf, (10, 14, 26, 255), (6, inp_y, self.W-12, input_h), border_radius=10)
        pygame.draw.rect(surf, (*self.C_CIANO, 200), (6, inp_y, self.W-12, input_h), 2, border_radius=10)
        cursor = "█" if int(time.time()*2) % 2 == 0 else " "
        inp = self.fnt_input.render("> "+input_texto+cursor, True, self.C_BRANCO)
        surf.blit(inp, (18, inp_y+13))
        # Dica
        if ouvindo:
            dica = self.fnt_mini.render("OUVINDO... fale agora!", True, self.C_VERDE)
        else:
            dica = self.fnt_sys.render(
                "  F2=falar | F3=hist | F4=conversa | F5=DITADO | Ctrl+V=colar | ajuda | ESC=sair  ",
                True, (220, 230, 245))
        pygame.draw.rect(surf, (4, 10, 22, 255), (0, inp_y-22, self.W, 22))
        pygame.draw.line(surf, (0, 150, 190, 150), (0, inp_y-22), (self.W, inp_y-22), 1)
        surf.blit(dica, (self.W//2-dica.get_width()//2, inp_y-19))
        # Divisória esfera/sistema
        pygame.draw.line(surf, (*self.C_CIANO, 60), (self.ESF_W, 0), (self.ESF_W, self.ESF_H), 1)
        # Cantos decorativos
        for cx2, cy2, dx, dy in [(0, 0, 1, 1), (self.W, 0, -1, 1),
                                 (self.W, self.H, -1, -1), (0, self.H, 1, -1)]:
            pygame.draw.lines(surf, (*self.C_CIANO, 150), False,
                              [(cx2+dx*20, cy2), (cx2, cy2), (cx2, cy2+dy*20)], 2)

    def renderizar_gl(self, surf, W, H):
        """Renderiza surface pygame no OpenGL."""
        glViewport(0, 0, W, H)
        glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity()
        glOrtho(0, W, 0, H, -1, 1)
        glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        tex_data = pygame.image.tostring(surf, "RGBA", False)
        if self._tex_id is None:
            self._tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self._tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, W, H, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glEnable(GL_TEXTURE_2D); glColor4f(1, 1, 1, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1); glVertex2f(0, 0)
        glTexCoord2f(1, 1); glVertex2f(W, 0)
        glTexCoord2f(1, 0); glVertex2f(W, H)
        glTexCoord2f(0, 0); glVertex2f(0, H)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION); glPopMatrix()
        glMatrixMode(GL_MODELVIEW); glPopMatrix()

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

# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    IRIS().rodar()
