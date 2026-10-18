import os
from dotenv import load_dotenv
from .vector_store import semantic_search

try:
    from google import genai
except ImportError:
    genai = None

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY")


def generate_rag_response(user_query, chat_history=None):
    """
    RAG Pipeline:
    1. Retrieve relevant knowledge chunks from ChromaDB (with distance threshold).
    2. Enforce Anti-Hallucination Guardrail if no close context matches.
    3. Synthesize natural response via LLM (or grounded fallback).
    """
    # 1. Retrieve filtered context from Vector DB
    retrieved_items = semantic_search(user_query, n_results=2, distance_threshold=0.65)
    
    # 2. Strict Anti-Hallucination Guardrail: Agar database mein context nahi hai
    if not retrieved_items:
        return (
            "I apologize, but that information is not available in the Big Brains official records. "
            "Our programs focus on Artificial Intelligence, Data Science, and Software Engineering. "
            "Please feel free to ask about our courses, internships, fees, or refund policies."
        )

    context_chunks = [item.get("document", "") for item in retrieved_items if item.get("document")]
    retrieved_context = "\n---\n".join(context_chunks)

    # 3. System Instructions for Grounded Synthesis
    system_prompt = f"""You are the official Customer Support Agent for "Big Brains".
Assist the user politely, concisely, and professionally using ONLY the official knowledge context below.

Official Context:
\"\"\"
{retrieved_context}
\"\"\"

Guidelines:
1. Answer the question using ONLY facts stated in the context above.
2. If the context does not contain the answer, politely state: "I apologize, but that information is not available in the Big Brains official records."
3. Speak naturally as a helpful support agent. Never mention "according to the text" or "as per the context".
"""

    # 4. LLM Generation (if Gemini API key is configured)
    if GEMINI_KEY and genai:
        try:
            client = genai.Client(api_key=GEMINI_KEY)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    {"role": "user", "parts": [{"text": f"{system_prompt}\n\nUser Question: {user_query}"}]}
                ]
            )
            if response.text:
                return response.text.strip()
        except Exception as e:
            print(f"[!] LLM Generation Error: {e}")

    # 5. Grounded Fallback (jab API key na ho ya network issue ho)
    top_doc = context_chunks[0]
    clean_info = top_doc.split("Info:")[-1].strip() if "Info:" in top_doc else top_doc
    return f"{clean_info} If you need help enrolling or have more questions, our team is happy to assist!"