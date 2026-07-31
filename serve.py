import os, urllib.parse, urllib.request
from http.server import SimpleHTTPRequestHandler, HTTPServer

port = int(os.environ.get('PORT', 3456))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = {
    'openapi.twse.com.tw',
    'www.twse.com.tw',
    'www.tpex.org.tw',
    'query1.finance.yahoo.com',
    'query2.finance.yahoo.com',
}


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/proxy?'):
            self.handle_proxy()
        else:
            super().do_GET()

    def handle_proxy(self):
        target = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get('url', [''])[0]
        if (urllib.parse.urlparse(target).hostname or '') not in ALLOWED_HOSTS:
            self.send_error(403, 'Host not allowed')
            return
        try:
            req = urllib.request.Request(target, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=20) as r:
                body = r.read()
        except Exception as e:
            self.send_error(502, f'Upstream fetch failed: {e}')
            return
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        super().end_headers()
        self.wfile.write(body)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, must-revalidate')
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


httpd = HTTPServer(('', port), Handler)
print(f'Serving on port {port}', flush=True)
httpd.serve_forever()
