"""
IRIS v2.0 — Interação Humana Avançada
Biometria de Voz, Análise de Expressão, Controle de Gestos, Síntese de Contexto
"""
import json, threading, time, logging, hashlib, tempfile, os, subprocess
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple


# ══════════════════════════════════════════════════════════════
#  BIOMETRIA DE VOZ — identifica quem está falando
# ══════════════════════════════════════════════════════════════
@dataclass
class PerfilVoz:
    nome: str
    permissoes: List[str] = field(default_factory=list)
    assinatura_hash: str = ""
    ativo: bool = True
    ultimo_acesso: float = field(default_factory=time.time)


class BiometriaVoz:
    """Identifica o locutor e aplica permissões personalizadas."""
    DATA_PATH = Path.home() / ".iris" / "perfis_voz.json"

    PERMISSOES_DISPONIVEIS = [
        "controle_total", "smart_home", "leitura_apenas",
        "telegram", "financeiro", "emergencia"
    ]

    def __init__(self, ia=None):
        self.ia = ia
        self._perfis: Dict[str, PerfilVoz] = {}
        self._locutor_atual: Optional[str] = None
        self._confianca: float = 0.0
        self._lock = threading.Lock()
        self._carregar()

    def _carregar(self):
        try:
            if self.DATA_PATH.exists():
                data = json.loads(self.DATA_PATH.read_text())
                for nome, p in data.items():
                    self._perfis[nome] = PerfilVoz(**p)
        except Exception as e:
            logging.exception(e)

    def _salvar(self):
        try:
            self.DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
            data = {k: asdict(v) for k, v in self._perfis.items()}
            self.DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2))
        except Exception as e:
            logging.exception(e)

    def cadastrar_perfil(self, nome: str, permissoes: List[str] = None) -> str:
        perms = permissoes or ["smart_home", "leitura_apenas"]
        self._perfis[nome] = PerfilVoz(nome=nome, permissoes=perms)
        self._salvar()
        return f"Perfil '{nome}' cadastrado com permissões: {', '.join(perms)}"

    def _extrair_mfcc_simples(self, caminho_audio: str) -> Optional[str]:
        """Extrai características básicas de áudio para comparação de voz."""
        try:
            import wave, struct, math
            with wave.open(caminho_audio, 'rb') as wf:
                frames = wf.readframes(wf.getnframes())
                samples = struct.unpack(f"{len(frames)//2}h", frames)
            # energia em bandas de frequência simples
            n = len(samples)
            if n < 100:
                return None
            bandas = [samples[i*n//8:(i+1)*n//8] for i in range(8)]
            energias = [sum(abs(s) for s in b) / max(len(b), 1) for b in bandas]
            fingerprint = "|".join(f"{e:.0f}" for e in energias)
            return hashlib.md5(fingerprint.encode()).hexdigest()[:16]
        except Exception:
            return None

    def identificar(self, caminho_audio: Optional[str] = None, texto: Optional[str] = None) -> Tuple[Optional[str], float]:
        """Identifica locutor por análise de áudio ou texto via IA."""
        if caminho_audio and self.ia:
            try:
                prompt = ("Analise este áudio e descreva características da voz "
                          "(tom, ritmo, sotaque) em 2 frases:")
                descricao = self.ia.gemini_audio(caminho_audio, prompt)
                # comparação simplificada por IA
                if self._perfis:
                    nomes = list(self._perfis.keys())
                    prompt_id = (
                        f"Perfis cadastrados: {', '.join(nomes)}\n"
                        f"Descrição da voz: {descricao}\n"
                        "Qual perfil é mais provável? Responda APENAS o nome ou DESCONHECIDO."
                    )
                    resposta = self.ia.groq_rapido(prompt_id, max_tokens=20, temperature=0.0)
                    nome = resposta.strip().strip("'\"")
                    if nome in self._perfis:
                        self._locutor_atual = nome
                        self._confianca = 0.75
                        self._perfis[nome].ultimo_acesso = time.time()
                        return nome, 0.75
            except Exception as e:
                logging.exception(e)

        # fallback: usa o primeiro perfil ativo como padrão
        for nome, p in self._perfis.items():
            if p.ativo:
                self._locutor_atual = nome
                self._confianca = 0.5
                return nome, 0.5

        return None, 0.0

    def verificar_permissao(self, permissao: str, locutor: Optional[str] = None) -> bool:
        nome = locutor or self._locutor_atual
        if not nome or nome not in self._perfis:
            return permissao in ("leitura_apenas",)
        perfil = self._perfis[nome]
        return "controle_total" in perfil.permissoes or permissao in perfil.permissoes

    def status(self) -> str:
        linhas = ["BIOMETRIA DE VOZ:"]
        if self._locutor_atual:
            linhas.append(f"  Locutor ativo: {self._locutor_atual} ({self._confianca*100:.0f}%)")
        else:
            linhas.append("  Nenhum locutor identificado")
        linhas.append(f"  Perfis cadastrados: {len(self._perfis)}")
        for nome, p in self._perfis.items():
            perms = ", ".join(p.permissoes)
            linhas.append(f"  • {nome}: {perms}")
        return "\n".join(linhas)

    def listar_permissoes(self, nome: Optional[str] = None) -> str:
        n = nome or self._locutor_atual
        if not n or n not in self._perfis:
            return "Perfil não encontrado"
        p = self._perfis[n]
        return f"Permissões de {n}: {', '.join(p.permissoes)}"


# ══════════════════════════════════════════════════════════════
#  ANÁLISE DE EXPRESSÃO — detecta cansaço/estresse via câmera
# ══════════════════════════════════════════════════════════════
@dataclass
class EstadoEmocional:
    cansaco: float = 0.0      # 0-1
    estresse: float = 0.0     # 0-1
    atencao: float = 1.0      # 0-1
    humor: str = "neutro"
    sugestao: str = ""
    timestamp: float = field(default_factory=time.time)


class AnalisadorExpressao:
    """Detecta estado emocional via imagem de webcam + IA."""

    SUGESTOES = {
        "cansaco":  "Sugerindo ambiente de descanso: iluminação baixa, temperatura 20°C",
        "estresse": "Modo relaxamento: música suave, iluminação âmbar, temperatura 22°C",
        "atento":   "Modo foco: iluminação branca intensa, silêncio",
        "animado":  "Modo energia: música animada, luzes vivas",
    }

    def __init__(self, ia=None):
        self.ia = ia
        self._ultimo_estado: Optional[EstadoEmocional] = None
        self._historico: List[EstadoEmocional] = []

    def analisar(self, caminho_imagem: Optional[str] = None) -> EstadoEmocional:
        if not caminho_imagem:
            caminho_imagem = self._capturar_webcam()
        if not caminho_imagem:
            return EstadoEmocional(humor="indefinido", sugestao="Webcam indisponível")

        estado = EstadoEmocional()
        if self.ia:
            try:
                prompt = (
                    "Analise a expressão facial nesta imagem e responda em JSON:\n"
                    '{"cansaco": 0.0-1.0, "estresse": 0.0-1.0, '
                    '"atencao": 0.0-1.0, "humor": "neutro|cansado|estressado|animado|triste"}'
                    "\nApenas o JSON, sem mais texto."
                )
                resposta = self.ia.gemini_visao(caminho_imagem, prompt)
                import re
                m = re.search(r'\{.*\}', resposta, re.DOTALL)
                if m:
                    dados = json.loads(m.group())
                    estado.cansaco = float(dados.get("cansaco", 0))
                    estado.estresse = float(dados.get("estresse", 0))
                    estado.atencao = float(dados.get("atencao", 1))
                    estado.humor = dados.get("humor", "neutro")
            except Exception as e:
                logging.exception(e)

        # gera sugestão baseada no estado
        if estado.cansaco > 0.6:
            estado.sugestao = self.SUGESTOES["cansaco"]
        elif estado.estresse > 0.6:
            estado.sugestao = self.SUGESTOES["estresse"]
        elif estado.atencao > 0.8:
            estado.sugestao = self.SUGESTOES["atento"]
        elif estado.humor == "animado":
            estado.sugestao = self.SUGESTOES["animado"]

        self._ultimo_estado = estado
        self._historico.append(estado)
        if len(self._historico) > 100:
            self._historico = self._historico[-100:]
        return estado

    def _capturar_webcam(self) -> Optional[str]:
        try:
            tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
            tmp.close()
            subprocess.run(["fswebcam", "-r", "640x480", "--no-banner", tmp.name],
                           capture_output=True, timeout=8)
            if os.path.exists(tmp.name) and os.path.getsize(tmp.name) > 0:
                return tmp.name
        except Exception as e:
            logging.exception(e)
        return None

    def resumo(self) -> str:
        e = self._ultimo_estado
        if not e:
            return "Nenhuma análise realizada ainda. Use: analisa expressao"
        return (
            f"ESTADO EMOCIONAL DETECTADO:\n"
            f"  Cansaço: {e.cansaco*100:.0f}% | Estresse: {e.estresse*100:.0f}%\n"
            f"  Atenção: {e.atencao*100:.0f}% | Humor: {e.humor}\n"
            f"  → {e.sugestao}" if e.sugestao else f"  Humor: {e.humor}"
        )


# ══════════════════════════════════════════════════════════════
#  CONTROLE DE GESTOS — interpreta movimentos via câmera
# ══════════════════════════════════════════════════════════════
class ControladorGestos:
    """Interpreta gestos de mão via câmera para controlar a casa."""

    GESTOS = {
        "palma_aberta":   "parar_tudo",
        "punho":          "modo_foco",
        "polegar_cima":   "aumentar_volume",
        "polegar_baixo":  "diminuir_volume",
        "dois_dedos":     "ligar_luzes",
        "palma_esquerda": "proxima_musica",
        "palma_direita":  "musica_anterior",
        "cinco_dedos":    "status_casa",
    }

    def __init__(self, ia=None, smarthome=None):
        self.ia = ia
        self.smarthome = smarthome
        self._ativo = False
        self._ultimo_gesto: Optional[str] = None
        self._callbacks: Dict[str, list] = {}

    def detectar_gesto(self, caminho_imagem: str) -> Optional[str]:
        if not self.ia:
            return None
        try:
            prompt = (
                "Analise os gestos de mão nesta imagem. Identifique se há:\n"
                "palma_aberta, punho, polegar_cima, polegar_baixo, "
                "dois_dedos, palma_esquerda, palma_direita, cinco_dedos, nenhum\n"
                "Responda APENAS o nome do gesto detectado ou 'nenhum'."
            )
            gesto = self.ia.gemini_visao(caminho_imagem, prompt).strip().lower()
            gesto = gesto.replace(" ", "_")
            if gesto in self.GESTOS:
                self._ultimo_gesto = gesto
                return gesto
            return None
        except Exception as e:
            logging.exception(e)
            return None

    def executar_gesto(self, gesto: str) -> str:
        acao = self.GESTOS.get(gesto)
        if not acao:
            return f"Gesto '{gesto}' não reconhecido"

        # notifica callbacks customizados
        for cb in self._callbacks.get(gesto, []):
            try:
                cb(gesto, acao)
            except Exception:
                pass

        # ações padrão no smart home
        if self.smarthome:
            if acao == "ligar_luzes":
                return self.smarthome.controlar("Luz Sala", ligado=True)
            if acao == "parar_tudo":
                return self.smarthome.modo_ausente()
            if acao == "status_casa":
                return self.smarthome.painel_status()

        return f"Gesto reconhecido: {gesto} → {acao}"

    def mapear_gesto(self, gesto: str, acao: str) -> str:
        if gesto not in self.GESTOS:
            return f"Gesto '{gesto}' inválido. Disponíveis: {', '.join(self.GESTOS)}"
        self.GESTOS[gesto] = acao
        return f"Gesto '{gesto}' mapeado para '{acao}'"

    def ao_detectar(self, gesto: str, callback):
        self._callbacks.setdefault(gesto, []).append(callback)

    def status(self) -> str:
        linhas = ["CONTROLE DE GESTOS:"]
        linhas.append(f"  Último gesto: {self._ultimo_gesto or 'nenhum'}")
        linhas.append("  Mapeamentos:")
        for g, a in self.GESTOS.items():
            linhas.append(f"    ✋ {g} → {a}")
        return "\n".join(linhas)


# ══════════════════════════════════════════════════════════════
#  SÍNTESE DE CONTEXTO — resume o status da casa em áudio/texto
# ══════════════════════════════════════════════════════════════
class SintesContexto:
    """Gera resumo inteligente do status da casa para leitura em voz."""

    def __init__(self, ia=None, voz=None):
        self.ia = ia
        self.voz = voz

    def gerar_resumo(self, smarthome, seguranca=None, logistica=None) -> str:
        partes = []

        # Status dos dispositivos
        ativos = [n for n, d in smarthome.dispositivos.items() if d.ligado]
        if ativos:
            partes.append(f"{len(ativos)} dispositivos ligados: {', '.join(ativos[:3])}")
        else:
            partes.append("Todos os dispositivos estão desligados")

        # Sensores
        fusao = smarthome.sensores.fusao()
        partes.append(
            f"Ambiente: {fusao.temperatura}°C, {fusao.umidade}% umidade, "
            f"{'presença detectada' if fusao.presenca else 'ninguém detectado'}"
        )

        # Consumo
        consumo = sum(d.consumo_w for d in smarthome.dispositivos.values() if d.ligado)
        if consumo > 0:
            partes.append(f"Consumo atual: {consumo:.0f} watts")

        # Segurança
        if seguranca:
            alertas = seguranca.alertas_ativos()
            if alertas:
                partes.append(f"ATENÇÃO: {'; '.join(alertas[:2])}")

        # Logística
        if logistica:
            pendentes = logistica.itens_pendentes()
            if pendentes:
                partes.append(f"Pendente: {pendentes[0]}")

        texto_bruto = ". ".join(partes) + "."

        # refina via IA se disponível
        if self.ia:
            try:
                prompt = (
                    f"Reescreva este status da casa de forma natural e concisa em 2 frases, "
                    f"como se estivesse falando para o dono:\n{texto_bruto}"
                )
                texto_refinado = self.ia.groq_rapido(prompt, max_tokens=100, temperature=0.7)
                return texto_refinado
            except Exception:
                pass

        return texto_bruto

    def narrar(self, smarthome, seguranca=None, logistica=None) -> str:
        resumo = self.gerar_resumo(smarthome, seguranca, logistica)
        if self.voz:
            try:
                self.voz.falar(resumo)
            except Exception as e:
                logging.exception(e)
        return resumo
