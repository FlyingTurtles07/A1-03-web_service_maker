# `api/index.py`

from http.server import BaseHTTPRequestHandler
import json
import os

from google import genai

from .risk_assessment import (
    validate_input,
    calculate_risk_score,
)


class handler(BaseHTTPRequestHandler):

    # ----------------------------------------
    # GET
    # ----------------------------------------

    def do_GET(self):
        """브라우저에서 직접 접속했을 때 안내 메시지"""

        self._send(
            200,
            {
                "message": "이 API는 POST 요청만 받습니다.",
                "usage": (
                    "age, sbp, dbp, sugar를 "
                    "JSON으로 보내주세요."
                ),
            },
        )

    # ----------------------------------------
    # POST
    # ----------------------------------------

    def do_POST(self):

        # ----------------------------------------
        # 1. JSON 요청 읽기
        # ----------------------------------------

        try:
            content_length = self.headers.get("Content-Length")

            if not content_length:
                self._send(
                    400,
                    {
                        "error": "요청 데이터가 없습니다."
                    },
                )
                return

            length = int(content_length)

            body = self.rfile.read(length)

            try:
                data = json.loads(body)

            except json.JSONDecodeError:
                self._send(
                    400,
                    {
                        "error": (
                            "잘못된 JSON 요청입니다. "
                            "올바른 JSON 형식으로 보내주세요."
                        )
                    },
                )
                return

        except (TypeError, ValueError):
            self._send(
                400,
                {
                    "error": "잘못된 요청 형식입니다."
                },
            )
            return

        # ----------------------------------------
        # 2. JSON 객체 검사
        # ----------------------------------------

        if not isinstance(data, dict):
            self._send(
                400,
                {
                    "error": (
                        "요청 데이터는 JSON 객체 형식이어야 합니다."
                    )
                },
            )
            return

        # ----------------------------------------
        # 3. 입력값 가져오기
        # ----------------------------------------

        age = data.get("age")
        sbp = data.get("sbp")
        dbp = data.get("dbp")
        sugar = data.get("sugar")

        # ----------------------------------------
        # 4. 백엔드 입력값 검증
        # ----------------------------------------

        valid, error_message = validate_input(
            age,
            sbp,
            dbp,
            sugar,
        )

        if not valid:
            self._send(
                400,
                {
                    "error": error_message
                },
            )
            return

        # ----------------------------------------
        # 5. 위험도 계산
        # ----------------------------------------

        try:
            risk_result = calculate_risk_score(
                age,
                sbp,
                dbp,
                sugar,
            )

        except Exception:
            self._send(
                500,
                {
                    "error": (
                        "건강정보 분석 중 "
                        "오류가 발생했습니다."
                    )
                },
            )
            return

        # ----------------------------------------
        # 6. Gemini API 키 확인
        # ----------------------------------------

        api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            self._send(
                503,
                {
                    "error": (
                        "AI 서비스 설정이 되어 있지 않습니다. "
                        "관리자에게 문의해주세요."
                    )
                },
            )
            return

        # ----------------------------------------
        # 7. Gemini API 호출
        # ----------------------------------------

        try:
            client = genai.Client(
                api_key=api_key
            )

            prompt = f"""
당신은 만성질환 건강관리 도우미입니다.

다음 사용자의 위험도 분석 결과를 바탕으로
건강관리 안내를 작성해주세요.

나이: {age}세
수축기 혈압: {sbp} mmHg
이완기 혈압: {dbp} mmHg
공복혈당: {sugar} mg/dL

위험도: {risk_result["risk_level"]}
총점: {risk_result["total_score"]}점

조건:
1. 3~4문장으로 작성합니다.
2. 사용자가 이해하기 쉬운 표현을 사용합니다.
3. 생활습관 관리 방법을 안내합니다.
4. 질병을 확정적으로 진단하지 않습니다.
5. 증상이 심하거나 위험도가 높은 경우
   의료진 상담을 권고합니다.
"""

            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
            )

            result_text = getattr(
                response,
                "text",
                None,
            )

            if not result_text:
                raise RuntimeError(
                    "Gemini API에서 응답을 받지 못했습니다."
                )

        # ----------------------------------------
        # 8. Gemini API 오류
        # ----------------------------------------

        except Exception as e:

            print(
                "Gemini API ERROR:",
                repr(e),
            )

            self._send(
                502,
                {
                    "error": (
                        "AI 안내문을 생성하는 과정에서 "
                        "오류가 발생했습니다. "
                        "잠시 후 다시 시도해주세요."
                    )
                },
            )
            return

        # ----------------------------------------
        # 9. 최종 성공 응답
        # ----------------------------------------

        self._send(
            200,
            {
                "total_score": risk_result["total_score"],
                "age_score": risk_result["age_score"],
                "bp_score": risk_result["bp_score"],
                "glucose_score": (
                    risk_result["glucose_score"]
                ),
                "risk_level": risk_result["risk_level"],
                "ai_message": result_text,
            },
        )

    # ----------------------------------------
    # JSON 응답
    # ----------------------------------------

    def _send(self, code, data):

        self.send_response(code)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8",
        )

        self.end_headers()

        self.wfile.write(
            json.dumps(
                data,
                ensure_ascii=False,
            ).encode("utf-8")
        )

