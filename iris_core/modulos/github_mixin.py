"""
IRIS v2.0 — Mixin GitHub
Busca, download, estudo de repositórios e auto-evolução da IRIS.
"""
import os, sys, re, shutil, subprocess, logging
from pathlib import Path
import datetime


class GithubMixin:
    """Métodos de GitHub e auto-evolução extraídos de acoes.py."""

    def github_buscar(self, tema: str) -> str:
        import requests
        try:
            r = requests.get(
                "https://api.github.com/search/repositories",
                params={"q": tema, "sort": "stars", "per_page": 5},
                headers={"Accept": "application/vnd.github+json"},
                timeout=10).json()
            itens = r.get("items", [])
            if not itens:
                return f"Nada encontrado no GitHub para '{tema}'"
            linhas = [f"GITHUB — top repositórios para '{tema}':"]
            for it in itens:
                linhas.append(
                    f"- {it['full_name']} ({it['stargazers_count']} estrelas)\n"
                    f"    {(it.get('description') or 'sem descrição')[:90]}")
            linhas.append(f"\nPara estudar: baixa github {itens[0]['full_name']}")
            self._reg(f"Buscou GitHub: {tema}")
            return "\n".join(linhas)
        except Exception as e:
            return f"Erro na busca GitHub: {e}"

    def github_baixar(self, repo: str) -> str:
        import requests, zipfile, io
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
                r = subprocess.run(
                    ["git", "clone", "--depth", "1",
                     f"https://github.com/{repo}", str(destino)],
                    capture_output=True, text=True, timeout=120)
                if r.returncode != 0:
                    return "Erro no clone: " + (r.stderr or "")[-200:]
            else:
                conteudo = None
                for branch in ("main", "master"):
                    resp = requests.get(
                        f"https://codeload.github.com/{repo}/zip/refs/heads/{branch}",
                        timeout=60)
                    if resp.status_code == 200:
                        conteudo = resp.content
                        break
                if not conteudo:
                    return "Não consegui baixar (repo privado ou inexistente?)"
                with zipfile.ZipFile(io.BytesIO(conteudo)) as z:
                    z.extractall(str(destino_base))
                for d in destino_base.iterdir():
                    if d.is_dir() and d.name.startswith(nome + "-"):
                        if destino.exists():
                            shutil.rmtree(str(destino), ignore_errors=True)
                        d.rename(destino)
                        break
            arqs = list(destino.rglob("*"))
            n_py = sum(1 for f in arqs if f.suffix == ".py")
            n_ino = sum(1 for f in arqs if f.suffix == ".ino")
            self._reg(f"Baixou GitHub: {repo}")
            return (f"Baixado: {repo} → ~/IRIS_Projetos/GitHub/{nome}\n"
                    f"{len(arqs)} arquivos ({n_py} .py, {n_ino} .ino)\n"
                    f"Para estudar: estuda github {nome}")
        except Exception as e:
            return f"Erro ao baixar: {e}"

    def github_estudar(self, nome: str) -> str:
        base = Path.home() / "IRIS_Projetos" / "GitHub"
        pasta = base / nome.strip()
        if not pasta.exists():
            cands = [d for d in base.iterdir()
                     if d.is_dir() and nome.lower() in d.name.lower()] if base.exists() else []
            if not cands:
                return f"Não achei '{nome}' baixado. Primeiro: baixa github usuario/repo"
            pasta = cands[0]
        material = []
        for rd in ("README.md", "readme.md", "README.txt", "README"):
            f = pasta / rd
            if f.exists():
                material.append("=== README ===\n" +
                                f.read_text(encoding="utf-8", errors="ignore")[:3000])
                break
        codigos = sorted(
            [f for f in pasta.rglob("*")
             if f.suffix in (".py", ".ino", ".c", ".cpp", ".v") and
             f.is_file() and f.stat().st_size < 30_000],
            key=lambda f: f.stat().st_size)[:6]
        for f in codigos:
            material.append(f"=== {f.name} ===\n" +
                            f.read_text(encoding="utf-8", errors="ignore")[:2000])
        if not material:
            return "Pasta vazia ou sem arquivos legíveis."
        r = self.ia.gemini_complexo(
            "Francisco baixou este repositório. Analise e responda em português:\n"
            "1) O que o projeto faz\n"
            "2) As 3 técnicas mais úteis que ele pode aplicar (IRIS, Arduino, FPGA, NTM)\n"
            "3) Algum risco ou cuidado\nSeja concreto.\n\n" +
            "\n\n".join(material)[:12_000])
        self._reg(f"Estudou GitHub: {pasta.name}")
        return (f"ESTUDO — {pasta.name}:\n{r[:1200]}\n\n"
                f"(Eu estudo e proponho — quem decide aplicar é você!)")

    def forjar_de_estudo(self, ideia: str) -> str:
        base = Path.home() / "IRIS_Projetos" / "GitHub"
        amostras = []
        if base.exists():
            for f in (list(base.rglob("*.py"))[:8] + list(base.rglob("*.ino"))[:4]):
                if f.is_file() and f.stat().st_size < 20_000:
                    amostras.append(f"=== {f.name} ===\n" +
                                    f.read_text(encoding="utf-8", errors="ignore")[:1500])
        ctx = ("\n\n".join(amostras))[:8000] if amostras else \
            "(nenhum repositório estudado ainda)"
        codigo = self.prog._extrair_codigo(self.ia.gemini_complexo(
            "Crie um plugin Python seguro com GATILHOS, DESCRICAO e def executar(args).\n"
            f"IDEIA: {ideia}\n\nINSPIRAÇÃO:\n{ctx}\nResponda APENAS em ```python```."))
        erro = self.prog._validar_python(codigo)
        if erro or "def executar" not in codigo:
            return (f"Forjei rascunho mas tem problema ({erro or 'faltou def executar'}). "
                    f"Tenta descrever diferente?")
        pasta = Path.home() / "IRIS_Plugins" / "rascunhos"
        pasta.mkdir(parents=True, exist_ok=True)
        nome = "rascunho_" + re.sub(r"[^a-z0-9]+", "_", ideia.lower())[:20].strip("_") + ".py"
        (pasta / nome).write_text(codigo, encoding="utf-8")
        self._reg(f"Forjou rascunho: {ideia[:40]}")
        return (f"FORJEI RASCUNHO: {nome}\n"
                f"Guardei em ~/IRIS_Plugins/rascunhos/ — revise antes de ativar.\n\n"
                f"{codigo[:450]}{'...' if len(codigo) > 450 else ''}")

    def propor_blueprint_ia(self, objetivo: str = "") -> str:
        r = self.ia.gemini_complexo(
            "Você é a IRIS. Projete uma IA MELHOR em português:\n"
            "1) Arquitetura modular\n2) Modelos locais/nuvem\n"
            "3) 5 capacidades novas\n4) Segurança\n5) Primeiro passo concreto\n"
            f"Objetivo: {objetivo or 'evolução geral'}")
        dest = Path("iris_blueprint_proxima_ia.txt")
        with open(dest, "a", encoding="utf-8") as f:
            f.write(f"\n\n===== {datetime.datetime.now():%d/%m/%Y %H:%M} =====\n{r}")
        self._reg("Projetou blueprint de IA")
        return (f"BLUEPRINT DA PRÓXIMA IA:\n{r[:1100]}\n\n"
                f"Salvo em iris_blueprint_proxima_ia.txt")

    def propor_melhoria(self, tema: str = "") -> str:
        try:
            with open(os.path.abspath(sys.argv[0] if sys.argv else "iris.py"),
                      encoding="utf-8") as f:
                codigo = f.read()
            foco = tema.strip() or "qualidade geral"
            r = self.ia.gemini_complexo(
                f"Proponha UMA melhoria concreta sobre: {foco}. "
                "Mostre o trecho atual e o proposto.\n\n" + codigo[:9000])
            dest = Path("iris_melhorias.txt")
            with open(dest, "a", encoding="utf-8") as f:
                f.write(f"\n\n===== {datetime.datetime.now():%d/%m/%Y %H:%M} ({foco}) =====\n{r}")
            self._reg(f"Propôs melhoria: {foco[:40]}")
            return (f"PROPOSTA ({foco}):\n{r[:800]}\n\n"
                    f"Salva em iris_melhorias.txt — eu nunca me altero sozinha!")
        except Exception as e:
            return f"Erro: {e}"
