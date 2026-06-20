"""
Tipos compartilhados entre acoes.py e os mixins.
Mantido em módulo separado para evitar importação circular.
"""


class Pergunta:
    """
    Retorno especial: quando um método devolve Pergunta, o Processador
    exibe o texto ao usuário e, na próxima fala, chama callback(resposta).
    Permite fluxos multi-turno sem bloquear a thread principal.
    Perguntas podem ser encadeadas — o callback pode devolver outra Pergunta.

    Exemplo de uso simples (confirmação):
        return Pergunta(
            "Confirma reinício do celular? (sim/não)",
            lambda r: self._reiniciar_exec()
                      if r in ("sim", "s", "confirmo") else "Cancelado."
        )

    Exemplo encadeado (formulário em 2 etapas):
        return Pergunta(
            "Nome do dispositivo?",
            lambda nome: Pergunta(
                f"Tipo de '{nome}'? (luz/som/tv/tomada/sensor)",
                lambda tipo: self.smarthome_adicionar(nome, tipo)
            )
        )
    """
    def __init__(self, texto: str, callback):
        self.texto = texto        # pergunta exibida ao usuário
        self.callback = callback  # fn(resposta: str) -> str | Pergunta
