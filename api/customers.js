import { getCollection, setCorsHeaders } from './_db.js';

export default async function handler(req, res) {
  setCorsHeaders(res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  const defaultCustomers = [
    { id: 1, name: "Trần Khả Hào", phone: "0332255107", zalo: "0332255107", email: "haotrankha53@gmail.com", registered_date: "2026-08-07 14:42:44" },
    { id: 2, name: "Trần Vương Lâm", phone: "0984840024", zalo: "0984840024", email: "wanglin654654@gmail.com", registered_date: "2026-08-07 14:45:26" },
    { id: 3, name: "Trần Thư Hoài", phone: "0386504118", zalo: "0386504118", email: "haotrankha53@gmail.com", registered_date: "2026-08-09 05:40:09" },
    { id: 4, name: "TeST review", phone: "0755598888", zalo: "0755598888", email: "test@gmail.com", registered_date: "2026-08-09 06:06:03" }
  ];

  try {
    const resp = await fetch('https://kvdb.io/windear_crm_v1/customers');
    if (resp.ok) {
      const cloudCusts = await resp.json();
      if (Array.isArray(cloudCusts) && cloudCusts.length > 0) {
        const localMemory = await getCollection('customers');
        const map = new Map();
        [...cloudCusts, ...localMemory, ...defaultCustomers].forEach(c => {
          if (c && (c.phone || c.id || c.email)) {
            const key = c.phone || c.email || c.id;
            if (!map.has(key)) map.set(key, c);
          }
        });
        return res.status(200).json(Array.from(map.values()));
      }
    }
  } catch (err) {
    console.error('KVDB Fetch Error:', err);
  }

  try {
    const customers = await getCollection('customers');
    return res.status(200).json(customers);
  } catch (err) {
    return res.status(200).json(defaultCustomers);
  }
}
