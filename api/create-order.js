import { getCollection, saveCollection, setCorsHeaders } from './_db.js';

export default async function handler(req, res) {
  setCorsHeaders(res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
    const { product_id, name, phone, email } = body;

    const products = await getCollection('products');
    const customers = await getCollection('customers');
    const orders = await getCollection('orders');

    const prod = products.find(p => p.id == product_id) || products[0];

    // Find or create customer
    let cust = customers.find(c => c.phone === phone);
    if (!cust) {
      cust = {
        id: customers.length ? Math.max(...customers.map(c => c.id)) + 1 : 1,
        name: name || 'Khách hàng mới',
        phone: phone || '',
        zalo: phone || '',
        email: email || '',
        registered_date: new Date().toLocaleString('vi-VN')
      };
      customers.push(cust);
      await saveCollection('customers', customers);
    }

    const randCode = 'WD' + Math.floor(1000 + Math.random() * 9000);
    const amount = prod.price || 2000;

    const newOrder = {
      id: orders.length ? Math.max(...orders.map(o => o.id)) + 1 : 1,
      customer_id: cust.id,
      product_id: prod.id,
      product_name: prod.name,
      customer_name: name || cust.name,
      customer_phone: phone || cust.phone,
      amount: amount,
      status: 'pending',
      order_code: randCode,
      created_at: new Date().toLocaleString('vi-VN')
    };

    // Inventory handling: only subtract stock if physical product
    if (prod.type === 'physical') {
      prod.stock = Math.max(0, (prod.stock || 0) - 1);
      await saveCollection('products', products);
      console.log(`📦 Trừ tồn kho sản phẩm vật lý ${prod.name}, còn ${prod.stock}`);
    } else {
      console.log(`✨ Sản phẩm số / Dịch vụ ${prod.name} không trừ tồn kho.`);
    }

    orders.unshift(newOrder);
    await saveCollection('orders', orders);

    return res.status(200).json({
      success: true,
      order_id: newOrder.id,
      order_code: randCode,
      amount: amount,
      status: 'pending',
      product_name: prod.name
    });
  } catch (err) {
    console.error('Lỗi create-order:', err);
    return res.status(500).json({ error: err.message });
  }
}
