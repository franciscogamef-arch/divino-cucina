#!/usr/bin/env python3
"""
IRIS — MODO SERVIDOR (sem janela)
Roda a IRIS em segundo plano, só respondendo pelo Telegram.
Você fala com ela do celular de qualquer lugar, sem abrir a interface 3D.

Uso:
    python3 iris_servidor.py

Requer: TELEGRAM_TOKEN e TELEGRAM_CHAT_ID configurados no iris_config.json
Deixe o notebook ligado e rode este arquivo. Pode fechar o terminal com:
    nohup python3 iris_servidor.py &
(assim continua rodando mesmo fechando o terminal)
"""
import sys, time, json
from pathlib import Path

# carrega os módulos da IRIS sem abrir a interface gráfica
from iris_core.memoria import Memoria
from iris_core.ia import IA
from iris_core.acoes import Acoes
from iris_core.processador import Processador
from iris_core.config import CFG, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def main():
    print("=" * 50)
    print("IRIS — MODO SERVIDOR (Telegram, sem janela)")
    print("=" * 50)
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("\n[ERRO] Falta configurar o Telegram no iris_config.json:")
        print('  "TELEGRAM_TOKEN": "seu_token_do_BotFather"')
        print('  "TELEGRAM_CHAT_ID": "seu_chat_id"')
        print("\nComo pegar:")
        print("  1. No Telegram, fale com @BotFather, mande /newbot, copie o token")
        print("  2. Fale com @userinfobot pra pegar seu chat_id")
        return

    usuario = CFG.get("USUARIO", "Francisco")
    print("\nIniciando o cérebro da IRIS (sem interface)...")
    mem = Memoria()
    ia = IA(usuario, mem)
    ac = Acoes(usuario, mem, ia)
    proc = Processador(usuario, mem, ia, ac, None)
    ac.processador = proc
    # callback de fala vira "manda no telegram" (não tem voz sem interface)
    ac.ia_callback = lambda msg: ac.telegram(str(msg))
    ac._falar_callback = lambda msg: ac.telegram(str(msg))

    print("Conectando ao Telegram...")
    # avisa que está online
    try:
        ac.telegram("🔵 IRIS online (modo servidor)! Pode falar comigo daqui de qualquer lugar, "
                    + usuario + ". Manda comando ou foto que eu respondo.")
    except Exception as e:
        print("[ERRO] Não consegui conectar ao Telegram:", e)
        return

    # inicia o loop do bot (recebe texto e foto, responde, manda avisos proativos)
    ac._bot_ativo = True
    ac._bot_callback = proc.processar
    print("\n✓ IRIS no ar! Fale com ela pelo Telegram do seu celular.")
    print("  (deixe este terminal aberto, ou rode com 'nohup python3 iris_servidor.py &')")
    print("  Ctrl+C para desligar.\n")
    try:
        ac._loop_bot_telegram()  # roda pra sempre, escutando o Telegram
    except KeyboardInterrupt:
        ac._bot_ativo = False
        print("\nIRIS servidor desligado. Até logo!")

if __name__ == "__main__":
    main()
