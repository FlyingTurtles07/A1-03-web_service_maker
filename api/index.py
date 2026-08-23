from http.server import BaseHTTPRequestHandler
import json, os
from google import genai
from .risk_assessment import assess_risk   # 같은 폴더에서 import

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length))

            # 1. 위험도 계산 (risk_assessment.py에 위임)
            risk_level = assess_risk(
                data['age'], data['sbp'], data['dbp'], data['sugar']
            )

            # 2. AI 안내문 생성 (새 패키지 방식)
            client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
            prompt = f"위험도 분류가 '{risk_level}'인 사용자에게 건강 관리 조언을 해주세요."
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt
            )
            result = response.text

            # 3. 응답
            self._send(200, {"risk_level": risk_level, "message": result})
        except Exception as e:
            self._send(500, {"error": str(e)})

    def _send(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))