"""
IRIS v2.0 — Sistema de Roteamento de Comandos (Dict-based)
Substitui a cadeia de if/elif por um sistema declarativo de padrões + handlers.
Mais fácil de manter, testar e estender: um novo comando = uma nova entrada na lista.
"""
import re, logging
from typing import Callable, List, Optional, Tuple, Any


# ══════════════════════════════════════════════════════════════
#  TIPOS DE PADRÃO
# ══════════════════════════════════════════════════════════════
class Padrao:
    """Wrapper que sabe verificar se um texto bate em um padrão."""

    def __init__(self, valor):
        self._v = valor

    def bate(self, texto: str) -> Optional[re.Match]:
        v = self._v
        if callable(v):
            r = v(texto)
            return r if r else None
        if isinstance(v, str):
            return re.match("^" + re.escape(v) + "$", texto) if v == texto else (
                re.search(re.escape(v), texto) if v in texto else None)
        if hasattr(v, "match"):          # regex compilado
            return v.search(texto)
        return None


def exato(*palavras):
    """O texto é exatamente uma dessas palavras."""
    return Padrao(lambda t: t in set(palavras))

def contem(*frases):
    """O texto contém pelo menos uma das frases."""
    return Padrao(lambda t: any(f in t for f in frases))

def comeca(*prefixos):
    """O texto começa com pelo menos um dos prefixos."""
    return Padrao(lambda t: any(t.startswith(p) for p in prefixos))

def regex(padrao: str):
    """O texto casa com o regex dado."""
    return Padrao(re.compile(padrao))

def qualquer(*padroes):
    """Qualquer dos sub-padrões bater."""
    return Padrao(lambda t: any(p.bate(t) for p in padroes))


# ══════════════════════════════════════════════════════════════
#  ROTA — padrão + handler
# ══════════════════════════════════════════════════════════════
class Rota:
    def __init__(self, padrao: Padrao, handler: Callable, prioridade: int = 0):
        self.padrao = padrao
        self.handler = handler
        self.prioridade = prioridade


# ══════════════════════════════════════════════════════════════
#  ROTEADOR — tabela de rotas com despacho
# ══════════════════════════════════════════════════════════════
class Roteador:
    def __init__(self):
        self._rotas: List[Rota] = []

    def adicionar(self, padrao: Padrao, handler: Callable, prioridade: int = 0):
        self._rotas.append(Rota(padrao, handler, prioridade))
        self._rotas.sort(key=lambda r: -r.prioridade)

    def rota(self, padrao: Padrao, prioridade: int = 0):
        """Decorator para registrar rotas de forma declarativa."""
        def decorator(fn: Callable):
            self.adicionar(padrao, fn, prioridade)
            return fn
        return decorator

    def despachar(self, texto: str, contexto: Any = None) -> Optional[str]:
        """Tenta cada rota em ordem. Retorna o resultado do primeiro match."""
        p = texto.lower().strip()
        for rota in self._rotas:
            m = rota.padrao.bate(p)
            if m is not None:
                try:
                    if contexto is not None:
                        return rota.handler(p, contexto, m)
                    return rota.handler(p, m)
                except Exception as e:
                    logging.exception("Roteador: erro em handler para '%s': %s", p, e)
                    return f"Erro ao executar: {e}"
        return None

    def listar(self) -> str:
        return f"Rotas registradas: {len(self._rotas)}"


# ══════════════════════════════════════════════════════════════
#  EXTRATORES DE ARGUMENTOS — helpers para parsear o texto
# ══════════════════════════════════════════════════════════════
def extrair_apos(texto: str, *prefixos) -> str:
    """Remove o prefixo do texto e retorna o resto limpo."""
    for p in sorted(prefixos, key=len, reverse=True):
        if p in texto:
            return texto.replace(p, "", 1).strip()
    return texto.strip()

def extrair_numeros(texto: str) -> List[float]:
    """Extrai todos os números do texto."""
    return [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", texto)]

def extrair_inteiros(texto: str) -> List[int]:
    return [int(n) for n in re.findall(r"-?\d+", texto)]


# ══════════════════════════════════════════════════════════════
#  FÁBRICA DE ROTEADOR PARA SMART HOME
#  Cria e configura todas as rotas do módulo smart home.
#  O Processador pode instanciar isso e chamar despachar() antes
#  de entrar em seu próprio if/elif.
# ══════════════════════════════════════════════════════════════
def criar_roteador_smarthome(ac) -> Roteador:
    r = Roteador()

    # ── Painel ──
    @r.rota(contem("painel casa", "status casa", "smart home", "smarthome",
                   "o que ta ligado", "o que está ligado"), prioridade=10)
    def _painel(p, m): return ac.smarthome_painel()

    # ── Controle de dispositivos ──
    TIPOS_CASA = ("luz", "ar", "som", "tv", "tomada", "quarto", "sala",
                  "climatizacao", "aquecimento")

    @r.rota(Padrao(lambda t: (
        any(t.startswith(x) for x in ("liga ", "ligar ", "desliga ", "desligar ",
                                      "acende ", "apaga ")) and
        any(tp in t for tp in TIPOS_CASA)
    )), prioridade=9)
    def _controlar(p, m):
        ligar = not any(x in p for x in ("desliga", "apaga", "desligar", "apagar"))
        alvo = extrair_apos(p, "liga ", "ligar ", "desliga ", "desligar ",
                            "acende ", "apaga ", "a ", "o ")
        return ac.smarthome_controlar(alvo, ligado=ligar)

    # ── Perfis ──
    PERFIS = ("trabalho", "descanso", "cinema", "refeicao", "refeição",
              "dormir", "exercicio", "exercício")

    @r.rota(Padrao(lambda t: any(
        t.startswith(pref + " " + perf)
        for pref in ("modo", "perfil", "ambiente")
        for perf in PERFIS
    )), prioridade=9)
    def _perfil(p, m):
        perfil = extrair_apos(p, "modo ", "perfil ", "ambiente ").replace("ç", "c").replace("ã", "a")
        return ac.smarthome_perfil(perfil)

    # ── Sensores ──
    @r.rota(contem("sensores", "temperatura ambiente", "umidade ambiente",
                   "fusao sensores", "fusão sensores", "leitura ambiente",
                   "score de conforto"), prioridade=8)
    def _sensores(p, m): return ac.smarthome_fusao_sensores()

    # ── Ajuste climático ──
    @r.rota(contem("ajusta por clima", "ajuste automático", "ajuste automatico",
                   "casa pelo clima"), prioridade=8)
    def _clima(p, m): return ac.smarthome_clima_auto()

    # ── Modo ausente / chegada ──
    @r.rota(contem("saindo de casa", "vou sair", "modo ausente",
                   "ninguem em casa", "ninguém em casa"), prioridade=8)
    def _ausente(p, m): return ac.smarthome_modo_ausente()

    @r.rota(contem("cheguei", "chegando em casa", "modo chegada",
                   "estou em casa", "tô em casa"), prioridade=8)
    def _chegada(p, m): return ac.smarthome_modo_chegada()

    # ── Energia ──
    @r.rota(contem("consumo energia", "tarifa energia", "tarifa atual",
                   "horario pico", "horário pico", "kwh", "conta de luz"), prioridade=7)
    def _tarifa(p, m): return ac.smarthome_tarifas()

    @r.rota(contem("proximo horario barato", "próximo horário barato",
                   "quando energia fica barata"), prioridade=7)
    def _horario_barato(p, m): return ac.log_proximo_horario_barato()

    @r.rota(contem("consumo total", "consumo da casa"), prioridade=7)
    def _consumo(p, m): return ac.smarthome_consumo()

    # ── Roteamento de sinal ──
    @r.rota(contem("roteamento", "melhor rede", "qual rede", "status redes"), prioridade=7)
    def _rede(p, m):
        if "otimiza" in p or "otimizar" in p:
            return ac.smarthome_otimizar_redes()
        return ac.smarthome_roteador()

    # ── Geofencing ──
    @r.rota(contem("geofence", "cerca gps", "onde estou"), prioridade=7)
    def _geo(p, m):
        if "adiciona" in p or "cria zona" in p:
            nums = extrair_numeros(p)
            if len(nums) >= 2:
                nome = p.split()[-1] if not p.split()[-1].replace(".", "").replace("-", "").isdigit() else "home"
                return ac.smarthome_geofence_add(nome, nums[0], nums[1])
        if "status" in p or "zonas" in p:
            return ac.smarthome_geofence_status()
        return ac.smarthome_geofence_check()

    # ── Biometria ──
    @r.rota(contem("biometria voz", "status voz", "quem esta falando",
                   "perfis de voz"), prioridade=7)
    def _bio_voz(p, m): return ac.bio_status_voz()

    @r.rota(comeca("cadastra perfil", "novo perfil voz"), prioridade=7)
    def _bio_cadastra(p, m):
        nome = extrair_apos(p, "cadastra perfil", "novo perfil voz", "voz")
        return ac.bio_cadastrar_perfil(nome or "usuario")

    @r.rota(contem("analisa expressao", "analisa expressão", "como estou",
                   "meu estado emocional", "detecta cansaço"), prioridade=7)
    def _expressao(p, m): return ac.bio_analisar_expressao()

    @r.rota(contem("narra a casa", "resume a casa", "como ta a casa",
                   "como está a casa", "sintese casa"), prioridade=7)
    def _narracao(p, m): return ac.bio_narrar_casa()

    @r.rota(contem("gestos", "controle gestos", "gestos da mão"), prioridade=6)
    def _gestos(p, m): return ac.bio_gestos_status()

    # ── Segurança ──
    @r.rota(contem("seguranca casa", "segurança casa", "central de seguranca"), prioridade=8)
    def _seg(p, m): return ac.seg_status()

    @r.rota(contem("alertas ativos", "alertas de segurança", "alertas agora"), prioridade=8)
    def _alertas(p, m): return ac.seg_alertas()

    @r.rota(comeca("cadastra pet", "meu cachorro", "meu gato"), prioridade=7)
    def _pet(p, m):
        nome = extrair_apos(p, "cadastra pet", "meu cachorro", "meu gato", "o", "a")
        return ac.seg_cadastrar_pet(nome or "pet")

    @r.rota(contem("cerca virtual", "monitora crianca", "monitora criança"), prioridade=7)
    def _cerca(p, m): return ac.seg_cerca_status()

    @r.rota(contem("emergencia gas", "emergência gás", "vazamento gas",
                   "corta gas", "corta agua", "vazamento agua"), prioridade=10)
    def _emergencia(p, m): return ac.seg_cortar_tudo()

    @r.rota(contem("restaura valvulas", "restaurar válvulas", "libera gas",
                   "libera agua"), prioridade=9)
    def _restaura(p, m): return ac.seg_restaurar_valvulas()

    @r.rota(contem("valvulas", "válvulas", "emergencia status"), prioridade=6)
    def _valvulas(p, m): return ac.seg_emergencia_status()

    @r.rota(contem("auditoria acesso", "historico fechadura",
                   "acessos suspeitos"), prioridade=7)
    def _auditoria(p, m):
        nums = extrair_inteiros(p)
        return ac.seg_auditoria(nums[0] if nums else 7)

    # ── Logística ──
    @r.rota(contem("logistica", "logística", "suprimentos", "compras automaticas"), prioridade=6)
    def _log_status(p, m): return ac.log_status()

    @r.rota(contem("o que precisa comprar", "o que falta", "nivel suprimentos"), prioridade=6)
    def _suprimentos(p, m): return ac.log_suprimentos()

    @r.rota(contem("verificar compras", "pedidos automaticos"), prioridade=6)
    def _verificar_compras(p, m): return ac.log_verificar_compras()

    @r.rota(contem("auto correcao", "auto correção", "limpa cache sistema",
                   "auto corrige", "sistema preso", "sistema travado"), prioridade=7)
    def _auto_corr(p, m): return ac.log_auto_correcao()

    @r.rota(contem("analisa logs", "erros do sistema", "log do sistema",
                   "que erros tem"), prioridade=6)
    def _logs(p, m): return ac.log_relatorio_logs()

    @r.rota(contem("relatorio hardware", "relatório hardware",
                   "saude do hardware", "hardware status"), prioridade=6)
    def _hw(p, m): return ac.log_relatorio_hardware()

    # ── Agente Tool Use ──
    @r.rota(contem("lista ferramentas", "ferramentas disponiveis",
                   "minhas tools"), prioridade=6)
    def _tools(p, m): return ac.agente_tools_listar()

    @r.rota(comeca("agente executa", "agente faz", "tool use",
                   "executa objetivo ia"), prioridade=8)
    def _agente(p, m):
        obj = extrair_apos(p, "agente executa", "agente faz", "tool use",
                           "executa objetivo ia")
        return ac.agente_tools_executar(obj)

    @r.rota(contem("historico agente", "histórico agente", "o que o agente fez"), prioridade=6)
    def _hist_agente(p, m): return ac.agente_tools_historico()

    @r.rota(comeca("executa codigo isolado", "sandbox", "executa seguro"), prioridade=7)
    def _sandbox(p, m):
        codigo = extrair_apos(p, "executa codigo isolado", "sandbox", "executa seguro")
        return ac.agente_executar_codigo(codigo)

    # ── Histórico de sensores ──
    @r.rota(contem("historico sensores", "histórico sensores",
                   "grafico sensores", "gráfico sensores",
                   "grafico temperatura", "gráfico temperatura"), prioridade=7)
    def _hist_sens(p, m):
        if hasattr(ac, "historico_sensores_painel"):
            return ac.historico_sensores_painel()
        return "Módulo de histórico não inicializado"

    @r.rota(contem("gera grafico png", "gera gráfico png",
                   "salva grafico sensores"), prioridade=7)
    def _png(p, m):
        if hasattr(ac, "historico_sensores_png"):
            return ac.historico_sensores_png()
        return "Módulo de gráficos não inicializado"

    return r
