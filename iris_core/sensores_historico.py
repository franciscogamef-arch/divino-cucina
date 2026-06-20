"""
IRIS v2.0 — Histórico de Sensores com Gráficos
Armazena séries temporais e gera gráficos ASCII e PNG
"""
import json, time, math, logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict, field


@dataclass
class PontoSensor:
    timestamp: float
    temperatura: float
    umidade: float
    presenca: bool
    co2: float
    luminosidade: float
    consumo_w: float = 0.0
    conforto: float = 0.0


# ══════════════════════════════════════════════════════════════
#  SÉRIES TEMPORAIS — persiste no disco, carrega na inicialização
# ══════════════════════════════════════════════════════════════
class SeriesTempo:
    DATA_PATH = Path.home() / ".iris" / "sensores_historico.json"
    MAX_PONTOS = 2880  # 48h em intervalos de 1min

    def __init__(self):
        self._dados: List[PontoSensor] = []
        self._carregar()

    def _carregar(self):
        try:
            if self.DATA_PATH.exists():
                raw = json.loads(self.DATA_PATH.read_text())
                self._dados = [PontoSensor(**p) for p in raw]
                logging.info("Histórico de sensores: %d pontos carregados", len(self._dados))
        except Exception as e:
            logging.exception(e)
            self._dados = []

    def salvar(self):
        try:
            self.DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
            data = [asdict(p) for p in self._dados[-self.MAX_PONTOS:]]
            self.DATA_PATH.write_text(json.dumps(data))
        except Exception as e:
            logging.exception(e)

    def registrar(self, ponto: PontoSensor):
        self._dados.append(ponto)
        if len(self._dados) > self.MAX_PONTOS:
            self._dados = self._dados[-self.MAX_PONTOS:]
        if len(self._dados) % 10 == 0:  # salva a cada 10 pontos
            self.salvar()

    def ultimas(self, n: int = 60) -> List[PontoSensor]:
        return self._dados[-n:]

    def periodo(self, horas: float = 24.0) -> List[PontoSensor]:
        corte = time.time() - horas * 3600
        return [p for p in self._dados if p.timestamp >= corte]

    def estatisticas(self, horas: float = 24.0) -> Dict[str, dict]:
        dados = self.periodo(horas)
        if not dados:
            return {}

        def stats(valores):
            if not valores:
                return {}
            return {
                "min": round(min(valores), 1),
                "max": round(max(valores), 1),
                "media": round(sum(valores) / len(valores), 1),
                "atual": round(valores[-1], 1)
            }

        return {
            "temperatura": stats([p.temperatura for p in dados]),
            "umidade":     stats([p.umidade for p in dados]),
            "co2":         stats([p.co2 for p in dados]),
            "consumo":     stats([p.consumo_w for p in dados]),
            "conforto":    stats([p.conforto for p in dados]),
            "presenca_pct": round(sum(1 for p in dados if p.presenca) / len(dados) * 100, 1),
            "total_pontos": len(dados)
        }


# ══════════════════════════════════════════════════════════════
#  GRÁFICOS ASCII — funciona sempre, sem dependências extras
# ══════════════════════════════════════════════════════════════
class GraficoASCII:
    LARGURA = 60
    ALTURA = 10

    @classmethod
    def linha(cls, valores: List[float], titulo: str = "",
              unidade: str = "", cor: bool = True) -> str:
        if not valores:
            return f"{titulo}: sem dados"

        # normaliza para 0-ALTURA
        vmin, vmax = min(valores), max(valores)
        faixa = vmax - vmin if vmax != vmin else 1.0

        # reduz para a largura do gráfico
        n = len(valores)
        if n > cls.LARGURA:
            step = n / cls.LARGURA
            vals_plot = [valores[int(i * step)] for i in range(cls.LARGURA)]
        else:
            vals_plot = valores + [valores[-1]] * (cls.LARGURA - n)

        # monta a grade
        grade = [[" "] * cls.LARGURA for _ in range(cls.ALTURA)]
        for x, v in enumerate(vals_plot):
            y = int((v - vmin) / faixa * (cls.ALTURA - 1))
            y = max(0, min(cls.ALTURA - 1, y))
            grade[cls.ALTURA - 1 - y][x] = "█"

        linhas = []
        if titulo:
            linhas.append(f"┌─ {titulo} ({'%.1f' % vmin} ~ {'%.1f' % vmax}{unidade}) ─")
        for row in grade:
            linhas.append("│" + "".join(row))
        linhas.append("└" + "─" * cls.LARGURA)
        return "\n".join(linhas)

    @classmethod
    def barra_horizontal(cls, nome: str, valor: float,
                         vmin: float = 0, vmax: float = 100,
                         unidade: str = "", largura: int = 30) -> str:
        pct = max(0.0, min(1.0, (valor - vmin) / (vmax - vmin) if vmax != vmin else 0))
        cheias = int(pct * largura)
        barra = "█" * cheias + "░" * (largura - cheias)
        return f"  {nome:<18} [{barra}] {valor:.1f}{unidade}"

    @classmethod
    def mini_sparkline(cls, valores: List[float], largura: int = 20) -> str:
        chars = " ▁▂▃▄▅▆▇█"
        if not valores:
            return " " * largura
        vmin, vmax = min(valores), max(valores)
        faixa = vmax - vmin if vmax != vmin else 1.0
        n = len(valores)
        if n > largura:
            step = n / largura
            vals = [valores[int(i * step)] for i in range(largura)]
        else:
            vals = valores + [vmin] * (largura - n)
        return "".join(chars[int((v - vmin) / faixa * 8)] for v in vals)

    @classmethod
    def painel_resumo(cls, series: "SeriesTempo", horas: float = 6.0) -> str:
        dados = series.periodo(horas)
        if not dados:
            return "Sem dados de sensores ainda. Leituras serão coletadas automaticamente."

        stats = series.estatisticas(horas)
        linhas = [f"╔══════ HISTÓRICO DE SENSORES (últimas {horas:.0f}h) ══════╗"]

        for campo, label, unid, vmin, vmax in [
            ("temperatura", "Temperatura", "°C", 15, 35),
            ("umidade",     "Umidade",     "%",  0,  100),
            ("co2",         "CO₂",         "ppm", 300, 1500),
            ("consumo",     "Consumo",     "W",  0,  2000),
            ("conforto",    "Conforto",    "/100", 0, 100),
        ]:
            if campo not in stats:
                continue
            s = stats[campo]
            vals = [getattr(p, campo) for p in dados]
            spark = cls.mini_sparkline(vals, largura=25)
            linhas.append(
                f"  {label:<12} {spark}  {s['atual']:.1f}{unid} "
                f"(↓{s['min']} ↑{s['max']} ø{s['media']})"
            )

        presenca = stats.get("presenca_pct", 0)
        linhas.append(f"  Presença detectada: {presenca:.0f}% do tempo")
        linhas.append(f"  Amostras: {stats.get('total_pontos', 0)}")
        linhas.append("╚══════════════════════════════════════════════╝")
        return "\n".join(linhas)


# ══════════════════════════════════════════════════════════════
#  GRÁFICOS PNG — opcional, usa matplotlib se instalado
# ══════════════════════════════════════════════════════════════
class GraficoPNG:
    @staticmethod
    def disponivel() -> bool:
        try:
            import matplotlib
            return True
        except ImportError:
            return False

    @staticmethod
    def gerar(series: "SeriesTempo", horas: float = 24.0,
              destino: Optional[str] = None) -> str:
        if not GraficoPNG.disponivel():
            return "matplotlib não instalado. Use: pip install matplotlib"

        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates

        dados = series.periodo(horas)
        if not dados:
            return "Sem dados para plotar"

        dts = [datetime.fromtimestamp(p.timestamp) for p in dados]
        fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
        fig.patch.set_facecolor("#0a0a1a")

        def plot_eixo(ax, vals, label, cor, unidade, ymin=None, ymax=None):
            ax.set_facecolor("#0d0d2b")
            ax.plot(dts, vals, color=cor, linewidth=1.5, alpha=0.9)
            ax.fill_between(dts, vals, alpha=0.15, color=cor)
            ax.set_ylabel(f"{label} ({unidade})", color="white", fontsize=9)
            ax.tick_params(colors="gray", labelsize=8)
            for spine in ax.spines.values():
                spine.set_color("#333366")
            ax.grid(True, color="#1a1a3e", linewidth=0.5)
            if ymin is not None:
                ax.set_ylim(ymin, ymax)

        plot_eixo(axes[0], [p.temperatura for p in dados],
                  "Temperatura", "#ff6b6b", "°C", 10, 40)
        plot_eixo(axes[1], [p.umidade for p in dados],
                  "Umidade", "#4ecdc4", "%", 0, 100)
        plot_eixo(axes[2], [p.consumo_w for p in dados],
                  "Consumo", "#ffe66d", "W")

        axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        axes[-1].tick_params(axis="x", colors="gray", labelsize=8)

        titulo = f"IRIS — Sensores ({horas:.0f}h)"
        fig.suptitle(titulo, color="white", fontsize=12, fontweight="bold")
        plt.tight_layout(rect=[0, 0, 1, 0.96])

        if not destino:
            nome = f"sensores_{datetime.now().strftime('%d%m%Y_%H%M')}.png"
            destino = str(Path.home() / "Pictures" / nome)
        Path(destino).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(destino, dpi=120, bbox_inches="tight",
                    facecolor=fig.get_facecolor())
        plt.close()
        return f"Gráfico salvo: {destino}"


# ══════════════════════════════════════════════════════════════
#  COLETOR AUTOMÁTICO — lê smartohme e registra em background
# ══════════════════════════════════════════════════════════════
class ColetorSensores:
    def __init__(self, series: SeriesTempo, smarthome=None, intervalo: int = 60):
        self.series = series
        self.smarthome = smarthome
        self.intervalo = intervalo
        self._ativo = False

    def iniciar(self):
        import threading
        self._ativo = True
        threading.Thread(target=self._loop, daemon=True).start()
        logging.info("ColetorSensores iniciado (intervalo=%ds)", self.intervalo)

    def parar(self):
        self._ativo = False

    def _loop(self):
        import time as _time
        while self._ativo:
            try:
                self._coletar()
            except Exception as e:
                logging.exception(e)
            _time.sleep(self.intervalo)

    def _coletar(self):
        import time as _time
        if not self.smarthome:
            return
        fusao = self.smarthome.sensores.fusao()
        consumo = sum(d.consumo_w for d in self.smarthome.dispositivos.values()
                      if d.ligado)
        ponto = PontoSensor(
            timestamp=_time.time(),
            temperatura=fusao.temperatura,
            umidade=fusao.umidade,
            presenca=fusao.presenca,
            co2=fusao.co2,
            luminosidade=fusao.luminosidade,
            consumo_w=consumo,
            conforto=fusao.conforto_score()
        )
        self.series.registrar(ponto)

    def status(self) -> str:
        return (f"Coletor: {'ativo' if self._ativo else 'parado'} | "
                f"Intervalo: {self.intervalo}s | "
                f"Pontos: {len(self.series._dados)}")
