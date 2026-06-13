from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime


class StatusHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Получаем параметр status из URL
        status = parse_qs(urlparse(self.path).query).get('status', [''])[0].lower()

        # Определяем цвет, текст и сообщение для терминала
        if status == 'on':
            color, text, log_msg = '#10b981', 'ON', '▶ СИСТЕМА ВКЛЮЧЕНА'
        elif status == 'off':
            color, text, log_msg = '#ef4444', 'OFF', '■ СИСТЕМА ОТКЛЮЧЕНА'
        else:
            color, text, log_msg = '#94a3b8', '?', '● СТАТУС НЕ ЗАДАН'

        # Выводим действие переключения в терминал
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] Запрос: {log_msg}")

        # HTML
        html = f"""<body style="margin:0; height:100vh; display:flex; align-items:center; justify-content:center; 
        background:{color}; color:#fff; font-family:monospace; font-size:8rem; font-weight:bold;">{text}</body>"""

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def log_message(self, format, *args):
        pass


if __name__ == '__main__':
    port = 8000
    print("=" * 50)
    print(f"Сервер запущен: http://localhost:{port}")
    print("Откройте в браузере для переключения:")
    print(f"  http://localhost:{port}/?status=on")
    print(f"  http://localhost:{port}/?status=off")
    print("=" * 50)

    try:
        HTTPServer(('localhost', port), StatusHandler).serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Сервер остановлен пользователем.")
