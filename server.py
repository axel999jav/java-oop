from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class StatusHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Получаем статус из URL
        status = parse_qs(urlparse(self.path).query).get('status', [''])[0].lower()

        # Определяем цвет фона и текст
        if status == 'on':
            color, text = '#10b981', 'ON'
        elif status == 'off':
            color, text = '#ef4444', 'OFF'
        else:
            color, text = '#94a3b8', '?'

        # HTML
        html = f"""<body style="margin:0; height:100vh; display:flex; align-items:center; justify-content:center; background:{color}; color:#fff; font-family:sans-serif; font-size:8rem; font-weight:bold;">{text}</body>"""

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def log_message(self, format, *args):
        pass


if __name__ == '__main__':
    port = 8000
    print(f"Откройте в браузере:")
    print(f"  http://localhost:{port}")
    HTTPServer(('localhost', port), StatusHandler).serve_forever()