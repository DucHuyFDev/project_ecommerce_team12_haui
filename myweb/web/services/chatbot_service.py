from web.services.product_service import (
    get_product_info,
    check_stock,
    get_product_price,
    get_discount_products,
    compare_products,
    get_products_by_category,
    get_product_attributes
)


def handle_user_question(question: str):
    q = question.lower()

    # 1. Sản phẩm đang khuyến mãi
    if "giảm giá" in q or "khuyến mãi" in q:
        return {
            "type": "discount_products",
            "data": get_discount_products()
        }

    # 2. Kiểm tra tồn kho
    if "còn hàng" in q or "hết hàng" in q:
        keyword = question.replace("còn hàng", "").replace("hết hàng", "").strip()
        return {
            "type": "check_stock",
            "data": check_stock(keyword)
        }

    # 3. Giá sản phẩm
    if "giá" in q:
        return {
            "type": "product_price",
            "data": get_product_price(question)
        }

    # 4. So sánh
    if "so sánh" in q:
        names = question.replace("so sánh", "").split("và")
        product_names = [n.strip() for n in names]
        return {
            "type": "compare",
            "data": compare_products(product_names)
        }

    # 5. Theo danh mục
    if "danh mục" in q:
        category = question.replace("danh mục", "").strip()
        return {
            "type": "category",
            "data": get_products_by_category(category)
        }

    # 6. Thuộc tính sản phẩm
    if "màu" in q or "dung lượng" in q:
        return {
            "type": "attributes",
            "data": get_product_attributes(question)
        }

    # 7. Thông tin chung (Khi không rơi vào các trường hợp trên)
    product_data = get_product_info(question)
    
    # 8. Kiểm tra xem có dữ liệu trả về không (product_data là một list)
    if not product_data:
        return {
            "type": "not_understood",
            "data": {
                "message": "Xin lỗi, Shop chưa tìm thấy sản phẩm này. Bạn có thể thử hỏi về giá hoặc tình trạng hàng của các sản phẩm khác nhé!"
            }
        }
    
    # Nếu có dữ liệu, trả về dạng product_info
    return {
        "type": "product_info",
        "data": product_data
    }
