"""
Fotocopiadora SyP — Secure Static HTTP Server
Protege el directorio web local bloqueando el acceso a bases de datos SQLite,
código fuente Python, directorios .git y archivos de configuración sensibles.
"""
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = 5500
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

FORBIDDEN_EXTENSIONS = ('.db', '.sqlite', '.sqlite3', '.py', '.env', '.md', '.jsonl', '.key')
FORBIDDEN_PREFIXES = ('/.git', '/fastapi_backend', '/backend', '/.vscode', '/.stitch')

class SecureHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        normalized_path = self.path.split('?')[0].lower()

        # Bloquear prefijos sensibles
        for prefix in FORBIDDEN_PREFIXES:
            if normalized_path.startswith(prefix) or f"{prefix}/" in normalized_path:
                self.send_error(403, "Acceso Prohibido: Recurso del sistema protegido.")
                return

        # Bloquear extensiones sensibles
        for ext in FORBIDDEN_EXTENSIONS:
            if normalized_path.endswith(ext):
                self.send_error(403, "Acceso Prohibido: Tipo de archivo restringido.")
                return

        super().do_GET()

    def do_HEAD(self):
        normalized_path = self.path.split('?')[0].lower()
        for prefix in FORBIDDEN_PREFIXES:
            if normalized_path.startswith(prefix) or f"{prefix}/" in normalized_path:
                self.send_error(403, "Acceso Prohibido")
                return
        for ext in FORBIDDEN_EXTENSIONS:
            if normalized_path.endswith(ext):
                self.send_error(403, "Acceso Prohibido")
                return
        super().do_HEAD()

    def end_headers(self):
        # Cabeceras de seguridad
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.send_header('X-XSS-Protection', '1; mode=block')
        super().end_headers()

if __name__ == '__main__':
    server = ThreadingHTTPServer(('127.0.0.1', PORT), SecureHandler)
    print(f"Servidor estatico seguro iniciado en http://127.0.0.1:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
