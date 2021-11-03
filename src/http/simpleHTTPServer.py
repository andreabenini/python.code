#!/usr/bin/env python3
#
# @see No deps (flask,...), straight and simple httpserver
from http.server import BaseHTTPRequestHandler, HTTPServer

host = "localhost"
port = 8008

class MyServer(BaseHTTPRequestHandler):
    def _headerSend(self, response=200):
        self.send_response(response)
        self.send_header("Content-type", 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path == '/path':
            self._headerSend()
            self.wfile.write(bytes("<html><head><title>Page</title></head>", "utf-8"))
            self.wfile.write(bytes("<body>URL: {}</body></html>\n".format(self.path), "utf-8"))
        else:
            self._headerSend(response=404)
            self.wfile.write(bytes("{} not found\n".format(self.path), "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((host, port), MyServer)
    print("Serving on http://{}:{}".format(host, port))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
