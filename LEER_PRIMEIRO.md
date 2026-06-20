# 🔵 IRIS v2.0 — Smart Home Edition
Assistente pessoal do Francisco. Modular, testada, completa.
Agora com Smart Home, Biometria, Segurança Avançada, Logística e Tool Use.

## Rodar
cd iris && python3 iris.py
(mantenha iris.py e a pasta iris_core/ SEMPRE juntos)

## Instalar dependências (uma vez)
pip3 install pygame PyOpenGL psutil groq google-genai pyautogui edge-tts requests --break-system-packages
sudo apt install mpg123 xclip wmctrl xdotool -y

## Chaves (no iris_config.json, criado no 1º arranque)
  "GROQ_API_KEY": "..."      (console.groq.com/keys)
  "GEMINI_API_KEY": "..."    (aistudio.google.com/apikey)
  "OPENROUTER_KEY": "..."    (openrouter.ai/keys) - opcional, modelos grátis
  "OPENROUTER_MODELO": "qwen/qwen3-coder:free"

## O QUE ELA FAZ (300+ funções)
CONVERSA: Groq+Gemini+Ollama+OpenRouter (rotação automática), voz, visão,
  conversa contínua, ditado, humor, briefing de chegada, aprende com o tempo.
PROGRAMA: escreve/corrige/compacta código; cria plugins (testa antes de ativar).
ARDUINO: firmware universal (servo/LED/PWM/sensor), compila, grava; UDP p/ ESP32.
CELULAR (Poco X7): status, screenshot, WiFi, guarda-costas, achar (Find My Device).
SISTEMA: monitor tempo real, otimiza, alivia CPU, organiza, foco, agente visual.
PROJETOS: coordena (NTM, exoesqueleto, livro), tarefas, diário, próximo passo.
NTM: rede neuronal ternária (Hopfield + spiking). IA do exoesqueleto (detecta queda).
CONTROLE REMOTO: Telegram (texto+foto, de qualquer lugar), painel web (navegador).
SE PROTEGE: Guardiã (backup de si), autoverifica, autoteste, restaura versões.

## NOVIDADES v2.0 — SMART HOME

### Sensores e Automação (smarthome.py)
- FUSÃO DE SENSORES: junta temperatura, umidade, presença com média ponderada
- AJUSTE DINÂMICO: perfis (trabalho/descanso/cinema/dormir) + adapta ao clima externo
- ROTEAMENTO DE SINAL: escolhe Wi-Fi, Zigbee ou Bluetooth automaticamente por dispositivo
- GEOFENCING: ativa/desativa casa pela sua localização GPS

### Interação Humana Avançada (biometria.py)
- BIOMETRIA DE VOZ: identifica locutor + aplica permissões personalizadas por perfil
- ANÁLISE DE EXPRESSÃO: detecta cansaço/estresse via webcam e sugere ambiente
- CONTROLE DE GESTOS: 8 gestos de mão reconhecidos via câmera
- SÍNTESE DE CONTEXTO: narra o status completo da casa em linguagem natural

### Segurança e Monitoramento (seguranca_casa.py)
- FILTRO DE ALARMES: ignora pets (altura/tamanho/velocidade), só alerta pessoas
- CERCA VIRTUAL: monitora crianças/idosos em zonas perigosas com alertas
- BLOQUEIO DE EMERGÊNCIA: corta água e gás automaticamente ao detectar vazamento
- AUDITORIA DE ACESSO: registra e analisa padrões suspeitos de fechaduras digitais

### Diagnóstico e Logística (logistica.py)
- CÁLCULO DE TARIFAS: desliga aparelhos pesados no horário de ponta da energia
- AUTOCOMPRA: monitora filtros, tintas, suprimentos e gera pedidos automaticamente
- AUTO-CORREÇÃO: limpa caches, reinicia serviços travados, diagnostica problemas
- RELATÓRIO TÉCNICO: traduz erros de kernel/hardware em linguagem simples

### Agente de Execução / Tool Use (agente_execucao.py)
- Loop agêntico com Function Calling: a IA planeja e executa ferramentas reais
- Sandbox seguro para execução de código Python com whitelist de imports
- Ferramentas extensíveis: qualquer função pode virar uma "tool" da IA

## COMANDOS GARANTIDOS
Veja COMANDOS_QUE_FUNCIONAM.md — as palavras exatas que sempre funcionam.
Dica: "testa voce mesma" faz ela testar as próprias habilidades.

## ARQUIVOS
iris.py + iris_core/      -> versão modular (recomendada, não quebra fácil)
iris_unico.py            -> tudo num arquivo só (backup)
iris_unico_compacto.py   -> versão enxuta

## Auditada: sintaxe perfeita, zero métodos fantasma, zero código morto.
## Único e modular idênticos (247 métodos). Da v7 à v1.0 oficial.
