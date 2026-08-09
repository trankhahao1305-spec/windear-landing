// Shared Database Helper for Vercel Serverless Functions
// Uses Cloud Key-Value REST sync + in-memory cache to ensure all reviewers/devices share the exact same state in real-time

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

// Global in-memory cache
global._windear_cache = global._windear_cache || {
  products: null,
  customers: null,
  orders: null
};

export async function getCollection(name) {
  // 1. Try fetching from Cloud KV
  try {
    const res = await fetch(`${BUCKET}/${name}`, { cache: 'no-store' });
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data) && data.length > 0) {
        global._windear_cache[name] = data;
        return data;
      }
    }
  } catch (err) {
    console.error(`Error reading cloud ${name}:`, err.message);
  }

  // 2. Return memory cache if available
  if (global._windear_cache[name] && global._windear_cache[name].length > 0) {
    return global._windear_cache[name];
  }

  // 3. Fallback to defaults
  let defaults = [];
  if (name === 'products') defaults = [...DEFAULT_PRODUCTS];
  else if (name === 'customers') defaults = [...DEFAULT_CUSTOMERS];
  else if (name === 'orders') defaults = [...DEFAULT_ORDERS];

  global._windear_cache[name] = defaults;
  // Initialize Cloud KV in background
  saveCollection(name, defaults).catch(() => {});
  return defaults;
}

export async function saveCollection(name, data) {
  global._windear_cache[name] = data;
  try {
    await fetch(`${BUCKET}/${name}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  } catch (err) {
    console.error(`Error saving cloud ${name}:`, err.message);
  }
}

export function setCorsHeaders(res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-SePay-Signature');
}
