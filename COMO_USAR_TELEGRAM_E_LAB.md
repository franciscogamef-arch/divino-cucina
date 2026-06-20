# IRIS v1.1 — Telegram sem janela + Laboratório de IA

## 1. FALAR COM ELA PELO TELEGRAM (sem abrir a janela)

### Configurar uma vez (no iris_config.json):
  "TELEGRAM_TOKEN": "token_do_BotFather",
  "TELEGRAM_CHAT_ID": "seu_id_do_userinfobot"

Como pegar:
- Token: no Telegram, fale com @BotFather -> /newbot -> copie o token
- Chat ID: fale com @userinfobot -> ele te mostra seu id

### Rodar o modo servidor (sem janela):
    cd ~/Área\ de\ trabalho/iris_nova
    python3 iris_servidor.py

Ela manda "IRIS online" no seu Telegram. Agora você fala com ela do
celular de QUALQUER LUGAR — texto ou foto — e ela responde.

### Deixar rodando mesmo fechando o terminal:
    nohup python3 iris_servidor.py &
(o notebook fica ligado em casa, ela responde de onde você estiver)

## 2. LABORATÓRIO DE IA (treina modelos de verdade)

Comandos (na janela ou pelo Telegram):
  treina modelo que classifica se o servo vai falhar
  treina modelo pra prever temperatura pelo tempo de uso
  meus experimentos    -> lista o que já treinou

Ela escreve o código, treina no SEU PC, mostra a precisão e salva o
modelo. É machine learning local real (scikit-learn), pra fins acadêmicos.

HONESTIDADE: são modelos PEQUENOS (rodam no Ryzen). Não é um ChatGPT —
isso exige data centers. Mas é IA local de verdade, treinada por ela,
no seu hardware. Pra LLM local use o Ollama (modo local).
