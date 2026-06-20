import os, sys, json, queue, threading, subprocess, socket, requests, atexit
import datetime, random, time, math, shutil, asyncio, re, tempfile
from pathlib import Path
import logging


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
