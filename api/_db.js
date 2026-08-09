// Shared Database Helper — Persistent KV Cloud Storage via kvdb.io
// kvdb.io: GET to read, PUT to write (NOT POST)
// Falls back to in-memory if cloud unavailable (dev only)

const BUCKET = 'https://kvdb.io/A8v8Qz6D5xQzY7wB2yJ4tK';

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

const DEFAULTS = { products: DEFAULT_PRODUCTS, customers: DEFAULT_CUSTOMERS, orders: DEFAULT_ORDERS };

// In-memory cache per Lambda instance (warm cache, NOT cross-function)
if (!global._wc) global._wc = {};

export async function getCollection(name) {
  // 1. Try Cloud KV first
  try {
    const res = await fetch(`${BUCKET}/${name}`, {
      headers: { 'Accept': 'application/json' }
    });
    if (res.ok) {
      const text = await res.text();
      if (text && text.trim().startsWith('[')) {
        const data = JSON.parse(text);
        if (Array.isArray(data)) {
          global._wc[name] = data;
          return data;
        }
      }
    }
  } catch (err) {
    console.error(`[getCollection] cloud read ${name} failed:`, err.message);
  }

  // 2. Memory cache fallback (within same Lambda warm instance)
  if (Array.isArray(global._wc[name])) {
    return global._wc[name];
  }

  // 3. Default + initialize cloud in background
  const defaults = JSON.parse(JSON.stringify(DEFAULTS[name] || []));
  global._wc[name] = defaults;
  saveCollection(name, defaults).catch(() => {});
  return defaults;
}

export async function saveCollection(name, data) {
  // Update memory cache immediately
  global._wc[name] = data;

  // Persist to Cloud KV using PUT
  try {
    await fetch(`${BUCKET}/${name}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  } catch (err) {
    console.error(`[saveCollection] cloud write ${name} failed:`, err.message);
  }
  return data;
}

export function setCorsHeaders(res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-SePay-Signature, Authorization');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
}
