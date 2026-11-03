from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ضع مفتاح Google Gemini API الخاص بك هنا
GEMINI_API_KEY = "AQ.Ab8RN6IYl7KsO0FH2xr-gNotsMf75u4q-pGhd0mlCoRJ5-lemA"  # (أو مفتاح جوجل الخاص بك)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')

    # رابط API المباشر لجوجل مع أحدث موديل
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"أنت مساعد ذكي داخل لعبة روبلوكس. أجب باختصار باللغة العربية على هذا السؤال: {user_message}"}
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, json=payload)
        res_data = response.json()
        
        # استخراج رد الذكاء الاصطناعي
        ai_reply = res_data["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"success": True, "reply": ai_reply})
        
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "reply": "عذراً، حدث خطأ في الاتصال بالخادم!"})

if __name__ == '__main__':
    # هذا السطر مهم لكي يتعرف السيرفر على البورت السحابي أو المحلي تلقائياً
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)