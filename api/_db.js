// Shared Database Helper — Upstash Redis REST API
// Correct command format: POST / with body ["COMMAND", "args..."]
// Docs: https://upstash.com/docs/redis/features/restapi

const UPSTASH_URL = process.env.UPSTASH_REDIS_REST_URL;
const UPSTASH_TOKEN = process.env.UPSTASH_REDIS_REST_TOKEN;

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

if (!global._wc) global._wc = {};

// ---- Upstash Redis REST API helpers ----
async function upstashCmd(...args) {
  if (!UPSTASH_URL || !UPSTASH_TOKEN) return null;
  try {
    const res = await fetch(UPSTASH_URL, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${UPSTASH_TOKEN}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(args)
    });
    const json = await res.json();
    if (!res.ok) {
      console.error(`[upstash] ${args[0]} error ${res.status}:`, json);
      return null;
    }
    return json.result ?? null;
  } catch (e) {
    console.error('[upstash] network error:', e.message);
    return null;
  }
}

async function upstashGet(key) {
  const result = await upstashCmd('GET', key);
  if (result && typeof result === 'string') {
    try { return JSON.parse(result); } catch(e) { return null; }
  }
  return null;
}

async function upstashSet(key, value) {
  // SET key value — store JSON string
  const result = await upstashCmd('SET', key, JSON.stringify(value));
  console.log(`[upstash] SET ${key} →`, result); // Should log "OK"
  return result;
}

// ---- Public API ----
export async function getCollection(name) {
  // 1. Try Upstash cloud
  const cloudData = await upstashGet(`windear:${name}`);
  if (Array.isArray(cloudData) && cloudData.length > 0) {
    global._wc[name] = cloudData;
    return cloudData;
  }

  // 2. Warm in-memory cache (same Lambda invocation)
  if (Array.isArray(global._wc[name]) && global._wc[name].length > 0) {
    return global._wc[name];
  }

  // 3. Defaults — write to cloud to bootstrap
  const defaults = JSON.parse(JSON.stringify(DEFAULTS[name] || []));
  global._wc[name] = defaults;
  upstashSet(`windear:${name}`, defaults).catch(() => {});
  return defaults;
}

export async function saveCollection(name, data) {
  global._wc[name] = data;
  await upstashSet(`windear:${name}`, data);
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
