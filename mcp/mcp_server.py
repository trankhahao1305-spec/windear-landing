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
        cur.execute("SELECT id, customer_name, product_name, amount, status, created_at FROM orders WHERE created_at LIKE ?", (f"{target_date}%",))
        rows = [dict(r) for r in cur.fetchall()]
        
        # Nếu chưa có đơn hôm nay, lấy danh sách 5 đơn mới nhất làm báo cáo tổng quan
        if not rows:
            cur.execute("SELECT id, customer_name, product_name, amount, status, created_at FROM orders ORDER BY id DESC LIMIT 5")
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

        req_id = body.get("id", 1)
        method = body.get("method") or body.get("tool")
        params = body.get("params", {})

        # 1. MCP Protocol Initialize
        if method == "initialize":
            return self._send_json({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "my-business", "version": "1.0.0"}
                }
            })

        # 1.b Notifications (initialized, cancelled, etc.)
        elif method and method.startswith("notifications/"):
            return self._send_json({"jsonrpc": "2.0", "id": req_id, "result": {}})

        # 2. MCP Protocol List Tools
        elif method == "tools/list":
            return self._send_json({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": [
                        {
                            "name": "get_today_orders",
                            "description": "Báo cáo đơn hàng và doanh thu trong ngày từ brain.db",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "date": {"type": "string", "description": "Ngày cần xem dạng YYYY-MM-DD"}
                                }
                            }
                        },
                        {
                            "name": "update_landing_hero",
                            "description": "Cập nhật tiêu đề H1 chính trên Landing Page index.html",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "new_headline": {"type": "string", "description": "Nội dung tiêu đề mới"}
                                },
                                "required": ["new_headline"]
                            }
                        },
                        {
                            "name": "send_customer_email",
                            "description": "Gửi email chăm sóc hoặc thông báo cho khách hàng qua Resend API",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "to_email": {"type": "string", "description": "Email người nhận"},
                                    "subject": {"type": "string", "description": "Tiêu đề email"},
                                    "content": {"type": "string", "description": "Nội dung email"}
                                },
                                "required": ["to_email", "content"]
                            }
                        }
                    ]
                }
            })

        # 3. MCP Protocol Call Tool
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            if tool_name == "get_today_orders":
                res = mcp_get_today_orders(tool_args)
            elif tool_name == "update_landing_hero":
                res = mcp_update_landing_hero(tool_args)
            elif tool_name == "send_customer_email":
                res = mcp_send_customer_email(tool_args)
            else:
                res = {"status": "error", "message": f"Unknown tool {tool_name}"}

            return self._send_json({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(res, ensure_ascii=False)}]
                }
            })

        # Backward compatibility for direct tool invocations
        elif method == "get_today_orders":
            return self._send_json(mcp_get_today_orders(params))
        elif method == "update_landing_hero":
            return self._send_json(mcp_update_landing_hero(params))
        elif method == "send_customer_email":
            return self._send_json(mcp_send_customer_email(params))
        else:
            return self._send_json({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method {method} not found"}
            }, 400)

if __name__ == "__main__":
    log(f"🚀 Windear MCP Server starting on port {PORT}")
    with socketserver.TCPServer(("", PORT), MCPRequestHandler) as httpd:
        httpd.serve_forever()
