"""
IRIS v2.0 — Mixin Celular (Poco X7 via ADB + Proteção de Dispositivos)
Métodos de controle ADB e segurança do celular extraídos de acoes.py.
"""
import os, subprocess, threading, time, logging
from ..tipos import Pergunta
from pathlib import Path
import datetime

from ..config import POCO_IP, TELEGRAM_TOKEN


class CelularMixin:
    """Controle ADB do Poco X7 e proteção de dispositivos."""

    # ══════════════════════════════════════════════════════════════
    #  HELPERS ADB
    # ══════════════════════════════════════════════════════════════
    def _adb(self, cmd):
        try:
            import shlex
            r = subprocess.run(["adb"] + shlex.split(cmd),
                               capture_output=True, text=True, timeout=15)
            return (r.stdout or r.stderr or "").strip()
        except Exception as e:
            logging.exception(e)
            return "Erro ADB: " + str(e)

    def _adb_conectado(self):
        r = subprocess.getoutput("adb devices")
        linhas = [l for l in r.split("\n")[1:] if l.strip()]
        return any(l.strip().endswith("device") for l in linhas)

    def _adb_wifi(self):
        if not self._adb_conectado():
            subprocess.getoutput("adb connect " + POCO_IP + ":5555")
        return self._adb_conectado()

    def _poco_ok(self):
        return self._adb_conectado() or self._adb_wifi()

    # ══════════════════════════════════════════════════════════════
    #  STATUS E INFORMAÇÕES
    # ══════════════════════════════════════════════════════════════
    def celular_status(self):
        if not self._poco_ok():
            return "Poco X7 não conectado. Conecta o cabo USB ou a mesma WiFi!"
        bat = self._adb("shell dumpsys battery | grep level").replace("level:", "").strip()
        android = self._adb("shell getprop ro.build.version.release").strip()
        arq = self._adb("shell df -h /data | tail -1").strip()
        self._reg("Status do celular")
        return ("Poco X7 | Android " + android + "\n" +
                "Bateria: " + bat + "%\n" +
                "Armazenamento: " + arq)

    def celular_bateria(self):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        bat = self._adb("shell dumpsys battery | grep level").replace("level:", "").strip()
        status = self._adb("shell dumpsys battery | grep status")
        temp = self._adb("shell dumpsys battery | grep temperature").replace("temperature:", "").strip()
        try:
            temp_c = str(round(int(temp) / 10)) + "C"
        except Exception:
            temp_c = temp
        status_txt = "Carregando" if "2" in status else "Descarregando"
        self._reg("Bateria do celular")
        return "Poco X7: " + bat + "% | " + status_txt + " | Temp: " + temp_c

    def celular_armazenamento(self):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        r = self._adb("shell df -h /data /sdcard 2>/dev/null")
        self._reg("Armazenamento do celular")
        return "Armazenamento Poco X7:\n" + r

    def celular_apps(self):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        r = self._adb("shell pm list packages -3")
        apps = [l.replace("package:", "") for l in r.split("\n") if l][:15]
        self._reg("Apps do celular")
        return "Apps instalados:\n" + "\n".join(apps)

    def celular_notificacoes(self):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        r = self._adb("shell dumpsys notification | grep NotificationRecord | head -10")
        self._reg("Notificações do celular")
        return "Notificações:\n" + (r if r else "Nenhuma notificação")

    def celular_info_completa(self):
        if not self._poco_ok():
            return "Poco X7 não conectado! Certifique que estão na mesma WiFi."
        android = self._adb("shell getprop ro.build.version.release").strip()
        bat = self._adb("shell dumpsys battery | grep level").replace("level:", "").strip()
        temp_b = self._adb("shell dumpsys battery | grep temperature").replace("temperature:", "").strip()
        try:
            temp_c = str(round(int(temp_b) / 10)) + "C"
        except Exception:
            temp_c = "?"
        ram = self._adb("shell cat /proc/meminfo | grep MemAvailable").strip()
        disco = self._adb("shell df -h /sdcard | tail -1").strip()
        ip = self._adb("shell ip addr show wlan0 | grep 'inet '").strip()
        self._reg("Info completa do celular")
        return ("Poco X7 | Android " + android + "\n" +
                "Bateria: " + bat + "% | Temp: " + temp_c + "\n" +
                "RAM livre: " + ram + "\n" +
                "Disco: " + disco + "\n" +
                "IP: " + ip[:40])

    def celular_espaco_livre(self):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        r = self._adb("shell df -h /sdcard /data 2>/dev/null")
        self._reg("Espaço livre do celular")
        return "Espaço no Poco X7:\n" + r

    def celular_status_painel(self):
        """Dados para o painel — não bloqueia se desconectado."""
        if not self._adb_conectado():
            return {"conectado": False}
        try:
            bat = int(self._adb("shell dumpsys battery | grep level")
                      .replace("level:", "").strip() or 0)
            plugado = "2" in self._adb("shell dumpsys battery | grep status")
            temp_b = self._adb("shell dumpsys battery | grep temperature").replace("temperature:", "").strip()
            temp_c = round(int(temp_b) / 10) if temp_b.isdigit() else 0
            disco_r = self._adb("shell df /sdcard 2>/dev/null | tail -1").split()
            disco_p = int(disco_r[4].replace("%", "")) if len(disco_r) > 4 else 0
            ram_r = self._adb("shell cat /proc/meminfo | grep MemAvailable").split()
            ram_mb = int(ram_r[1]) // 1024 if len(ram_r) > 1 else 0
            return {"bat": bat, "plugado": plugado, "temp": temp_c,
                    "disco": disco_p, "ram_livre_mb": ram_mb, "conectado": True}
        except Exception:
            return {"conectado": False}

    # ══════════════════════════════════════════════════════════════
    #  CONTROLES
    # ══════════════════════════════════════════════════════════════
    def celular_screenshot(self):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        nome = "poco_" + datetime.datetime.now().strftime("%d%m%Y_%H%M%S") + ".png"
        dest = str(Path.home() / "Pictures" / nome)
        self._adb("shell screencap -p /sdcard/iris_screen.png")
        self._adb("pull /sdcard/iris_screen.png " + dest)
        self._adb("shell rm /sdcard/iris_screen.png")
        self._reg("Screenshot do celular: " + nome)
        import subprocess as _sp
        _sp.Popen(["xdg-open", dest], stdout=_sp.DEVNULL, stderr=_sp.DEVNULL)
        return "Screenshot do Poco X7 salvo em ~/Pictures/" + nome

    def celular_desinstalar_app(self, pacote):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        r = self._adb("uninstall " + pacote)
        self._reg("Desinstalou app: " + pacote)
        return "App '" + pacote + "': " + r

    def celular_volume(self, acao):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        if acao == "aumentar":
            self._adb("shell input keyevent 24")
            self._adb("shell input keyevent 24")
        elif acao == "diminuir":
            self._adb("shell input keyevent 25")
            self._adb("shell input keyevent 25")
        elif acao == "mudo":
            self._adb("shell input keyevent 164")
        self._reg("Volume celular: " + acao)
        return "Volume do Poco X7 " + acao + "!"

    def celular_ligar_tela(self, ligar=True):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        self._adb("shell input keyevent 26")
        if ligar:
            self._adb("shell input keyevent 82")
        self._reg("Tela celular: " + ("ligada" if ligar else "desligada"))
        return "Tela do Poco X7 " + ("ligada!" if ligar else "desligada!")

    def celular_enviar_texto(self, texto):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        self._adb("shell input text " + texto.replace(" ", "%s"))
        self._reg("Digitou no celular: " + texto[:30])
        return "Texto digitado no Poco X7!"

    def celular_reiniciar(self) -> Pergunta:
        _SIM = {"sim", "s", "confirmo", "confirma", "pode"}
        return Pergunta(
            "Confirma reinício do Poco X7? O celular ficará ~30s offline. (sim / não)",
            lambda r: self._celular_reiniciar_exec()
                      if r.strip().lower() in _SIM
                      else "Reinício cancelado."
        )

    def _celular_reiniciar_exec(self) -> str:
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        self._adb("reboot")
        self._reg("Reiniciou o celular")
        return "Poco X7 reiniciando... aguarde ~30s"

    def celular_ligar_wifi(self, ligar=True):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        self._adb("shell svc wifi " + ("enable" if ligar else "disable"))
        self._reg("WiFi do celular: " + str(ligar))
        return "WiFi do Poco X7 " + ("ligado!" if ligar else "desligado!")

    # ══════════════════════════════════════════════════════════════
    #  ARQUIVOS
    # ══════════════════════════════════════════════════════════════
    def celular_enviar_arquivo(self, arquivo_local):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        nome = Path(arquivo_local).name
        self._adb("push " + arquivo_local + " /sdcard/Download/" + nome)
        self._reg("Enviou arquivo: " + nome)
        return "Arquivo enviado para Downloads do Poco X7: " + nome

    def celular_baixar_arquivo(self, arquivo_celular):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        dest = str(Path.home() / "Downloads" / Path(arquivo_celular).name)
        self._adb("pull " + arquivo_celular + " " + dest)
        self._reg("Baixou arquivo do celular")
        return "Arquivo baixado para ~/Downloads/!"

    def celular_listar_arquivos(self, pasta="/sdcard"):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        r = self._adb("shell ls -lh " + pasta + " 2>/dev/null")
        linhas = [l for l in r.split("\n") if l.strip()][:20]
        self._reg("Listou arquivos do celular: " + pasta)
        return "Arquivos em " + pasta + ":\n" + "\n".join(linhas)

    def celular_apagar_arquivo(self, caminho):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        self._adb("shell rm -f " + caminho)
        self._reg("Apagou do celular: " + caminho)
        return "Arquivo apagado: " + caminho

    def celular_apagar_downloads(self):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        self._adb("shell find /sdcard/Download -type f -delete")
        self._reg("Apagou downloads do celular")
        return "Downloads do Poco X7 apagados!"

    def celular_apagar_fotos_antigas(self, dias=30):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        self._adb("shell find /sdcard/DCIM -name '*.jpg' -mtime +" + str(dias) + " -delete")
        self._reg("Apagou fotos antigas do celular")
        return "Fotos com mais de " + str(dias) + " dias apagadas!"

    def celular_instalar_apk(self, caminho_apk):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        r = self._adb("install " + caminho_apk)
        self._reg("Instalou APK: " + caminho_apk)
        return "APK instalado: " + r[:100]

    def celular_fazer_backup_fotos(self):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        dest = str(Path.home() / "Pictures" / "Backup_Poco_X7")
        Path(dest).mkdir(parents=True, exist_ok=True)
        self._adb("pull /sdcard/DCIM/Camera " + dest)
        self._reg("Backup de fotos do celular")
        return "Fotos copiadas para ~/Pictures/Backup_Poco_X7!"

    def celular_limpar_cache(self):
        if not self._poco_ok():
            return "Poco X7 não conectado!"
        self._adb("shell pm clear --user 0 com.android.chrome")
        self._adb("shell pm clear --user 0 com.miui.gallery")
        r = self._adb("shell df -h /data | tail -1")
        self._reg("Limpou cache do celular")
        return "Cache limpo!\n" + r

    # ══════════════════════════════════════════════════════════════
    #  PROTEÇÃO DE DISPOSITIVOS
    # ══════════════════════════════════════════════════════════════
    def achar_celular(self):
        import subprocess as _sp
        url = "https://www.google.com/android/find"
        try:
            _sp.Popen(["xdg-open", url], stdout=_sp.DEVNULL, stderr=_sp.DEVNULL)
        except Exception as e:
            logging.exception(e)
        self._reg("Abriu Find My Device")
        msg = ("Abri o Encontrar Meu Dispositivo do Google!\n"
               "Lá você pode: ver no mapa, fazer tocar (mesmo no silencioso), "
               "bloquear ou apagar o Poco X7 remotamente.\n"
               "Link: " + url)
        if self._adb_conectado() or self._adb_wifi():
            try:
                self._adb("shell media volume --stream 3 --set 15")
                self._adb("shell input keyevent 24")
                msg += "\n\nO Poco ainda está na nossa rede — subi o volume dele!"
            except Exception as e:
                logging.exception(e)
        return msg

    def tocar_celular(self):
        if not (self._adb_conectado() or self._adb_wifi()):
            return ("Poco X7 não está na rede. Use 'acha meu celular' para o "
                    "Find My Device do Google (funciona de qualquer lugar).")
        self._adb("shell media volume --stream 3 --set 15")
        self._adb("shell cmd media_session volume --stream 4 --set 15")
        for _ in range(3):
            self._adb("shell input keyevent 24")
        self._reg("Fez o celular tocar")
        return "Volume do Poco X7 no máximo! Se estiver por perto, deve dar pra ouvir."

    def cofre_emergencia(self):
        if not (self._adb_conectado() or self._adb_wifi()):
            return "Poco X7 não conectado — conecte para eu guardar suas coisas."
        dest = Path.home() / "Cofre_IRIS"
        dest.mkdir(exist_ok=True)
        salvos = []
        try:
            fotos = dest / "Fotos"
            fotos.mkdir(exist_ok=True)
            self._adb("pull /sdcard/DCIM/Camera " + str(fotos))
            salvos.append("fotos")
            dls = dest / "Downloads"
            dls.mkdir(exist_ok=True)
            self._adb("pull /sdcard/Download " + str(dls))
            salvos.append("downloads")
            self._adb("pull /sdcard/Documents " + str(dest / "Documentos"))
            self._reg("Cofre de emergência")
            return ("Cofre atualizado em ~/Cofre_IRIS!\n"
                    "Guardei: " + ", ".join(salvos) +
                    "\nSe o celular sumir, suas coisas estão seguras aqui no PC.")
        except Exception as e:
            return "Erro no cofre: " + str(e)

    def modo_panico(self):
        passos = []
        try:
            self.telegram("MODO PÂNICO ativado por Francisco! "
                          "Localizando e protegendo dispositivos.")
            passos.append("Avisei no Telegram")
        except Exception:
            pass
        try:
            import subprocess as _sp
            _sp.Popen(["xdg-open", "https://www.google.com/android/find"],
                      stdout=_sp.DEVNULL, stderr=_sp.DEVNULL)
            passos.append("Abri o Find My Device")
        except Exception:
            pass
        if self._adb_conectado() or self._adb_wifi():
            try:
                self.tocar_celular()
                passos.append("Fiz o Poco tocar")
                self.cofre_emergencia()
                passos.append("Fiz backup de emergência")
            except Exception as e:
                logging.exception(e)
        else:
            passos.append("Poco fora da rede — use o Find My Device pra localizar")
        self._reg("MODO PÂNICO")
        return "MODO PÂNICO:\n" + "\n".join("- " + p for p in passos)

    def vigia_dispositivos(self, ativar=True):
        if ativar:
            if getattr(self, "_vigia_disp", False):
                return "Já estou de olho nos dispositivos!"
            self._vigia_disp = True
            threading.Thread(target=self._loop_vigia_disp, daemon=True).start()
            self._reg("Vigia de dispositivos ativado")
            return ("Guarda-costas ATIVO! Vou avisar no Telegram se o Poco X7 "
                    "sumir da rede por mais de alguns minutos.")
        self._vigia_disp = False
        return "Guarda-costas desativado."

    def _loop_vigia_disp(self):
        sumido_contador = 0
        estava_presente = False
        while getattr(self, "_vigia_disp", False):
            try:
                presente = self._adb_conectado() or self._adb_wifi()
                if presente:
                    estava_presente = True
                    sumido_contador = 0
                elif estava_presente:
                    sumido_contador += 1
                    if sumido_contador == 4:
                        self.telegram("Atenção: o Poco X7 saiu da rede. "
                                      "Se não foi você, diga 'modo panico' no Telegram.")
                        self.notificar("IRIS", "Poco X7 saiu da rede!")
            except Exception as e:
                logging.exception(e)
            time.sleep(30)
