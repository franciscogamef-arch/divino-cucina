"""
IRIS v2.0 — Mixin Smart Home
Métodos de controle da casa integrados ao Acoes via herança múltipla.
"""
from ..tipos import Pergunta


class SmartHomeMixin:
    """Agrupa todos os métodos de smart home, biometria, segurança e logística."""

    # ══════════════════════════════════════════════════════════════
    #  SMART HOME
    # ══════════════════════════════════════════════════════════════
    def smarthome_painel(self) -> str:
        self._reg("Painel smart home")
        return self.smarthome.painel_status()

    def smarthome_controlar(self, nome: str, ligado=None, valor=None) -> str:
        self._reg(f"Controla dispositivo: {nome}")
        return self.smarthome.controlar(nome, ligado, valor)

    def smarthome_adicionar(self, nome: str, tipo: str) -> str:
        self._reg(f"Adiciona dispositivo: {nome}")
        return self.smarthome.adicionar_dispositivo(nome, tipo)

    def smarthome_perfil(self, perfil: str) -> str:
        self._reg(f"Perfil ambiente: {perfil}")
        return self.smarthome.ajuste.aplicar_perfil(perfil)

    def smarthome_clima_auto(self) -> str:
        self._reg("Ajuste automático por clima")
        from ..config import CIDADE_PADRAO
        return self.smarthome.atualizar_clima_e_ajustar(CIDADE_PADRAO, self.ia)

    def smarthome_modo_ausente(self) -> str:
        self._reg("Modo ausente")
        return self.smarthome.modo_ausente()

    def smarthome_modo_chegada(self) -> str:
        self._reg("Modo chegada")
        return self.smarthome.modo_chegada()

    def smarthome_fusao_sensores(self) -> str:
        self._reg("Fusão sensores")
        leitura = self.smarthome.sensores.simular_leitura()
        ajustes = self.smarthome.ajuste.ajuste_por_conforto(leitura)
        resultado = self.smarthome.sensores.resumo()
        if ajustes:
            resultado += "\n\nAjustes realizados:\n" + "\n".join(f"  • {a}" for a in ajustes)
        return resultado

    def smarthome_consumo(self) -> str:
        return self.smarthome.consumo_total()

    def smarthome_tarifas(self) -> str:
        self._reg("Tarifas energia")
        return self.logistica.tarifas.custo_atual()

    def smarthome_geofence_status(self) -> str:
        return self.smarthome.geo.status()

    def smarthome_geofence_add(self, nome: str, lat: float,
                               lon: float, raio: float = 200) -> str:
        self._reg(f"Geofence: {nome}")
        return self.smarthome.geo.adicionar_zona(nome, lat, lon, raio)

    def smarthome_geofence_check(self) -> str:
        pos = self.smarthome.geo.obter_gps_ip()
        if not pos:
            return "Não consegui obter localização GPS via IP"
        lat, lon = pos
        resultado = self.smarthome.geo.verificar_posicao(lat, lon)
        linhas = [f"Posição atual: {lat:.4f}, {lon:.4f}"]
        for zona, dentro in resultado.items():
            linhas.append(f"  {zona}: {'📍 DENTRO' if dentro else '○ fora'}")
        return "\n".join(linhas)

    def smarthome_roteador(self) -> str:
        return self.smarthome.roteador.status()

    def smarthome_otimizar_redes(self) -> str:
        mudancas = self.smarthome.roteador.atribuir_redes(self.smarthome.dispositivos)
        if not mudancas:
            return "Redes já estão otimizadas"
        return "Roteamento otimizado:\n" + "\n".join(f"  {m}" for m in mudancas)

    def dispositivo_novo_interativo(self) -> Pergunta:
        """Cadastra dispositivo em 2 etapas: pergunta nome, depois tipo."""
        self._reg("Cadastro interativo de dispositivo")
        _TIPOS = ("luz", "som", "tv", "tomada", "sensor", "climatizacao")
        return Pergunta(
            "Como vai se chamar o novo dispositivo?\n"
            "(ex: Ventilador Sala, TV Quarto, Lâmpada Entrada...)",
            lambda nome: Pergunta(
                f"Que tipo é '{nome.strip()}'?\n"
                "Escolha: luz / som / tv / tomada / sensor / climatizacao",
                lambda tipo: self.smarthome_adicionar(
                    nome.strip(),
                    tipo.strip().split()[0] if tipo.strip().split()[0] in _TIPOS else "tomada"
                )
            )
        )

    # ══════════════════════════════════════════════════════════════
    #  BIOMETRIA E INTERAÇÃO HUMANA
    # ══════════════════════════════════════════════════════════════
    def bio_status_voz(self) -> str:
        return self.biometria_voz.status()

    def bio_cadastrar_perfil(self, nome: str) -> str:
        self._reg(f"Perfil de voz: {nome}")
        return self.biometria_voz.cadastrar_perfil(nome)

    def bio_analisar_expressao(self) -> str:
        self._reg("Análise de expressão")
        estado = self.expressao.analisar()
        base = self.expressao.resumo()
        if estado.sugestao and self.smarthome:
            if "descanso" in estado.sugestao:
                self.smarthome.ajuste.aplicar_perfil("descanso")
            elif "foco" in estado.sugestao:
                self.smarthome.ajuste.aplicar_perfil("trabalho")
        return base

    def bio_gestos_status(self) -> str:
        return self.gestos.status()

    def bio_narrar_casa(self) -> str:
        self._reg("Narração do status da casa")
        voz = getattr(self, "voz", None)
        self.sintecontexto.voz = voz
        return self.sintecontexto.narrar(
            self.smarthome, self.seguranca, self.logistica
        )

    # ══════════════════════════════════════════════════════════════
    #  SEGURANÇA
    # ══════════════════════════════════════════════════════════════
    def seg_status(self) -> str:
        return self.seguranca.status_completo()

    def seg_cadastrar_pet(self, nome: str) -> str:
        self._reg(f"Pet cadastrado: {nome}")
        return self.seguranca.filtro.cadastrar_pet(nome)

    def seg_cerca_status(self) -> str:
        return self.seguranca.cerca.status()

    def seg_cerca_cadastrar(self, nome: str, tipo: str, dispositivo: str) -> str:
        self._reg(f"Cerca virtual: {nome}")
        return self.seguranca.cerca.cadastrar(nome, tipo, dispositivo)

    def seg_emergencia_status(self) -> str:
        return self.seguranca.emergencia.status()

    def seg_cortar_tudo(self) -> Pergunta:
        self._reg("EMERGÊNCIA: solicitado corte gás+água")
        _SIM = {"sim", "s", "confirmo", "confirma", "pode", "pode sim", "isso"}
        return Pergunta(
            "⚠️ EMERGÊNCIA — Confirma corte imediato de GÁS e ÁGUA? (sim / não)",
            lambda r: self._seg_cortar_exec()
                      if r.strip().lower() in _SIM
                      else "Corte cancelado. Válvulas continuam abertas."
        )

    def _seg_cortar_exec(self) -> str:
        resultado = self.seguranca.emergencia.cortar_tudo()
        self.notificar("EMERGÊNCIA", resultado)
        return resultado

    def seg_restaurar_valvulas(self) -> str:
        return self.seguranca.emergencia.restaurar()

    def seg_auditoria(self, dias: int = 7) -> str:
        return self.seguranca.auditoria.analisar_padroes(dias)

    def seg_acesso(self, dispositivo: str, usuario: str,
                   tipo: str = "entrada") -> str:
        return self.seguranca.auditoria.registrar_acesso(dispositivo, usuario, tipo)

    def seg_alertas(self) -> str:
        alertas = self.seguranca.alertas_ativos()
        if not alertas:
            return "Nenhum alerta de segurança ativo"
        return "ALERTAS ATIVOS:\n" + "\n".join(f"  ⚠️ {a}" for a in alertas)

    # ══════════════════════════════════════════════════════════════
    #  LOGÍSTICA
    # ══════════════════════════════════════════════════════════════
    def log_status(self) -> str:
        return self.logistica.status_completo()

    def log_suprimentos(self) -> str:
        return self.logistica.compras.status()

    def log_atualizar_nivel(self, item: str, nivel: float) -> str:
        return self.logistica.compras.atualizar_nivel(item, nivel)

    def log_verificar_compras(self) -> str:
        pedidos = self.logistica.compras.verificar_e_pedir()
        if not pedidos:
            return "Todos os suprimentos estão OK"
        return "\n".join(pedidos)

    def log_auto_correcao(self) -> str:
        self._reg("Auto-correção do sistema")
        return self.logistica.correcao.limpar_cache_sistema()

    def log_relatorio_logs(self) -> str:
        return self.logistica.relatorio.analisar_logs_sistema()

    def log_relatorio_hardware(self) -> str:
        return self.logistica.relatorio.gerar_relatorio_hardware()

    def log_proximo_horario_barato(self) -> str:
        return self.logistica.tarifas.proximo_horario_barato()

    # ══════════════════════════════════════════════════════════════
    #  HISTÓRICO DE SENSORES
    # ══════════════════════════════════════════════════════════════
    def historico_sensores_painel(self, horas: float = 6.0) -> str:
        self._reg("Histórico sensores")
        return self._series_tempo.painel_resumo(horas) if hasattr(self, "_series_tempo") \
            else "Coletor de sensores não inicializado"

    def historico_sensores_png(self, horas: float = 24.0) -> str:
        self._reg("Gráfico PNG sensores")
        if not hasattr(self, "_series_tempo"):
            return "Coletor não inicializado"
        from ..sensores_historico import GraficoPNG
        return GraficoPNG.gerar(self._series_tempo, horas)

    def historico_sensores_stats(self, horas: float = 24.0) -> str:
        if not hasattr(self, "_series_tempo"):
            return "Coletor não inicializado"
        stats = self._series_tempo.estatisticas(horas)
        if not stats:
            return "Sem dados suficientes ainda"
        linhas = [f"ESTATÍSTICAS DOS SENSORES ({horas:.0f}h):"]
        for campo, label in [("temperatura", "Temperatura"), ("umidade", "Umidade"),
                              ("co2", "CO₂"), ("consumo", "Consumo"), ("conforto", "Conforto")]:
            if campo in stats:
                s = stats[campo]
                linhas.append(f"  {label}: atual={s['atual']} min={s['min']} "
                              f"max={s['max']} média={s['media']}")
        linhas.append(f"  Presença: {stats.get('presenca_pct', 0):.0f}% do tempo")
        return "\n".join(linhas)

    # ══════════════════════════════════════════════════════════════
    #  AGENTE DE EXECUÇÃO / TOOL USE
    # ══════════════════════════════════════════════════════════════
    def agente_tools_listar(self) -> str:
        return self.agente.listar_tools()

    def agente_tools_executar(self, objetivo: str) -> str:
        self._reg(f"Agente tool-use: {objetivo[:60]}")
        return self.agente.executar_tarefa(objetivo)

    def agente_tools_historico(self) -> str:
        return self.agente.historico_execucoes()

    def agente_executar_codigo(self, codigo: str) -> str:
        self._reg("Agente: execução de código")
        return self.agente.executor.executar_e_formatar(codigo)
