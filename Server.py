from http.server import *

SERVER = "localhost"
PORT = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<H1>This is our hacker browser.</H1>", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((SERVER, PORT), MyServer)
    print(f"Server started http://{SERVER}:{PORT}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
