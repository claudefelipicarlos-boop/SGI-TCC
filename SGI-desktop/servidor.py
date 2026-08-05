#!/usr/bin/env python3
# SGI - Servidor de envio WhatsApp automatico
# Roda junto com o servidor do SGI
# Uso: python servidor.py
# Requer: pip install selenium flask

import threading
import time
import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# ──────────────────────────────────────────────
# CONFIG
PORTA_SGI    = 8080   # servidor do index.html
PORTA_ZAP    = 5000   # servidor de envio WhatsApp
PERFIL_CHROME = os.path.join(os.path.expanduser("~"), "SGI_Chrome_Profile")
# ──────────────────────────────────────────────

driver = None
driver_lock = threading.Lock()

def get_driver():
    global driver
    if driver:
        try:
            _ = driver.window_handles  # testa se ainda está aberto
            return driver
        except:
            driver = None

    opts = Options()
    opts.add_argument(f"--user-data-dir={PERFIL_CHROME}")
    opts.add_argument("--profile-directory=Default")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--start-maximized")
    # Não fechar o Chrome ao terminar o script
    opts.add_experimental_option("detach", True)

    try:
        driver = webdriver.Chrome(options=opts)
    except Exception as e:
        print(f"[ERRO] Chrome não encontrado: {e}")
        print("Instale o ChromeDriver: https://chromedriver.chromium.org/downloads")
        driver = None
    return driver

def enviar_whatsapp(numero, mensagem):
    """Abre WhatsApp Web e envia a mensagem para o número."""
    numero = ''.join(filter(str.isdigit, numero))
    url = f"https://web.whatsapp.com/send?phone={numero}&text={mensagem}"

    with driver_lock:
        d = get_driver()
        if not d:
            return False, "Chrome/ChromeDriver não disponível"

        try:
            # Abrir URL do WhatsApp com mensagem pré-preenchida
            d.get(url)

            # Aguardar campo de mensagem aparecer (até 30s para QR code / carregamento)
            wait = WebDriverWait(d, 30)
            campo = wait.until(
                EC.presence_of_element_located((By.XPATH,
                    '//div[@contenteditable="true"][@data-tab="10"]'
                ))
            )

            time.sleep(1.5)  # pequena pausa para garantir foco

            # Clicar no campo e enviar
            campo.click()
            time.sleep(0.5)
            campo.send_keys(Keys.ENTER)
            time.sleep(1)

            return True, f"Mensagem enviada para {numero}"

        except Exception as e:
            return False, f"Erro ao enviar: {str(e)}"

class SGIHandler(SimpleHTTPRequestHandler):
    """Serve o index.html (porta 8080) + endpoint /enviar (porta 5000)."""

    def do_OPTIONS(self):
        """CORS preflight"""
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/status":
            self._json({"status": "ok", "servidor": "SGI WhatsApp v1.0"})

        elif parsed.path == "/enviar":
            params = parse_qs(parsed.query)
            numero   = params.get("numero",   [""])[0]
            mensagem = unquote(params.get("mensagem", [""])[0])

            if not numero or not mensagem:
                self._json({"ok": False, "erro": "numero e mensagem obrigatorios"}, 400)
                return

            print(f"[ZAP] Enviando para {numero}: {mensagem[:60]}...")
            ok, msg = enviar_whatsapp(numero, mensagem)
            self._json({"ok": ok, "msg": msg})

        else:
            # Servir arquivos estáticos (index.html, importar.html)
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/enviar":
            length = int(self.headers.get("Content-Length", 0))
            body   = self.rfile.read(length)
            try:
                data = json.loads(body)
            except:
                self._json({"ok": False, "erro": "JSON inválido"}, 400)
                return

            numero   = str(data.get("numero",   ""))
            mensagem = str(data.get("mensagem", ""))

            if not numero or not mensagem:
                self._json({"ok": False, "erro": "numero e mensagem obrigatorios"}, 400)
                return

            print(f"[ZAP] Enviando para {numero}: {mensagem[:60]}...")
            ok, msg = enviar_whatsapp(numero, mensagem)
            self._json({"ok": ok, "msg": msg})
        else:
            self._json({"ok": False, "erro": "rota nao encontrada"}, 404)

    def _json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.rfile  # flush
        self.wfile.write(body)

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin",  "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, fmt, *args):
        # Silenciar logs de arquivo estático, mostrar só /enviar
        if "/enviar" in (args[0] if args else ""):
            print(f"[HTTP] {fmt % args}")

def iniciar_servidor_sgi():
    """Servidor na porta 8080 para o index.html"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    srv = HTTPServer(("0.0.0.0", PORTA_SGI), SimpleHTTPRequestHandler)
    print(f"[SGI] Servidor principal: http://localhost:{PORTA_SGI}")
    srv.serve_forever()

def iniciar_servidor_zap():
    """Servidor na porta 5000 para envio WhatsApp"""
    srv = HTTPServer(("0.0.0.0", PORTA_ZAP), SGIHandler)
    print(f"[ZAP] Servidor WhatsApp:  http://localhost:{PORTA_ZAP}/enviar")
    srv.serve_forever()

if __name__ == "__main__":
    print("=" * 55)
    print("  SGI - Sistema de Gestão Industrial")
    print("  Servidor com envio automático WhatsApp")
    print("=" * 55)
    print()

    # Verificar ChromeDriver
    try:
        from selenium.webdriver.chrome.service import Service
        print("[OK] Selenium instalado")
    except ImportError:
        print("[ERRO] Instale: pip install selenium flask")
        sys.exit(1)

    # Iniciar servidor SGI (porta 8080) em thread separada
    t1 = threading.Thread(target=iniciar_servidor_sgi, daemon=True)
    t1.start()

    print()
    print(f"  Abra no Chrome: http://localhost:{PORTA_SGI}")
    print(f"  API WhatsApp:   http://localhost:{PORTA_ZAP}/status")
    print()
    print("  Na primeira vez: escaneie o QR Code do WhatsApp Web.")
    print("  Após isso, o login fica salvo automaticamente.")
    print()
    print("  Pressione Ctrl+C para encerrar.")
    print("=" * 55)

    # Iniciar servidor WhatsApp na thread principal
    try:
        iniciar_servidor_zap()
    except KeyboardInterrupt:
        print("\n[SGI] Encerrando servidores...")
        if driver:
            try: driver.quit()
            except: pass
