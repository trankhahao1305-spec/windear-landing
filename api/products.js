import { getCollection, saveCollection, setCorsHeaders } from './_db.js';

export default async function handler(req, res) {
  setCorsHeaders(res);
  if (req.method === 'OPTIONS') return res.status(200).end();

  const products = await getCollection('products');

  if (req.method === 'GET') {
    return res.status(200).json(products);
  }

  if (req.method === 'POST') {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
    const newProd = {
      id: products.length ? Math.max(...products.map(p => p.id)) + 1 : 1,
      name: body.name,
      type: body.type,
      price: parseFloat(body.price),
      description: body.description || '',
      stock: body.type === 'physical' ? parseInt(body.stock || 0) : null
    };
    products.push(newProd);
    await saveCollection('products', products);
    return res.status(200).json({ success: true, product: newProd });
  }

  if (req.method === 'DELETE') {
    const { id } = req.query;
    const filtered = products.filter(p => p.id != id);
    await saveCollection('products', filtered);
    return res.status(200).json({ success: true });
  }

  return res.status(405).json({ error: 'Method Not Allowed' });
}
