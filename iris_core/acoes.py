import os, sys, json, queue, threading, subprocess, socket, requests, atexit
import datetime, random, time, math, shutil, asyncio, re, tempfile
from pathlib import Path
import logging
try:
    import pyautogui
except Exception:
    pyautogui = None
from .config import (CFG, CONFIG_PATH, GROQ_API_KEY, GEMINI_API_KEY,
    OPENWEATHER_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, ARDUINO_PORTA, ARDUINO_ATIVO,
    POCO_IP, CIDADE_PADRAO, MODELO_GROQ, MODELO_GEMINI)
from .ia import CerebroLocal
from .neural import RedeNeuronal
from .programadora import Programadora, Plugins
from .projetos import GerenciadorProjetos
from .smarthome import SmartHomeHub, LeituraAmbiente
from .biometria import BiometriaVoz, AnalisadorExpressao, ControladorGestos, SintesContexto
from .seguranca_casa import CentralSeguranca
from .logistica import CentralLogistica
from .agente_execucao import AgenteExecucao, ExecutorCodigo
from .sensores_historico import SeriesTempo, ColetorSensores, GraficoASCII
from .modulos.smarthome_mixin import SmartHomeMixin
from .modulos.github_mixin import GithubMixin
from .modulos.celular_mixin import CelularMixin
from .tipos import Pergunta  # re-exportado; use `from iris_core.tipos import Pergunta` nos mixins

_FALLBACK_HTML = """<!doctype html><html><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>IRIS</title><style>
body{background:#0a0e1a;color:#cde;font-family:sans-serif;margin:0;padding:16px}
h1{color:#00c8f5}button{background:#13243a;color:#9df;border:1px solid #00c8f5;
border-radius:10px;padding:14px;margin:5px;font-size:15px;width:46%}
button:active{background:#00c8f5;color:#000}
#out{margin-top:14px;padding:12px;background:#0d1424;border-radius:10px;
white-space:pre-wrap;min-height:60px}
input{width:70%;padding:12px;border-radius:10px;border:1px solid #00c8f5;
background:#0d1424;color:#cde;font-size:15px}
</style></head><body><h1>IRIS — controle</h1>
<div id=devs></div>
<div style="margin-top:10px">
<input id=txt placeholder="comando...">
<button style="width:25%" onclick="cmd(document.getElementById('txt').value)">enviar</button>
</div><div id=out>Carregando...</div>
<script>
function cmd(c){fetch('/cmd?c='+encodeURIComponent(c)).then(r=>r.text())
  .then(t=>{document.getElementById('out').textContent=t});}
function refresh(){fetch('/api/casa').then(r=>r.json()).then(d=>{
  let h='';d.dispositivos.forEach(dv=>{
    h+='<button onclick="cmd(\''+(dv.ligado?'desliga ':'liga ')+dv.nome+'\')">'
      +dv.nome+' '+(dv.ligado?'ON':'OFF')+'</button>';});
  document.getElementById('devs').innerHTML=h;
  if(d.alertas&&d.alertas.length)
    document.getElementById('out').textContent='⚠️ '+d.alertas.join(' | ');
});}
refresh();setInterval(refresh,10000);
</script></body></html>"""


# ══════════════════════════════════════════════════════════════
#  AÇÕES — tudo que a IRIS pode fazer no sistema
# ══════════════════════════════════════════════════════════════
class Acoes(SmartHomeMixin, GithubMixin, CelularMixin):
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
        # v9.0 — módulos originais
        self.cerebro = CerebroLocal()
        self.rede = RedeNeuronal()
        self.prog = Programadora(ia)
        self.proj = GerenciadorProjetos()
        self.plugins = Plugins()
        # v2.0 — smart home
        self.smarthome = SmartHomeHub(ia)
        self.biometria_voz = BiometriaVoz(ia)
        self.expressao = AnalisadorExpressao(ia)
        self.gestos = ControladorGestos(ia, self.smarthome)
        self.sintecontexto = SintesContexto(ia)
        self.seguranca = CentralSeguranca(ia, notificar_callback=self.notificar)
        self.logistica = CentralLogistica(ia, self.smarthome, notificar_callback=self._notif_logistica)
        self.agente = AgenteExecucao(ia, self)
        self._registrar_tools_smarthome()
        # histórico de sensores e coletor automático
        self._series_tempo = SeriesTempo()
        self._coletor = ColetorSensores(self._series_tempo, self.smarthome)
        self._coletor.iniciar()
        threading.Thread(target=self._checar_lembretes, daemon=True).start()
        self._iniciar_arduino()

    def _notif_logistica(self, titulo: str, msg: str):
        self.notificar(titulo, msg)

    def _registrar_tools_smarthome(self):
        sh = self.smarthome
        self.agente.registrar_tool(
            "controlar_dispositivo",
            "Liga/desliga ou ajusta valor de dispositivo da casa",
            {
                "nome": {"type": "string", "description": "Nome do dispositivo", "required": True},
                "ligado": {"type": "boolean", "description": "True=ligar, False=desligar"},
                "valor": {"type": "number", "description": "Brilho/volume/temperatura 0-100"}
            },
            lambda nome, ligado=None, valor=None: sh.controlar(nome, ligado, valor)
        )
        self.agente.registrar_tool(
            "status_casa",
            "Retorna o painel completo de status da casa",
            {},
            lambda: sh.painel_status()
        )
        self.agente.registrar_tool(
            "aplicar_perfil_ambiente",
            "Aplica um perfil de ambiente (trabalho, descanso, cinema, etc)",
            {"perfil": {"type": "string", "description": "Nome do perfil", "required": True}},
            lambda perfil: sh.ajuste.aplicar_perfil(perfil)
        )

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
            self.telegram("IRIS v1.0 online! Mande um comando. Digite: ajuda")
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
        import urllib.parse, json as _json
        acoes_self = self
        _tpl = Path(__file__).parent.parent / "templates" / "casa.html"

        class H(BaseHTTPRequestHandler):
            def log_message(self, *a): pass

            def _send(self, body, tipo="text/html", code=200):
                enc = body.encode("utf-8") if isinstance(body, str) else body
                self.send_response(code)
                self.send_header("Content-Type", tipo + "; charset=utf-8")
                self.send_header("Content-Length", str(len(enc)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(enc)

            def do_GET(self):
                parsed = urllib.parse.urlparse(self.path)
                path = parsed.path

                # ── REST: executa comando ──
                if path == "/cmd":
                    q = urllib.parse.parse_qs(parsed.query)
                    comando = q.get("c", [""])[0]
                    try:
                        r = (acoes_self.processador.processar(comando)
                             if acoes_self.processador else "sem processador")
                    except Exception as e:
                        r = f"Erro: {e}"
                    self._send(str(r), "text/plain")
                    return

                # ── REST: estado da casa em JSON ──
                if path == "/api/casa":
                    try:
                        sh = acoes_self.smarthome
                        devs = []
                        for nome, d in sh.dispositivos.items():
                            devs.append({
                                "nome": nome,
                                "tipo": getattr(d, "tipo", "?"),
                                "ligado": getattr(d, "ligado", False),
                                "valor": getattr(d, "valor", None),
                                "consumo_w": getattr(d, "consumo_w", 0),
                            })
                        leitura = sh.sensores.simular_leitura() if sh.sensores else {}
                        alertas = acoes_self.seguranca.alertas_ativos() if acoes_self.seguranca else []
                        hist = {}
                        if hasattr(acoes_self, "_series_tempo"):
                            hist = acoes_self._series_tempo.estatisticas(1) or {}
                        payload = {
                            "dispositivos": devs,
                            "sensores": {
                                "temperatura": getattr(leitura, "temperatura", None),
                                "umidade": getattr(leitura, "umidade", None),
                                "co2": getattr(leitura, "co2", None),
                                "conforto": getattr(leitura, "conforto", None),
                                "presenca": getattr(leitura, "presenca", False),
                            },
                            "alertas": alertas,
                            "historico": hist,
                            "ts": datetime.datetime.now().isoformat(),
                        }
                        self._send(_json.dumps(payload, ensure_ascii=False), "application/json")
                    except Exception as e:
                        self._send(_json.dumps({"erro": str(e)}), "application/json", 500)
                    return

                # ── Dashboard HTML ──
                if path in ("/", "/casa", "/index.html"):
                    if _tpl.exists():
                        self._send(_tpl.read_text(encoding="utf-8"))
                    else:
                        # fallback simples caso o template não exista
                        self._send(_FALLBACK_HTML)
                    return

                self._send("Not found", "text/plain", 404)

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

