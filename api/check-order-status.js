import { getCollection, setCorsHeaders } from './_db.js';

export default async function handler(req, res) {
  setCorsHeaders(res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  const { order_code } = req.query;
  if (!order_code) {
    return res.status(400).json({ error: 'Missing order_code' });
  }

  const orders = await getCollection('orders');
  const order = orders.find(o => o.order_code === order_code || o.id == order_code);

  if (order) {
    return res.status(200).json(order);
  }

  return res.status(404).json({ status: 'not_found' });
}
