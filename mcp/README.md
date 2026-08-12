# Windear MCP Server Documentation

## 1. Giới thiệu
MCP Server này được thiết kế để kết nối hệ thống AI Gateway **GoClaw** với dữ liệu và tính năng của website **Windear Landing & CRM**.

## 2. Các MCP Function Được Hỗ Trợ
1. **`get_today_orders`**: Báo cáo tổng số đơn hàng, doanh thu và danh sách đơn phát sinh trong ngày từ `brain.db`.
2. **`update_landing_hero`**: Thay đổi tiêu đề chính H1 trên trang `index.html` của website.
3. **`send_customer_email`**: Gửi email tự động tới khách hàng qua Resend API.

## 3. Hướng dẫn Deploy lên VPS

### Chạy trực tiếp qua Python
```bash
python3 /opt/windear-landing/mcp/mcp_server.py
```

### Chạy nền 24/7 với Systemd Service
Tạo file `/etc/systemd/system/windear-mcp.service`:

```ini
[Unit]
Description=Windear MCP Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/windear-landing/mcp
ExecStart=/usr/bin/python3 /opt/windear-landing/mcp/mcp_server.py
Restart=always
RestartSec=5
Environment=MCP_PORT=3001

[Install]
WantedBy=multi-user.target
```

Kích hoạt Service trên VPS:
```bash
systemctl daemon-reload
systemctl enable windear-mcp
systemctl restart windear-mcp
systemctl status windear-mcp
```

## 4. Test Kết Nối

Test endpoint sức khỏe:
```bash
curl http://127.0.0.1:3001/health
```

Test gọi tool `get_today_orders`:
```bash
curl -X POST http://127.0.0.1:3001/ -H "Content-Type: application/json" -d '{"tool": "get_today_orders", "params": {}}'
```
