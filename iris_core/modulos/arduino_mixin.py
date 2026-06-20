"""
IRIS v2.0 — Mixin Arduino
Controle completo via serial: firmware universal v2, servo, LED, PWM,
sensor analógico/digital, ultrassônico, buzzer, relé, motor DC, I2C.
"""
import re, time, shutil, subprocess, logging
from pathlib import Path


class ArduinoMixin:
    """Todos os métodos de Arduino extraídos de acoes.py, com novos sensores e atuadores."""

    # ─────────────────────────────────────────────────────────────────────────
    #  FIRMWARE UNIVERSAL v2
    #  Grave uma vez: instala firmware
    #  Protocolo: comandos em texto terminados em \n, respostas em \n
    # ─────────────────────────────────────────────────────────────────────────
    FIRMWARE = r"""// IRIS Firmware Universal v2
// Protocolo serial 9600 baud — comandos terminados em \n
//
//  PING                        -> PONG
//  LED <pino> ON|OFF           -> digital write
//  RELAY <pino> ON|OFF         -> relé (igual LED)
//  LEDS <p1,p2,...> ON|OFF     -> múltiplos pinos de uma vez
//  PWM <pino> <0-255>          -> analogWrite (pinos PWM: 3,5,6,9,10,11)
//  SERVO <pino> <0-180>        -> move servo
//  LER A<n>                    -> analogRead (A0-A5)
//  LER D<n>                    -> digitalRead
//  ULTRASSONICO <trig> <echo>  -> distância cm (HC-SR04)
//  TONE <pino> <freq> <ms>     -> buzzer (ms=0 = continua até NOTONE)
//  NOTONE <pino>               -> para buzzer
//  MOTOR <pA> <pB> <vel>       -> L298N (-255=ré, 0=para, 255=frente)
//  PINMODE <pino> I|O|P        -> Input / Output / Input_Pullup
//  SCAN_I2C                    -> varre barramento I2C (Wire.h)
//  TODOS_OFF                   -> desliga todos os pinos digitais (2-13)
//
#include <Servo.h>
#include <Wire.h>
Servo servos[14];
bool servoOn[14] = {false};
String buf = "";

void setup() {
  Serial.begin(9600);
  Wire.begin();
  Serial.println("IRIS_FIRMWARE_V2_OK");
}

void processa(String cmd) {
  cmd.trim();
  String cmdU = cmd; cmdU.toUpperCase();

  if (cmdU == "PING") { Serial.println("PONG"); return; }

  if (cmdU == "TODOS_OFF") {
    for (int i = 2; i <= 13; i++) { pinMode(i, OUTPUT); digitalWrite(i, LOW); }
    Serial.println("TODOS_OFF:OK"); return;
  }

  if (cmdU == "SCAN_I2C") {
    String found = "I2C:";
    for (uint8_t a = 1; a < 127; a++) {
      Wire.beginTransmission(a);
      if (Wire.endTransmission() == 0) { found += "0x"; found += String(a, HEX); found += ","; }
    }
    Serial.println(found.length() > 5 ? found : "I2C:NENHUM"); return;
  }

  if (cmdU.startsWith("LED ") || cmdU.startsWith("RELAY ")) {
    int off = cmdU.startsWith("LED ") ? 4 : 6;
    int sp = cmd.indexOf(' ', off);
    int pino = cmd.substring(off, sp < 0 ? cmd.length() : sp).toInt();
    bool on = cmdU.endsWith("ON");
    pinMode(pino, OUTPUT); digitalWrite(pino, on ? HIGH : LOW);
    Serial.println(cmdU.substring(0, off - 1) + " " + String(pino) + (on ? " ON" : " OFF")); return;
  }

  if (cmdU.startsWith("LEDS ")) {
    int lastSp = cmdU.lastIndexOf(' ');
    bool on = cmdU.substring(lastSp + 1) == "ON";
    String pinos = cmd.substring(5, lastSp);
    String tok = "", r = "LEDS:";
    for (int i = 0; i <= pinos.length(); i++) {
      char c = i < pinos.length() ? pinos[i] : ',';
      if (c == ',') {
        int p = tok.toInt();
        if (p > 0) { pinMode(p, OUTPUT); digitalWrite(p, on ? HIGH : LOW); r += String(p) + ","; }
        tok = "";
      } else tok += c;
    }
    Serial.println(r + (on ? "ON" : "OFF")); return;
  }

  if (cmdU.startsWith("PWM ")) {
    int sp = cmd.indexOf(' ', 4);
    int pino = cmd.substring(4, sp).toInt();
    int val = constrain(cmd.substring(sp + 1).toInt(), 0, 255);
    pinMode(pino, OUTPUT); analogWrite(pino, val);
    Serial.println("PWM " + String(pino) + "=" + String(val)); return;
  }

  if (cmdU.startsWith("SERVO ")) {
    int sp1 = cmd.indexOf(' ', 6);
    int pino = cmd.substring(6, sp1).toInt();
    int ang = constrain(cmd.substring(sp1 + 1).toInt(), 0, 180);
    if (pino >= 0 && pino < 14) {
      if (!servoOn[pino]) { servos[pino].attach(pino); servoOn[pino] = true; }
      servos[pino].write(ang);
      Serial.println("SERVO " + String(pino) + "->" + String(ang));
    } return;
  }

  if (cmdU.startsWith("TONE ")) {
    int sp1 = cmd.indexOf(' ', 5), sp2 = cmd.indexOf(' ', sp1 + 1);
    int pino = cmd.substring(5, sp1).toInt();
    int freq = cmd.substring(sp1 + 1, sp2 < 0 ? cmd.length() : sp2).toInt();
    int ms   = sp2 < 0 ? 0 : cmd.substring(sp2 + 1).toInt();
    if (ms > 0) tone(pino, freq, ms); else tone(pino, freq);
    Serial.println("TONE " + String(pino) + " " + String(freq) + "Hz"); return;
  }

  if (cmdU.startsWith("NOTONE ")) {
    noTone(cmd.substring(7).toInt());
    Serial.println("NOTONE:OK"); return;
  }

  if (cmdU.startsWith("MOTOR ")) {
    int sp1 = cmd.indexOf(' ', 6), sp2 = cmd.indexOf(' ', sp1 + 1);
    int pA = cmd.substring(6, sp1).toInt();
    int pB = cmd.substring(sp1 + 1, sp2).toInt();
    int vel = constrain(cmd.substring(sp2 + 1).toInt(), -255, 255);
    pinMode(pA, OUTPUT); pinMode(pB, OUTPUT);
    if (vel == 0)      { digitalWrite(pA, LOW);  digitalWrite(pB, LOW);  }
    else if (vel > 0)  { analogWrite(pA, vel);   digitalWrite(pB, LOW);  }
    else               { digitalWrite(pA, LOW);  analogWrite(pB, -vel);  }
    Serial.println("MOTOR=" + String(vel)); return;
  }

  if (cmdU.startsWith("ULTRASSONICO ")) {
    int sp = cmd.indexOf(' ', 13);
    int trig = cmd.substring(13, sp).toInt(), echo = cmd.substring(sp + 1).toInt();
    pinMode(trig, OUTPUT); pinMode(echo, INPUT);
    digitalWrite(trig, LOW); delayMicroseconds(2);
    digitalWrite(trig, HIGH); delayMicroseconds(10); digitalWrite(trig, LOW);
    long dur = pulseIn(echo, HIGH, 30000);
    Serial.println("DISTANCIA=" + String(dur * 0.0343 / 2.0, 1) + "cm"); return;
  }

  if (cmdU.startsWith("PINMODE ")) {
    int sp = cmd.indexOf(' ', 8);
    int pino = cmd.substring(8, sp).toInt();
    String m = cmdU.substring(sp + 1);
    if (m == "O") pinMode(pino, OUTPUT);
    else if (m == "P") pinMode(pino, INPUT_PULLUP);
    else pinMode(pino, INPUT);
    Serial.println("PINMODE " + String(pino) + " " + m); return;
  }

  if (cmdU.startsWith("LER A")) { Serial.println("A" + cmd.substring(5) + "=" + String(analogRead(cmd.substring(5).toInt()))); return; }
  if (cmdU.startsWith("LER D")) {
    int n = cmd.substring(5).toInt(); pinMode(n, INPUT);
    Serial.println("D" + String(n) + "=" + String(digitalRead(n))); return;
  }

  Serial.println("ERRO: " + cmd);
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') { processa(buf); buf = ""; } else if (c != '\r') buf += c;
  }
}
"""

    # ─────────────────────────────────────────────────────────────────────────
    #  HELPERS INTERNOS
    # ─────────────────────────────────────────────────────────────────────────
    def _porta_arduino(self) -> str:
        import glob
        portas = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")
        from ..config import ARDUINO_PORTA
        return portas[0] if portas else ARDUINO_PORTA

    def arduino_enviar(self, comando: str) -> str:
        """Envia comando cru pela serial e lê a resposta."""
        try:
            import serial
        except ImportError:
            return "Instala: pip3 install pyserial --break-system-packages"
        porta = self._porta_arduino()
        arduino = getattr(self, "_arduino", None)
        try:
            if arduino is None or not getattr(arduino, "is_open", False):
                arduino = serial.Serial(porta, 9600, timeout=2)
                self._arduino = arduino
                time.sleep(2)  # Arduino reseta ao abrir porta
            arduino.write((comando.strip() + "\n").encode())
            time.sleep(0.4)
            resp = arduino.readline().decode(errors="ignore").strip()
            self._reg("Arduino: " + comando[:30])
            return ("Arduino ← " + comando +
                    ("\n→ " + resp if resp else "\n(sem resposta)"))
        except Exception as e:
            self._arduino = None
            return "Erro serial " + porta + ": " + str(e)

    # ─────────────────────────────────────────────────────────────────────────
    #  STATUS E DIAGNÓSTICO
    # ─────────────────────────────────────────────────────────────────────────
    def portas_serial(self) -> str:
        import glob
        portas = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")
        self._reg("Listou portas serial")
        if not portas:
            return ("Nenhuma porta serial encontrada. Conecta o Arduino!\n"
                    "(se conectado e não aparecer: sudo usermod -aG dialout $USER e relogue)")
        return "Portas seriais:\n" + "\n".join("  • " + p for p in portas)

    def arduino_status(self) -> str:
        """Status completo: porta, firmware e ping."""
        porta = self._porta_arduino()
        import glob
        portas = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")
        if not portas:
            return ("Arduino: DESCONECTADO\n"
                    "Conecte o cabo USB e rode: instala firmware")
        r = self.arduino_enviar("PING")
        fw = "v2 OK" if "PONG" in r else "não responde (grave o firmware)"
        return (f"Arduino: CONECTADO em {porta}\n"
                f"Firmware: {fw}\n"
                f"Portas disponíveis: {', '.join(portas)}\n"
                f"arduino-cli: {'instalado' if shutil.which('arduino-cli') else 'não encontrado'}")

    def ping_arduino(self) -> str:
        r = self.arduino_enviar("PING")
        if "PONG" in r:
            return "Arduino PONG! Firmware v2 rodando. Tudo sob controle."
        return r + "\n(Sem PONG? Grave o firmware: instala firmware)"

    def monitor_serial(self, segundos: int = 5) -> str:
        """Lê o que o Arduino está imprimindo por alguns segundos."""
        try:
            import serial
        except ImportError:
            return "Instala: pip3 install pyserial --break-system-packages"
        porta = self._porta_arduino()
        linhas = []
        try:
            arduino = getattr(self, "_arduino", None)
            if arduino is None or not getattr(arduino, "is_open", False):
                arduino = serial.Serial(porta, 9600, timeout=1)
                self._arduino = arduino
                time.sleep(2)
            fim = time.time() + min(int(segundos), 30)
            while time.time() < fim:
                l = arduino.readline().decode(errors="ignore").strip()
                if l:
                    linhas.append(l)
                if len(linhas) >= 20:
                    break
            self._reg("Monitor serial")
            return ("Serial " + porta + " (" + str(segundos) + "s):\n" +
                    ("\n".join(linhas) if linhas else "(silêncio na serial)"))
        except Exception as e:
            return "Erro: " + str(e)

    # ─────────────────────────────────────────────────────────────────────────
    #  SAÍDAS DIGITAIS
    # ─────────────────────────────────────────────────────────────────────────
    def led(self, pino: int, ligar: bool = True) -> str:
        return self.arduino_enviar(f"LED {pino} {'ON' if ligar else 'OFF'}")

    def arduino_leds_multiplos(self, pinos, ligar: bool = True) -> str:
        """Liga/desliga vários LEDs de uma vez. pinos = [13, 12, 11] ou '13,12,11'."""
        if isinstance(pinos, (list, tuple)):
            pinos = ",".join(str(p) for p in pinos)
        return self.arduino_enviar(f"LEDS {pinos} {'ON' if ligar else 'OFF'}")

    def arduino_todos_off(self) -> str:
        """Desliga TODOS os pinos digitais (2-13) de uma vez."""
        r = self.arduino_enviar("TODOS_OFF")
        self._reg("Arduino: todos os pinos desligados")
        return r

    def arduino_relay(self, pino: int, ligar: bool = True) -> str:
        return self.arduino_enviar(f"RELAY {pino} {'ON' if ligar else 'OFF'}")

    def arduino_pinmode(self, pino: int, modo: str = "O") -> str:
        """Define modo do pino: O=Output, I=Input, P=Input_Pullup."""
        m = modo.upper().strip()[0] if modo.strip() else "O"
        return self.arduino_enviar(f"PINMODE {pino} {m}")

    # ─────────────────────────────────────────────────────────────────────────
    #  SAÍDAS ANALÓGICAS / PWM
    # ─────────────────────────────────────────────────────────────────────────
    def pwm(self, pino: int, valor: int) -> str:
        """PWM em pinos compatíveis (3, 5, 6, 9, 10, 11). Valor 0-255."""
        valor = max(0, min(int(valor), 255))
        return self.arduino_enviar(f"PWM {pino} {valor}")

    # ─────────────────────────────────────────────────────────────────────────
    #  SERVO MOTOR
    # ─────────────────────────────────────────────────────────────────────────
    def servo(self, graus: int, pino: int = 9) -> str:
        graus = max(0, min(int(graus), 180))
        return self.arduino_enviar(f"SERVO {pino} {graus}")

    # ─────────────────────────────────────────────────────────────────────────
    #  MOTOR DC (via L298N)
    # ─────────────────────────────────────────────────────────────────────────
    def arduino_motor(self, pinoA: int, pinoB: int, velocidade: int) -> str:
        """Controla motor DC via L298N. velocidade: -255 (ré) a 255 (frente), 0=para."""
        vel = max(-255, min(int(velocidade), 255))
        return self.arduino_enviar(f"MOTOR {pinoA} {pinoB} {vel}")

    def arduino_motor_parar(self, pinoA: int, pinoB: int) -> str:
        return self.arduino_motor(pinoA, pinoB, 0)

    # ─────────────────────────────────────────────────────────────────────────
    #  BUZZER
    # ─────────────────────────────────────────────────────────────────────────
    def arduino_buzzer(self, pino: int = 8, freq: int = 440, duracao_ms: int = 500) -> str:
        """Toca o buzzer. duracao_ms=0 toca até arduino_buzzer_parar."""
        return self.arduino_enviar(f"TONE {pino} {freq} {duracao_ms}")

    def arduino_buzzer_parar(self, pino: int = 8) -> str:
        return self.arduino_enviar(f"NOTONE {pino}")

    def arduino_bip(self, pino: int = 8, repeticoes: int = 1) -> str:
        """Emite bips curtos de 100ms."""
        for _ in range(repeticoes):
            self.arduino_enviar(f"TONE {pino} 1000 100")
            time.sleep(0.15)
        self._reg(f"Arduino bip x{repeticoes}")
        return f"Bip! ({repeticoes}x no pino {pino})"

    # ─────────────────────────────────────────────────────────────────────────
    #  LEITURA DE SENSORES
    # ─────────────────────────────────────────────────────────────────────────
    def ler_sensor(self, qual: str) -> str:
        qual = qual.upper().strip()
        if not re.fullmatch(r"[AD]\d{1,2}", qual):
            return "Use: le sensor a0 (analógico) ou le sensor d7 (digital)"
        return self.arduino_enviar("LER " + qual)

    def arduino_ultrassonico(self, pino_trig: int = 9, pino_echo: int = 10) -> str:
        """Lê distância do sensor HC-SR04. Retorna distância em cm."""
        r = self.arduino_enviar(f"ULTRASSONICO {pino_trig} {pino_echo}")
        self._reg(f"Ultrassônico: trig={pino_trig} echo={pino_echo}")
        return r

    def arduino_scan_i2c(self) -> str:
        """Varre o barramento I2C e lista endereços de dispositivos encontrados."""
        r = self.arduino_enviar("SCAN_I2C")
        self._reg("Scan I2C")
        if "NENHUM" in r:
            return "Nenhum dispositivo I2C encontrado. Verifique SDA/SCL (pinos A4/A5 no Uno)."
        return "Dispositivos I2C encontrados:\n  " + r.replace("I2C:", "").replace(",", "\n  ").strip(",")

    # ─────────────────────────────────────────────────────────────────────────
    #  SEQUÊNCIAS E AUTOMAÇÃO
    # ─────────────────────────────────────────────────────────────────────────
    def arduino_sequencia(self, comandos: list, intervalo_s: float = 0.5) -> str:
        """Envia lista de comandos em sequência com intervalo entre eles.
        comandos = ['LED 13 ON', 'PWM 5 128', 'SERVO 9 90']"""
        resultados = []
        for cmd in comandos:
            r = self.arduino_enviar(str(cmd))
            resultados.append(f"  {cmd} → {r.splitlines()[-1] if r else '?'}")
            time.sleep(intervalo_s)
        self._reg(f"Sequência Arduino: {len(comandos)} cmds")
        return f"Sequência ({len(comandos)} comandos):\n" + "\n".join(resultados)

    # ─────────────────────────────────────────────────────────────────────────
    #  FIRMWARE — INSTALAÇÃO
    # ─────────────────────────────────────────────────────────────────────────
    def instalar_firmware(self) -> str:
        pasta = Path.home() / "iris_firmware"
        pasta.mkdir(exist_ok=True)
        ino = pasta / "iris_firmware.ino"
        ino.write_text(self.FIRMWARE, encoding="utf-8")
        self._reg("Gerou firmware universal v2")
        if shutil.which("arduino-cli"):
            r = self.arduino_gravar(str(ino))
            return (f"Firmware v2 salvo em ~/iris_firmware/iris_firmware.ino\n{r}\n"
                    "Agora: servo 90 | liga led 13 | pwm 5 200 | le sensor a0 | "
                    "ultrassonico | buzzer | motor | scan i2c")
        return ("Firmware v2 salvo em ~/iris_firmware/iris_firmware.ino!\n"
                "Grave pela IDE do Arduino, ou instale arduino-cli:\n"
                "  curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/"
                "master/install.sh | sh && arduino-cli core install arduino:avr\n"
                "Depois: grava arduino iris_firmware/iris_firmware.ino")

    # ─────────────────────────────────────────────────────────────────────────
    #  COMPILAÇÃO E GRAVAÇÃO
    # ─────────────────────────────────────────────────────────────────────────
    def arduino_compilar(self, arquivo: str, placa: str = "arduino:avr:uno") -> str:
        p = Path(arquivo).expanduser()
        if not p.exists():
            p = Path.home() / arquivo
        if not p.exists():
            return f"Não achei '{arquivo}'"
        if not shutil.which("arduino-cli"):
            return ("arduino-cli não instalado. Instala com:\n"
                    "curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/"
                    "master/install.sh | sh\narduino-cli core install arduino:avr")
        try:
            r = subprocess.run(["arduino-cli", "compile", "--fqbn", placa, str(p)],
                               capture_output=True, text=True, timeout=120)
            self._reg("Compilou Arduino: " + p.name)
            if r.returncode == 0:
                return "Compilou sem erros! " + p.name + " pronto.\n" + r.stdout[-300:]
            return "Erro de compilação:\n" + (r.stderr or r.stdout)[-500:]
        except Exception as e:
            return "Erro: " + str(e)

    def arduino_gravar(self, arquivo: str, placa: str = "arduino:avr:uno") -> str:
        p = Path(arquivo).expanduser()
        if not p.exists():
            p = Path.home() / arquivo
        if not p.exists():
            return f"Não achei '{arquivo}'"
        if not shutil.which("arduino-cli"):
            return "arduino-cli não instalado (veja: compila arduino)"
        porta = self._porta_arduino()
        try:
            arduino = getattr(self, "_arduino", None)
            if arduino and getattr(arduino, "is_open", False):
                arduino.close()
                self._arduino = None
            r = subprocess.run(["arduino-cli", "upload", "-p", porta,
                                 "--fqbn", placa, str(p)],
                                capture_output=True, text=True, timeout=120)
            self._reg("Gravou Arduino: " + p.name)
            if r.returncode == 0:
                return f"GRAVADO em {porta}! {p.name} rodando."
            return "Erro ao gravar:\n" + (r.stderr or r.stdout)[-500:]
        except Exception as e:
            return "Erro: " + str(e)

    def gerar_codigo_arduino(self, desc: str) -> str:
        import datetime
        r = self.ia.gemini_complexo(
            "Gere código Arduino C++ completo e funcional para: " + desc +
            ". Compatível com Uno/Nano/Mega. Comentários em português. "
            "Inclua setup() e loop(). Código prático e direto.")
        nome = "arduino_" + datetime.datetime.now().strftime("%d%m%Y_%H%M") + ".ino"
        try:
            with open(nome, "w", encoding="utf-8") as f:
                f.write(r)
        except Exception as _e:
            logging.exception(_e)
        self._reg("Gerou sketch Arduino: " + desc[:40])
        return r[:700] + "\n\nSalvo como " + nome
