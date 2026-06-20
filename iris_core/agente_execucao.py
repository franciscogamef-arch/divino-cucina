"""
IRIS v2.0 — Agente de Execução com Tool Use / Function Calling
Permite que a IA invoque ferramentas reais de forma dinâmica e estruturada.
"""
import os, json, threading, time, logging, subprocess, tempfile, sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


# ══════════════════════════════════════════════════════════════
#  REGISTRO DE FERRAMENTAS — define o que a IA pode invocar
# ══════════════════════════════════════════════════════════════
class RegistroFerramentas:
    def __init__(self):
        self._tools: Dict[str, dict] = {}
        self._handlers: Dict[str, Callable] = {}

    def registra(self, nome: str, descricao: str, parametros: dict, handler: Callable):
        self._tools[nome] = {
            "name": nome,
            "description": descricao,
            "parameters": {
                "type": "object",
                "properties": parametros,
                "required": [k for k, v in parametros.items() if v.get("required", False)]
            }
        }
        self._handlers[nome] = handler
        logging.info("Tool registrada: %s", nome)

    def schema_lista(self) -> List[dict]:
        return list(self._tools.values())

    def invocar(self, nome: str, args: dict) -> Any:
        if nome not in self._handlers:
            return {"erro": f"Ferramenta '{nome}' não encontrada"}
        try:
            resultado = self._handlers[nome](**args)
            logging.info("Tool %s executada: args=%s", nome, args)
            return resultado
        except Exception as e:
            logging.exception(e)
            return {"erro": str(e)}

    def listar(self) -> str:
        if not self._tools:
            return "Nenhuma ferramenta registrada ainda."
        linhas = ["FERRAMENTAS DISPONÍVEIS:"]
        for nome, info in self._tools.items():
            linhas.append(f"• {nome}: {info['description']}")
        return "\n".join(linhas)


# ══════════════════════════════════════════════════════════════
#  EXECUTOR DE CÓDIGO — sandbox seguro para rodar Python
# ══════════════════════════════════════════════════════════════
class ExecutorCodigo:
    TIMEOUT_PADRAO = 10
    IMPORTS_PERMITIDOS = {
        "math", "json", "re", "datetime", "time", "random",
        "os.path", "pathlib", "collections", "itertools", "string",
        "statistics", "decimal", "fractions"
    }
    IMPORTS_BLOQUEADOS = {
        "subprocess", "socket", "http", "urllib", "requests",
        "ftplib", "smtplib", "telnetlib", "shutil", "ctypes"
    }

    def executar(self, codigo: str, timeout: int = TIMEOUT_PADRAO) -> dict:
        resultado = {"saida": "", "erro": "", "sucesso": False}
        # verifica imports proibidos
        for imp in self.IMPORTS_BLOQUEADOS:
            if f"import {imp}" in codigo or f"from {imp}" in codigo:
                resultado["erro"] = f"Import bloqueado por segurança: {imp}"
                return resultado
        # cria arquivo temp
        tmp = tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w", encoding="utf-8")
        tmp.write(codigo)
        tmp.close()
        try:
            proc = subprocess.run(
                [sys.executable, tmp.name],
                capture_output=True, text=True, timeout=timeout,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
            )
            resultado["saida"] = (proc.stdout or "")[:2000]
            resultado["erro"] = (proc.stderr or "")[:500]
            resultado["sucesso"] = proc.returncode == 0
        except subprocess.TimeoutExpired:
            resultado["erro"] = f"Timeout de {timeout}s excedido"
        except Exception as e:
            resultado["erro"] = str(e)
        finally:
            try:
                os.remove(tmp.name)
            except Exception:
                pass
        return resultado

    def executar_e_formatar(self, codigo: str) -> str:
        r = self.executar(codigo)
        if r["sucesso"]:
            return "Executei! Resultado:\n" + (r["saida"] or "(sem saída)")
        return "Erro na execução:\n" + r["erro"]


# ══════════════════════════════════════════════════════════════
#  AGENTE DE EXECUÇÃO — IA chama ferramentas em loop
# ══════════════════════════════════════════════════════════════
class AgenteExecucao:
    MAX_PASSOS = 8

    def __init__(self, ia, acoes=None):
        self.ia = ia
        self.acoes = acoes
        self.registro = RegistroFerramentas()
        self.executor = ExecutorCodigo()
        self._historico_execucoes: List[dict] = []
        self._registrar_tools_padrao()

    def _registrar_tools_padrao(self):
        ex = self.executor

        self.registro.registra(
            "executar_python",
            "Executa código Python de forma segura com sandbox",
            {
                "codigo": {"type": "string", "description": "Código Python a executar", "required": True},
                "timeout": {"type": "integer", "description": "Timeout em segundos (máx 30)", "required": False}
            },
            lambda codigo, timeout=10: ex.executar(codigo, min(int(timeout), 30))
        )

        self.registro.registra(
            "calcular",
            "Calcula expressão matemática de forma segura",
            {
                "expressao": {"type": "string", "description": "Expressão matemática", "required": True}
            },
            self._calcular_seguro
        )

        self.registro.registra(
            "ler_arquivo",
            "Lê conteúdo de um arquivo de texto",
            {
                "caminho": {"type": "string", "description": "Caminho do arquivo", "required": True}
            },
            self._ler_arquivo
        )

        self.registro.registra(
            "salvar_arquivo",
            "Salva texto em um arquivo",
            {
                "caminho": {"type": "string", "description": "Caminho do arquivo", "required": True},
                "conteudo": {"type": "string", "description": "Conteúdo a salvar", "required": True}
            },
            self._salvar_arquivo
        )

        self.registro.registra(
            "info_sistema",
            "Retorna informações do sistema (CPU, RAM, disco)",
            {},
            self._info_sistema
        )

    def _calcular_seguro(self, expressao: str) -> dict:
        import math
        try:
            permitidos = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
            permitidos.update({"abs": abs, "round": round, "int": int, "float": float,
                               "min": min, "max": max, "sum": sum, "len": len})
            resultado = eval(expressao, {"__builtins__": {}}, permitidos)
            return {"resultado": resultado, "expressao": expressao}
        except Exception as e:
            return {"erro": str(e)}

    def _ler_arquivo(self, caminho: str) -> dict:
        p = Path(caminho).expanduser()
        if not p.exists():
            return {"erro": f"Arquivo não encontrado: {caminho}"}
        try:
            conteudo = p.read_text(encoding="utf-8", errors="ignore")[:5000]
            return {"conteudo": conteudo, "tamanho": p.stat().st_size}
        except Exception as e:
            return {"erro": str(e)}

    def _salvar_arquivo(self, caminho: str, conteudo: str) -> dict:
        p = Path(caminho).expanduser()
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(conteudo, encoding="utf-8")
            return {"sucesso": True, "caminho": str(p)}
        except Exception as e:
            return {"erro": str(e)}

    def _info_sistema(self) -> dict:
        try:
            import psutil
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory()
            disco = psutil.disk_usage("/")
            return {
                "cpu_percent": cpu,
                "ram_percent": ram.percent,
                "ram_livre_gb": round(ram.available / 1e9, 2),
                "disco_percent": disco.percent,
                "disco_livre_gb": round(disco.free / 1e9, 2)
            }
        except Exception as e:
            return {"erro": str(e)}

    def registrar_tool(self, nome: str, descricao: str, parametros: dict, handler: Callable):
        self.registro.registra(nome, descricao, parametros, handler)

    def executar_tarefa(self, objetivo: str, max_passos: int = MAX_PASSOS) -> str:
        """Loop agentico: a IA planeja, executa tools, avalia resultado, repete."""
        historico = []
        schema = json.dumps(self.registro.schema_lista(), ensure_ascii=False, indent=2)

        sistema = (
            "Você é um agente executor da IRIS. Seu trabalho é completar a tarefa do usuário "
            "usando as ferramentas disponíveis. Em cada passo:\n"
            "1. Analise o estado atual\n"
            "2. Decida qual ferramenta usar (ou CONCLUÍDO se terminou)\n"
            "3. Responda APENAS em JSON no formato:\n"
            '   {"acao": "nome_ferramenta", "args": {...}} ou {"acao": "CONCLUÍDO", "resposta": "..."}\n\n'
            f"FERRAMENTAS DISPONÍVEIS:\n{schema}"
        )

        prompt_atual = f"TAREFA: {objetivo}"
        passos_log = []

        for passo in range(max_passos):
            if historico:
                contexto = "\n".join(
                    f"Passo {i+1}: {h['acao']} → {h['resultado'][:200]}"
                    for i, h in enumerate(historico)
                )
                prompt_atual = f"TAREFA: {objetivo}\n\nO QUE FEZ ATÉ AGORA:\n{contexto}\n\nPRÓXIMO PASSO:"

            try:
                resposta_ia = self.ia.groq_rapido(prompt_atual, max_tokens=300, temperature=0.2)
                # extrai JSON da resposta
                json_match = re.search(r'\{.*\}', resposta_ia, re.DOTALL)
                if not json_match:
                    break
                decisao = json.loads(json_match.group())
            except Exception as e:
                logging.exception(e)
                break

            acao = decisao.get("acao", "")

            if acao == "CONCLUÍDO":
                resultado_final = decisao.get("resposta", "Tarefa concluída.")
                self._historico_execucoes.append({
                    "objetivo": objetivo,
                    "passos": passos_log,
                    "resultado": resultado_final,
                    "timestamp": time.time()
                })
                return f"✓ {resultado_final}\n\n({passo+1} passos executados)"

            args = decisao.get("args", {})
            resultado_tool = self.registro.invocar(acao, args)
            resultado_str = json.dumps(resultado_tool, ensure_ascii=False)[:500]

            historico.append({"acao": acao, "args": args, "resultado": resultado_str})
            passos_log.append(f"{acao}({args}) → {resultado_str[:100]}")

        return ("Agente encerrou após " + str(max_passos) +
                " passos.\n" + ("\n".join(passos_log[-3:]) if passos_log else ""))

    def listar_tools(self) -> str:
        return self.registro.listar()

    def historico_execucoes(self) -> str:
        if not self._historico_execucoes:
            return "Nenhuma execução registrada ainda."
        linhas = ["HISTÓRICO DO AGENTE:"]
        for h in self._historico_execucoes[-5:]:
            ts = time.strftime("%d/%m %H:%M", time.localtime(h["timestamp"]))
            linhas.append(f"\n[{ts}] {h['objetivo'][:60]}")
            linhas.append(f"  Resultado: {h['resultado'][:120]}")
        return "\n".join(linhas)


import re  # necessário para parsear JSON da IA
