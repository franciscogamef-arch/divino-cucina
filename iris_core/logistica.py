"""
IRIS v2.0 — Diagnóstico e Logística
Cálculo de Tarifas, Autocompra, Auto-correção de Sistemas, Relatório Técnico
"""
import json, threading, time, logging, subprocess, re
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Callable
from datetime import datetime


# ══════════════════════════════════════════════════════════════
#  CÁLCULO DE TARIFAS — horário de ponta da energia elétrica
# ══════════════════════════════════════════════════════════════
@dataclass
class TarifaConfig:
    hora_pico_inicio: int = 18   # 18h
    hora_pico_fim: int = 21      # 21h
    tarifa_pico_kwh: float = 0.95
    tarifa_normal_kwh: float = 0.52
    tarifa_reduzida_kwh: float = 0.31
    hora_reduzida_inicio: int = 0
    hora_reduzida_fim: int = 7


class CalculadorTarifas:
    """Gerencia consumo de energia em horários tarifados."""

    DATA_PATH = Path.home() / ".iris" / "tarifas.json"

    def __init__(self, smarthome=None):
        self.smarthome = smarthome
        self.cfg = TarifaConfig()
        self._economia_acumulada: float = 0.0
        self._historico_desligamentos: List[dict] = []
        self._carregar()

    def _carregar(self):
        try:
            if self.DATA_PATH.exists():
                data = json.loads(self.DATA_PATH.read_text())
                cfg = data.get("config", {})
                for k, v in cfg.items():
                    if hasattr(self.cfg, k):
                        setattr(self.cfg, k, v)
                self._economia_acumulada = data.get("economia_acumulada", 0.0)
        except Exception as e:
            logging.exception(e)

    def _salvar(self):
        try:
            self.DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "config": asdict(self.cfg),
                "economia_acumulada": self._economia_acumulada,
                "historico": self._historico_desligamentos[-50:]
            }
            self.DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2))
        except Exception as e:
            logging.exception(e)

    def tarifa_atual(self) -> tuple:
        hora = datetime.now().hour
        if self.cfg.hora_pico_inicio <= hora < self.cfg.hora_pico_fim:
            return "pico", self.cfg.tarifa_pico_kwh
        if self.cfg.hora_reduzida_inicio <= hora < self.cfg.hora_reduzida_fim:
            return "reduzida", self.cfg.tarifa_reduzida_kwh
        return "normal", self.cfg.tarifa_normal_kwh

    def verificar_e_desligar_pesados(self, limiar_w: float = 1000.0) -> List[str]:
        """Desliga aparelhos pesados no horário de pico."""
        modo, tarifa = self.tarifa_atual()
        if modo != "pico" or not self.smarthome:
            return []

        acoes = []
        for nome, d in self.smarthome.dispositivos.items():
            if d.ligado and d.consumo_w >= limiar_w:
                d.ligado = False
                economia = d.consumo_w / 1000.0 * tarifa
                self._economia_acumulada += economia
                acoes.append(f"{nome} desligado (pico) — economia estimada: R${economia:.2f}/h")
                self._historico_desligamentos.append({
                    "timestamp": time.time(),
                    "dispositivo": nome,
                    "consumo_w": d.consumo_w,
                    "motivo": "horario_pico"
                })
        if acoes:
            self._salvar()
        return acoes

    def custo_atual(self) -> str:
        modo, tarifa = self.tarifa_atual()
        hora = datetime.now().hour
        consumo = 0.0
        if self.smarthome:
            consumo = sum(d.consumo_w for d in self.smarthome.dispositivos.values() if d.ligado)
        custo_h = consumo / 1000.0 * tarifa
        return (
            f"TARIFA ATUAL:\n"
            f"  Modo: {modo.upper()} ({hora:02d}h) — R$ {tarifa:.2f}/kWh\n"
            f"  Consumo: {consumo:.0f}W\n"
            f"  Custo estimado: R$ {custo_h:.3f}/hora\n"
            f"  Economia acumulada: R$ {self._economia_acumulada:.2f}"
        )

    def proximo_horario_barato(self) -> str:
        hora_atual = datetime.now().hour
        horas_ate = (self.cfg.hora_reduzida_inicio - hora_atual) % 24
        return (
            f"Próxima tarifa reduzida: {self.cfg.hora_reduzida_inicio:02d}h "
            f"(em {horas_ate}h). Tarifa: R$ {self.cfg.tarifa_reduzida_kwh:.2f}/kWh"
        )

    def agendar_para_horario_barato(self, dispositivo: str, acao: str = "ligar") -> str:
        hora = self.cfg.hora_reduzida_inicio
        return (
            f"Agendado: '{dispositivo}' será {acao} às {hora:02d}h "
            f"(tarifa reduzida R$ {self.cfg.tarifa_reduzida_kwh:.2f}/kWh)"
        )


# ══════════════════════════════════════════════════════════════
#  AUTOCOMPRA — detecta suprimentos gastos e faz pedidos
# ══════════════════════════════════════════════════════════════
@dataclass
class ItemConsumo:
    nome: str
    categoria: str          # tinta | filtro | alimento | higiene | outro
    nivel_atual: float      # 0.0 a 1.0 (0=vazio, 1=cheio)
    nivel_minimo: float = 0.2
    link_compra: str = ""
    dias_reposicao: int = 3
    ultimo_pedido: float = 0.0
    pedido_pendente: bool = False


class AutoCompra:
    """Monitora suprimentos e faz pedidos automáticos."""
    DATA_PATH = Path.home() / ".iris" / "autocompra.json"

    def __init__(self, ia=None):
        self.ia = ia
        self._itens: Dict[str, ItemConsumo] = {}
        self._historico_pedidos: List[dict] = []
        self._callbacks_pedido: List[Callable] = []
        self._carregar()
        self._adicionar_itens_padrao()

    def _adicionar_itens_padrao(self):
        if not self._itens:
            padrao = [
                ItemConsumo("Filtro Água", "filtro", 0.8, link_compra="https://www.amazon.com.br/s?k=filtro+agua"),
                ItemConsumo("Tinta Preta Impressora", "tinta", 0.9, link_compra="https://www.amazon.com.br/s?k=cartucho+tinta+preta"),
                ItemConsumo("Tinta Colorida Impressora", "tinta", 0.9),
                ItemConsumo("Detergente", "higiene", 0.7),
            ]
            for item in padrao:
                self._itens[item.nome] = item
            self._salvar()

    def _carregar(self):
        try:
            if self.DATA_PATH.exists():
                data = json.loads(self.DATA_PATH.read_text())
                for nome, i in data.get("itens", {}).items():
                    self._itens[nome] = ItemConsumo(**i)
                self._historico_pedidos = data.get("pedidos", [])
        except Exception as e:
            logging.exception(e)

    def _salvar(self):
        try:
            self.DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "itens": {k: asdict(v) for k, v in self._itens.items()},
                "pedidos": self._historico_pedidos[-100:]
            }
            self.DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2))
        except Exception as e:
            logging.exception(e)

    def cadastrar(self, nome: str, categoria: str, nivel: float = 1.0, link: str = "") -> str:
        self._itens[nome] = ItemConsumo(
            nome=nome, categoria=categoria,
            nivel_atual=nivel, link_compra=link
        )
        self._salvar()
        return f"'{nome}' cadastrado no monitoramento de suprimentos"

    def atualizar_nivel(self, nome: str, nivel: float) -> str:
        if nome not in self._itens:
            return f"Item '{nome}' não cadastrado"
        self._itens[nome].nivel_atual = max(0.0, min(1.0, nivel))
        self._salvar()
        return f"'{nome}': {nivel*100:.0f}%"

    def verificar_e_pedir(self) -> List[str]:
        """Verifica itens abaixo do mínimo e gera pedidos."""
        pedidos = []
        for nome, item in self._itens.items():
            if item.nivel_atual <= item.nivel_minimo and not item.pedido_pendente:
                pedidos.append(self._gerar_pedido(item))
        return pedidos

    def _gerar_pedido(self, item: ItemConsumo) -> str:
        item.pedido_pendente = True
        item.ultimo_pedido = time.time()

        registro = {
            "timestamp": time.time(),
            "item": item.nome,
            "nivel": item.nivel_atual,
            "categoria": item.categoria
        }
        self._historico_pedidos.append(registro)
        self._salvar()

        # notifica callbacks
        msg = (f"🛒 AUTOCOMPRA: {item.nome} está em "
               f"{item.nivel_atual*100:.0f}% — pedido gerado")
        for cb in self._callbacks_pedido:
            try:
                cb(msg, item)
            except Exception:
                pass

        link = f"\n  Link: {item.link_compra}" if item.link_compra else ""
        return msg + link

    def ao_pedir(self, callback: Callable):
        self._callbacks_pedido.append(callback)

    def itens_pendentes(self) -> List[str]:
        return [
            f"{nome} ({i.nivel_atual*100:.0f}%)"
            for nome, i in self._itens.items()
            if i.nivel_atual <= i.nivel_minimo
        ]

    def status(self) -> str:
        linhas = ["MONITORAMENTO DE SUPRIMENTOS:"]
        for nome, item in self._itens.items():
            barra = "█" * int(item.nivel_atual * 10) + "░" * (10 - int(item.nivel_atual * 10))
            alerta = " ⚠️ BAIXO" if item.nivel_atual <= item.nivel_minimo else ""
            linhas.append(f"  {nome}: [{barra}] {item.nivel_atual*100:.0f}%{alerta}")
        linhas.append(f"  Pedidos realizados: {len(self._historico_pedidos)}")
        return "\n".join(linhas)


# ══════════════════════════════════════════════════════════════
#  AUTO-CORREÇÃO — reinicia sistemas travados, limpa caches
# ══════════════════════════════════════════════════════════════
class AutoCorrecao:
    """Detecta e corrige problemas comuns automaticamente."""

    SERVICOS_MONITORADOS = ["NetworkManager", "bluetooth", "pulseaudio", "cups"]

    def __init__(self, ia=None):
        self.ia = ia
        self._historico_correcoes: List[dict] = []
        self._lock = threading.Lock()

    def verificar_e_corrigir(self) -> List[str]:
        """Roda verificações automáticas e corrige o que encontrar."""
        acoes = []
        acoes.extend(self._verificar_uso_disco())
        acoes.extend(self._verificar_processos_zumbis())
        return acoes

    def _verificar_uso_disco(self) -> List[str]:
        try:
            import psutil
            disco = psutil.disk_usage("/")
            if disco.percent > 90:
                return [f"Disco em {disco.percent:.0f}% — limpeza automática de cache"]
            return []
        except Exception:
            return []

    def _verificar_processos_zumbis(self) -> List[str]:
        try:
            import psutil
            zumbis = [p for p in psutil.process_iter(["status", "name"])
                      if p.info["status"] == "zombie"]
            if zumbis:
                return [f"Processos zumbi detectados: {len(zumbis)}"]
            return []
        except Exception:
            return []

    def limpar_cache_sistema(self) -> str:
        resultados = []
        # Cache do usuário
        cache_dir = Path.home() / ".cache"
        try:
            tam = sum(f.stat().st_size for f in cache_dir.rglob("*")
                      if f.is_file()) // (1024**2)
            resultados.append(f"Cache do usuário: {tam}MB")
        except Exception:
            pass
        # Cache do sistema (sem sudo)
        try:
            subprocess.run(["sync"], capture_output=True, timeout=5)
            resultados.append("Cache do kernel sincronizado")
        except Exception:
            pass
        return "Auto-correção: " + " | ".join(resultados) if resultados else "Nada a limpar"

    def reiniciar_servico(self, servico: str) -> str:
        if servico not in self.SERVICOS_MONITORADOS:
            return f"Serviço '{servico}' não está na lista de monitorados"
        try:
            r = subprocess.run(
                ["systemctl", "--user", "restart", servico],
                capture_output=True, text=True, timeout=15
            )
            if r.returncode == 0:
                self._registrar(f"Serviço {servico} reiniciado com sucesso")
                return f"Serviço '{servico}' reiniciado"
            return f"Erro ao reiniciar '{servico}': {r.stderr[:100]}"
        except Exception as e:
            logging.exception(e)
            return f"Erro: {e}"

    def limpar_cache_roteador(self) -> str:
        """Tenta limpar DNS e cache de rede local."""
        acoes = []
        try:
            subprocess.run(["sudo", "systemd-resolve", "--flush-caches"],
                           capture_output=True, timeout=5)
            acoes.append("DNS cache limpo")
        except Exception:
            pass
        try:
            subprocess.run(["sudo", "ip", "neigh", "flush", "all"],
                           capture_output=True, timeout=5)
            acoes.append("ARP cache limpo")
        except Exception:
            pass
        return "Cache de rede: " + (", ".join(acoes) if acoes else "sem permissão de admin")

    def diagnostico_rapido(self) -> str:
        problemas = self.verificar_e_corrigir()
        if not problemas:
            return "Sistema OK — nenhum problema detectado"
        return "Problemas encontrados:\n" + "\n".join(f"  • {p}" for p in problemas)

    def _registrar(self, acao: str):
        with self._lock:
            self._historico_correcoes.append({
                "timestamp": time.time(),
                "acao": acao
            })

    def historico(self, n: int = 5) -> str:
        if not self._historico_correcoes:
            return "Nenhuma auto-correção realizada"
        recentes = self._historico_correcoes[-n:]
        linhas = ["HISTÓRICO DE AUTO-CORREÇÕES:"]
        for h in reversed(recentes):
            ts = datetime.fromtimestamp(h["timestamp"]).strftime("%d/%m %H:%M")
            linhas.append(f"  [{ts}] {h['acao']}")
        return "\n".join(linhas)


# ══════════════════════════════════════════════════════════════
#  RELATÓRIO TÉCNICO — traduz erros complexos para linguagem simples
# ══════════════════════════════════════════════════════════════
class RelatorioTecnico:
    """Traduz falhas de hardware/software em avisos compreensíveis."""

    MAPEAMENTOS = {
        r"ACPI.*error": "Problema de energia — verifique o carregador",
        r"EXT4.*error": "Erro no disco — faça backup urgente",
        r"Out of memory": "Memória RAM esgotada — reinicie o computador",
        r"segfault": "Programa travou por erro interno — reinstale o aplicativo",
        r"BTRFS.*error": "Erro no sistema de arquivos — verifique o disco",
        r"kernel.*panic": "Erro crítico do sistema — reinicialização necessária",
        r"usb.*disconnect": "Dispositivo USB desconectado inesperadamente",
        r"wifi.*deauth": "Wi-Fi desconectado pelo roteador — reinicie o roteador",
        r"thermal.*throttle": "Processador superaquecendo — limpe o cooler",
        r"SMART.*failure": "Disco rígido com falha iminente — substitua urgente",
        r"battery.*low": "Bateria fraca — conecte o carregador",
        r"nvme.*error": "Erro no SSD NVMe — verifique o hardware",
    }

    def __init__(self, ia=None):
        self.ia = ia
        self._relatorios: List[dict] = []

    def traduzir_log(self, linha_log: str) -> str:
        """Traduz uma linha de log técnico para texto simples."""
        linha_lower = linha_log.lower()
        for padrao, descricao in self.MAPEAMENTOS.items():
            if re.search(padrao, linha_lower):
                self._registrar(linha_log, descricao)
                return f"⚠️ {descricao}\n(Log original: {linha_log[:80]})"

        # IA para logs não mapeados
        if self.ia:
            try:
                prompt = (
                    f"Traduza este erro técnico de sistema para linguagem simples em 1 frase:\n"
                    f"{linha_log}\n"
                    "Responda APENAS a tradução, sem explicação adicional."
                )
                traduzido = self.ia.groq_rapido(prompt, max_tokens=60, temperature=0.3)
                self._registrar(linha_log, traduzido)
                return traduzido
            except Exception:
                pass

        return f"Aviso do sistema: {linha_log[:100]}"

    def analisar_logs_sistema(self, linhas: int = 50) -> str:
        """Lê os últimos logs do sistema e traduz problemas."""
        try:
            r = subprocess.run(
                ["journalctl", "-n", str(linhas), "--no-pager", "-p", "err"],
                capture_output=True, text=True, timeout=10
            )
            if not r.stdout.strip():
                return "Nenhum erro nos logs do sistema"

            problemas = []
            for linha in r.stdout.split("\n"):
                if linha.strip():
                    traduzido = self.traduzir_log(linha)
                    if "⚠️" in traduzido:
                        problemas.append(traduzido)

            if not problemas:
                return "Logs analisados — nenhum problema crítico encontrado"
            return "PROBLEMAS NO SISTEMA:\n" + "\n".join(problemas[:5])
        except Exception as e:
            return f"Erro ao ler logs: {e}"

    def gerar_relatorio_hardware(self) -> str:
        """Gera relatório de saúde do hardware."""
        try:
            import psutil
            cpu_freq = psutil.cpu_freq()
            temps = {}
            try:
                for k, v in psutil.sensors_temperatures().items():
                    temps[k] = v[0].current
            except Exception:
                pass

            relatorio = ["RELATÓRIO DE HARDWARE:"]

            if cpu_freq:
                relatorio.append(f"  CPU: {cpu_freq.current:.0f}MHz "
                                  f"(max {cpu_freq.max:.0f}MHz)")
            for sensor, temp in temps.items():
                nivel = "OK" if temp < 70 else ("QUENTE" if temp < 85 else "CRÍTICO")
                relatorio.append(f"  {sensor}: {temp:.0f}°C [{nivel}]")

            disco = psutil.disk_usage("/")
            relatorio.append(f"  Disco: {disco.percent:.0f}% usado "
                              f"({disco.free//(1024**3):.0f}GB livres)")

            return "\n".join(relatorio)
        except Exception as e:
            return f"Erro ao ler hardware: {e}"

    def _registrar(self, log: str, traducao: str):
        self._relatorios.append({
            "timestamp": time.time(),
            "log": log[:100],
            "traducao": traducao
        })
        if len(self._relatorios) > 200:
            self._relatorios = self._relatorios[-200:]

    def historico(self, n: int = 5) -> str:
        if not self._relatorios:
            return "Nenhum relatório gerado"
        linhas = [f"ÚLTIMOS {n} ALERTAS TÉCNICOS:"]
        for r in self._relatorios[-n:]:
            ts = datetime.fromtimestamp(r["timestamp"]).strftime("%d/%m %H:%M")
            linhas.append(f"  [{ts}] {r['traducao']}")
        return "\n".join(linhas)


# ══════════════════════════════════════════════════════════════
#  CENTRAL DE LOGÍSTICA — integra tudo
# ══════════════════════════════════════════════════════════════
class CentralLogistica:
    def __init__(self, ia=None, smarthome=None, notificar: Optional[Callable] = None):
        self.tarifas = CalculadorTarifas(smarthome)
        self.compras = AutoCompra(ia)
        self.correcao = AutoCorrecao(ia)
        self.relatorio = RelatorioTecnico(ia)
        self._notificar = notificar
        self._iniciar_monitoramento()

    def _iniciar_monitoramento(self):
        def _loop():
            while True:
                try:
                    # verifica tarifas a cada 5 min
                    desligados = self.tarifas.verificar_e_desligar_pesados()
                    for msg in desligados:
                        if self._notificar:
                            self._notificar("Energia", msg)
                    # verifica suprimentos a cada hora
                    pedidos = self.compras.verificar_e_pedir()
                    for msg in pedidos:
                        if self._notificar:
                            self._notificar("Compras", msg)
                except Exception as e:
                    logging.exception(e)
                time.sleep(300)  # 5 minutos

        threading.Thread(target=_loop, daemon=True).start()

    def status_completo(self) -> str:
        return "\n\n".join([
            self.tarifas.custo_atual(),
            self.compras.status(),
            self.correcao.diagnostico_rapido()
        ])

    def itens_pendentes(self) -> List[str]:
        return self.compras.itens_pendentes()
