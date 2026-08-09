import urllib.request
import urllib.error
import json
import os
import ssl

# Đường dẫn config API Key
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(DIRECTORY, "resend_config.txt")

def get_api_key():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def send_email(to_email, subject, html_content, from_email="Windear <hello@windear.online>"):
    """
    Gửi email tự động qua Resend API sử dụng urllib mặc định của Python (không cần cài thêm thư viện).
    """
    api_key = get_api_key()
    if not api_key:
        print("❌ Lỗi: Không tìm thấy Resend API Key trong resend_config.txt")
        return False, "Missing API Key"

    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    data = {
        "from": from_email,
        "to": [to_email] if isinstance(to_email, str) else to_email,
        "subject": subject,
        "html": html_content
    }

    try:
        req = urllib.request.Request(
            url, 
            data=json.dumps(data).encode("utf-8"), 
            headers=headers, 
            method="POST"
        )
        # Bỏ qua xác thực SSL nghiêm ngặt ở local để tránh lỗi SSL UNEXPECTED_EOF trên Windows
        ssl_context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=ssl_context) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            print(f"✅ Gửi email thành công tới {to_email}. ID: {res_json.get('id')}")
            return True, res_json
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            error_json = json.loads(error_body)
            error_msg = error_json.get("message", error_body)
        except Exception:
            error_msg = error_body
        print(f"❌ Lỗi gửi email qua Resend (HTTP {e.code}): {error_msg}")
        return False, f"HTTP {e.code}: {error_msg}"
    except Exception as e:
        print(f"❌ Lỗi gửi email qua Resend: {e}")
        return False, str(e)

if __name__ == "__main__":
    # Chế độ test nhanh khi chạy file trực tiếp
    import sys
    print("--- TEST KẾT NỐI RESEND ---")
    test_email = input("Nhập địa chỉ email thật của bạn để nhận thử: ").strip()
    if test_email:
        print(f"Đang gửi thử nghiệm tới {test_email}...")
        success, res = send_email(
            to_email=test_email, 
            subject="Test kết nối Resend API", 
            html_content="<h1>Kết nối thành công! 🎉</h1><p>Email này được gửi tự động từ hệ thống Windear CRM qua Resend API bằng tên miền <strong>windear.online</strong>.</p>"
        )
        if success:
            print("🎉 Thành công! Hãy kiểm tra hộp thư của bạn (cả hộp thư rác/spam).")
        else:
            print(f"💥 Thất bại. Chi tiết lỗi: {res}")
