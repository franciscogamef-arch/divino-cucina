import os, sys, json, queue, threading, subprocess, socket, requests, atexit
import datetime, random, time, math, shutil, asyncio, re, tempfile
from pathlib import Path
import logging
from .config import (CFG, CONFIG_PATH, GROQ_API_KEY, GEMINI_API_KEY,
    OPENWEATHER_KEY, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, ARDUINO_PORTA, ARDUINO_ATIVO,
    POCO_IP, CIDADE_PADRAO, MODELO_GROQ, MODELO_GEMINI)
from .roteador import criar_roteador_smarthome, criar_roteador_arduino


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
projeta uma ia melhor que voce [objetivo]
--- SMART HOME v2.0 ---
painel casa | status casa | smart home
liga/desliga [dispositivo] | modo trabalho | modo descanso | modo cinema | modo dormir
sensores | fusao sensores | ajusta por clima | consumo energia | tarifa atual
saindo de casa | cheguei | modo ausente | modo chegada
geofence | onde estou | gps | geofence adiciona [nome] [lat] [lon]
roteamento | melhor rede | otimiza redes | status redes
adiciona dispositivo [nome] [tipo]
--- BIOMETRIA E INTERAÇÃO ---
biometria voz | cadastra perfil [nome] | quem esta falando
analisa expressao | como estou | meu estado emocional
gestos | controle gestos | narra a casa | como ta a casa
--- SEGURANÇA ---
seguranca casa | alertas ativos | alertas de seguranca
cadastra pet [nome] | cerca virtual | monitora crianca
emergencia gas | corta gas | corta agua | emergencia agua
restaura valvulas | status valvulas | valvulas
auditoria acesso [dias] | historico fechadura | acessos suspeitos
--- LOGÍSTICA ---
logistica | suprimentos | status suprimentos | o que precisa comprar
verificar compras | auto correcao | limpa cache sistema
analisa logs | erros do sistema | relatorio hardware | saude hardware
proximo horario barato | consumo total
--- AGENTE TOOL USE ---
lista ferramentas | agente executa [objetivo] | historico agente
executa codigo isolado [codigo] | tool use [tarefa]"""

    def __init__(self, usuario, mem, ia, acoes, mon, voz=None):
        self.usuario = usuario
        self.mem = mem
        self.ia = ia
        self.ac = acoes
        self.mon = mon
        self.voz = voz
        self._pendente = None  # ação aguardando confirmação ou resposta do usuário
        self._roteador_smarthome = criar_roteador_smarthome(acoes)
        self._roteador_arduino = criar_roteador_arduino(acoes)

    def _tratar_resultado(self, resultado):
        """Se o resultado for uma Pergunta, guarda o callback e retorna o texto."""
        from .tipos import Pergunta
        if isinstance(resultado, Pergunta):
            self._pendente = ("callback", resultado.callback)
            return resultado.texto
        return resultado

    def processar(self, prompt):
        p = prompt.lower().strip()
        if not p:
            return "Diga alguma coisa!"

        # ── CONFIRMAÇÃO / PERGUNTA PENDENTE ──
        if self._pendente:
            acao, *resto = self._pendente
            self._pendente = None

            # Callback genérico: qualquer método pode devolver Pergunta(texto, fn)
            if acao == "callback":
                fn = resto[0]
                try:
                    resultado = fn(p)
                    # a resposta pode gerar outra Pergunta (fluxo encadeado)
                    return self._tratar_resultado(resultado)
                except Exception as e:
                    return f"Erro ao executar: {e}"

            # Confirmações binárias (sim/não) pré-existentes
            if p in ("sim", "s", "confirmo", "confirma", "pode", "pode sim", "isso"):
                dado = resto[0] if resto else None
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

        # ── ARDUINO ──
        _r = self._roteador_arduino.despachar(p)
        if _r is not None:
            return self._tratar_resultado(_r)

        # ── SMART HOME / BIO / SEGURANÇA / LOGÍSTICA / AGENTE ──
        _r = self._roteador_smarthome.despachar(p)
        if _r is not None:
            return self._tratar_resultado(_r)

        # ── Adicionar dispositivo (precisa de parse especial) ──
        if any(p.startswith(x) for x in ["adiciona dispositivo", "novo dispositivo",
                                          "cadastra dispositivo", "registra dispositivo"]):
            partes = p.split()
            if len(partes) >= 3:
                tipo = partes[-1] if partes[-1] in (
                    "luz", "som", "tomada", "sensor", "tv", "climatizacao") else "tomada"
                nome = " ".join(partes[2:-1]) if len(partes) > 3 else partes[-1]
                return self.ac.smarthome_adicionar(nome, tipo)
            return "Use: adiciona dispositivo [nome] [tipo]\nTipos: luz, som, tomada, sensor, tv, climatizacao"

        # ── Atualizar nível de suprimento (precisa de parse especial) ──
        if any(p.startswith(x) for x in ["atualiza nivel", "nível de", "nivel de",
                                          "atualizei o nivel", "gastei"]):
            nums = re.findall(r"\d+", p)
            if nums:
                nivel = float(nums[0]) / 100.0
                item = p
                for w in ["atualiza nivel", "nível de", "nivel de", "atualizei o nivel", "gastei"]:
                    item = item.replace(w, "", 1)
                item = re.sub(r"\d+", "", item).strip()
                return self.ac.log_atualizar_nivel(item, nivel)

        # ── PARAR DE FALAR (interrupção imediata) ──
        if p in ("para", "pare", "silencio", "silêncio", "cala a boca",
                 "para de falar", "quieta", "shh"):
            if self.voz:
                self.voz.parar()
            return "Ok, parei."

        # ── MODO DITADO (v14) — fale por minutos, ela escreve tudo ──
        if p in ("ditado", "modo ditado", "quero ditar", "vou ditar", "anota o que vou falar"):
            return self.ac.iniciar_ditado()

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
        if any(x in p for x in ["reinicia o celular"]):
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

        # ── LABORATÓRIO DE IA (v29) — treina modelos de verdade ──
        if any(x in p for x in ["treina modelo", "treinar modelo", "cria modelo",
                                "experimento de ia", "laboratorio de ia", "novo modelo"]):
            d = p
            for w in ["treina modelo", "treinar modelo", "cria modelo",
                      "experimento de ia", "laboratorio de ia", "novo modelo", "pra", "para"]:
                d = d.replace(w, "", 1)
            return self.ac.laboratorio_treinar(d.strip())
        if any(x in p for x in ["meus experimentos", "lista experimentos", "modelos treinados"]):
            return self.ac.laboratorio_listar()

        # ── HABILIDADES EXTRAS (v28) ──
        if any(x in p for x in ["treina ia", "treinar ia", "gera ia", "ia do exo",
                                "treina rede do exo", "auto treinar rede"]):
            return self.ac.treinar_ia_exo(p)
        if any(x in p for x in ["alivia cpu", "aliviar cpu", "libera cpu", "processos pesados"]):
            return self.ac.aliviar_cpu(p)
        if p.startswith("udp ") or p.startswith("envia udp") or p.startswith("comando udp"):
            arg = p.replace("comando udp", "").replace("envia udp", "").replace("udp", "", 1).strip()
            return self.ac.enviar_udp(arg)
        if any(x in p for x in ["clipboard", "copia texto", "area de transferencia",
                                "cola texto", "ctrl c"]):
            arg = p
            for w in ["sincroniza clipboard", "clipboard", "copia texto", "cola texto",
                      "area de transferencia", "ctrl c"]:
                arg = arg.replace(w, "", 1)
            return self.ac.sincronizar_clipboard(arg.strip())
        if any(x in p for x in ["ver logs", "ultimos erros", "ver log", "log da iris",
                                "dmesg", "erros do kernel"]):
            return self.ac.ver_logs(p)

        # ── PAINEL WEB (v26) — controle pelo navegador do celular ──
        if any(x in p for x in ["painel web", "abre painel", "controle web", "ativa painel"]):
            return self.ac.iniciar_painel_web()

        # ── BRIEFING DE CHEGADA (v24) ──
        if any(x in p for x in ["briefing", "como estamos", "me poe a par", "novidades",
                                "resumo de chegada", "bom dia iris", "o que temos pra hoje"]):
            return self.ac.briefing()

        # ── AUTOTESTE (v23) — ela testa as próprias habilidades ──
        if any(x in p for x in ["testa voce mesma", "teste voce mesma", "testa suas funcoes",
                                "autoteste", "testa suas habilidades", "testa tudo",
                                "verifica suas funcoes"]):
            area = "tudo"
            for marcador in ["arduino", "celular", "rede", "neural", "ia", "sistema",
                             "memoria", "projetos", "plugins", "codigo"]:
                if marcador in p:
                    area = marcador
                    break
            return self.ac.autoteste(area)

        # ── FILA DE TAREFAS (v22) — várias ações em sequência ──
        if any(p.startswith(x) for x in ["faz tudo", "faça tudo", "faz em sequencia",
                                          "executa em sequencia", "uma depois da outra"]):
            t = p
            for w in ["faz tudo:", "faça tudo:", "faz tudo", "faça tudo", "faz em sequencia",
                      "executa em sequencia", "uma depois da outra"]:
                t = t.replace(w, "", 1)
            return self.ac.executar_fila(t.strip())

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
            return ("IRIS v1.0 — Comandos:\n" + self.LISTA_COMANDOS +
                    "\n$ [comando linux]\nF2=voz | F3=histórico | F4=conversa contínua"
                    "\nDiga 'para' para eu calar a boca :)"
                    "\nOu fale livremente comigo — eu entendo linguagem natural!")

        # ── PERGUNTAS SOBRE TAREFAS/PROJETO (v1.7) — busca dados reais ──
        if any(x in p for x in ["qual tarefa", "quais tarefas", "que tarefa", "qual a tarefa",
                                "minhas tarefas", "o que falta", "o que tenho pra fazer",
                                "o que eu tenho pra fazer", "tarefa pendente", "tarefas pendentes"]):
            return self.ac.proj.responder_sobre_tarefas()

        # ── FERRAMENTAS DO FRANCISCO (v1.6) ──
        if p.startswith("acha arquivo") or p.startswith("busca arquivo") or p.startswith("procura arquivo") or p.startswith("encontra arquivo"):
            nome = p
            for w in ["acha arquivo", "busca arquivo", "procura arquivo", "encontra arquivo", "o"]:
                nome = nome.replace(w, "", 1)
            return self.ac.buscar_arquivo(nome.strip())
        if any(x in p for x in ["backup dos projetos", "backup projetos", "faz backup", "salva meus projetos"]):
            return self.ac.backup_projetos()
        if p.startswith("diario livro") or p.startswith("diario do livro") or p.startswith("diario erebo") or p.startswith("diario do erebo"):
            t = p
            for w in ["diario do livro", "diario livro", "diario do erebo", "diario erebo"]:
                t = t.replace(w, "", 1)
            return self.ac.diario_livro(t.strip())
        if any(x in p for x in ["acha duplicados", "arquivos duplicados", "limpa duplicados", "duplicados"]):
            pasta = p
            for w in ["acha duplicados", "arquivos duplicados", "limpa duplicados", "duplicados", "em", "de", "na"]:
                pasta = pasta.replace(w, "", 1)
            msg, lista = self.ac.achar_duplicados(pasta.strip())
            if lista:
                self._pendente = ("apagar_duplicados", lista)
            return msg
        if any(x in p for x in ["analisa meus aparelhos", "analisa aparelhos", "melhora meus aparelhos",
                                "como melhorar meus aparelhos", "otimizar aparelhos"]):
            return self.ac.analisar_aparelhos()

        # ── GESTÃO DE FOTOS (v1.5) — ver/descrever/apagar/organizar, com confirmação ──
        if any(p.startswith(x) for x in ["ver fotos", "lista fotos", "minhas fotos", "mostra fotos"]):
            pasta = p
            for w in ["ver fotos", "lista fotos", "minhas fotos", "mostra fotos", "de", "da", "em"]:
                pasta = pasta.replace(w, "", 1)
            return self.ac.listar_fotos(pasta.strip())
        if p.startswith("descreve foto") or p.startswith("o que tem na foto") or p.startswith("que foto e"):
            nome = p
            for w in ["descreve foto", "o que tem na foto", "que foto e", "a"]:
                nome = nome.replace(w, "", 1)
            return self.ac.descrever_foto(nome.strip())
        if p.startswith("apaga foto") or p.startswith("apagar foto") or p.startswith("deleta foto"):
            nome = p
            for w in ["apaga foto", "apagar foto", "deleta foto", "a"]:
                nome = nome.replace(w, "", 1)
            msg, pend = self.ac.preparar_apagar_foto(nome.strip())
            if pend:
                self._pendente = ("apagar_foto", pend)
            return msg
        if p.startswith("organiza fotos") or p.startswith("organizar fotos") or p.startswith("arruma fotos"):
            pasta = p
            for w in ["organiza fotos", "organizar fotos", "arruma fotos", "de", "da", "em"]:
                pasta = pasta.replace(w, "", 1)
            return self.ac.organizar_fotos(pasta.strip())

        # ── GESTÃO DE ARQUIVOS (v1.4) — apagar/criar/mover, com confirmação ──
        if p.startswith("apaga arquivo") or p.startswith("apagar arquivo") or p.startswith("deleta arquivo"):
            alvo = p
            for w in ["apaga arquivo", "apagar arquivo", "deleta arquivo", "o"]:
                alvo = alvo.replace(w, "", 1)
            msg, pendente = self.ac.preparar_apagar_arquivo(alvo.strip())
            if pendente:
                self._pendente = ("apagar_arquivo", pendente)
            return msg
        if p.startswith("cria pasta") or p.startswith("criar pasta") or p.startswith("nova pasta"):
            nome = p
            for w in ["cria pasta", "criar pasta", "nova pasta", "chamada", "chamado"]:
                nome = nome.replace(w, "", 1)
            return self.ac.criar_pasta(nome.strip())
        if p.startswith("move ") or p.startswith("mover ") or p.startswith("renomeia"):
            arg = p
            for w in ["mover", "move", "renomeia", "o arquivo", "arquivo"]:
                arg = arg.replace(w, "", 1)
            return self.ac.mover_arquivo(arg.strip())

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
