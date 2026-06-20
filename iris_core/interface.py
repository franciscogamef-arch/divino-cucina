import os, sys, json, queue, threading, subprocess, socket, requests, atexit
import datetime, random, time, math, shutil, asyncio, re, tempfile
from pathlib import Path
import logging
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


# ══════════════════════════════════════════════════════════════
#  INTERFACE 3D — esfera estilo Jarvis
# ══════════════════════════════════════════════════════════════
class Esfera3D:
    def __init__(self, esf_w, esf_h):
        self.ESF_W = esf_w
        self.ESF_H = esf_h
        self.tick = 0.0
        self.rot_y = 0.0
        self.raio_base = 1.1
        self.raio_atual = 1.1
        self.raio_alvo = 1.1
        self.ondas = []
        self.barras = [0.1] * 32
        self.barras_alvo = [0.1] * 32
        self.aneis = [
            {"incl": 0,   "rot": 0,   "vel": 1.0,  "raio": 1.60, "esp": 2, "seg": 4},
            {"incl": 70,  "rot": 60,  "vel": -0.8, "raio": 1.75, "esp": 1, "seg": 6},
            {"incl": -50, "rot": 180, "vel": 1.3,  "raio": 1.55, "esp": 1, "seg": 3},
            {"incl": 90,  "rot": 45,  "vel": -0.6, "raio": 1.85, "esp": 1, "seg": 5},
        ]
        self.particulas = [
            {"theta": random.uniform(0, math.pi*2), "phi": random.uniform(0, math.pi),
             "dist": random.uniform(1.8, 3.2), "vt": random.uniform(-0.006, 0.006),
             "vp": random.uniform(-0.004, 0.004), "b": random.uniform(0.5, 1.0)}
            for _ in range(60)
        ]
        # Cores por estado: azul=idle, dourado=pensando, verde=falando, vermelho=ouvindo
        self.CORES = {
            "idle":     (0.0, 0.75, 1.0),
            "pensando": (1.0, 0.78, 0.1),
            "falando":  (0.1, 0.95, 0.5),
            "ouvindo":  (1.0, 0.35, 0.35),
        }
        self.cor_atual = list(self.CORES["idle"])

    def atualizar(self, estado):
        self.tick += 0.035
        vel_rot = 3.0 if estado == "falando" else 1.5 if estado == "pensando" else 0.5
        self.rot_y += vel_rot
        if estado == "falando":
            self.raio_alvo = self.raio_base + math.sin(self.tick*6)*0.18
            if int(self.tick*28) % 8 == 0:
                self.ondas.append({"r": self.raio_atual, "a": 0.8, "v": 0.04})
        elif estado == "pensando":
            self.raio_alvo = self.raio_base + math.sin(self.tick*2)*0.06
        else:
            self.raio_alvo = self.raio_base + math.sin(self.tick)*0.03
        self.raio_atual += (self.raio_alvo - self.raio_atual)*0.1
        self.ondas = [{**o, "r": o["r"]+o["v"], "a": o["a"]-0.02}
                      for o in self.ondas if o["a"] > 0]
        for i in range(32):
            if estado == "falando":
                self.barras_alvo[i] = random.uniform(0.3, 1.0)
            elif estado == "pensando":
                self.barras_alvo[i] = random.uniform(0.1, 0.4)
            else:
                self.barras_alvo[i] = random.uniform(0.03, 0.12)
            self.barras[i] += (self.barras_alvo[i]-self.barras[i])*0.2
        vel_p = 3.0 if estado == "falando" else 1.5 if estado == "pensando" else 0.4
        for p in self.particulas:
            p["theta"] += p["vt"]*vel_p
            p["phi"] += p["vp"]*vel_p
        vel_a = 4.0 if estado == "falando" else 2.0 if estado == "pensando" else 0.7
        for a in self.aneis:
            a["rot"] += a["vel"]*vel_a
        # Transição suave de cor por estado
        alvo = self.CORES.get(estado, self.CORES["idle"])
        for i in range(3):
            self.cor_atual[i] += (alvo[i] - self.cor_atual[i]) * 0.08

    def desenhar(self, W, H):
        glViewport(0, H-self.ESF_H, self.ESF_W, self.ESF_H)
        glMatrixMode(GL_PROJECTION); glLoadIdentity()
        gluPerspective(45, self.ESF_W/self.ESF_H, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW); glLoadIdentity()
        gluLookAt(0, 0, 6, 0, 0, 0, 0, 1, 0)
        glScissor(0, H-self.ESF_H, self.ESF_W, self.ESF_H)
        glEnable(GL_SCISSOR_TEST)
        glClearColor(0.02, 0.03, 0.07, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDisable(GL_SCISSOR_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        r, g, b = self.cor_atual
        glPushMatrix()
        glRotatef(15, 1, 0, 0); glRotatef(self.rot_y, 0, 1, 0)
        # Glow interno
        glColor4f(r, g, b, 0.05)
        q = gluNewQuadric(); gluQuadricDrawStyle(q, GLU_FILL)
        gluSphere(q, self.raio_atual*0.88, 32, 32); gluDeleteQuadric(q)
        # Wireframe
        glLineWidth(1.2); glColor4f(r, g, b, 0.6)
        q = gluNewQuadric(); gluQuadricDrawStyle(q, GLU_LINE)
        gluSphere(q, self.raio_atual, 24, 24); gluDeleteQuadric(q)
        # Anéis
        for anel in self.aneis:
            glPushMatrix()
            glRotatef(anel["incl"], 1, 0, 0); glRotatef(anel["rot"], 0, 1, 0)
            raio = anel["raio"]*(self.raio_atual/self.raio_base)
            glLineWidth(float(anel["esp"]))
            glBegin(GL_LINE_LOOP)
            for i in range(120):
                a = (i/120)*math.pi*2
                glColor4f(r, g, b, (0.5+0.5*math.sin(a*anel["seg"]+self.tick*3))*0.85)
                glVertex3f(raio*math.cos(a), 0, raio*math.sin(a))
            glEnd()
            glPointSize(4.0); glBegin(GL_POINTS)
            for i in range(anel["seg"]*2):
                a = (i/(anel["seg"]*2))*math.pi*2
                glColor4f(r, g, b, 1.0)
                glVertex3f(raio*math.cos(a), 0, raio*math.sin(a))
            glEnd(); glPopMatrix()
        # Partículas
        glPointSize(3.0); glBegin(GL_POINTS)
        for p in self.particulas:
            d = p["dist"]*(self.raio_atual/self.raio_base)
            x = d*math.sin(p["phi"])*math.cos(p["theta"])
            y = d*math.cos(p["phi"])
            z = d*math.sin(p["phi"])*math.sin(p["theta"])
            glColor4f(r, g, b, p["b"]*(0.5+0.5*math.sin(self.tick+p["theta"])))
            glVertex3f(x, y, z)
        glEnd(); glPopMatrix()
        # Barras de frequência
        rb = self.raio_atual*1.5; glLineWidth(2.5)
        for i in range(32):
            a = (i/32)*math.pi*2
            alt = self.barras[i]*0.45
            glBegin(GL_LINES)
            glColor4f(r, g, b, 0.9)
            glVertex3f(rb*math.cos(a), rb*math.sin(a), 0)
            glColor4f(r, g, b, 0.0)
            glVertex3f((rb+alt)*math.cos(a), (rb+alt)*math.sin(a), 0)
            glEnd()
        # Ondas
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        for o in self.ondas:
            glColor4f(r, g, b, o["a"]*0.5)
            q = gluNewQuadric(); gluQuadricDrawStyle(q, GLU_LINE)
            gluSphere(q, o["r"], 16, 16); gluDeleteQuadric(q)


# ══════════════════════════════════════════════════════════════
#  INTERFACE 2D — Painel + Chat
# ══════════════════════════════════════════════════════════════
class Painel2D:
    def __init__(self, W, H, ESF_W, ESF_H, SYS_X, SYS_W, usuario):
        self.W = W; self.H = H
        self.ESF_W = ESF_W; self.ESF_H = ESF_H
        self.SYS_X = SYS_X; self.SYS_W = SYS_W
        self.usuario = usuario
        self._tex_id = None
        # Cores
        self.C_CIANO   = (0, 200, 245)
        self.C_BRANCO  = (255, 255, 255)
        self.C_CINZA   = (130, 150, 170)
        self.C_VERDE   = (0, 230, 120)
        self.C_AMARELO = (255, 215, 0)
        self.C_VERM    = (255, 75, 75)
        self.C_IRIS    = (255, 255, 255)
        self.C_USER    = (255, 255, 255)
        # Fontes
        self.fnt_chat  = pygame.font.SysFont("monospace", 17, bold=True)
        self.fnt_input = pygame.font.SysFont("monospace", 17, bold=True)
        self.fnt_title = pygame.font.SysFont("monospace", 16, bold=True)
        self.fnt_mini  = pygame.font.SysFont("monospace", 13)
        self.fnt_sys   = pygame.font.SysFont("monospace", 13, bold=True)
        self.fnt_valor = pygame.font.SysFont("monospace", 22, bold=True)

    def _barra(self, surf, x, y, w, h, valor, cor):
        pygame.draw.rect(surf, (15, 25, 40), (x, y, w, h), border_radius=3)
        fill = max(1, int(w*min(valor, 100)/100))
        pygame.draw.rect(surf, cor, (x, y, fill, h), border_radius=3)
        pct = self.fnt_mini.render(str(round(valor))+"%", True, (160, 185, 210))
        surf.blit(pct, (x+w+5, y-2))

    def _grafico(self, surf, x, y, w, h, dados, cor):
        pygame.draw.rect(surf, (10, 18, 30), (x, y, w, h), border_radius=4)
        pygame.draw.rect(surf, (*cor, 60), (x, y, w, h), 1, border_radius=4)
        pts = dados[-w:]
        for i, v in enumerate(pts):
            bh = max(1, int((v/100)*h))
            pygame.draw.rect(surf, (*cor, int(80+175*(v/100))), (x+i, y+h-bh, 2, bh))
        if len(pts) > 1:
            media = sum(pts)/len(pts)
            my = y+h-int((media/100)*h)
            pygame.draw.line(surf, (*cor, 100), (x, my), (x+len(pts), my), 1)

    def desenhar(self, surf, mon, mensagens, input_texto, estado, ouvindo,
                 ultima_acao, poco_data=None):
        sx = self.SYS_X; sw = self.SYS_W; sy = 4
        # ══ PAINEL SISTEMA ══
        pygame.draw.rect(surf, (6, 10, 22, 252), (sx, sy, sw, self.ESF_H-8), border_radius=12)
        pygame.draw.rect(surf, (*self.C_CIANO, 100), (sx, sy, sw, self.ESF_H-8), 1, border_radius=12)
        pygame.draw.rect(surf, (0, 18, 36, 255), (sx, sy, sw, 30), border_radius=12)
        surf.blit(self.fnt_title.render("SISTEMA EM TEMPO REAL", True, self.C_CIANO), (sx+10, sy+8))
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except Exception:
            ip = "127.0.0.1"
        h2 = self.fnt_mini.render(ip, True, (130, 155, 180))
        surf.blit(h2, (sx+sw-h2.get_width()-8, sy+10))
        pygame.draw.line(surf, (*self.C_CIANO, 50), (sx, sy+30), (sx+sw, sy+30), 1)
        y = sy+36
        # CPU
        cor_cpu = self.C_VERDE if mon.cpu < 50 else self.C_AMARELO if mon.cpu < 80 else self.C_VERM
        surf.blit(self.fnt_sys.render("CPU", True, (190, 205, 220)), (sx+8, y))
        v = self.fnt_valor.render(str(round(mon.cpu))+"%", True, cor_cpu)
        surf.blit(v, (sx+sw-v.get_width()-8, y-4))
        if mon.temp > 0:
            surf.blit(self.fnt_mini.render(str(round(mon.temp))+"C", True, (180, 110, 60)),
                      (sx+sw-v.get_width()-55, y+4))
        y += 24; self._barra(surf, sx+8, y, sw-50, 12, mon.cpu, cor_cpu)
        y += 16; self._grafico(surf, sx+8, y, sw-16, 38, mon.hist_cpu, cor_cpu); y += 42
        # RAM
        cor_ram = self.C_VERDE if mon.ram < 60 else self.C_AMARELO if mon.ram < 85 else self.C_VERM
        surf.blit(self.fnt_sys.render("RAM", True, (190, 205, 220)), (sx+8, y))
        v = self.fnt_valor.render(str(round(mon.ram))+"%", True, cor_ram)
        surf.blit(v, (sx+sw-v.get_width()-8, y-4))
        y += 24; self._barra(surf, sx+8, y, sw-50, 12, mon.ram, cor_ram); y += 18
        # DISCO
        cor_d = self.C_VERDE if mon.disco < 70 else self.C_AMARELO if mon.disco < 90 else self.C_VERM
        surf.blit(self.fnt_sys.render("DISCO", True, (190, 205, 220)), (sx+8, y))
        v = self.fnt_valor.render(str(round(mon.disco))+"%", True, cor_d)
        surf.blit(v, (sx+sw-v.get_width()-8, y-4))
        y += 24; self._barra(surf, sx+8, y, sw-50, 12, mon.disco, cor_d); y += 18
        # BATERIA (agora funciona — Monitor lê psutil.sensors_battery)
        if mon.bat > 0:
            cor_b = self.C_VERDE if mon.bat > 50 else self.C_AMARELO if mon.bat > 20 else self.C_VERM
            lbl = "BAT+" if mon.plugado else "BAT"
            surf.blit(self.fnt_sys.render(lbl, True, (190, 205, 220)), (sx+8, y))
            v = self.fnt_valor.render(str(round(mon.bat))+"%", True, cor_b)
            surf.blit(v, (sx+sw-v.get_width()-8, y-4))
            y += 24; self._barra(surf, sx+8, y, sw-50, 12, mon.bat, cor_b); y += 18
        # REDE
        pygame.draw.line(surf, (*self.C_CIANO, 40), (sx+8, y), (sx+sw-8, y), 1); y += 6
        surf.blit(self.fnt_sys.render("REDE", True, (190, 205, 220)), (sx+8, y))
        rede = self.fnt_mini.render(
            "UP "+str(round(mon.net_up, 1))+"  DN "+str(round(mon.net_dn, 1))+" KB/s",
            True, (100, 175, 215))
        surf.blit(rede, (sx+sw-rede.get_width()-8, y+2)); y += 18
        # POCO X7
        if poco_data and poco_data.get("conectado"):
            pygame.draw.line(surf, (*self.C_CIANO, 40), (sx+8, y), (sx+sw-8, y), 1); y += 6
            surf.blit(self.fnt_sys.render("POCO X7", True, self.C_VERDE), (sx+8, y))
            info = self.fnt_mini.render(
                "Bat "+str(poco_data.get("bat", "?"))+"%  "+
                str(poco_data.get("temp", "?"))+"C  Disco "+
                str(poco_data.get("disco", "?"))+"%", True, (140, 230, 170))
            surf.blit(info, (sx+sw-info.get_width()-8, y+2)); y += 18
        # TOP PROCESSOS
        pygame.draw.line(surf, (*self.C_CIANO, 40), (sx+8, y), (sx+sw-8, y), 1); y += 6
        surf.blit(self.fnt_sys.render("TOP PROCESSOS", True, (220, 235, 255)), (sx+8, y)); y += 18
        try:
            for nome, pct in mon.get_procs()[:4]:
                cor_p = self.C_VERDE if pct < 30 else self.C_AMARELO if pct < 70 else self.C_VERM
                surf.blit(self.fnt_sys.render(nome[:26], True, (200, 220, 240)), (sx+10, y))
                pct_s = self.fnt_mini.render(str(round(pct, 1))+"%", True, cor_p)
                surf.blit(pct_s, (sx+sw-pct_s.get_width()-8, y+2))
                y += 18
        except Exception as _e:
            logging.exception(_e)
        # ÚLTIMA AÇÃO
        pygame.draw.line(surf, (*self.C_CIANO, 40), (sx+8, y), (sx+sw-8, y), 1); y += 6
        surf.blit(self.fnt_sys.render("ULTIMA ACAO", True, self.C_VERDE), (sx+8, y)); y += 18
        if ultima_acao:
            surf.blit(self.fnt_sys.render(ultima_acao[:44], True, (160, 245, 180)), (sx+8, y)); y += 18
        # RODAPÉ DO PAINEL
        pygame.draw.line(surf, (*self.C_CIANO, 40), (sx+8, y), (sx+sw-8, y), 1); y += 6
        surf.blit(self.fnt_sys.render("IRIS v1.0  |  Memoria ativa", True, (180, 200, 225)), (sx+8, y))
        # ══ CHAT ══
        cy = self.ESF_H; ch = self.H-self.ESF_H; input_h = 52
        pygame.draw.rect(surf, (8, 10, 18, 255), (0, cy, self.W, ch))
        pygame.draw.line(surf, (*self.C_CIANO, 200), (0, cy), (self.W, cy), 2)
        pygame.draw.rect(surf, (4, 8, 20, 255), (0, cy, self.W, 32))
        titulo = self.fnt_title.render(
            "IRIS v1.0   "+self.usuario+"   "+time.strftime("%H:%M:%S"), True, (255, 255, 255))
        surf.blit(titulo, (14, cy+8))
        st_cores = {"idle": self.C_CIANO, "pensando": self.C_AMARELO,
                    "falando": self.C_VERDE, "ouvindo": self.C_VERM}
        st_txt = {"idle": "● aguardando", "pensando": "◌ pensando...",
                  "falando": "◉ falando", "ouvindo": "◉ ouvindo"}
        st = self.fnt_mini.render(st_txt.get(estado, ""), True, st_cores.get(estado, self.C_CIANO))
        surf.blit(st, (self.W-st.get_width()-12, cy+10))
        pygame.draw.line(surf, (*self.C_CIANO, 60), (8, cy+32), (self.W-8, cy+32), 1)
        # Mensagens
        area_y = cy+38; area_fim = cy+ch-input_h-40; y2 = area_fim-4
        for msg in reversed(mensagens):
            quem = msg["quem"]; texto = msg["texto"]; hora = msg.get("hora", "")
            cor_msg = self.C_IRIS if quem == "iris" else self.C_USER
            bg_cor = (0, 28, 48, 75) if quem == "iris" else (40, 32, 0, 75)
            prefixo = ("IRIS "+hora+" | " if quem == "iris" else self.usuario+" "+hora+" | ")
            palavras = texto.split(); linhas, linha = [], ""
            for pal in palavras:
                if len(linha)+len(pal)+1 <= 82:
                    linha += (" " if linha else "")+pal
                else:
                    linhas.append(linha); linha = pal
            if linha:
                linhas.append(linha)
            total_h = len(linhas)*19+6
            bg_y = y2-total_h+4
            if bg_y > area_y:
                pygame.draw.rect(surf, bg_cor, (6, bg_y, self.W-12, total_h), border_radius=6)
            for i, l in enumerate(reversed(linhas)):
                pref = prefixo if i == len(linhas)-1 else " "*len(prefixo)
                t = self.fnt_chat.render(pref+l, True, cor_msg)
                if y2 > area_y:
                    surf.blit(t, (12, y2))
                y2 -= 22
            if y2 > area_y:
                pygame.draw.line(surf, (25, 35, 50, 150), (12, y2+4), (self.W-12, y2+4), 1)
            y2 -= 8
            if y2 < area_y:
                break
        # Input
        inp_y = cy+ch-input_h-6
        pygame.draw.rect(surf, (10, 14, 26, 255), (6, inp_y, self.W-12, input_h), border_radius=10)
        pygame.draw.rect(surf, (*self.C_CIANO, 200), (6, inp_y, self.W-12, input_h), 2, border_radius=10)
        cursor = "█" if int(time.time()*2) % 2 == 0 else " "
        inp = self.fnt_input.render("> "+input_texto+cursor, True, self.C_BRANCO)
        surf.blit(inp, (18, inp_y+13))
        # Dica
        if ouvindo:
            dica = self.fnt_mini.render("OUVINDO... fale agora!", True, self.C_VERDE)
        else:
            dica = self.fnt_sys.render(
                "  F2=falar | F3=hist | F4=conversa | F5=DITADO | Ctrl+V=colar | ajuda | ESC=sair  ",
                True, (220, 230, 245))
        pygame.draw.rect(surf, (4, 10, 22, 255), (0, inp_y-22, self.W, 22))
        pygame.draw.line(surf, (0, 150, 190, 150), (0, inp_y-22), (self.W, inp_y-22), 1)
        surf.blit(dica, (self.W//2-dica.get_width()//2, inp_y-19))
        # Divisória esfera/sistema
        pygame.draw.line(surf, (*self.C_CIANO, 60), (self.ESF_W, 0), (self.ESF_W, self.ESF_H), 1)
        # Cantos decorativos
        for cx2, cy2, dx, dy in [(0, 0, 1, 1), (self.W, 0, -1, 1),
                                 (self.W, self.H, -1, -1), (0, self.H, 1, -1)]:
            pygame.draw.lines(surf, (*self.C_CIANO, 150), False,
                              [(cx2+dx*20, cy2), (cx2, cy2), (cx2, cy2+dy*20)], 2)

    def renderizar_gl(self, surf, W, H):
        """Renderiza surface pygame no OpenGL."""
        glViewport(0, 0, W, H)
        glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity()
        glOrtho(0, W, 0, H, -1, 1)
        glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
        glDisable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        tex_data = pygame.image.tostring(surf, "RGBA", False)
        if self._tex_id is None:
            self._tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self._tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, W, H, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glEnable(GL_TEXTURE_2D); glColor4f(1, 1, 1, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1); glVertex2f(0, 0)
        glTexCoord2f(1, 1); glVertex2f(W, 0)
        glTexCoord2f(1, 0); glVertex2f(W, H)
        glTexCoord2f(0, 0); glVertex2f(0, H)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION); glPopMatrix()
        glMatrixMode(GL_MODELVIEW); glPopMatrix()
