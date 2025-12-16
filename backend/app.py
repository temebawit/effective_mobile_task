from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os

PORT = int(os.environ.get('PORT', 8080))

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            response_text = "Hello from Effective Mobile!"
            self.wfile.write(response_text.encode('utf-8'))
            logging.info(f"GET request, Path: {self.path}, Response: 200")
        else:
            self.send_response(404)
            self.end_headers()
            logging.warning(f"GET request, Path: {self.path}, Response: 404")

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    logging.basicConfig(level=logging.INFO)
    server_address = ('0.0.0.0', PORT)
    httpd = server_class(server_address, handler_class)
    logging.info(f'Starting httpd server on port {PORT}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd server...\n')

if __name__ == '__main__':
    run()
