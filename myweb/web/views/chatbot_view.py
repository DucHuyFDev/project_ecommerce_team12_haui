import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from web.services.chatbot_service import handle_user_question

def safe_serializer(obj):
    from decimal import Decimal
    from datetime import datetime, date
    if isinstance(obj, Decimal): return float(obj)
    if isinstance(obj, (datetime, date)): return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

@csrf_exempt
def chat_ask(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
        user_question = body.get("message", "").strip()

        if not user_question:
            return JsonResponse({"reply": "Chào bạn! Shop có thể giúp gì cho bạn ạ?"})

        # BƯỚC 1: Lấy dữ liệu từ Database thông qua service
        analysis_result = handle_user_question(user_question)
        print(f"DEBUG DATA FROM DB: {analysis_result}")

        # BƯỚC 2: Đóng gói và gửi sang FastAPI (Cổng 8001)
        payload = {
            "question": user_question,
            "context_data": json.loads(json.dumps(analysis_result, default=safe_serializer)),
            "conversation_history": []
        }

        try:
            api_response = requests.post(
                "http://127.0.0.1:8001/chat",
                json=payload,
                timeout=30
            )
            api_response.raise_for_status()
            api_data = api_response.json()
            final_reply = api_data.get("response", "AI đang bận một chút, bạn thử lại nhé!")
            
        except Exception as e:
            print(f"API Connection Error: {e}")
            final_reply = "Rất tiếc, hệ thống AI của Shop đang bảo trì. Vui lòng quay lại sau!"

        return JsonResponse({
            "reply": final_reply,
            "analysis_type": analysis_result.get("type", "general")
        })

    except Exception as e:
        return JsonResponse({"reply": f"Lỗi hệ thống Django: {str(e)}"}, status=500)