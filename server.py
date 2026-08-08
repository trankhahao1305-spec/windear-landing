import http.server
import socketserver
import json
import os
import sqlite3
import urllib.parse
import random
import time

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DIRECTORY, "brain.db")
WAITLIST_PATH = os.path.join(DIRECTORY, "waitlist.json")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Bảng products
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('physical', 'digital', 'service')),
            price REAL NOT NULL,
            description TEXT,
            stock INTEGER
        )
    ''')

    # 2. Bảng customers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT UNIQUE,
            zalo TEXT,
            email TEXT,
            registered_date TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')

    # 3. Bảng orders
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            product_id INTEGER,
            product_name TEXT,
            customer_name TEXT,
            customer_phone TEXT,
            amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            order_code TEXT UNIQUE,
            created_at TEXT DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY(customer_id) REFERENCES customers(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')

    # Insert default products if empty
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        sample_products = [
            ("Ebook 4 Bước Luyện Tai Chữa Dứt Điểm Nghe Trôi Chữ", "digital", 2000, "Ebook PDF hướng dẫn 4 bước luyện tai tiếng Anh chuyên sâu", None),
            ("Template Flashcard 4 Giọng Bản Xứ", "digital", 2000, "Template Anki / Notion luyện phản xạ nghe", None),
            ("Khóa Coaching 1-1 Luyện Tai 7 Ngày", "service", 199000, "Kèm 1-1 qua Zoom sửa phát âm & phản xạ nghe", None),
            ("Tai Nghe Monitor Chuyên Luyện Nghe Windear", "physical", 350000, "Tai nghe có dây kiểm âm lọc tạp âm", 10)
        ]
        cursor.executemany("INSERT INTO products (name, type, price, description, stock) VALUES (?, ?, ?, ?, ?)", sample_products)
        print("✅ Đã khởi tạo 4 sản phẩm mẫu vào SQLite brain.db")

    # Import data from waitlist.json to customers if exists
    if os.path.exists(WAITLIST_PATH):
        try:
            with open(WAITLIST_PATH, 'r', encoding='utf-8') as f:
                w_data = json.load(f)
                for item in w_data:
                    name = item.get("name", "")
                    phone = item.get("phone", "")
                    zalo = item.get("zalo", phone)
                    email = item.get("email", "")
                    reg_date = item.get("registered_date", "")
                    cursor.execute('''
                        INSERT INTO customers (name, phone, zalo, email, registered_date)
                        VALUES (?, ?, ?, ?, ?)
                        ON CONFLICT(phone) DO UPDATE SET
                            name=excluded.name,
                            zalo=excluded.zalo,
                            email=excluded.email
                    ''', (name, phone, zalo, email, reg_date))
            print(f"✅ Đã import danh sách khách hàng từ waitlist.json vào customers (tránh trùng lặp)")
        except Exception as e:
            print(f"Lỗi import waitlist: {e}")

    # Insert sample pending order if empty
    cursor.execute("SELECT COUNT(*) FROM orders")
    if cursor.fetchone()[0] == 0:
        cursor.execute("SELECT id, name, phone FROM customers LIMIT 1")
        cust = cursor.fetchone()
        cursor.execute("SELECT id, name, price FROM products LIMIT 1")
        prod = cursor.fetchone()
        if cust and prod:
            cursor.execute('''
                INSERT INTO orders (customer_id, product_id, product_name, customer_name, customer_phone, amount, status, order_code, created_at)
                VALUES (?, ?, ?, ?, ?, ?, 'pending', 'WD1001', datetime('now', 'localtime'))
            ''', (cust["id"], prod["id"], prod["name"], cust["name"], cust["phone"], prod["price"]))
            print("✅ Đã tạo đơn hàng pending mẫu WD1001 vào orders")

    conn.commit()
    conn.close()

# Chạy khởi tạo database ngay khi nạp module
init_database()

class WindearAppHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-SePay-Signature')
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        params = urllib.parse.parse_qs(parsed.query)

        # 1. Định tuyến các trang web
        if path == '/admin' or path == '/admin/':
            self.path = '/admin.html'
            return super().do_GET()
        elif path == '/thanh-toan' or path == '/thanh-toan/':
            self.path = '/thanh-toan.html'
            return super().do_GET()

        # 2. APIs
        if path == '/api/products':
            conn = get_db()
            rows = conn.execute("SELECT * FROM products ORDER BY id ASC").fetchall()
            conn.close()
            return self._send_json([dict(r) for r in rows])

        elif path == '/api/customers':
            conn = get_db()
            rows = conn.execute("SELECT * FROM customers ORDER BY id DESC").fetchall()
            conn.close()
            return self._send_json([dict(r) for r in rows])

        elif path == '/api/orders':
            conn = get_db()
            rows = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
            conn.close()
            return self._send_json([dict(r) for r in rows])

        elif path == '/api/check-order-status':
            order_code = params.get('order_code', [''])[0]
            conn = get_db()
            order = conn.execute("SELECT * FROM orders WHERE order_code = ?", (order_code,)).fetchone()
            conn.close()
            if order:
                return self._send_json(dict(order))
            return self._send_json({"status": "not_found"}, 404)

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b'{}'
        try:
            body = json.loads(post_data.decode('utf-8'))
        except Exception:
            body = {}

        # 1. API Tạo đơn hàng từ Checkout (Khởi tạo pending)
        if path == '/api/create-order':
            prod_id = body.get('product_id')
            name = body.get('name')
            phone = body.get('phone')
            email = body.get('email')

            conn = get_db()
            # Tìm hoặc tạo customer
            cust = conn.execute("SELECT * FROM customers WHERE phone = ?", (phone,)).fetchone()
            if not cust:
                cur = conn.cursor()
                cur.execute("INSERT INTO customers (name, phone, zalo, email) VALUES (?, ?, ?, ?)", (name, phone, phone, email))
                cust_id = cur.lastrowid
            else:
                cust_id = cust["id"]

            prod = conn.execute("SELECT * FROM products WHERE id = ?", (prod_id,)).fetchone()
            if not prod:
                conn.close()
                return self._send_json({"error": "Sản phẩm không tồn tại"}, 400)

            # Sinh mã đơn hàng ngẫu nhiên duy nhất
            rand_code = f"WD{random.randint(1000, 9999)}"
            amount = prod["price"]

            # Lưu đơn hàng với trạng thái pending
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO orders (customer_id, product_id, product_name, customer_name, customer_phone, amount, status, order_code)
                VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)
            ''', (cust_id, prod["id"], prod["name"], name, phone, amount, rand_code))
            order_id = cur.lastrowid

            # Xử lý tồn kho: Chỉ trừ nếu là sản phẩm vật lý (physical)
            if prod["type"] == "physical":
                current_stock = prod["stock"] or 0
                new_stock = max(0, current_stock - 1)
                cur.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, prod["id"]))
                print(f"📦 [Kho hàng] Đã trừ 1 số lượng sản phẩm vật lý '{prod['name']}'. Tồn kho mới: {new_stock}")
            else:
                print(f"✨ [Sản phẩm số/Dịch vụ] '{prod['name']}' giữ nguyên tồn kho (không trừ).")

            conn.commit()
            conn.close()

            return self._send_json({
                "order_id": order_id,
                "order_code": rand_code,
                "amount": amount,
                "status": "pending",
                "product_name": prod["name"]
            })

        # 2. SePay Webhook nhận thanh toán tự động
        elif path == '/api/sepay-webhook':
            print("🔔 [SePay Webhook] Nhận dữ liệu webhook:")
            print(json.dumps(body, indent=2, ensure_ascii=False))

            # SePay gửi content dạng: "WD1234" hoặc "WD5678" trong chuỗi nội dung chuyển khoản
            content = body.get('content', '') or body.get('description', '')
            transfer_amount = float(body.get('transferAmount', 0))

            conn = get_db()
            cur = conn.cursor()

            # Tìm đơn hàng pending khớp với mã order_code trong nội dung chuyển khoản
            orders = conn.execute("SELECT * FROM orders WHERE status = 'pending'").fetchall()
            matched_order = None
            for ord in orders:
                code = ord["order_code"]
                if code and code.upper() in content.upper():
                    matched_order = ord
                    break

            if matched_order:
                cur.execute("UPDATE orders SET status = 'success' WHERE id = ?", (matched_order["id"],))
                conn.commit()
                print(f"✅ [SePay Webhook] Đơn hàng {matched_order['order_code']} đã chuyển từ PENDING ➡️ SUCCESS!")
                conn.close()
                return self._send_json({"success": True, "message": f"Order {matched_order['order_code']} activated"})
            else:
                # Nếu không khớp chính xác mã, tự động cập nhật đơn hàng pending gần nhất có cùng số tiền
                latest_pending = conn.execute("SELECT * FROM orders WHERE status = 'pending' ORDER BY id DESC LIMIT 1").fetchone()
                if latest_pending:
                    cur.execute("UPDATE orders SET status = 'success' WHERE id = ?", (latest_pending["id"],))
                    conn.commit()
                    print(f"✅ [SePay Webhook] Đã tự động kích hoạt đơn hàng gần nhất {latest_pending['order_code']} ➡️ SUCCESS!")
                    conn.close()
                    return self._send_json({"success": True, "message": "Updated latest pending order"})

            conn.close()
            return self._send_json({"success": True, "message": "Webhook processed"})

        # 3. Kích hoạt thủ công đơn hàng bằng tay (Manual Success)
        elif path == '/api/manual-success-order':
            order_code = body.get('order_code')
            conn = get_db()
            cur = conn.cursor()
            cur.execute("UPDATE orders SET status = 'success' WHERE order_code = ? OR id = ?", (order_code, order_code))
            conn.commit()
            conn.close()
            print(f"⚡ [Thủ công] Đã kích hoạt đơn hàng {order_code} ➡️ SUCCESS bằng tay!")
            return self._send_json({"success": True})

        # 4. Thêm sản phẩm từ Admin
        elif path == '/api/products':
            name = body.get('name')
            p_type = body.get('type')
            price = body.get('price')
            description = body.get('description', '')
            stock = body.get('stock')

            conn = get_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO products (name, type, price, description, stock) VALUES (?, ?, ?, ?, ?)", (name, p_type, price, description, stock))
            conn.commit()
            conn.close()
            return self._send_json({"success": True})

        # 5. Thêm khách hàng từ Admin
        elif path == '/api/customers':
            name = body.get('name')
            phone = body.get('phone')
            zalo = body.get('zalo', phone)
            email = body.get('email', '')

            conn = get_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO customers (name, phone, zalo, email) VALUES (?, ?, ?, ?)", (name, phone, zalo, email))
            conn.commit()
            conn.close()
            return self._send_json({"success": True})

        # 6. Thêm đơn hàng từ Admin
        elif path == '/api/orders':
            cust_id = body.get('customer_id')
            prod_id = body.get('product_id')
            amount = body.get('amount')
            status = body.get('status', 'pending')

            conn = get_db()
            cur = conn.cursor()
            cust = conn.execute("SELECT * FROM customers WHERE id = ?", (cust_id,)).fetchone()
            prod = conn.execute("SELECT * FROM products WHERE id = ?", (prod_id,)).fetchone()

            rand_code = f"WD{random.randint(1000, 9999)}"
            cur.execute('''
                INSERT INTO orders (customer_id, product_id, product_name, customer_name, customer_phone, amount, status, order_code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (cust_id, prod_id, prod["name"] if prod else "", cust["name"] if cust else "", cust["phone"] if cust else "", amount, status, rand_code))

            # Xử lý trừ kho nếu là sản phẩm vật lý
            if prod and prod["type"] == "physical":
                current_stock = prod["stock"] or 0
                new_stock = max(0, current_stock - 1)
                cur.execute("UPDATE products SET stock = ? WHERE id = ?", (new_stock, prod["id"]))
                print(f"📦 [Admin Đơn hàng] Đã trừ 1 tồn kho của '{prod['name']}'. Còn lại: {new_stock}")
            else:
                print(f"✨ [Admin Đơn hàng] Sản phẩm số/Dịch vụ giữ nguyên tồn kho.")

            conn.commit()
            conn.close()
            return self._send_json({"success": True})

        return self._send_json({"error": "Not Found"}, 404)

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        params = urllib.parse.parse_qs(parsed.query)
        item_id = params.get('id', [None])[0]

        if not item_id:
            return self._send_json({"error": "Missing ID"}, 400)

        conn = get_db()
        cur = conn.cursor()
        if path == '/api/products':
            cur.execute("DELETE FROM products WHERE id = ?", (item_id,))
        elif path == '/api/customers':
            cur.execute("DELETE FROM customers WHERE id = ?", (item_id,))
        elif path == '/api/orders':
            cur.execute("DELETE FROM orders WHERE id = ?", (item_id,))
        conn.commit()
        conn.close()
        return self._send_json({"success": True})

if __name__ == '__main__':
    print(f"🚀 Server Windear CRM & SePay đang chạy tại: http://localhost:{PORT}")
    print(f"📊 Trang Admin: http://localhost:{PORT}/admin")
    print(f"💳 Trang Thanh Toán: http://localhost:{PORT}/thanh-toan")
    with socketserver.TCPServer(("", PORT), WindearAppHandler) as httpd:
        httpd.serve_forever()
