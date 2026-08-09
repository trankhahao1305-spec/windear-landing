// Debug & Init endpoint — dùng để test connectivity và khởi tạo dữ liệu mặc định
// GET /api/debug — trả về trạng thái cloud KV và dữ liệu hiện tại
// POST /api/debug — force re-initialize mọi collections về default

import { getCollection, saveCollection, setCorsHeaders } from './_db.js';

const BUCKET = 'https://kvdb.io/A8v8Qz6D5xQzY7wB2yJ4tK';

export default async function handler(req, res) {
  setCorsHeaders(res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  const results = {};

  // Test raw kvdb connectivity
  try {
    const testRes = await fetch(`${BUCKET}/orders`, { headers: { 'Accept': 'application/json' } });
    results.kvdb_orders_status = testRes.status;
    results.kvdb_orders_text = (await testRes.text()).slice(0, 200);
  } catch (e) {
    results.kvdb_error = e.message;
  }

  // Force reset if POST
  if (req.method === 'POST') {
    const DEFAULT_PRODUCTS = [
      { id: 1, name: "Sổ Tay 100 Cụm Từ Nối Âm & Nuốt Âm Hollywood", type: "digital", price: 2000, description: "Cẩm nang PDF giải mã 100 cụm từ nuốt âm hay gặp nhất trong phim", stock: null },
      { id: 2, name: "Ebook 4 Bước Luyện Tai Chữa Dứt Điểm Nghe Trôi Chữ", type: "digital", price: 2000, description: "Ebook PDF hướng dẫn 4 bước luyện tai tiếng Anh chuyên sâu", stock: null },
      { id: 3, name: "Khóa Coaching 1-1 Luyện Tai 7 Ngày", type: "service", price: 199000, description: "Kèm 1-1 qua Zoom sửa phát âm & phản xạ nghe", stock: null },
      { id: 4, name: "Tai Nghe Monitor Chuyên Luyện Nghe Windear", type: "physical", price: 350000, description: "Tai nghe có dây kiểm âm lọc tạp âm", stock: 10 }
    ];
    const DEFAULT_CUSTOMERS = [
      { id: 1, name: "Trần Khả Hào", phone: "0332255107", zalo: "0332255107", email: "haotrankha53@gmail.com", registered_date: "2026-08-07 14:42:44" },
      { id: 2, name: "Trần Vương Lâm", phone: "0984840024", zalo: "0984840024", email: "wanglin654654@gmail.com", registered_date: "2026-08-07 14:45:26" }
    ];
    const DEFAULT_ORDERS = [
      { id: 1, customer_id: 1, product_id: 1, product_name: "Sổ Tay 100 Cụm Từ Nối Âm & Nuốt Âm Hollywood", customer_name: "Trần Khả Hào", customer_phone: "0332255107", amount: 2000, status: "pending", order_code: "WD1001", created_at: "2026-08-08 23:55:00" }
    ];

    const writes = await Promise.allSettled([
      saveCollection('products', DEFAULT_PRODUCTS),
      saveCollection('customers', DEFAULT_CUSTOMERS),
      saveCollection('orders', DEFAULT_ORDERS)
    ]);
    results.reset = writes.map((w, i) => ({ index: i, status: w.status }));
  }

  // Read current state
  try {
    const [products, customers, orders] = await Promise.all([
      getCollection('products'),
      getCollection('customers'),
      getCollection('orders')
    ]);
    results.products_count = products.length;
    results.customers_count = customers.length;
    results.orders_count = orders.length;
    results.orders_sample = orders.slice(0, 2);
  } catch (e) {
    results.read_error = e.message;
  }

  return res.status(200).json(results);
}
