# 📚 VPPShop - Website Bán Văn Phòng Phẩm

## 🚀 Giới thiệu

VPPShop là dự án website thương mại điện tử chuyên cung cấp các sản phẩm văn phòng phẩm, sách vở và dụng cụ học tập. Đây là bài tập lớn môn Phát triển ứng dụng Thương mại điện tử - nhóm 12 - Trường CNTT và TT - Đại học Công nghiệp Hà Nội (HaUI).

## ✨ Tính năng chính

- **Đăng nhập/Đăng ký**: Hệ thống xác thực người dùng an toàn
- **Danh mục sản phẩm đa dạng**: Sách giáo khoa, vở viết, bút các loại, dụng cụ học tập, đồ dùng văn phòng
- **Tìm kiếm & Lọc sản phẩm**: Tìm kiếm nhanh chóng, lọc theo danh mục, giá cả, thương hiệu
- **Giỏ hàng thông minh**: Quản lý giỏ hàng, thanh toán trực tuyến an toàn
- **Đánh giá sản phẩm**: Người dùng có thể đánh giá và xếp hạng sản phẩm
- **Theo dõi đơn hàng**: Cập nhật trạng thái đơn hàng theo thời gian thực
- **Hệ thống khuyến mãi**: Áp dụng mã giảm giá, chương trình khuyến mại
- **Phân quyền người dùng**: Phân quyền Admin/User với các chức năng riêng biệt
- **Tích hợp AI Chatbot**: Tích hợp Gemini AI để giao tiếp với khách hàng trong 1 số kịch bản cơ bản

## 💻 Yêu cầu hệ thống

- **Backend**:
  - Python 3.11+
  - Django 4.2+
  - Django REST Framework
  - PostgreSQL/MySQL/SQL Server (tùy chọn)
  - JWT Authentication
- **Frontend**:
  - HTML5, CSS3, JavaScript
  - Bootstrap 5
  - jQuery
- **Công cụ phát triển**:
  - Git
  - Visual Studio Code (khuyến nghị)
  - Postman (cho API Testing)

## 🛠 Cài đặt
1. **Clone repository**:
   ```bash
   git clone https://github.com/DucHuyFDev/project_ecommerce_team12_haui.git
   cd project_ecommerce_team12_haui
   ```

2. **Tạo và kích hoạt môi trường ảo (khuyến nghị)**:
   ```bash
   # Trên Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Trên macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Cài đặt các gói cần thiết**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Áp dụng migrations và tạo database**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Tạo tài khoản quản trị**:
   ```bash
   python manage.py createsuperuser
   ```
6. **Tạo tài khoản Google Cloud Platform và tạo key API cho Google Cloud Platform** 
- Tạo 1 file config.py trong thư mục chatbot_api với với your-key là key bạn lấy được từ Google AI Studio https://aistudio.google.com/
    ```bash
    GOOGLE_AI_API_KEY = "<your-key>"
    ```

- Đăng ký merchant cho môi trường test VNPay tại website: https://sandbox.vnpayment.vn/devreg, sau đó điền các thông tin sau vào file myweb/setting.py
    ```bash
    VNPAY_RETURN_URL = 'http://localhost:8000/vnpay/payment_return'  # get from config
    VNPAY_PAYMENT_URL = 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html'  # get from config
    VNPAY_API_URL = 'https://sandbox.vnpayment.vn/merchant_webapi/api/transaction'
    VNPAY_TMN_CODE = 'xxxxxxxx'  # Website ID in VNPAY System, get from config
    VNPAY_HASH_SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  # Secret key for create checksum,get from config
    ```

6. **Chạy máy chủ FastAPI**:
    ```bash
    uvicorn main:app --reload --port 8001 
    ```

7.  **Chạy máy chủ Django**:
    ```bash
    python manage.py runserver
    ```
   Duy trì cả 2 máy chủ, không được tắt FastAPI đi
   
8. **Truy cập ứng dụng**:
   - Trang chủ: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Trang quản trị: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## 🚀 Cách sử dụng

### Người dùng thông thường
- Đăng ký tài khoản mới
- Duyệt và tìm kiếm sản phẩm
- Thêm sản phẩm vào giỏ hàng
- Thanh toán đơn hàng
- Theo dõi đơn hàng
- Trò chuyện cơ bản với chatbot

### Quản trị viên
- Quản lý danh mục sản phẩm
- Quản lý đơn hàng
- Quản lý người dùng
- Xem báo cáo thống kê

## 📁 Cấu trúc thư mục

```
project_root/
├── myweb/                  # Django project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # Cấu hình dự án
│   ├── urls.py            # Định tuyến URL chính
│   └── wsgi.py
├── accounts/              # Ứng dụng quản lý người dùng
├── products/              # Ứng dụng quản lý sản phẩm
├── cart/                  # Ứng dụng giỏ hàng
├── orders/                # Ứ dụng quản lý đơn hàng
├── chatbot_api/           # API cho chatbot AI
├── static/                # File tĩnh (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/             # Các file template HTML
│   ├── base.html
│   ├── products/
│   └── accounts/
├── manage.py             # Script quản lý Django
├── requirements.txt      # Các gói Python cần thiết
└── README.md
```

## 📫 Liên hệ

Đại diện đội ngũ phát triển - [@DucHuyFDev](https://github.com/DucHuyFDev)

