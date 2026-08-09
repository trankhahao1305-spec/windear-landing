import { getCollection, setCorsHeaders } from './_db.js';

export default async function handler(req, res) {
  setCorsHeaders(res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  try {
    const customers = await getCollection('customers');
    return res.status(200).json(customers);
  } catch (err) {
    console.error('Lỗi getCollection customers:', err);
    return res.status(500).json({ error: err.message });
  }
}
