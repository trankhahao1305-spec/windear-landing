import http.server
import socketserver
import json
import os
import sqlite3
import datetime
import sys

# Import helper gửi email từ thư mục cha nếu có
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
try:
    from email_sender import send_email
except ImportError:
    send_email = None

PORT = int(os.environ.get("MCP_PORT", 3001))
DB_PATH = os.path.join(BASE_DIR, "brain.db")
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

def log(msg):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] [MCP-SERVER] {msg}")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 1. Function get_today_orders
def mcp_get_today_orders(params):
    log(f"Executing tool 'get_today_orders' with params: {params}")
    target_date = params.get("date", datetime.date.today().strftime("%Y-%m-%d"))
    
    if not os.path.exists(DB_PATH):
        return {"status": "error", "message": f"Database file not found at {DB_PATH}"}

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, customer_name, product_name, amount, status, registered_date FROM orders WHERE registered_date LIKE ?", (f"{target_date}%",))
        rows = [dict(r) for r in cur.fetchall()]
        
        total_revenue = sum(r.get("amount", 0) for r in rows)
        conn.close()
        
        return {
            "status": "success",
            "date": target_date,
            "total_orders": len(rows),
            "total_revenue": total_revenue,
            "orders": rows
        }
    except Exception as e:
        log(f"Error in get_today_orders: {e}")
        return {"status": "error", "message": str(e)}

# 2. Function update_landing_hero
def mcp_update_landing_hero(params):
    log(f"Executing tool 'update_landing_hero' with params: {params}")
    new_headline = params.get("new_headline")
    if not new_headline:
        return {"status": "error", "message": "Missing required parameter 'new_headline'"}

    if not os.path.exists(INDEX_PATH):
        return {"status": "error", "message": f"index.html not found at {INDEX_PATH}"}

    try:
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # Thay thế tiêu đề H1 chính trên Landing Page
        import re
        new_content, count = re.subn(r'(<h1[^>]*>)(.*?)(</h1>)', f'\\1{new_headline}\\3', content, flags=re.DOTALL)
        
        if count > 0:
            with open(INDEX_PATH, "w", encoding="utf-8") as f:
                f.write(new_content)
            log(f"Successfully updated H1 headline in index.html to: {new_headline}")
            return {
                "status": "success",
                "message": f"Updated landing hero headline successfully",
                "new_headline": new_headline,
                "timestamp": datetime.datetime.now().isoformat()
            }
        else:
            return {"status": "error", "message": "Could not locate <h1> tag in index.html"}
    except Exception as e:
        log(f"Error in update_landing_hero: {e}")
        return {"status": "error", "message": str(e)}

# 3. Function send_customer_email
def mcp_send_customer_email(params):
    log(f"Executing tool 'send_customer_email' with params: {params}")
    to_email = params.get("to_email")
    subject = params.get("subject", "Thông báo từ Windear")
    content = params.get("content", "")

    if not to_email or not content:
        return {"status": "error", "message": "Missing 'to_email' or 'content'"}

    if send_email:
        html_body = f"<div><p>{content}</p></div>"
        success, res = send_email(to_email=to_email, subject=subject, html_content=html_body)
        if success:
            return {"status": "success", "message": f"Email sent successfully to {to_email}", "resend_id": res.get("id") if isinstance(res, dict) else res}
        else:
            return {"status": "error", "message": f"Failed to send email: {res}"}
    else:
        return {"status": "success", "message": f"[Simulated] Email to {to_email} with subject '{subject}' logged successfully."}

class MCPRequestHandler(http.server.BaseHTTPRequestHandler):
    def _send_json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_OPTIONS(self):
        self._send_json({"status": "ok"})

    def do_GET(self):
        if self.path == "/" or self.path == "/health":
            return self._send_json({
                "status": "healthy",
                "service": "Windear-MCP-Server",
                "tools": ["get_today_orders", "update_landing_hero", "send_customer_email"]
            })
        return self._send_json({"error": "Not Found"}, 404)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            body = json.loads(body_bytes.decode("utf-8"))
        except Exception:
            body = {}

        tool_name = body.get("tool") or body.get("method")
        params = body.get("params", {})

        if tool_name == "get_today_orders":
            return self._send_json(mcp_get_today_orders(params))
        elif tool_name == "update_landing_hero":
            return self._send_json(mcp_update_landing_hero(params))
        elif tool_name == "send_customer_email":
            return self._send_json(mcp_send_customer_email(params))
        else:
            return self._send_json({
                "error": "Unknown tool",
                "available_tools": ["get_today_orders", "update_landing_hero", "send_customer_email"]
            }, 400)

if __name__ == "__main__":
    log(f"🚀 Windear MCP Server starting on port {PORT}")
    with socketserver.TCPServer(("", PORT), MCPRequestHandler) as httpd:
        httpd.serve_forever()
