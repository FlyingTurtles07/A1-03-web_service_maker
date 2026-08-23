from http.server import BaseHTTPRequestHandler
import json
import os
import google.generativeai as genai

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 1. 프론트에서 보낸 데이터 읽기
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)

            # 2. 위험도 분류 결과 받기 (프론트에서 계산한 값)
            risk_level = data.get('risk_level', '안정군')
            age = data.get('age', '')
            bp = data.get('bp', '')       # 혈압
            sugar = data.get('sugar', '') # 혈당

            # 3. 빈 입력 검증
            if not age or not bp or not sugar:
                self.send_error_response(400, "필수값을 입력하세요.")
                return

            # 4. Gemini API 설정 (환경변수에서 키 읽기)
            api_key = os.environ.get('GEMINI_API_KEY')
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')

            # 5. 프롬프트 작성
            prompt = f"""
당신은 만성질환 건강관리 도우미입니다.
아래 사용자의 위험도 분류 결과에 맞는 맞춤 안내 문구를 작성하세요.

- 나이: {age}세
- 혈압: {bp}
- 혈당: {sugar}
- 위험도 분류: {risk_level}

조건:
1. 왜 이 분류에 해당하는지 쉽게 설명
2. 지금 무엇을 해야 하는지 구체적으로 안내
3. 따뜻하고 이해하기 쉬운 말투
"""

            # 6. AI 호출
            response = model.generate_content(prompt)
            result_text = response.text

            # 7. 성공 응답
            self.send_success_response({"message": result_text})

        except Exception as e:
            self.send_error_response(500, f"오류가 발생했습니다: {str(e)}")

    # --- 응답 헬퍼 함수 ---
    def send_success_response(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def send_error_response(self, code, message):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}, ensure_ascii=False).encode('utf-8'))