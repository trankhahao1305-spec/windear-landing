// Debug endpoint — test Upstash Redis connectivity and data state
import { getCollection, saveCollection, setCorsHeaders } from './_db.js';

export default async function handler(req, res) {
  setCorsHeaders(res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  const UPSTASH_URL = process.env.UPSTASH_REDIS_REST_URL;
  const UPSTASH_TOKEN = process.env.UPSTASH_REDIS_REST_TOKEN;
  const results = {
    env_upstash_url: UPSTASH_URL ? UPSTASH_URL.slice(0, 40) + '...' : 'MISSING',
    env_upstash_token: UPSTASH_TOKEN ? 'SET (' + UPSTASH_TOKEN.length + ' chars)' : 'MISSING'
  };

  // Test 1: Direct Upstash SET
  try {
    const setRes = await fetch(UPSTASH_URL, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${UPSTASH_TOKEN}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(['SET', 'windear:test', 'hello_windear_' + Date.now()])
    });
    const setJson = await setRes.json();
    results.upstash_set_status = setRes.status;
    results.upstash_set_result = setJson.result; // Should be "OK"
  } catch (e) {
    results.upstash_set_error = e.message;
  }

  // Test 2: Direct Upstash GET (verify SET worked)
  try {
    const getRes = await fetch(UPSTASH_URL, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${UPSTASH_TOKEN}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(['GET', 'windear:test'])
    });
    const getJson = await getRes.json();
    results.upstash_get_status = getRes.status;
    results.upstash_get_result = getJson.result; // Should be "hello_windear_..."
  } catch (e) {
    results.upstash_get_error = e.message;
  }

  // Reset collections if POST
  if (req.method === 'POST') {
    const DEFAULT_PRODUCTS = [
      { id: 1, name: "Sổ Tay 100 Cụm Từ Nối Âm & Nuốt Âm Hollywood", type: "digital", price: 2000, description: "Cẩm nang PDF", stock: null },
      { id: 2, name: "Ebook 4 Bước Luyện Tai Chữa Dứt Điểm Nghe Trôi Chữ", type: "digital", price: 2000, description: "Ebook PDF", stock: null },
      { id: 3, name: "Khóa Coaching 1-1 Luyện Tai 7 Ngày", type: "service", price: 199000, description: "Kèm 1-1 qua Zoom", stock: null },
      { id: 4, name: "Tai Nghe Monitor Chuyên Luyện Nghe Windear", type: "physical", price: 350000, description: "Tai nghe kiểm âm", stock: 10 }
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
    results.reset_status = writes.map((w, i) => ({ index: i, status: w.status, reason: w.reason?.message }));
  }

  // Read back via getCollection
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
