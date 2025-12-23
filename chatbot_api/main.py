from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime
import google.generativeai as genai
import json
from config import GOOGLE_AI_API_KEY

# --- Cấu hình API Key ---

app = FastAPI(title="Gemini Chat API")

# Khởi tạo Gemini
try:
    genai.configure(api_key=GOOGLE_AI_API_KEY)
    # Sử dụng model gemini-1.5-flash để phản hồi nhanh và mượt
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    print(f"Lỗi khởi tạo Gemini: {e}")

class ChatRequest(BaseModel):
    question: str
    context_data: Optional[Dict[str, Any]] = None
    conversation_history: Optional[List[Dict[str, Any]]] = []

@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    try:
        user_query = chat_request.question
        db_data = chat_request.context_data
        
        # Xây dựng Prompt "làm mượt" thông tin từ Database
        if db_data and db_data.get("data"):
            data_type = db_data.get("type", "thông tin")
            items = db_data.get("data", [])
            
            # prompt = f"""
            # Bạn là trợ lý ảo thân thiện của 'VPP Shop'. 
            # Nhiệm vụ: Dùng dữ liệu hệ thống dưới đây để trả lời câu hỏi của khách hàng một cách tự nhiên, lịch sự.

            # [DỮ LIỆU HỆ THỐNG - LOẠI: {data_type}]:
            # {json.dumps(items, ensure_ascii=False)}

            # [CÂU HỎI CỦA KHÁCH]:
            # {user_query}

            # [YÊU CẦU]:
            # - KHÔNG liệt kê thô cứng. Hãy viết thành câu văn hoàn chỉnh, mượt mà.
            # - Nếu là giá cả, hãy nêu rõ giá gốc và giá giảm (nếu có).
            # - Nếu không có dữ liệu phù hợp, hãy xin lỗi khách chân thành.
            # - Xưng hô 'Shop' và 'Bạn'.
            # """
            prompt = f"""
            BẠN LÀ TRỢ LÝ BÁN HÀNG TẠI 'VPP SHOP'. 
            
            [DỮ LIỆU TỪ HỆ THỐNG]:
            {json.dumps(items, ensure_ascii=False)}

            [CÂU HỎI CỦA KHÁCH]:
            {user_query}

            [QUY TẮC BẮT BUỘC]:
            1. ƯU TIÊN DỮ LIỆU: Chỉ sử dụng thông tin trong [DỮ LIỆU TỪ HỆ THỐNG] để trả lời. Nếu có thông tin trong đó, TUYỆT ĐỐI KHÔNG được nói là shop không có hàng.
            2. GIÁ CẢ: Nếu khách hỏi giá, hãy lấy con số từ dữ liệu. Nếu có 'GiaSauGiam', hãy báo giá đó là giá đang khuyến mãi.
            3. PHONG CÁCH: Trả lời ngắn gọn, tối đa 3 câu. Xưng hô 'Shop' - 'Bạn'.
            4. LÀM MƯỢT: Viết thành câu tư vấn tự nhiên, không liệt kê gạch đầu dòng khô khan.

            Ví dụ: "Dạ, cuốn sách Tư Duy Nhanh Và Chậm bên Shop đang có giá ưu đãi là 242.100đ ạ. Bạn có muốn Shop lên đơn cho mình không?"
            """
        else:
            prompt = f"Bạn là trợ lý VPP Shop. Hãy trả lời lịch sự câu hỏi: {user_query}"

        response = await model.generate_content_async(prompt)
        
        return {
            "response": response.text.strip(),
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"FastAPI Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))