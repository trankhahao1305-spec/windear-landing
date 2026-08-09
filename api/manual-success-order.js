import { getCollection, saveCollection, setCorsHeaders } from './_db.js';

export default async function handler(req, res) {
  setCorsHeaders(res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
    const { order_code } = body;

    const orders = await getCollection('orders');
    const order = orders.find(o => o.order_code === order_code || o.id == order_code);

    if (order) {
      order.status = 'success';
      await saveCollection('orders', orders);
      console.log(`⚡ [Manual Success] Kích hoạt thành công đơn hàng ${order_code}`);
      return res.status(200).json({ success: true, order });
    }

    // If not found, activate latest pending order
    const latestPending = orders.find(o => o.status === 'pending');
    if (latestPending) {
      latestPending.status = 'success';
      await saveCollection('orders', orders);
      return res.status(200).json({ success: true, order: latestPending });
    }

    return res.status(404).json({ error: 'Order not found' });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
