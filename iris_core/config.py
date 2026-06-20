"""
IRIS v1.0 — Assistente Pessoal Avançada (estilo Jarvis)
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

# Imports gráficos são OPCIONAIS — assim a IRIS roda em modo servidor
# (só Telegram, sem janela) em máquinas/sessões sem display gráfico.
try:
    import pygame
    from pygame.locals import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    import pyautogui
    GUI_DISPONIVEL = True
except Exception:
    GUI_DISPONIVEL = False
try:
    import psutil
except Exception:
    psutil = None
try:
    from groq import Groq
except Exception:
    Groq = None
try:
    from google import genai as google_genai
except Exception:
    google_genai = None

if GUI_DISPONIVEL:
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
