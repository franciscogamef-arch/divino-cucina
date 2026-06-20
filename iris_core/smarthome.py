"""
IRIS v2.0 — Smart Home Hub
Fusão de Sensores, Ajuste Dinâmico, Roteamento de Sinal, Geofencing
"""
import json, threading, time, logging, math
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple
from datetime import datetime


# ══════════════════════════════════════════════════════════════
#  MODELOS DE DADOS
# ══════════════════════════════════════════════════════════════
@dataclass
class LeituraAmbiente:
    temperatura: float = 0.0    # °C
    umidade: float = 0.0        # %
    presenca: bool = False
    luminosidade: float = 0.0   # lux (0-1000)
    ruido: float = 0.0          # dB
    co2: float = 400.0          # ppm
    timestamp: float = field(default_factory=time.time)

    def conforto_score(self) -> float:
        """Score 0-100 de conforto térmico+umidade (ISO 7730 simplificado)."""
        t_score = max(0.0, 100.0 - abs(self.temperatura - 22.0) * 10.0)
        u_score = max(0.0, 100.0 - abs(self.umidade - 50.0) * 1.5)
        return round((t_score + u_score) / 2.0, 1)


@dataclass
class EstadoDispositivo:
    nome: str
    tipo: str               # luz | climatizacao | som | tomada | sensor
    ligado: bool = False
    valor: float = 0.0      # brilho 0-100, volume 0-100, temp alvo
    rede: str = "wifi"      # wifi | zigbee | bluetooth
    consumo_w: float = 0.0
    ultimo_update: float = field(default_factory=time.time)


@dataclass
class ZonaGeofence:
    nome: str
    lat: float
    lon: float
    raio_m: float = 200.0
    ativa: bool = True


# ══════════════════════════════════════════════════════════════
#  FUSÃO DE SENSORES
# ══════════════════════════════════════════════════════════════
class FusaoSensores:
    """Agrega leituras de múltiplos sensores com média ponderada."""

    def __init__(self):
        self._leituras: List[LeituraAmbiente] = []
        self._lock = threading.Lock()
        self._historico: List[LeituraAmbiente] = []

    def registrar(self, leitura: LeituraAmbiente):
        with self._lock:
            self._leituras.append(leitura)
            if len(self._leituras) > 10:
                self._leituras = self._leituras[-10:]
            self._historico.append(leitura)
            if len(self._historico) > 500:
                self._historico = self._historico[-500:]

    def fusao(self) -> LeituraAmbiente:
        with self._lock:
            if not self._leituras:
                return LeituraAmbiente()
            # média ponderada — leituras mais recentes têm peso maior
            n = len(self._leituras)
            pesos = [math.exp(0.3 * (i - n + 1)) for i in range(n)]
            soma_pesos = sum(pesos)

            def media_w(attr):
                return sum(getattr(l, attr) * pesos[i]
                           for i, l in enumerate(self._leituras)) / soma_pesos

            return LeituraAmbiente(
                temperatura=round(media_w("temperatura"), 1),
                umidade=round(media_w("umidade"), 1),
                presenca=any(l.presenca for l in self._leituras[-3:]),
                luminosidade=round(media_w("luminosidade"), 1),
                ruido=round(media_w("ruido"), 1),
                co2=round(media_w("co2"), 0)
            )

    def simular_leitura(self, temp=22.0, umidade=50.0, presenca=True) -> LeituraAmbiente:
        import random
        leitura = LeituraAmbiente(
            temperatura=temp + random.uniform(-0.5, 0.5),
            umidade=umidade + random.uniform(-2, 2),
            presenca=presenca,
            luminosidade=random.uniform(200, 600),
            ruido=random.uniform(30, 55),
            co2=random.uniform(380, 600)
        )
        self.registrar(leitura)
        return leitura

    def resumo(self) -> str:
        f = self.fusao()
        score = f.conforto_score()
        return (
            f"FUSÃO DE SENSORES:\n"
            f"  Temperatura: {f.temperatura}°C | Umidade: {f.umidade}%\n"
            f"  Presença: {'✓ detectada' if f.presenca else '✗ vazio'}\n"
            f"  Luminosidade: {f.luminosidade:.0f} lux | Ruído: {f.ruido:.0f} dB\n"
            f"  CO₂: {f.co2:.0f} ppm\n"
            f"  Score de conforto: {score}/100"
        )


# ══════════════════════════════════════════════════════════════
#  AJUSTE DINÂMICO — clima externo → dispositivos internos
# ══════════════════════════════════════════════════════════════
class AjusteDinamico:
    PERFIS = {
        "trabalho":  {"brilho": 80, "volume": 30, "temp_alvo": 22, "musica": "focus"},
        "descanso":  {"brilho": 30, "volume": 20, "temp_alvo": 20, "musica": "ambient"},
        "refeicao":  {"brilho": 70, "volume": 40, "temp_alvo": 23, "musica": "jazz"},
        "exercicio": {"brilho": 90, "volume": 70, "temp_alvo": 19, "musica": "upbeat"},
        "cinema":    {"brilho": 10, "volume": 65, "temp_alvo": 21, "musica": None},
        "dormir":    {"brilho": 0,  "volume": 0,  "temp_alvo": 19, "musica": None},
    }

    def __init__(self, dispositivos: Dict[str, EstadoDispositivo]):
        self.dispositivos = dispositivos
        self._perfil_ativo = "trabalho"
        self._ajustes_log: List[dict] = []

    def ajustar_por_clima(self, temp_ext: float, chuva: bool, hora: int) -> List[str]:
        acoes = []

        # Temperatura interna vs externa
        if temp_ext > 30:
            self._setar("climatizacao", ligado=True, valor=20)
            acoes.append("Climatização ligada em 20°C (calor externo)")
        elif temp_ext < 15:
            self._setar("climatizacao", ligado=True, valor=24)
            acoes.append("Aquecimento em 24°C (frio externo)")

        # Luminosidade adaptativa
        if chuva or hora < 7 or hora > 19:
            self._setar("luz", ligado=True, valor=75)
            acoes.append("Luzes compensando pouca luz natural")
        else:
            luzes_ligadas = [d for d in self.dispositivos.values()
                             if d.tipo == "luz" and d.ligado]
            for l in luzes_ligadas:
                l.valor = max(30, l.valor - 20)
            if luzes_ligadas:
                acoes.append("Brilho reduzido — aproveitar luz natural")

        # Volume adaptativo ao horário
        if 7 <= hora < 22:
            self._setar("som", valor=50)
        else:
            self._setar("som", valor=20)
            acoes.append("Volume reduzido para horário noturno")

        self._ajustes_log.append({
            "timestamp": time.time(),
            "temp_ext": temp_ext,
            "chuva": chuva,
            "hora": hora,
            "acoes": acoes
        })
        return acoes

    def aplicar_perfil(self, nome: str) -> str:
        if nome not in self.PERFIS:
            return f"Perfil '{nome}' não existe. Disponíveis: {', '.join(self.PERFIS)}"
        perfil = self.PERFIS[nome]
        self._setar("luz", valor=perfil["brilho"])
        self._setar("som", valor=perfil["volume"])
        self._setar("climatizacao", valor=perfil["temp_alvo"])
        self._perfil_ativo = nome
        musica = f" | Música: {perfil['musica']}" if perfil["musica"] else ""
        return (f"Perfil '{nome}' ativado: brilho={perfil['brilho']}% "
                f"volume={perfil['volume']}% temp={perfil['temp_alvo']}°C{musica}")

    def ajuste_por_conforto(self, leitura: LeituraAmbiente) -> List[str]:
        acoes = []
        if leitura.temperatura > 26:
            self._setar("climatizacao", ligado=True, valor=22)
            acoes.append(f"AC ligado: {leitura.temperatura}°C detectado")
        if leitura.umidade < 30:
            acoes.append("Umidade baixa — considere ligar umidificador")
        if leitura.umidade > 70:
            acoes.append("Umidade alta — ventilação recomendada")
        if leitura.co2 > 1000:
            acoes.append(f"CO₂ alto ({leitura.co2:.0f}ppm) — abrindo ventilação")
        if not leitura.presenca:
            self._setar("luz", ligado=False)
            self._setar("som", ligado=False)
            acoes.append("Sala vazia — dispositivos desligados automaticamente")
        return acoes

    def _setar(self, tipo: str, **kwargs):
        for d in self.dispositivos.values():
            if d.tipo == tipo:
                for k, v in kwargs.items():
                    setattr(d, k, v)
                d.ultimo_update = time.time()

    def resumo(self) -> str:
        return (
            f"Perfil ativo: {self._perfil_ativo}\n"
            f"Ajustes recentes: {len(self._ajustes_log)} registros"
        )


# ══════════════════════════════════════════════════════════════
#  ROTEAMENTO DE SINAL — Wi-Fi / Zigbee / Bluetooth
# ══════════════════════════════════════════════════════════════
class RoteadorSinal:
    PRIORIDADES = {
        "wifi":      {"banda": "alta", "alcance": "longo",  "consumo": "alto",  "latencia": "baixa"},
        "zigbee":    {"banda": "baixa","alcance": "médio",  "consumo": "muito_baixo", "latencia": "muito_baixa"},
        "bluetooth": {"banda": "media","alcance": "curto",  "consumo": "baixo", "latencia": "baixa"},
        "zwave":     {"banda": "baixa","alcance": "médio",  "consumo": "muito_baixo", "latencia": "baixa"},
    }

    def __init__(self):
        self._redes_disponiveis: Dict[str, bool] = {
            "wifi": True, "zigbee": False, "bluetooth": True, "zwave": False
        }
        self._sinais: Dict[str, int] = {"wifi": -65, "bluetooth": -70}
        self._lock = threading.Lock()

    def detectar_redes(self) -> Dict[str, bool]:
        import subprocess
        try:
            r = subprocess.run(["nmcli", "-t", "-f", "DEVICE,TYPE,STATE", "device"],
                               capture_output=True, text=True, timeout=5)
            with self._lock:
                if "wifi" in r.stdout.lower():
                    self._redes_disponiveis["wifi"] = True
                if "bluetooth" in r.stdout.lower():
                    self._redes_disponiveis["bluetooth"] = True
        except Exception:
            pass
        return dict(self._redes_disponiveis)

    def melhor_rede(self, tipo_dispositivo: str, prioridade: str = "confiabilidade") -> str:
        """Escolhe a melhor rede para um tipo de dispositivo."""
        with self._lock:
            disponiveis = [r for r, ok in self._redes_disponiveis.items() if ok]

        if not disponiveis:
            return "wifi"  # fallback

        # Regras por tipo de dispositivo
        if tipo_dispositivo in ("sensor", "sensor_temperatura", "sensor_porta"):
            # sensores: prefere Zigbee/Z-Wave (baixo consumo, longa bateria)
            for r in ["zigbee", "zwave"]:
                if r in disponiveis:
                    return r
        elif tipo_dispositivo in ("camera", "tv", "speaker"):
            # streaming: precisa de banda alta
            if "wifi" in disponiveis:
                return "wifi"
        elif tipo_dispositivo in ("lampada", "tomada"):
            # controle: Zigbee > Bluetooth > Wi-Fi
            for r in ["zigbee", "bluetooth", "wifi"]:
                if r in disponiveis:
                    return r

        if prioridade == "economia":
            for r in ["zigbee", "zwave", "bluetooth", "wifi"]:
                if r in disponiveis:
                    return r
        if prioridade == "velocidade":
            for r in ["wifi", "bluetooth", "zigbee", "zwave"]:
                if r in disponiveis:
                    return r

        return disponiveis[0]

    def atribuir_redes(self, dispositivos: Dict[str, "EstadoDispositivo"]) -> List[str]:
        mudancas = []
        for nome, d in dispositivos.items():
            melhor = self.melhor_rede(d.tipo)
            if d.rede != melhor:
                mudancas.append(f"{nome}: {d.rede} → {melhor}")
                d.rede = melhor
        return mudancas

    def status(self) -> str:
        with self._lock:
            linhas = ["REDES DISPONÍVEIS:"]
            for rede, ok in self._redes_disponiveis.items():
                sinal = self._sinais.get(rede, "N/A")
                estado = f"✓ {sinal}dBm" if ok and isinstance(sinal, int) else ("✓" if ok else "✗")
                linhas.append(f"  {rede.capitalize():12} {estado}")
        return "\n".join(linhas)

    def forcar_rede(self, rede: str, disponivel: bool) -> str:
        if rede not in self._redes_disponiveis:
            return f"Rede '{rede}' não reconhecida"
        with self._lock:
            self._redes_disponiveis[rede] = disponivel
        return f"Rede {rede}: {'ativa' if disponivel else 'inativa'}"


# ══════════════════════════════════════════════════════════════
#  GEOFENCING — dispositivos por localização GPS
# ══════════════════════════════════════════════════════════════
class Geofencing:
    DATA_PATH = Path.home() / ".iris" / "geofence.json"

    def __init__(self):
        self.zonas: Dict[str, ZonaGeofence] = {}
        self._posicao_atual: Optional[Tuple[float, float]] = None
        self._dentro_das_zonas: set = set()
        self._callbacks_entrada: Dict[str, List[Callable]] = {}
        self._callbacks_saida: Dict[str, List[Callable]] = {}
        self._monitorando = False
        self._carregar()

    def _carregar(self):
        try:
            if self.DATA_PATH.exists():
                data = json.loads(self.DATA_PATH.read_text())
                for nome, z in data.items():
                    self.zonas[nome] = ZonaGeofence(**z)
        except Exception as e:
            logging.exception(e)

    def _salvar(self):
        try:
            self.DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
            data = {k: asdict(v) for k, v in self.zonas.items()}
            self.DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2))
        except Exception as e:
            logging.exception(e)

    def adicionar_zona(self, nome: str, lat: float, lon: float, raio: float = 200) -> str:
        self.zonas[nome] = ZonaGeofence(nome=nome, lat=lat, lon=lon, raio_m=raio)
        self._salvar()
        return f"Zona '{nome}' criada: {lat:.4f},{lon:.4f} raio={raio}m"

    def remover_zona(self, nome: str) -> str:
        if nome not in self.zonas:
            return f"Zona '{nome}' não encontrada"
        del self.zonas[nome]
        self._salvar()
        return f"Zona '{nome}' removida"

    @staticmethod
    def _distancia_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6_371_000.0
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    def verificar_posicao(self, lat: float, lon: float) -> Dict[str, bool]:
        self._posicao_atual = (lat, lon)
        resultado = {}
        for nome, zona in self.zonas.items():
            if not zona.ativa:
                continue
            dist = self._distancia_m(lat, lon, zona.lat, zona.lon)
            dentro = dist <= zona.raio_m
            resultado[nome] = dentro

            if dentro and nome not in self._dentro_das_zonas:
                self._dentro_das_zonas.add(nome)
                for cb in self._callbacks_entrada.get(nome, []):
                    try:
                        cb(nome, dist)
                    except Exception:
                        pass
            elif not dentro and nome in self._dentro_das_zonas:
                self._dentro_das_zonas.discard(nome)
                for cb in self._callbacks_saida.get(nome, []):
                    try:
                        cb(nome, dist)
                    except Exception:
                        pass
        return resultado

    def ao_entrar(self, zona: str, callback):
        self._callbacks_entrada.setdefault(zona, []).append(callback)

    def ao_sair(self, zona: str, callback):
        self._callbacks_saida.setdefault(zona, []).append(callback)

    def obter_gps_ip(self) -> Optional[Tuple[float, float]]:
        try:
            import requests
            r = requests.get("https://ipapi.co/json/", timeout=5).json()
            lat, lon = float(r["latitude"]), float(r["longitude"])
            self._posicao_atual = (lat, lon)
            return lat, lon
        except Exception as e:
            logging.exception(e)
            return None

    def status(self) -> str:
        if not self.zonas:
            return "Nenhuma zona de geofence configurada. Use: geofence adiciona [nome] [lat] [lon]"
        linhas = ["GEOFENCING:"]
        if self._posicao_atual:
            linhas.append(f"  Posição atual: {self._posicao_atual[0]:.4f}, {self._posicao_atual[1]:.4f}")
        for nome, zona in self.zonas.items():
            dentro = "📍 DENTRO" if nome in self._dentro_das_zonas else "○ fora"
            linhas.append(f"  {nome}: {dentro} (raio={zona.raio_m}m)")
        return "\n".join(linhas)


# ══════════════════════════════════════════════════════════════
#  HUB PRINCIPAL — integra tudo
# ══════════════════════════════════════════════════════════════
class SmartHomeHub:
    DATA_PATH = Path.home() / ".iris" / "smarthome.json"

    def __init__(self, ia=None):
        self.ia = ia
        self.dispositivos: Dict[str, EstadoDispositivo] = {}
        self.sensores = FusaoSensores()
        self.ajuste = AjusteDinamico(self.dispositivos)
        self.roteador = RoteadorSinal()
        self.geo = Geofencing()
        self._carregar()
        self._adicionar_dispositivos_padrao()
        self._configurar_geofence_padrao()

    def _adicionar_dispositivos_padrao(self):
        if not self.dispositivos:
            defaults = [
                EstadoDispositivo("Luz Sala", "luz", ligado=False, valor=70),
                EstadoDispositivo("Luz Quarto", "luz", ligado=False, valor=50),
                EstadoDispositivo("Ar Condicionado", "climatizacao", ligado=False, valor=22),
                EstadoDispositivo("Som Sala", "som", ligado=False, valor=40),
                EstadoDispositivo("Tomada PC", "tomada", ligado=True, consumo_w=180),
                EstadoDispositivo("Sensor Sala", "sensor", ligado=True),
                EstadoDispositivo("TV Sala", "tv", ligado=False),
            ]
            for d in defaults:
                d.rede = self.roteador.melhor_rede(d.tipo)
                self.dispositivos[d.nome] = d

    def _configurar_geofence_padrao(self):
        if not self.geo.zonas:
            self.geo.ao_entrar("casa", lambda nome, dist:
                self._acao_geofence_entrada("casa"))
            self.geo.ao_sair("casa", lambda nome, dist:
                self._acao_geofence_saida("casa"))

    def _acao_geofence_entrada(self, zona: str):
        if zona == "casa":
            self.dispositivos["Luz Sala"].ligado = True
            self.dispositivos["Ar Condicionado"].ligado = True
            logging.info("Geofence: entrou em casa — casa preparada")

    def _acao_geofence_saida(self, zona: str):
        if zona == "casa":
            for d in self.dispositivos.values():
                if d.tipo in ("luz", "som"):
                    d.ligado = False
            logging.info("Geofence: saiu de casa — dispositivos desligados")

    def _carregar(self):
        try:
            if self.DATA_PATH.exists():
                data = json.loads(self.DATA_PATH.read_text())
                for nome, d in data.items():
                    self.dispositivos[nome] = EstadoDispositivo(**d)
        except Exception as e:
            logging.exception(e)

    def salvar(self):
        try:
            self.DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
            data = {k: asdict(v) for k, v in self.dispositivos.items()}
            self.DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2))
        except Exception as e:
            logging.exception(e)

    def adicionar_dispositivo(self, nome: str, tipo: str) -> str:
        rede = self.roteador.melhor_rede(tipo)
        self.dispositivos[nome] = EstadoDispositivo(nome=nome, tipo=tipo, rede=rede)
        self.salvar()
        return f"Dispositivo '{nome}' ({tipo}) adicionado via {rede}"

    def controlar(self, nome: str, ligado: Optional[bool] = None, valor: Optional[float] = None) -> str:
        # busca por nome parcial
        alvo = next((d for n, d in self.dispositivos.items()
                     if nome.lower() in n.lower()), None)
        if not alvo:
            return f"Dispositivo '{nome}' não encontrado"
        if ligado is not None:
            alvo.ligado = ligado
        if valor is not None:
            alvo.valor = max(0.0, min(100.0, valor))
        alvo.ultimo_update = time.time()
        self.salvar()
        estado = "ligado" if alvo.ligado else "desligado"
        return f"{alvo.nome}: {estado}" + (f" | valor={alvo.valor:.0f}" if valor is not None else "")

    def painel_status(self) -> str:
        linhas = ["╔═══════════ SMART HOME ═══════════╗"]
        for nome, d in self.dispositivos.items():
            icone = {"luz": "💡", "climatizacao": "❄️", "som": "🔊",
                     "tomada": "🔌", "sensor": "📡", "tv": "📺"}.get(d.tipo, "•")
            estado = "ON" if d.ligado else "off"
            val = f" {d.valor:.0f}%" if d.valor > 0 else ""
            linhas.append(f"  {icone} {nome:<20} {estado}{val} [{d.rede}]")
        # sensores
        fusao = self.sensores.fusao()
        linhas.append("╠════════════ SENSORES ════════════╣")
        linhas.append(f"  🌡 {fusao.temperatura}°C  💧{fusao.umidade}%  "
                      f"{'👤 presente' if fusao.presenca else '○ vazio'}")
        linhas.append(f"  Conforto: {fusao.conforto_score()}/100")
        linhas.append("╚══════════════════════════════════╝")
        return "\n".join(linhas)

    def atualizar_clima_e_ajustar(self, cidade: str = "São Paulo", ia=None) -> str:
        import requests
        from .config import OPENWEATHER_KEY
        acoes = []
        hora = datetime.now().hour
        try:
            if OPENWEATHER_KEY:
                r = requests.get(
                    f"https://api.openweathermap.org/data/2.5/weather?q={cidade}"
                    f"&appid={OPENWEATHER_KEY}&units=metric&lang=pt_br",
                    timeout=8).json()
                temp = r["main"]["temp"]
                chuva = "rain" in r.get("weather", [{}])[0].get("main", "").lower()
            else:
                r = requests.get(f"https://wttr.in/{cidade}?format=j1", timeout=8).json()
                temp = float(r["current_condition"][0]["temp_C"])
                chuva = int(r["current_condition"][0]["precipMM"]) > 0
            acoes = self.ajuste.ajustar_por_clima(temp, chuva, hora)
            self.salvar()
            resultado = (f"Clima em {cidade}: {temp:.1f}°C {'🌧 chuva' if chuva else '☀️'}\n"
                         f"Ajustes automáticos:\n" + "\n".join(f"  • {a}" for a in acoes))
            return resultado
        except Exception as e:
            logging.exception(e)
            return f"Erro ao buscar clima: {e}"

    def modo_ausente(self) -> str:
        desligados = []
        for d in self.dispositivos.values():
            if d.tipo in ("luz", "som", "tv"):
                d.ligado = False
                desligados.append(d.nome)
        self.salvar()
        return "Modo ausente: " + ", ".join(desligados) + " desligados"

    def modo_chegada(self) -> str:
        self.dispositivos.get("Luz Sala") and setattr(
            self.dispositivos["Luz Sala"], "ligado", True)
        self.dispositivos.get("Ar Condicionado") and setattr(
            self.dispositivos["Ar Condicionado"], "ligado", True)
        self.salvar()
        return "Bem-vindo! Luz e climatização preparadas"

    def consumo_total(self) -> str:
        total = sum(d.consumo_w for d in self.dispositivos.values() if d.ligado)
        return f"Consumo atual: {total:.0f}W estimado"


from typing import Callable  # usado nos callbacks de geofence
