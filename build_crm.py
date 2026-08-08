import sqlite3
import json
import os

def build_crm_tables(db_path, waitlist_path):
    conn = sqlite3.connect(db_path)
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

    # Nạp data mẫu cho products nếu bảng trống
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        sample_products = [
            ("Ebook 4 Bước Luyện Tai Chữa Dứt Điểm Nghe Trôi Chữ", "digital", 2000, "Ebook PDF hướng dẫn 4 bước luyện tai tiếng Anh chuyên sâu", None),
            ("Template Flashcard 4 Giọng Bản Xứ", "digital", 2000, "Template Anki / Notion luyện phản xạ nghe", None),
            ("Khóa Coaching 1-1 Luyện Tai 7 Ngày", "service", 199000, "Kèm 1-1 qua Zoom sửa phát âm & phản xạ nghe", None),
            ("Tai Nghe Monitor Chuyên Luyện Nghe Windear", "physical", 350000, "Tai nghe có dây kiểm âm lọc tạp âm", 10)
        ]
        cursor.executemany("INSERT INTO products (name, type, price, description, stock) VALUES (?, ?, ?, ?, ?)", sample_products)
        print("✅ Đã thêm sản phẩm mẫu vào bảng products.")

    # Import data từ waitlist.json vào customers (tránh trùng lặp)
    if os.path.exists(waitlist_path):
        with open(waitlist_path, 'r', encoding='utf-8') as f:
            waitlist_data = json.load(f)
            for item in waitlist_data:
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
        print(f"✅ Đã import thành công {len(waitlist_data)} khách hàng từ waitlist.json vào bảng customers (không trùng lặp).")

    # Nạp đơn hàng mẫu nếu chưa có
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
            ''', (cust[0], prod[0], prod[1], cust[1], cust[2], prod[2]))
            print("✅ Đã tạo đơn hàng khởi tạo (pending) mẫu vào bảng orders.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.abspath(__file__))
    db_file = os.path.join(dir_path, "brain.db")
    waitlist_file = os.path.join(dir_path, "waitlist.json")
    build_crm_tables(db_file, waitlist_file)
    print(f"🎉 Hoàn tất cập nhật 3 bảng CRM vào {db_file}")
