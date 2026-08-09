import { getCollection, saveCollection, setCorsHeaders } from './_db.js';

export default async function handler(req, res) {
  setCorsHeaders(res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  const orders = await getCollection('orders');
  const products = await getCollection('products');
  const customers = await getCollection('customers');

  if (req.method === 'GET') {
    return res.status(200).json(orders);
  }

  if (req.method === 'POST') {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
    const custId = parseInt(body.customer_id);
    const prodId = parseInt(body.product_id);
    const amount = parseFloat(body.amount);
    const status = body.status || 'pending';

    const cust = customers.find(c => c.id === custId) || { name: 'Khách hàng', phone: '' };
    const prod = products.find(p => p.id === prodId) || { name: 'Sản phẩm', type: 'digital' };

    const randCode = 'WD' + Math.floor(1000 + Math.random() * 9000);

    const newOrder = {
      id: orders.length ? Math.max(...orders.map(o => o.id)) + 1 : 1,
      customer_id: custId,
      product_id: prodId,
      product_name: prod.name,
      customer_name: cust.name,
      customer_phone: cust.phone,
      amount: amount,
      status: status,
      order_code: randCode,
      created_at: new Date().toLocaleString('vi-VN')
    };

    // Inventory handling: only subtract stock if physical product
    if (prod.type === 'physical') {
      prod.stock = Math.max(0, (prod.stock || 0) - 1);
      await saveCollection('products', products);
      console.log(`📦 [Admin] Đã trừ 1 tồn kho của ${prod.name}, còn lại: ${prod.stock}`);
    } else {
      console.log(`✨ [Admin] Sản phẩm số / Dịch vụ giữ nguyên tồn kho.`);
    }

    orders.unshift(newOrder);
    await saveCollection('orders', orders);

    return res.status(200).json({ success: true, order: newOrder });
  }

  if (req.method === 'DELETE') {
    const { id } = req.query;
    const filtered = orders.filter(o => o.id != id);
    await saveCollection('orders', filtered);
    return res.status(200).json({ success: true });
  }

  return res.status(405).json({ error: 'Method Not Allowed' });
}
