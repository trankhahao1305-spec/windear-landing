-- Backup of brain.db SQLite Database Schema and Data
-- Generated on: 2026-08-10

BEGIN TRANSACTION;

-- Table: customers
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    zalo TEXT,
    email TEXT UNIQUE NOT NULL,
    registered_date TEXT,
    goal TEXT,
    note TEXT
);

INSERT INTO customers (id, name, phone, zalo, email, registered_date, goal, note) VALUES
(1, 'Trần Khả Hào', '0332255107', '0332255107', 'haotrankha53@gmail.com', '2026-08-07 14:42:44', 'Nghe không cần sub', ''),
(2, 'Trần Vương Lâm', '0984840024', '0984840024', 'wanglin654654@gmail.com', '2026-08-07 14:45:26', 'Nghe không cần sub', ''),
(3, 'Trần Bình An', '0912345678', '0912345678', 'trankhahao1305+test@gmail.com', '2026-08-10 14:52:00', 'Xem phim không cần sub', ''),
(4, 'TeST review', '0755598888', '0755598888', 'test@gmail.com', '2026-08-09 06:06:03', '', '');

-- Table: products
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT CHECK(type IN ('digital', 'service', 'physical')),
    price REAL NOT NULL,
    description TEXT,
    stock INTEGER
);

INSERT INTO products (id, name, type, price, description, stock) VALUES
(1, 'Sổ Tay 100 Cụm Từ Nối Âm & Nuốt Âm Hollywood', 'digital', 2000, 'PDF 100 cụm từ nuốt âm', NULL),
(2, 'Ebook 4 Bước Luyện Tai Chữa Dứt Điểm Nghe Trôi Chữ', 'digital', 2000, 'Ebook PDF hướng dẫn 4 bước luyện tai', NULL),
(3, 'Khóa Coaching 1-1 Luyện Tai 7 Ngày', 'service', 199000, 'Coaching 1-1 Zoom', NULL),
(4, 'Tai Nghe Monitor Chuyên Luyện Nghe Windear', 'physical', 350000, 'Tai nghe có dây kiểm âm', 10);

-- Table: orders
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_code TEXT UNIQUE NOT NULL,
    customer_id INTEGER,
    product_id INTEGER,
    product_name TEXT,
    customer_name TEXT,
    customer_phone TEXT,
    customer_email TEXT,
    amount REAL,
    status TEXT CHECK(status IN ('pending', 'success', 'failed')),
    created_at TEXT
);

INSERT INTO orders (id, order_code, customer_id, product_id, product_name, customer_name, customer_phone, customer_email, amount, status, created_at) VALUES
(1, 'WD1001', 1, 1, 'Sổ Tay 100 Cụm Từ Nối Âm & Nuốt Âm Hollywood', 'Trần Khả Hào', '0332255107', 'haotrankha53@gmail.com', 2000, 'pending', '2026-08-08 23:55:00'),
(2, 'WD8918', 3, 2, 'Ebook 4 Bước Luyện Tai Chữa Dứt Điểm Nghe Trôi Chữ', 'Trần Bình An', '0984567049', 'trankhahao1305+test@gmail.com', 2000, 'success', '2026-08-10 14:48:00');

COMMIT;
