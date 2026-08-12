# Deploy Notes - Windear Website

## 1. Các biến môi trường (.env) cần có trên VPS
Tạo file `.env` tại thư mục dự án trên VPS với nội dung mẫu:

```env
PORT=8000
GOCLAW_GATEWAY_TOKEN=7c16c2cfcd620ca59e760485ae8f4ff7
EMAIL_SENDER=trankhahao1305@gmail.com
RESEND_API_KEY=your_resend_api_key_here
```

## 2. Cổng đang lắng nghe (Listening Port)
- Mặc định: `8000` (Có thể tùy chỉnh qua biến môi trường `PORT`).

## 3. Lệnh khởi chạy Server trên VPS
```bash
python3 server.py
```

Hoặc chạy ngầm với systemd / nohup / pm2:
```bash
nohup python3 server.py > server.log 2>&1 &
```
