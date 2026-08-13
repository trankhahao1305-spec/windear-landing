import http.server
import socketserver
import json
import os
import sqlite3
import urllib.parse
import random
import time
import threading
from email_sender import send_email

PORT = int(os.environ.get("PORT", 8000))
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

def load_email_templates():
    """
    Đọc 3 template email từ file email_sequence.md trong thư mục my-brain.
    """
    my_brain_dir = os.path.join(os.path.dirname(DIRECTORY), "my-brain")
    email_sequence_path = os.path.join(my_brain_dir, "email_sequence.md")
    templates = {"email1": "", "email2": "", "email3": ""}
    
    if os.path.exists(email_sequence_path):
        try:
            with open(email_sequence_path, "r", encoding="utf-8") as f:
                content = f.read()
            # Tách các block ```html ... ```
            parts = content.split("```html")
            if len(parts) >= 4:
                templates["email1"] = parts[1].split("```")[0].strip()
                templates["email2"] = parts[2].split("```")[0].strip()
                templates["email3"] = parts[3].split("```")[0].strip()
                print("✅ Đã load thành công 3 email template từ email_sequence.md")
        except Exception as e:
            print(f"⚠️ Lỗi đọc email_sequence.md: {e}. Sử dụng template fallback.")
            
    # Mẫu dự phòng nếu không đọc được file
    if not templates["email1"]:
        templates["email1"] = "<h2>Chào bạn nha!</h2><p>Cảm ơn bạn đã đăng ký danh sách chờ Windear.</p>"
    if not templates["email2"]:
        templates["email2"] = "<h2>Mẹo nè!</h2><p>Luyện nghe tiếng Anh bằng cách chia nhỏ audio.</p>"
    if not templates["email3"]:
        templates["email3"] = "<h2>Bắt tay vào hành động thôi!</h2><p>Ebook 4 Bước Luyện Tai chỉ 2.000đ.</p>"
        
    return templates

def send_email_sequence_thread(to_email, is_test=False):
    """
    Thread chạy ngầm gửi chuỗi 3 email.
    """
    try:
        print(f"🚀 [Email Sequence] Bắt đầu thread gửi email cho: {to_email} (is_test={is_test})")
        templates = load_email_templates()
        from_email = "Windear <hello@windear.online>"
        
        # 1. Gửi Email 1 chào mừng ngay lập tức
        print(f"📬 [Email Sequence] Đang gửi Email 1 tới {to_email}...")
        ok1, res1 = send_email(
            to_email=to_email,
            subject="Chào bạn! Cảm ơn bạn đã đăng ký danh sách chờ Windear (Quà tặng bên trong 🎁)",
            html_content=templates["email1"],
            from_email=from_email
        )
        print(f"👉 Kết quả Email 1: ok={ok1}, res={res1}")
        
        if is_test:
            # Chế độ Test: Gửi ngay lập tức cả Email 2 & Email 3 (cách nhau 3s để hoàn toàn tránh Rate Limit của Resend)
            time.sleep(3)
            print(f"📬 [Email Sequence - Test] Đang gửi Email 2 tới {to_email}...")
            ok2, res2 = send_email(
                to_email=to_email,
                subject="Mẹo nè: Tại sao banh lỗ tai ra nghe hoài mà tiếng Anh vẫn trôi tuột? 👂💨",
                html_content=templates["email2"],
                from_email=from_email
            )
            print(f"👉 [Test Result Email 2] Success={ok2} | Response={res2}")

            time.sleep(3)
            print(f"📬 [Email Sequence - Test] Đang gửi Email 3 tới {to_email}...")
            ok3, res3 = send_email(
                to_email=to_email,
                subject="Bắt tay vào trị dứt điểm nghe trôi tuột chữ với Ebook 4 Bước Luyện Tai (Chỉ 2.000đ) 📚⚡",
                html_content=templates["email3"],
                from_email=from_email
            )
            print(f"👉 [Test Result Email 3] Success={ok3} | Response={res3}")
        else:
            # Chế độ Thường: Gửi sau 2 ngày và 1 ngày
            print(f"📬 [Email Sequence] Đã lên lịch gửi Email 2 tới {to_email} sau 2 ngày.")
            time.sleep(2 * 24 * 3600)
            print(f"📬 [Email Sequence] Đang gửi Email 2 tới {to_email}...")
            send_email(
                to_email=to_email,
                subject="Mẹo nè: Tại sao banh lỗ tai ra nghe hoài mà tiếng Anh vẫn trôi tuột? 👂💨",
                html_content=templates["email2"],
                from_email=from_email
            )
            
            print(f"📬 [Email Sequence] Đã lên lịch gửi Email 3 tới {to_email} sau 1 ngày nữa.")
            time.sleep(1 * 24 * 3600)
            print(f"📬 [Email Sequence] Đang gửi Email 3 tới {to_email}...")
            send_email(
                to_email=to_email,
                subject="Bắt tay vào trị dứt điểm nghe trôi tuột chữ với Ebook 4 Bước Luyện Tai (Chỉ 2.000đ) 📚⚡",
                html_content=templates["email3"],
                from_email=from_email
            )
    except Exception as err:
        print(f"💥 Lỗi nghiêm trọng trong thread send_email_sequence_thread: {err}")

def send_order_confirmation_email(order_code, customer_name, customer_email, product_name, amount):
    """
    Gửi email xác nhận đơn hàng tự động khi tạo đơn hàng mới.
    """
    if not customer_email:
        print(f"⚠️ Không có email khách hàng cho đơn #{order_code}, bỏ qua gửi email xác nhận.")
        return

    try:
        amount_val = float(amount)
        formatted_amount = f"{amount_val:,.0f} VNĐ".replace(",", ".")
    except Exception:
        formatted_amount = f"{amount} VNĐ"

    from_email = "Windear <hello@windear.online>"
    subject = f"Xác nhận đơn hàng #{order_code} — Cảm ơn bạn đã mua hàng tại Windear! 🎉"
    
    html_content = f"""
    <div style="font-family: 'Plus Jakarta Sans', Arial, sans-serif; line-height: 1.6; color: #1E293B; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #E2E8F0; border-radius: 12px;">
      <h2 style="color: #06B6D4; margin-top: 0;">Cảm ơn bạn {customer_name} nha! 🎉</h2>
      <p>Tui từ <strong>Windear</strong> đây. Xác nhận hệ thống đã ghi nhận đơn hàng mới của bạn thành công rồi nhé!</p>
      
      <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 15px; margin: 20px 0;">
        <h4 style="margin-top: 0; color: #0F172A; border-bottom: 1px solid #CBD5E1; padding-bottom: 8px;">📋 CHI TIẾT ĐƠN HÀNG #{order_code}</h4>
        <p style="margin: 6px 0;"><strong>Sản phẩm:</strong> {product_name}</p>
        <p style="margin: 6px 0;"><strong>Số tiền:</strong> <span style="color: #FF6B4A; font-weight: bold;">{formatted_amount}</span></p>
        <p style="margin: 6px 0;"><strong>Mã đơn hàng:</strong> <code style="background: #E2E8F0; padding: 2px 6px; border-radius: 4px;">{order_code}</code></p>
      </div>

      <h4 style="color: #0F172A;">📦 HƯỚNG DẪN NHẬN HÀNG & TRẢI NGHIỆM:</h4>
      <ul style="padding-left: 20px;">
        <li style="margin-bottom: 8px;"><strong>Sản phẩm số / Ebook:</strong> Bạn có thể mở tải file PDF trực tiếp từ trang xác nhận đơn hàng hoặc qua tài liệu đính kèm.</li>
        <li style="margin-bottom: 8px;"><strong>Khóa Coaching 1-1:</strong> Đội ngũ Windear sẽ nhắn qua Zalo/SĐT để chốt lịch hẹn Zoom trong ít phút nữa.</li>
        <li style="margin-bottom: 8px;"><strong>Tai nghe Windear:</strong> Đơn hàng sẽ được đóng gói và giao tới bạn trong 2-3 ngày làm việc.</li>
      </ul>

      <p>Thật ra, đơn giản thôi, chúc bạn sẽ có những phút giây luyện tai siêu hiệu quả và sớm trị dứt điểm chứng nghe trôi chữ cùng Windear!</p>
      
      <p style="margin-top: 30px; border-top: 1px solid #E2E8F0; padding-top: 15px; font-size: 0.9em; color: #64748B;">
        Thân mến,<br>
        <strong>Tui từ Windear App</strong>
      </p>
    </div>
    """

    print(f"📬 [Order Email] Đang gửi email xác nhận đơn #{order_code} tới {customer_email}...")
    threading.Thread(target=send_email, kwargs={
        "to_email": customer_email,
        "subject": subject,
        "html_content": html_content,
        "from_email": from_email
    }, daemon=True).start()

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

            # Kích hoạt gửi email xác nhận đơn hàng
            if email:
                send_order_confirmation_email(rand_code, name, email, prod["name"], amount)

            return self._send_json({
                "order_id": order_id,
                "order_code": rand_code,
                "amount": amount,
                "status": "pending",
                "product_name": prod["name"]
            })

        # API lưu khách hàng đăng ký từ form waitlist
        elif path == '/api/save-customer':
            name = body.get('name')
            phone = body.get('phone')
            zalo = body.get('zalo', phone)
            email = body.get('email', '')
            goal = body.get('goal', '')
            note = body.get('note', '')

            print(f"📥 [Server API] Nhận đăng ký khách hàng: Name='{name}', Phone='{phone}', Email='{email}'")

            conn = get_db()
            cur = conn.cursor()
            try:
                cur.execute('''
                    INSERT INTO customers (name, phone, zalo, email, registered_date)
                    VALUES (?, ?, ?, ?, datetime('now', 'localtime'))
                    ON CONFLICT(phone) DO UPDATE SET
                        name=excluded.name,
                        zalo=excluded.zalo,
                        email=excluded.email
                ''', (name, phone, zalo, email))
                conn.commit()
            except Exception as e:
                print(f"Lỗi lưu DB customer: {e}")
            finally:
                conn.close()

            # Đồng bộ ghi bổ sung vào waitlist.json
            waitlist_path = os.path.join(DIRECTORY, "waitlist.json")
            try:
                waitlist_data = []
                if os.path.exists(waitlist_path):
                    with open(waitlist_path, "r", encoding="utf-8") as f:
                        waitlist_data = json.load(f)
                
                updated = False
                for w_item in waitlist_data:
                    if w_item.get("phone") == phone:
                        w_item["name"] = name
                        w_item["email"] = email
                        w_item["zalo"] = zalo
                        updated = True
                        break
                if not updated:
                    waitlist_data.append({
                        "name": name,
                        "phone": phone,
                        "zalo": zalo,
                        "email": email,
                        "goal": goal,
                        "note": note,
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                with open(waitlist_path, "w", encoding="utf-8") as f:
                    json.dump(waitlist_data, f, ensure_ascii=False, indent=2)
                print("✅ [Server] Đã đồng bộ khách hàng mới vào waitlist.json")
            except Exception as w_err:
                print(f"⚠️ Lỗi ghi waitlist.json: {w_err}")

            # Cập nhật file waitlist.json để đồng bộ dữ liệu
            try:
                waitlist_data = []
                if os.path.exists(WAITLIST_PATH):
                    with open(WAITLIST_PATH, 'r', encoding='utf-8') as f:
                        waitlist_data = json.load(f)
                
                # Check xem đã có số điện thoại này chưa để cập nhật thông tin mới nhất
                exists = False
                for item in waitlist_data:
                    if item.get("phone") == phone:
                        item["name"] = name
                        item["email"] = email
                        item["zalo"] = zalo
                        item["goal"] = goal
                        item["note"] = note
                        exists = True
                        break
                if not exists:
                    waitlist_data.append({
                        "name": name,
                        "phone": phone,
                        "zalo": zalo,
                        "email": email,
                        "registered_date": time.strftime('%Y-%m-%d %H:%M:%S'),
                        "goal": goal,
                        "note": note
                    })
                with open(WAITLIST_PATH, 'w', encoding='utf-8') as f:
                    json.dump(waitlist_data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"Lỗi cập nhật waitlist.json: {e}")

            # Kích hoạt gửi email sequence tự động qua Resend
            if email:
                is_test = "+test" in email.lower()
                threading.Thread(target=send_email_sequence_thread, args=(email, is_test), daemon=True).start()

            return self._send_json({"success": True})

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
                cust = conn.execute("SELECT * FROM customers WHERE id = ?", (matched_order["customer_id"],)).fetchone() if matched_order["customer_id"] else None
                if cust and cust["email"]:
                    send_order_confirmation_email(matched_order["order_code"], matched_order["customer_name"], cust["email"], matched_order["product_name"], matched_order["amount"])
                conn.close()
                return self._send_json({"success": True, "message": f"Order {matched_order['order_code']} activated"})
            else:
                # Nếu không khớp chính xác mã, tự động cập nhật đơn hàng pending gần nhất có cùng số tiền
                latest_pending = conn.execute("SELECT * FROM orders WHERE status = 'pending' ORDER BY id DESC LIMIT 1").fetchone()
                if latest_pending:
                    cur.execute("UPDATE orders SET status = 'success' WHERE id = ?", (latest_pending["id"],))
                    conn.commit()
                    print(f"✅ [SePay Webhook] Đã tự động kích hoạt đơn hàng gần nhất {latest_pending['order_code']} ➡️ SUCCESS!")
                    cust = conn.execute("SELECT * FROM customers WHERE id = ?", (latest_pending["customer_id"],)).fetchone() if latest_pending["customer_id"] else None
                    if cust and cust["email"]:
                        send_order_confirmation_email(latest_pending["order_code"], latest_pending["customer_name"], cust["email"], latest_pending["product_name"], latest_pending["amount"])
                    conn.close()
                    return self._send_json({"success": True, "message": "Updated latest pending order"})

            conn.close()
            return self._send_json({"success": True, "message": "Webhook processed"})

        # 3. Kích hoạt thủ công đơn hàng bằng tay (Manual Success)
        elif path == '/api/manual-success-order':
            order_code = body.get('order_code')
            conn = get_db()
            cur = conn.cursor()
            ord_item = conn.execute("SELECT * FROM orders WHERE order_code = ? OR id = ?", (order_code, order_code)).fetchone()
            
            if ord_item:
                cur.execute("UPDATE orders SET status = 'success' WHERE id = ?", (ord_item["id"],))
                conn.commit()
                
                cust_id = ord_item["customer_id"]
                cust = conn.execute("SELECT * FROM customers WHERE id = ?", (cust_id,)).fetchone() if cust_id else None
                email = (cust["email"] if cust else None) or body.get("customer_email")
                cust_name = (cust["name"] if cust else None) or ord_item["customer_name"]
                
                if email:
                    send_order_confirmation_email(ord_item["order_code"], cust_name, email, ord_item["product_name"], ord_item["amount"])
                
                print(f"⚡ [Thủ công] Đã kích hoạt đơn hàng {ord_item['order_code']} ({cust_name}) ➡️ SUCCESS và gửi email!")
            else:
                print(f"⚠️ Không tìm thấy đơn hàng {order_code} để kích hoạt!")

            conn.close()
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

            # Kích hoạt gửi email xác nhận đơn hàng khi Admin tạo đơn
            if cust and dict(cust).get("email"):
                send_order_confirmation_email(rand_code, cust["name"], cust["email"], prod["name"] if prod else "", amount)

        elif path == '/api/clear-all-customers':
            conn = get_db()
            cur = conn.cursor()
            cur.execute("DELETE FROM customers")
            cur.execute("DELETE FROM orders")
            conn.commit()
            conn.close()
            
            if os.path.exists(WAITLIST_PATH):
                try:
                    with open(WAITLIST_PATH, "w", encoding="utf-8") as f:
                        json.dump([], f)
                except Exception as e:
                    print("⚠️ Error resetting waitlist.json:", e)
            print("🧹 [Admin] Đã xóa sạch toàn bộ dữ liệu khách hàng & đơn hàng!")
            return self._send_json({"success": True, "message": "All customers cleared"})

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
            c_phone = params.get('phone', [None])[0]
            c_email = params.get('email', [None])[0]
            
            # Xóa khỏi SQLite DB bằng cả ID, số điện thoại hoặc email
            cur.execute("""
                DELETE FROM customers 
                WHERE id = ? 
                   OR (phone = ? AND phone IS NOT NULL AND phone != '') 
                   OR (email = ? AND email IS NOT NULL AND email != '')
            """, (item_id, c_phone, c_email))

            # Xóa triệt để khỏi file waitlist.json
            if os.path.exists(WAITLIST_PATH):
                try:
                    with open(WAITLIST_PATH, "r", encoding="utf-8") as f:
                        w_list = json.load(f)
                    w_list = [
                        w for w in w_list 
                        if str(w.get("id")) != str(item_id) 
                        and (not c_phone or w.get("phone") != c_phone) 
                        and (not c_email or w.get("email") != c_email)
                    ]
                    with open(WAITLIST_PATH, "w", encoding="utf-8") as f:
                        json.dump(w_list, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    print("⚠️ Error updating waitlist.json:", e)
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
