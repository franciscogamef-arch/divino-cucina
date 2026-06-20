"""
IRIS v2.0 — Segurança e Monitoramento da Casa
Filtro de Alarmes (pets), Cerca Virtual, Bloqueio de Emergência, Auditoria de Acesso
"""
import json, threading, time, logging, hashlib
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Callable
from datetime import datetime


# ══════════════════════════════════════════════════════════════
#  FILTRO DE ALARMES — ignora movimentos de pets
# ══════════════════════════════════════════════════════════════
@dataclass
class EventoMovimento:
    zona: str
    tamanho_objeto: float   # metros estimados
    velocidade: float       # m/s estimado
    altura: float           # metros do chão
    temperatura_obj: float  # °C (câmera térmica)
    timestamp: float = field(default_factory=time.time)
    classificado: str = ""  # pessoa | pet | vento | falso


class FiltroAlarmes:
    """Distingue pessoas de pets para evitar falsos alertas."""

    PET_ALTURA_MAX = 0.6    # pets raramente passam de 60cm
    PET_TAMANHO_MAX = 0.5   # menos de 50cm de largura
    PESSOA_ALTURA_MIN = 0.8

    def __init__(self, ia=None):
        self.ia = ia
        self._pets_cadastrados: List[str] = []
        self._historico: List[EventoMovimento] = []
        self._alertas_suprimidos = 0
        self._callbacks_alerta: List[Callable] = []
        self._lock = threading.Lock()

    def cadastrar_pet(self, nome: str) -> str:
        self._pets_cadastrados.append(nome)
        return f"Pet '{nome}' cadastrado. Movimentos serão filtrados automaticamente."

    def classificar(self, evento: EventoMovimento) -> str:
        """Classifica o evento de movimento."""
        # Regras baseadas em características físicas
        if evento.altura < self.PET_ALTURA_MAX and evento.tamanho_objeto < self.PET_TAMANHO_MAX:
            evento.classificado = "pet"
            with self._lock:
                self._alertas_suprimidos += 1
            return "pet"

        if evento.velocidade > 8.0:
            evento.classificado = "vento"
            return "vento"

        if evento.altura >= self.PESSOA_ALTURA_MIN:
            evento.classificado = "pessoa"
            return "pessoa"

        # IA para casos ambíguos
        if self.ia and hasattr(self.ia, 'gemini_visao'):
            evento.classificado = "ambiguo"
        else:
            evento.classificado = "desconhecido"

        return evento.classificado

    def classificar_por_imagem(self, caminho_imagem: str, zona: str) -> dict:
        """Usa visão computacional para classificar o intruso."""
        if not self.ia:
            return {"classificado": "desconhecido", "confianca": 0.0}
        try:
            pets = ", ".join(self._pets_cadastrados) if self._pets_cadastrados else "gato, cachorro"
            prompt = (
                f"Analise o movimento detectado nesta imagem na zona '{zona}'.\n"
                f"Pets cadastrados: {pets}\n"
                "Classifique: pessoa | pet | vento | objeto | nenhum\n"
                'Responda JSON: {"classificado": "...", "confianca": 0.0-1.0, "descricao": "..."}'
            )
            resposta = self.ia.gemini_visao(caminho_imagem, prompt)
            import re
            m = re.search(r'\{.*\}', resposta, re.DOTALL)
            if m:
                return json.loads(m.group())
        except Exception as e:
            logging.exception(e)
        return {"classificado": "desconhecido", "confianca": 0.0}

    def processar_evento(self, evento: EventoMovimento, callback_alarme: Optional[Callable] = None) -> str:
        classificado = self.classificar(evento)
        with self._lock:
            self._historico.append(evento)
            if len(self._historico) > 200:
                self._historico = self._historico[-200:]

        if classificado == "pessoa":
            msg = f"⚠️ MOVIMENTO HUMANO em {evento.zona}!"
            for cb in self._callbacks_alerta:
                try:
                    cb(msg, evento)
                except Exception:
                    pass
            if callback_alarme:
                callback_alarme(msg)
            return msg
        elif classificado == "pet":
            return f"Movimento detectado em {evento.zona}: pet — alarme suprimido"
        else:
            return f"Movimento em {evento.zona}: {classificado} — monitorando"

    def ao_alertar(self, callback: Callable):
        self._callbacks_alerta.append(callback)

    def status(self) -> str:
        return (
            f"FILTRO DE ALARMES:\n"
            f"  Pets cadastrados: {', '.join(self._pets_cadastrados) or 'nenhum'}\n"
            f"  Alertas suprimidos (pets): {self._alertas_suprimidos}\n"
            f"  Eventos registrados: {len(self._historico)}"
        )

    def alertas_ativos(self) -> List[str]:
        recentes = [e for e in self._historico
                    if e.classificado == "pessoa" and time.time() - e.timestamp < 300]
        return [f"Movimento humano em {e.zona}" for e in recentes]


# ══════════════════════════════════════════════════════════════
#  CERCA VIRTUAL — monitora crianças e idosos
# ══════════════════════════════════════════════════════════════
@dataclass
class PessoaMonitorada:
    nome: str
    tipo: str           # crianca | idoso | outro
    dispositivo_id: str # MAC, UUID, ou IP do dispositivo
    zonas_permitidas: List[str] = field(default_factory=list)
    ativa: bool = True


class CercaVirtual:
    """Monitora se pessoas específicas cruzam limites perigosos."""
    DATA_PATH = Path.home() / ".iris" / "cerca_virtual.json"

    def __init__(self, ia=None):
        self.ia = ia
        self._pessoas: Dict[str, PessoaMonitorada] = {}
        self._zonas_perigosas: List[str] = ["escada", "area_externa", "piscina", "garagem"]
        self._alertas: List[dict] = []
        self._callbacks: List[Callable] = []
        self._carregar()

    def _carregar(self):
        try:
            if self.DATA_PATH.exists():
                data = json.loads(self.DATA_PATH.read_text())
                for nome, p in data.items():
                    self._pessoas[nome] = PessoaMonitorada(**p)
        except Exception as e:
            logging.exception(e)

    def _salvar(self):
        try:
            self.DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
            data = {k: asdict(v) for k, v in self._pessoas.items()}
            self.DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2))
        except Exception as e:
            logging.exception(e)

    def cadastrar(self, nome: str, tipo: str, dispositivo: str, zonas_ok: List[str] = None) -> str:
        self._pessoas[nome] = PessoaMonitorada(
            nome=nome, tipo=tipo, dispositivo_id=dispositivo,
            zonas_permitidas=zonas_ok or ["sala", "quarto", "cozinha", "banheiro"]
        )
        self._salvar()
        return f"'{nome}' ({tipo}) cadastrado na cerca virtual"

    def adicionar_zona_perigosa(self, zona: str) -> str:
        if zona not in self._zonas_perigosas:
            self._zonas_perigosas.append(zona)
        return f"Zona '{zona}' marcada como perigosa"

    def verificar_posicao(self, nome: str, zona_atual: str) -> Optional[str]:
        if nome not in self._pessoas:
            return None
        pessoa = self._pessoas[nome]
        if not pessoa.ativa:
            return None

        alerta = None
        if zona_atual in self._zonas_perigosas and zona_atual not in pessoa.zonas_permitidas:
            alerta = (f"⚠️ CERCA VIRTUAL: {nome} ({pessoa.tipo}) "
                      f"na zona PERIGOSA '{zona_atual}'!")
        elif zona_atual not in pessoa.zonas_permitidas:
            alerta = (f"⚠️ {nome} fora da área permitida: '{zona_atual}'")

        if alerta:
            self._alertas.append({
                "timestamp": time.time(),
                "nome": nome,
                "zona": zona_atual,
                "alerta": alerta
            })
            for cb in self._callbacks:
                try:
                    cb(alerta, nome, zona_atual)
                except Exception:
                    pass

        return alerta

    def ao_alertar(self, callback: Callable):
        self._callbacks.append(callback)

    def status(self) -> str:
        linhas = ["CERCA VIRTUAL:"]
        linhas.append(f"  Zonas perigosas: {', '.join(self._zonas_perigosas)}")
        if not self._pessoas:
            linhas.append("  Nenhuma pessoa cadastrada")
        for nome, p in self._pessoas.items():
            estado = "✓ ativa" if p.ativa else "pausada"
            linhas.append(f"  • {nome} ({p.tipo}): {estado}")
        linhas.append(f"  Alertas hoje: {len([a for a in self._alertas if time.time()-a['timestamp']<86400])}")
        return "\n".join(linhas)

    def alertas_recentes(self) -> List[str]:
        return [a["alerta"] for a in self._alertas if time.time() - a["timestamp"] < 3600]


# ══════════════════════════════════════════════════════════════
#  BLOQUEIO DE EMERGÊNCIA — corta água e gás em caso de vazamento
# ══════════════════════════════════════════════════════════════
class BloqueioEmergencia:
    """Detecta e responde a vazamentos de água e gás."""

    LIMITES = {
        "gas_ppm":   300.0,   # ppm de metano/GLP para alarme
        "agua_flow": 0.0,     # L/min — 0 = detectou fluxo sem torneira aberta
        "fumo_nivel": 0.3,    # 0-1
        "co_ppm":    50.0,    # ppm de monóxido de carbono
    }

    def __init__(self, ia=None):
        self.ia = ia
        self._estado_valvulas: Dict[str, bool] = {
            "agua_principal": True,   # True = aberta
            "gas_cozinha": True,
            "gas_aquecedor": True,
        }
        self._emergencia_ativa = False
        self._historico_eventos: List[dict] = []
        self._callbacks: List[Callable] = []

    def verificar_sensores(self, leituras: dict) -> List[str]:
        """Recebe dict com leituras de sensores e verifica emergências."""
        alertas = []

        gas = leituras.get("gas_ppm", 0)
        if gas > self.LIMITES["gas_ppm"]:
            alertas.append(f"GÁS DETECTADO: {gas:.0f}ppm!")
            self._cortar_gas("automático — gás detectado")

        co = leituras.get("co_ppm", 0)
        if co > self.LIMITES["co_ppm"]:
            alertas.append(f"MONÓXIDO DE CARBONO: {co:.0f}ppm!")

        agua = leituras.get("agua_flow", 0)
        if agua > 0 and not leituras.get("torneira_aberta", False):
            alertas.append(f"POSSÍVEL VAZAMENTO DE ÁGUA: {agua:.1f}L/min sem torneira aberta")
            self._cortar_agua("automático — vazamento detectado")

        fumo = leituras.get("fumo_nivel", 0)
        if fumo > self.LIMITES["fumo_nivel"]:
            alertas.append(f"FUMAÇA DETECTADA: {fumo*100:.0f}%!")

        if alertas:
            self._emergencia_ativa = True
            evento = {
                "timestamp": time.time(),
                "alertas": alertas,
                "leituras": leituras
            }
            self._historico_eventos.append(evento)
            for cb in self._callbacks:
                try:
                    cb(alertas, leituras)
                except Exception:
                    pass

        return alertas

    def _cortar_gas(self, motivo: str = "manual"):
        for valvula in ["gas_cozinha", "gas_aquecedor"]:
            self._estado_valvulas[valvula] = False
        logging.warning("EMERGÊNCIA: Gás cortado — %s", motivo)

    def _cortar_agua(self, motivo: str = "manual"):
        self._estado_valvulas["agua_principal"] = False
        logging.warning("EMERGÊNCIA: Água cortada — %s", motivo)

    def cortar_tudo(self) -> str:
        self._cortar_gas("comando manual")
        self._cortar_agua("comando manual")
        self._emergencia_ativa = True
        return "EMERGÊNCIA: Água e gás cortados. Acione a brigada de incêndio se necessário."

    def restaurar(self, valvula: str = "tudo") -> str:
        if valvula == "tudo":
            for v in self._estado_valvulas:
                self._estado_valvulas[v] = True
            self._emergencia_ativa = False
            return "Todas as válvulas restauradas"
        if valvula in self._estado_valvulas:
            self._estado_valvulas[valvula] = True
            return f"Válvula '{valvula}' reaberta"
        return f"Válvula '{valvula}' não encontrada"

    def ao_emergencia(self, callback: Callable):
        self._callbacks.append(callback)

    def status(self) -> str:
        linhas = ["BLOQUEIO DE EMERGÊNCIA:"]
        for valvula, aberta in self._estado_valvulas.items():
            icone = "✓ ABERTA" if aberta else "✗ FECHADA"
            linhas.append(f"  {valvula}: {icone}")
        if self._emergencia_ativa:
            linhas.append("  ⚠️ MODO EMERGÊNCIA ATIVO")
        linhas.append(f"  Eventos: {len(self._historico_eventos)}")
        return "\n".join(linhas)

    def alertas_ativos(self) -> List[str]:
        if not self._emergencia_ativa:
            return []
        return ["Emergência ativa — verificar gás/água"]


# ══════════════════════════════════════════════════════════════
#  AUDITORIA DE ACESSO — monitora padrões de fechaduras digitais
# ══════════════════════════════════════════════════════════════
@dataclass
class RegistroAcesso:
    timestamp: float
    dispositivo: str    # fechadura_frente | fechadura_garagem
    usuario: str
    tipo: str           # entrada | saida | tentativa_falha
    hora_local: str = ""
    suspeito: bool = False

    def __post_init__(self):
        if not self.hora_local:
            self.hora_local = datetime.fromtimestamp(self.timestamp).strftime("%d/%m %H:%M")


class AuditoriaAcesso:
    """Registra e analisa padrões de acesso a fechaduras digitais."""
    DATA_PATH = Path.home() / ".iris" / "auditoria_acesso.json"

    HORARIOS_SUSPEITOS = list(range(0, 5))  # 0h às 4h59m

    def __init__(self, ia=None):
        self.ia = ia
        self._registros: List[RegistroAcesso] = []
        self._callbacks_suspeito: List[Callable] = []
        self._usuarios_autorizados: List[str] = []
        self._carregar()

    def _carregar(self):
        try:
            if self.DATA_PATH.exists():
                data = json.loads(self.DATA_PATH.read_text())
                self._registros = [RegistroAcesso(**r) for r in data.get("registros", [])]
                self._usuarios_autorizados = data.get("usuarios", [])
        except Exception as e:
            logging.exception(e)

    def _salvar(self):
        try:
            self.DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "registros": [asdict(r) for r in self._registros[-500:]],
                "usuarios": self._usuarios_autorizados
            }
            self.DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2))
        except Exception as e:
            logging.exception(e)

    def autorizar_usuario(self, nome: str) -> str:
        if nome not in self._usuarios_autorizados:
            self._usuarios_autorizados.append(nome)
            self._salvar()
        return f"'{nome}' autorizado nas fechaduras"

    def registrar_acesso(self, dispositivo: str, usuario: str, tipo: str) -> str:
        ts = time.time()
        hora = datetime.fromtimestamp(ts).hour
        suspeito = (
            hora in self.HORARIOS_SUSPEITOS or
            usuario not in self._usuarios_autorizados or
            tipo == "tentativa_falha"
        )

        registro = RegistroAcesso(
            timestamp=ts, dispositivo=dispositivo,
            usuario=usuario, tipo=tipo, suspeito=suspeito
        )
        self._registros.append(registro)
        self._salvar()

        if suspeito:
            alerta = (f"⚠️ ACESSO SUSPEITO: {usuario} em {dispositivo} "
                      f"às {registro.hora_local} ({tipo})")
            for cb in self._callbacks_suspeito:
                try:
                    cb(alerta, registro)
                except Exception:
                    pass
            return alerta

        return f"Acesso registrado: {usuario} → {dispositivo} ({tipo})"

    def analisar_padroes(self, dias: int = 7) -> str:
        """IA analisa padrões dos últimos N dias."""
        corte = time.time() - dias * 86400
        recentes = [r for r in self._registros if r.timestamp > corte]

        if not recentes:
            return f"Sem registros nos últimos {dias} dias"

        suspeitos = [r for r in recentes if r.suspeito]
        usuarios = {}
        for r in recentes:
            usuarios[r.usuario] = usuarios.get(r.usuario, 0) + 1

        relatorio = (
            f"AUDITORIA ({dias} dias): {len(recentes)} acessos, "
            f"{len(suspeitos)} suspeitos\n"
            f"Usuários: {', '.join(f'{k}({v})' for k, v in usuarios.items())}"
        )

        if suspeitos and self.ia:
            try:
                dados = "\n".join(
                    f"{r.hora_local}: {r.usuario} - {r.dispositivo} ({r.tipo})"
                    for r in suspeitos[:10]
                )
                analise = self.ia.groq_rapido(
                    f"Analise estes acessos suspeitos em fechaduras digitais e "
                    f"indique o risco em 2 frases:\n{dados}",
                    max_tokens=150
                )
                relatorio += f"\n\nAnálise IA:\n{analise}"
            except Exception:
                pass

        return relatorio

    def ao_acesso_suspeito(self, callback: Callable):
        self._callbacks_suspeito.append(callback)

    def historico(self, n: int = 10) -> str:
        if not self._registros:
            return "Nenhum acesso registrado"
        recentes = self._registros[-n:]
        linhas = [f"ÚLTIMOS {n} ACESSOS:"]
        for r in reversed(recentes):
            flag = " ⚠️" if r.suspeito else ""
            linhas.append(f"  [{r.hora_local}] {r.usuario} → {r.dispositivo} ({r.tipo}){flag}")
        return "\n".join(linhas)

    def alertas_ativos(self) -> List[str]:
        corte = time.time() - 3600
        return [
            f"Acesso suspeito: {r.usuario} em {r.dispositivo}"
            for r in self._registros
            if r.suspeito and r.timestamp > corte
        ]

    def status(self) -> str:
        total = len(self._registros)
        suspeitos = sum(1 for r in self._registros if r.suspeito)
        return (
            f"AUDITORIA DE ACESSO:\n"
            f"  Total de registros: {total}\n"
            f"  Suspeitos: {suspeitos}\n"
            f"  Usuários autorizados: {', '.join(self._usuarios_autorizados) or 'nenhum'}"
        )


# ══════════════════════════════════════════════════════════════
#  CENTRAL DE SEGURANÇA — integra todos os módulos
# ══════════════════════════════════════════════════════════════
class CentralSeguranca:
    def __init__(self, ia=None, notificar_callback: Optional[Callable] = None):
        self.ia = ia
        self._notificar = notificar_callback
        self.filtro = FiltroAlarmes(ia)
        self.cerca = CercaVirtual(ia)
        self.emergencia = BloqueioEmergencia(ia)
        self.auditoria = AuditoriaAcesso(ia)
        self._configurar_callbacks()

    def _configurar_callbacks(self):
        def _alertar(msg, *args):
            logging.warning(msg)
            if self._notificar:
                try:
                    self._notificar("Segurança", str(msg))
                except Exception:
                    pass

        self.filtro.ao_alertar(lambda m, e: _alertar(m))
        self.cerca.ao_alertar(lambda m, n, z: _alertar(m))
        self.emergencia.ao_emergencia(lambda alertas, l: _alertar("\n".join(alertas)))
        self.auditoria.ao_acesso_suspeito(lambda m, r: _alertar(m))

    def status_completo(self) -> str:
        partes = [
            self.filtro.status(),
            self.cerca.status(),
            self.emergencia.status(),
            self.auditoria.status()
        ]
        return "\n\n".join(partes)

    def alertas_ativos(self) -> List[str]:
        return (
            self.filtro.alertas_ativos() +
            self.cerca.alertas_recentes() +
            self.emergencia.alertas_ativos() +
            self.auditoria.alertas_ativos()
        )
