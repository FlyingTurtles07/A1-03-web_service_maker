from http.server import BaseHTTPRequestHandler
import json, os
import google.generativeai as genai
from risk_assessment import assess_risk   # ← 계산 로직 import!

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length))

            # 1. 계산은 risk_assessment.py에 위임
            risk_level = assess_risk(
                data['age'], data['sbp'], data['dbp'], data['sugar']
            )

            # 2. AI 안내문 생성 (index.py의 역할)
            genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"위험도 분류가 '{risk_level}'인 사용자에게..."
            result = model.generate_content(prompt).text

            # 3. 응답
            self._send(200, {"risk_level": risk_level, "message": result})
        except Exception as e:
            self._send(500, {"error": str(e)})

    def _send(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))