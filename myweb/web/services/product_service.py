from django.db.models import Q, F
from web.models import SanPham

# 1. Hàm lấy thông tin chung (Hỏi: "Thông tin về túi canvas")
def get_product_info(question):
    search_term = question.lower()
    for w in ["thông tin", "về", "cho", "biết"]: search_term = search_term.replace(w, "")
    words = [w for w in search_term.split() if len(w) > 1]
    if not words: return []
    
    query = Q()
    for word in words: query &= Q(TenSanPham__icontains=word)
    products = SanPham.objects.filter(query)[:3]
    
    # Trả về các trường đúng theo Model: TenSanPham, MoTa, DonGia, SoLuongTonKho
    return list(products.values("TenSanPham", "MoTa", "DonGia", "SoLuongTonKho"))

# 2. Hàm kiểm tra tồn kho (Hỏi: "Túi canvas còn hàng không?")
def check_stock(keyword_from_chat):
    search_term = keyword_from_chat.lower()
    words = [w for w in search_term.split() if len(w) > 1]
    if not words: return []
    
    query = Q()
    for word in words: query &= Q(TenSanPham__icontains=word)
    products = SanPham.objects.filter(query)[:3]
    return list(products.values("TenSanPham", "SoLuongTonKho"))

# 3. Hàm lấy giá sản phẩm (Hỏi: "Giá túi canvas mèo")
def get_product_price(question):
    search_term = question.lower().replace("giá", "").replace("bao nhiêu", "").strip()
    words = [w for w in search_term.split() if len(w) > 1]
    if not words: return []
    
    query = Q()
    for word in words: query &= Q(TenSanPham__icontains=word)
    products = SanPham.objects.filter(query)[:3]
    
    results = []
    for p in products:
        # Gọi hàm get_discounted_price đã có trong Model SanPham của bạn
        new_price, discount_percent, _ = p.get_discounted_price()
        results.append({
            "TenSanPham": p.TenSanPham,
            "DonGia": float(p.DonGia),
            "GiaSauGiam": float(new_price),
            "PhanTramGiam": discount_percent
        })
    return results

# 4. Hàm lấy sản phẩm giảm giá (Hỏi: "Sản phẩm nào đang khuyến mãi?")
def get_discount_products():
    from django.utils import timezone
    now = timezone.now()
    # Tìm sản phẩm có liên kết KhuyenMai đang trong thời hạn
    products = SanPham.objects.filter(
        khuyen_mai__NgayBatDau__lte=now,
        khuyen_mai__NgayKetThuc__gte=now
    ).distinct()[:5]
    
    results = []
    for p in products:
        new_price, _, _ = p.get_discounted_price()
        results.append({
            "TenSanPham": p.TenSanPham,
            "DonGia": float(p.DonGia),
            "GiaSauGiam": float(new_price)
        })
    return results

# 5. Hàm so sánh sản phẩm (Hỏi: "So sánh túi canvas và bút bi")
def compare_products(product_names):
    all_results = []
    for name in product_names:
        words = [w for w in name.lower().split() if len(w) > 1]
        if not words: continue
        query = Q()
        for word in words: query &= Q(TenSanPham__icontains=word)
        product = SanPham.objects.filter(query).first()
        if product:
            all_results.append({
                "TenSanPham": product.TenSanPham, 
                "DonGia": float(product.DonGia), 
                "SoLuongTonKho": product.SoLuongTonKho
            })
    return all_results

# 6. Hàm lấy sản phẩm theo danh mục (Hỏi: "Danh mục văn phòng phẩm")
def get_products_by_category(category):
    search_term = category.lower()
    words = [w for w in search_term.split() if len(w) > 1]
    if not words: return []
    query = Q()
    for word in words: 
        query &= (Q(TenSanPham__icontains=word) | Q(DanhMuc__TenDanhMuc__icontains=word))
    products = SanPham.objects.filter(query)[:5]
    return list(products.values("TenSanPham", "DonGia"))

# 7. Hàm lấy thuộc tính sản phẩm (Hỏi: "Túi canvas màu gì?")
def get_product_attributes(question):
    search_term = question.lower()
    for w in ["màu", "gì", "loại", "chất liệu", "kích thước"]: search_term = search_term.replace(w, "")
    words = [w for w in search_term.split() if len(w) > 1]
    if not words: return []
    
    query = Q()
    for word in words: query &= Q(TenSanPham__icontains=word)
    
    # Model của bạn dùng EAV (SanPham_ThuocTinh), nên ta cần truy vấn ngược
    products = SanPham.objects.filter(query).first()
    if products:
        attrs = products.thuoc_tinh.all() # related_name='thuoc_tinh'
        attr_list = [f"{a.ThuocTinh.TenThuocTinh}: {a.GiaTriThuocTinh}" for a in attrs]
        return {"TenSanPham": products.TenSanPham, "ThuocTinh": attr_list}
    return []