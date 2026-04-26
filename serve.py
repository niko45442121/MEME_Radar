import os, sys
from http.server import SimpleHTTPRequestHandler, HTTPServer

port = int(os.environ.get('PORT', 3456))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
httpd = HTTPServer(('', port), SimpleHTTPRequestHandler)
print(f'Serving on port {port}', flush=True)
httpd.serve_forever()
