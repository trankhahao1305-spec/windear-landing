export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  
  if (req.method === 'OPTIONS') return res.status(200).end();

  const defaultCustomers = [
    { id: 1, name: "Trần Khả Hào", phone: "0332255107", zalo: "0332255107", email: "haotrankha53@gmail.com", registered_date: "2026-08-07 14:42:44" },
    { id: 2, name: "Trần Vương Lâm", phone: "0984840024", zalo: "0984840024", email: "wanglin654654@gmail.com", registered_date: "2026-08-07 14:45:26" },
    { id: 3, name: "Trần Thư Hoài", phone: "0386504118", zalo: "0386504118", email: "haotrankha53@gmail.com", registered_date: "2026-08-09 05:40:09" },
    { id: 4, name: "TeST review", phone: "0755598888", zalo: "0755598888", email: "test@gmail.com", registered_date: "2026-08-09 06:06:03" }
  ];

  try {
    const resp = await fetch('https://suited-marmot-48766.upstash.io', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer AcV-AAincDE1NGM4MDRiNmY5ZDY0OTg4OGY0OWEzNjY1MDQxZGUxN3AxNDg3NjY',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(["LRANGE", "windear_customers_list", "0", "100"])
    });
    if (resp.ok) {
      const data = await resp.json();
      if (data && Array.isArray(data.result) && data.result.length > 0) {
        const redisCusts = data.result.map(str => {
          try { return typeof str === 'string' ? JSON.parse(str) : str; } catch(e) { return null; }
        }).filter(Boolean);

        const map = new Map();
        [...redisCusts, ...defaultCustomers].forEach(c => {
          if (c && (c.phone || c.id || c.email)) {
            const key = c.phone || c.email || c.id;
            if (!map.has(key)) map.set(key, c);
          }
        });
        return res.status(200).json(Array.from(map.values()));
      }
    }
  } catch (err) {
    console.error('Upstash LRANGE Command Error:', err);
  }

  return res.status(200).json(defaultCustomers);
}
