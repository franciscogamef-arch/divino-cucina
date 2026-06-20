import os, sys, json, queue, threading, subprocess, socket, requests, atexit
import datetime, random, time, math, shutil, asyncio, re, tempfile
from pathlib import Path
import logging
from groq import Groq
from google import genai as google_genai
from .config import (CFG, CONFIG_PATH, GROQ_API_KEY, GEMINI_API_KEY,
    OPENWEATHER_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, ARDUINO_PORTA, ARDUINO_ATIVO,
    POCO_IP, CIDADE_PADRAO, MODELO_GROQ, MODELO_GEMINI)


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
