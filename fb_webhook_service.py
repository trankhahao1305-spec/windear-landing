import http.server
import socketserver
import subprocess
import urllib.parse
import json

PORT = 5005

class WebhookHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        try:
            data = json.loads(post_data)
            caption = data.get("caption", "[Windear - Luyện Tai 4 Bước]")
        except:
            caption = post_data

        cmd = ["python3", "/root/.goclaw/agents/me-me/skills/tao-creative-fb/scripts/post_facebook.py", caption]
        out = subprocess.run(cmd, capture_output=True, text=True)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success", "output": out.stdout}).encode('utf-8'))

with socketserver.TCPServer(("", PORT), WebhookHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
