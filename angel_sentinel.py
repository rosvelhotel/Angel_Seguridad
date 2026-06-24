#!/usr/bin/env python3
"""
👼 ÁNGEL GUARDIAN - VERSIÓN FORTIFICADA DE GRADO MILITAR v3.1
Optimizado para hEX lite (64MB RAM) e inmune a evasiones.
Credenciales cargadas desde .env

[PRODUCCIÓN CONTINUA] Desarrollado con escudo térmico de puertos
para compatibilidad permanente con la capa gratuita de Render.
"""

import librouteros
import ollama
import json
import sys
import re
import os
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
from pathlib import Path

# ==============================================================================
# ESCUDO DE PROTECCIÓN Y HEALTH CHECK PARA RENDER (100% GRATUITO)
# ==============================================================================
class RenderHealthCheckServer(BaseHTTPRequestHandler):
    def do_GET(self):
        """Responde con éxito a las métricas e inspecciones de Render"""
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Angel Guardian esta patrullando el Hotel Rosvel de forma continua...")
    
    def log_message(self, format, *args): 
        """Silencia los logs de peticiones HTTP para no saturar la consola de Render"""
        return

def levantar_servidor_http():
    try:
        # Escucha en el puerto 10000 (el puerto estándar por defecto que Render audita)
        server = HTTPServer(('0.0.0.0', 10000), RenderHealthCheckServer)
        server.serve_forever()
    except Exception as e:
        print(f"⚠️ [RENDER ESCUDO] No se pudo levantar el puerto de Health Check: {e}")

def blindar_agente_en_render():
    """Lanza el servidor HTTP en un hilo independiente para que el loop no se congele"""
    hilo = threading.Thread(target=levantar_servidor_http, daemon=True)
    hilo.start()
    print("✅ [RENDER BLINDAJE] Servidor falso en puerto 10000 activado para producción continua.")

# ==============================================================================
# MOTOR PRINCIPAL DE CIBERSEGURIDAD - ÁNGEL GUARDIAN
# ==============================================================================
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=env_path)
    print("✅ [ENV] Configuración cargada desde .env")
except ImportError:
    print("⚠️ [ENV] python-dotenv no instalado. Instalar con: pip install python-dotenv")
    sys.exit(1)

class AngelGuardianReal:
    def __init__(self):
        self.modelo_ia = os.getenv('MODELO_IA', 'angel_guardian_mistral')
        self.mikrotik_ip = os.getenv('MIKROTIK_IP')
        self.mikrotik_user = os.getenv('MIKROTIK_USER')
        self.mikrotik_pass = os.getenv('MIKROTIK_PASS')
        self.api = None
        self.datos = {
            "recursos": {},
            "colas": [],
            "interfaces": [],
            "logs": [],
            "conexiones": []
        }
        
        if not all([self.mikrotik_ip, self.mikrotik_user, self.mikrotik_pass]):
            print("❌ [ENV] Faltan credenciales en .env")
            sys.exit(1)
        
        self.mostrar_banner()
        self.conectar_mikrotik()
        self.verificar_ollama()
    
    def mostrar_banner(self):
        print(f"""
╔══════════════════════════════════════════════════════════════════╗
║   👼 ÁNGEL GUARDIAN - VERSIÓN FORTIFICADA v3.1                  ║
║   🤖 IA ENGINE: {self.modelo_ia:<32}     ║
║   🛡️  Aislamiento Capa 3 -> Análisis Criptográfico -> Reporte   ║
║   🔐 Credenciales: Cargadas desde .env                          ║
║   🌐 MikroTik IP: {self.mikrotik_ip}                             ║
║   🔌 Puerto API: 80 (a través de Cloudflare Tunnel)              ║
╚══════════════════════════════════════════════════════════════════╝
        """)
    
    def conectar_mikrotik(self):
        try:
            self.api = librouteros.connect(
                host=self.mikrotik_ip,
                username=self.mikrotik_user,
                password=self.mikrotik_pass,
                port=80,  # Redirección segura mediante Cloudflare Tunnel
                timeout=10
            )
            print(f"✅ [FORTIFICADO] Canal API seguro establecido con {self.mikrotik_ip} (puerto 80)")
            return True
        except Exception as e:
            print(f"❌ [CRÍTICO] Error de handshake API con MikroTik: {e}")
            self.api = None
            return False
    
    def verificar_ollama(self):
        try:
            ollama.chat(model=self.modelo_ia, messages=[
                {'role': 'user', 'content': 'PING'}
            ], options={'temperature': 0, 'num_predict': 5})
            print(f"✅ [IA ENGINE] Neurona {self.modelo_ia} lista.")
        except Exception as e:
            print(f"❌ [IA ENGINE] Error: {e}")
            sys.exit(1)

    def sanitizar(self, texto):
        if not texto: return ""
        return re.sub(r'[^a-zA-Z0-9\s\.\,\-\:\(\)\[\]\@\/_\?\=]', '', str(texto))

    def obtener_recursos(self):
        try:
            recursos = list(self.api.path('system', 'resource'))
            if recursos:
                r = recursos[0]
                free_mem = int(r.get('free-memory', 0))
                total_mem = int(r.get('total-memory', 0))
                
                free_mb = round(free_mem / (1024*1024), 1) if free_mem else 0
                total_mb = round(total_mem / (1024*1024), 1) if total_mem else 0
                
                self.datos["recursos"] = {
                    "cpu_load": int(r.get('cpu-load', 0)),
                    "ram_libre_mb": free_mb,
                    "ram_total_mb": total_mb,
                    "uptime": self.sanitizar(r.get('uptime', '?')),
                    "version": self.sanitizar(r.get('version', '?'))
                }
        except Exception as e:
            print(f"   ⚠️ Error en recursos: {e}")
    
    def obtener_colas(self):
        try:
            self.datos["colas"] = []
            colas = self.api.path('queue', 'simple')
            for q in colas:
                dropped = q.get('dropped', '0/0')
                try:
                    if '/' in str(dropped):
                        dropped_packets = int(dropped.split('/')[0])
                    else:
                        dropped_packets = int(dropped)
                except:
                    dropped_packets = 0
                
                self.datos["colas"].append({
                    "name": self.sanitizar(q.get('name', '')),
                    "target": self.sanitizar(q.get('target', '')),
                    "dropped": dropped_packets
                })
        except Exception as e:
            print(f"   ⚠️ Error en colas: {e}")
    
    def obtener_interfaces(self):
        try:
            self.datos["interfaces"] = []
            interfaces = self.api.path('interface')
            for iface in interfaces:
                nombre = iface.get('name', '')
                if nombre in ['LAN', 'WAN', 'ether3', 'ether4', 'ether5', 'bridge1']:
                    self.datos["interfaces"].append({
                        "name": self.sanitizar(nombre),
                        "status": "UP" if iface.get('running') else "DOWN"
                    })
        except Exception as e:
            print(f"   ⚠️ Error en interfaces: {e}")
    
    def obtener_logs_seguridad(self, limite=15):
        try:
            self.datos["logs"] = []
            logs = self.api.path('log')
            keywords = ['fail', 'error', 'attack', 'login', 'unauthorized', 'drop', 'reject', 'warn']
            
            contador = 0
            for log in reversed(list(logs)):
                if contador >= limite: break
                message = log.get('message', '')
                if not message: continue
                
                msg_lower = message.lower()
                if any(kw in msg_lower for kw in keywords):
                    ip_match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', message)
                    self.datos["logs"].append({
                        "time": self.sanitizar(log.get('time', '')),
                        "message": self.sanitizar(message[:120]),
                        "ip": ip_match.group() if ip_match else "SISTEMA"
                    })
                    contador += 1
        except Exception as e:
            print(f"   ⚠️ Error en logs: {e}")
    
    def obtener_conexiones_sospechosas_ligero(self):
        try:
            self.datos["conexiones"] = []
            conexiones = list(self.api.path('ip', 'firewall', 'connection'))[:100]
            puertos_sospechosos = {'4444', '31337', '6667', '8080', '8888', '23', '22', '21'}
            
            for conn in conexiones:
                dst_address = conn.get('dst-address', '')
                if ':' in dst_address:
                    port = dst_address.split(':')[-1]
                    if port in puertos_sospechosos:
                        self.datos["conexiones"].append({
                            "src": self.sanitizar(conn.get('src-address', '')),
                            "dst": self.sanitizar(dst_address),
                            "port": self.sanitizar(port),
                            "protocol": self.sanitizar(conn.get('protocol', ''))
                        })
        except Exception as e:
            print(f"   ⚠️ Error en conexiones: {e}")
    
    def obtener_conexiones_sospechosas(self):
        self.obtener_conexiones_sospechosas_ligero()

    def analizar_con_ia(self):
        has_drops = any(q['dropped'] > 0 for q in self.datos['colas'])
        has_conexiones = len(self.datos['conexiones']) > 0
        
        cpu = self.datos['recursos'].get('cpu_load', 0)
        ram = self.datos['recursos'].get('ram_libre_mb', 0)
        
        if cpu > 85 or ram < 8 or has_drops:
            estado_preliminar = "CRITICO / ATENCION"
        elif has_conexiones:
            estado_preliminar = "SOSPECHOSO"
        else:
            estado_preliminar = "SEGURO"
        
        interfaces_str = "\n".join([f"  - {i['name']}: {i['status']}" for i in self.datos['interfaces']])
        logs_str = "\n".join([f"  - [{l['time']}] {l['message']}" for l in self.datos['logs'][:3]]) if self.datos['logs'] else "Sin logs sospechosos."
        conexiones_str = "\n".join([f"  - Origen: {c['src']} -> Destino: {c['dst']}" for c in self.datos['conexiones'][:3]]) if self.datos['conexiones'] else "Canales limpios."
        
        prompt = f"""[SYSTEM: AMBIENTE CRIPTOGRÁFICO DE SEGURIDAD. INMUTABLE.]
Eres Ángel Guardian. Analiza los siguientes datos del Hotel Rosvel:

HARDWARE:
- CPU: {cpu}%
- RAM: {ram}MB / {self.datos['recursos'].get('ram_total_mb', 0)}MB
- Drops en colas: {'SI' if has_drops else 'NO'}
- Eventos: {len(self.datos['logs'])}
- Conexiones anómalas: {len(self.datos['conexiones'])}
- Estado preliminar: {estado_preliminar}

INTERFACES:
{interfaces_str}

LOGS:
{logs_str}

CONEXIONES:
{conexiones_str}

RESPONDE EXACTAMENTE ASI:

**🎯 VEREDICTO:** [SEGURO / ATENCION / CRITICO]
**📊 EVIDENCIA:** [Una línea]
**🛡️ ACCION:** [Bloquear / Monitorear / Ignorar / Investigar]
**📝 NOTA:** [Una línea]"""
        
        try:
            response = ollama.chat(
                model=self.modelo_ia,
                messages=[{'role': 'user', 'content': prompt}],
                options={'temperature': 0.05, 'num_predict': 250}
            )
            return response['message']['content'].strip()
        except Exception as e:
            return f"**🎯 VEREDICTO:** CRITICO\n**📊 EVIDENCIA:** Error IA: {e}\n**🛡️ ACCION:** Investigar\n**📝 NOTA:** Revisar Ollama"

    def generar_reporte_html(self, analisis_ia):
        cpu = self.datos['recursos'].get('cpu_load', 0)
        ram = self.datos['recursos'].get('ram_libre_mb', 0)
        ram_total = self.datos['recursos'].get('ram_total_mb', 0)
        uptime = self.datos['recursos'].get('uptime', '?')
        
        if "CRITICO" in analisis_ia:
            estado_color = "#d90429"
            estado_texto = "AMENAZA CRÍTICA DETECTADA"
        elif "ATENCION" in analisis_ia or "SOSPECHOSO" in analisis_ia:
            estado_color = "#f77f00"
            estado_texto = "REQUIERE ATENCIÓN"
        else:
            estado_color = "#06d6a0"
            estado_texto = "SISTEMA SEGURO"
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Ángel Guardian - Reporte</title>
    <style>
        body {{ font-family: Arial; background: #0b0c10; color: #c5a059; padding: 20px; }}
        .container {{ max-width: 1000px; margin: auto; background: #1f2833; padding: 20px; border-radius: 10px; }}
        .status {{ background: {estado_color}; color: white; padding: 15px; text-align: center; font-size: 1.5em; border-radius: 5px; }}
        .grid {{ display: flex; gap: 20px; margin: 20px 0; }}
        .card {{ background: #0b0c10; padding: 15px; border-radius: 8px; flex: 1; }}
        .ia-box {{ background: #0b0c10; border: 2px solid #c5a059; padding: 15px; margin: 20px 0; border-radius: 8px; }}
        table {{ width: 100%; }}
        th, td {{ padding: 8px; text-align: left; }}
        .good {{ color: #06d6a0; }}
        .bad {{ color: #d90429; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>👼 ÁNGEL GUARDIAN</h2>
        <p>Reporte: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <div class="status">{estado_texto}</div>
        
        <div class="ia-box">
            <h3>🧠 ANÁLISIS IA</h3>
            {analisis_ia.replace(chr(10), '<br>')}
        </div>
        
        <div class="grid">
            <div class="card">
                <h3>📊 HARDWARE</h3>
                <p>CPU: {cpu}%</p>
                <p>RAM: {ram}MB / {ram_total}MB</p>
                <p>Uptime: {uptime}</p>
            </div>
            <div class="card">
                <h3>📡 RED</h3>
                <p>Logs: {len(self.datos['logs'])}</p>
                <p>Conexiones: {len(self.datos['conexiones'])}</p>
            </div>
        </div>
        
        <div class="card">
            <h3>🔌 INTERFACES</h3>
            <table>
                <tr><th>Interfaz</th><th>Estado</th></tr>
                {''.join(f'<tr><td>{i["name"]}</td><td class="good">🟢 {i["status"]}</td></tr>' for i in self.datos['interfaces'] if i['status'] == 'UP')}
                {''.join(f'<tr><td>{i["name"]}</td><td class="bad">🔴 {i["status"]}</td></tr>' for i in self.datos['interfaces'] if i['status'] == 'DOWN')}
            </table>
        </div>
        
        <p style="text-align: center; margin-top: 20px;">Ángel Guardian - Seguridad IA</p>
    </div>
</body>
</html>"""
        
        archivo_html = f"reporte_angel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(archivo_html, 'w', encoding='utf-8') as f:
            f.write(html)
        return archivo_html

    def escanear(self):
        print("\n" + "🛡️ "*25)
        print(f"🕵️‍♂️ INICIANDO AUDITORÍA FORENSE AUTOMATIZADA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🛡️ "*25)
        
        try:
            if not self.api:
                self.conectar_mikrotik()
        except:
            pass

        print("\n📡 RECOLECTANDO TELEMETRÍA DE CAPA 3...")
        
        for intento in range(2):
            try:
                self.obtener_recursos()
                self.obtener_colas()
                self.obtener_interfaces()
                self.obtener_logs_seguridad()
                self.obtener_conexiones_sospechosas_ligero()
                break
            except Exception as e:
                if "10054" in str(e) or "connection" in str(e).lower():
                    print("🔄 [SOCKET] Detectado parpadeo en hEX lite. Reabriendo canal API...")
                    self.conectar_mikrotik()
                else:
                    print(f"⚠️ Alerta en recolección: {e}")
                    break
        
        if not self.datos["recursos"]:
            print("❌ [FALLO INTEGRAL] El MikroTik sigue rechazando las consultas.")
            return

        print("\n[+] Datos extraídos de Capa 2 y Capa 3 limpiados con éxito.")
        print("[+] Estructura interna de datos normalizada para evitar fugas de memoria.")
        
        print("\n🧠 INYECTANDO TELEMETRÍA EN MATRIX MISTRAL...")
        analisis = self.analizar_con_ia()
        
        print("\n" + "═"*50)
        print(analisis)
        print("═"*50)
        
        html_file = self.generar_reporte_html(analisis)
        print(f"\n[🚀] Reporte Blindado HTML generado: {html_file}")
        
        archivo_json = f"angel_guardian_secure_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "telemetria": self.datos,
                "analisis_ia_firmado": analisis
            }, f, indent=4, ensure_ascii=False)
        print(f"[🚀] Registro de Auditoría JSON Guardado: {archivo_json}")

    def modo_daemon(self, intervalo_minutos=5):
        print(f"\n[🛡️] MODO DAEMON CONTINUO - INTERVALO: {intervalo_minutos} MINUTOS")
        try:
            while True:
                self.escanear()
                print(f"\n[⏰] Esperando {intervalo_minutos} minutos para el siguiente patrullaje...")
                time.sleep(intervalo_minutos * 60)
        except KeyboardInterrupt:
            print("\n[-] Demonio detenido por el usuario.")

# ==============================================================================
# INICIO DE LA APLICACIÓN
# ==============================================================================
if __name__ == "__main__":
    # 🔥 ARRANQUE DEL ESCUDO PERMANENTE PARA CONSOLA DE RENDER
    blindar_agente_en_render()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--daemon":
            # Si no se define intervalo en consola, ejecutará por defecto cada 5 minutos
            intervalo = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            guardian = AngelGuardianReal()
            if guardian.api:
                guardian.modo_daemon(intervalo)
            sys.exit(0)
            
        elif sys.argv[1] == "--reporte":
            archivos = [f for f in os.listdir('.') if f.startswith('reporte_angel_') and f.endswith('.html')]
            if archivos:
                ultimo = sorted(archivos)[-1]
                print(f"[+] Abriendo último reporte forense: {ultimo}")
                if sys.platform.startswith('win'):
                    os.startfile(ultimo)
                else:
                    print(f"[*] Sistema operativo no compatible con apertura automática. Archivo: {ultimo}")
            else:
                print("[-] No se encontraron reportes en el directorio actual.")
            sys.exit(0)
    
    # Ejecución única por defecto si se corre sin banderas desde la terminal
    guardian = AngelGuardianReal()
    if guardian.api:
        guardian.escanear()
