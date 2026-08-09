import { getCollection, saveCollection, setCorsHeaders } from './_db.js';

export default async function handler(req, res) {
  setCorsHeaders(res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  const customers = await getCollection('customers');

  if (req.method === 'GET') {
    return res.status(200).json(customers);
  }

  if (req.method === 'POST') {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
    const newCust = {
      id: customers.length ? Math.max(...customers.map(c => c.id)) + 1 : 1,
      name: body.name,
      phone: body.phone,
      zalo: body.zalo || body.phone,
      email: body.email || '',
      registered_date: new Date().toLocaleString('vi-VN')
    };
    customers.unshift(newCust);
    await saveCollection('customers', customers);
    return res.status(200).json({ success: true, customer: newCust });
  }

  if (req.method === 'DELETE') {
    const { id } = req.query;
    const filtered = customers.filter(c => c.id != id);
    await saveCollection('customers', filtered);
    return res.status(200).json({ success: true });
  }

  return res.status(405).json({ error: 'Method Not Allowed' });
}
