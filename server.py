import http.server
import socketserver
import json
import os

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def insert_customer_into_md(timestamp, name, email, phone, goal, note):
    cust_file_path = os.path.join(DIRECTORY, 'data', 'customers', 'customers.md')
    if not os.path.exists(cust_file_path):
        return False
    
    row = f"| **{timestamp}** | {name} | {email} | {phone} | {goal} | {note} |\n"
    
    with open(cust_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the table header line
    marker = "| :--- | :--- | :--- | :--- | :--- | :--- |"
    if marker in content:
        parts = content.split(marker, 1)
        new_content = parts[0] + marker + "\n" + row + parts[1].lstrip('\n')
    else:
        new_content = content + "\n" + row

    with open(cust_file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

class LocalCustomerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == '/api/save-customer':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                timestamp = data.get('timestamp', '')
                name = data.get('name', '')
                email = data.get('email', '')
                phone = data.get('phone', '')
                goal = data.get('goal', '')
                note = data.get('note', '')

                success = insert_customer_into_md(timestamp, name, email, phone, goal, note)

                print(f"✅ Đã chèn khách hàng mới trực tiếp vào BẢNG `customers.md`: {name} ({phone})")

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "message": "Inserted into customers.md table"}).encode('utf-8'))
            except Exception as e:
                print(f"❌ Lỗi ghi file: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    print(f"🚀 Server Windear đang chạy tại: http://localhost:{PORT}")
    with socketserver.TCPServer(("", PORT), LocalCustomerHandler) as httpd:
        httpd.serve_forever()
