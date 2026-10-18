import json
import time
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .rag_agent import generate_rag_response

def chat_view(request):
    """Renders the main customer support chat interface."""
    return render(request, 'chat/index.html')

@csrf_exempt
def ask_support(request):
    """
    Phase 4 RAG API Endpoint:
    Receives user query, passes through RAG pipeline (ChromaDB + LLM),
    and returns context-grounded response.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            raw_msg = data.get("message", "").strip()

            if not raw_msg:
                return JsonResponse({"error": "Message cannot be empty."}, status=400)

            # Realistic response delay for UI animation
            time.sleep(0.8)

            user_msg_lower = raw_msg.lower()

            # 1. Natural Conversational Greeting Check
            if any(greet in user_msg_lower.split() for greet in ["hello", "hi", "hey"]):
                reply = (
                    "Hello! I am your Big Brains AI Support Agent powered by RAG and Vector Intelligence. "
                    "How can I assist you with our courses, internships, products, or policies today?"
                )
                return JsonResponse({"status": "success", "reply": reply})

            # 2. Phase 4: Full RAG Pipeline Call
            reply = generate_rag_response(raw_msg)

            return JsonResponse({
                "status": "success",
                "reply": reply
            })

        except Exception as e:
            return JsonResponse({"error": "Internal Server Error occurred."}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)