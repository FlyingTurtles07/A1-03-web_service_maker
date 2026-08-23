"""
api/index.py

Vercel Serverless Function

역할:
1. 프론트엔드에서 건강정보 받기
2. 입력값 검증
3. risk_assessment.py에서 V2 위험도 계산
4. Gemini API로 맞춤 건강관리 안내 생성
5. JSON으로 프론트엔드에 반환
"""

from http.server import BaseHTTPRequestHandler
import json
import os

from google import genai

from .risk_assessment import assess_risk


# ----------------------------------------
# JSON 응답 함수
# ----------------------------------------

def send_json(handler, status_code, data):

    body = json.dumps(
        data,
        ensure_ascii=False
    ).encode("utf-8")

    handler.send_response(status_code)

    handler.send_header(
        "Content-Type",
        "application/json; charset=utf-8"
    )

    handler.send_header(
        "Access-Control-Allow-Origin",
        "*"
    )

    handler.send_header(
        "Access-Control-Allow-Methods",
        "POST, OPTIONS"
    )

    handler.send_header(
        "Access-Control-Allow-Headers",
        "Content-Type"
    )

    handler.end_headers()

    handler.wfile.write(body)


# ----------------------------------------
# Vercel Handler
# ----------------------------------------

class handler(BaseHTTPRequestHandler):

    # ------------------------------------
    # GET
    # ------------------------------------

    def do_GET(self):

        send_json(
            self,
            200,
            {
                "message": "건강 위험도 분석 API입니다.",
                "usage": "POST 요청으로 age, sbp, dbp, sugar를 보내주세요."
            }
        )

    # ------------------------------------
    # OPTIONS
    # ------------------------------------

    def do_OPTIONS(self):

        send_json(
            self,
            200,
            {}
        )

    # ------------------------------------
    # POST
    # ------------------------------------

    def do_POST(self):

        try:

            # --------------------------------
            # 1. 요청 데이터 읽기
            # --------------------------------

            content_length = int(
                self.headers.get(
                    "Content-Length",
                    0
                )
            )

            if content_length <= 0:

                send_json(
                    self,
                    400,
                    {
                        "error": "요청 데이터가 없습니다."
                    }
                )

                return

            body = self.rfile.read(
                content_length
            )

            data = json.loads(
                body.decode("utf-8")
            )


            # --------------------------------
            # 2. 입력값 가져오기
            # --------------------------------

            age = data.get("age")
            sbp = data.get("sbp")
            dbp = data.get("dbp")
            sugar = data.get("sugar")


            # --------------------------------
            # 3. 필수값 검증
            # --------------------------------

            if (
                age is None
                or sbp is None
                or dbp is None
                or sugar is None
            ):

                send_json(
                    self,
                    400,
                    {
                        "error":
                        "나이, 수축기 혈압, 이완기 혈압, 공복혈당을 모두 입력해주세요."
                    }
                )

                return


            # --------------------------------
            # 4. 숫자 변환
            # --------------------------------

            try:

                age = float(age)
                sbp = float(sbp)
                dbp = float(dbp)
                sugar = float(sugar)

            except (TypeError, ValueError):

                send_json(
                    self,
                    400,
                    {
                        "error":
                        "건강정보는 숫자로 입력해주세요."
                    }
                )

                return


            # --------------------------------
            # 5. 범위 검증
            # --------------------------------

            if age < 1 or age > 120:

                send_json(
                    self,
                    400,
                    {
                        "error":
                        "나이는 1세 이상 120세 이하로 입력해주세요."
                    }
                )

                return


            if sbp < 50 or sbp > 250:

                send_json(
                    self,
                    400,
                    {
                        "error":
                        "수축기 혈압(SBP)을 확인해주세요."
                    }
                )

                return


            if dbp < 30 or dbp > 150:

                send_json(
                    self,
                    400,
                    {
                        "error":
                        "이완기 혈압(DBP)을 확인해주세요."
                    }
                )

                return


            if dbp >= sbp:

                send_json(
                    self,
                    400,
                    {
                        "error":
                        "이완기 혈압(DBP)은 수축기 혈압(SBP)보다 낮게 입력해주세요."
                    }
                )

                return


            if sugar < 30 or sugar > 500:

                send_json(
                    self,
                    400,
                    {
                        "error":
                        "공복혈당 수치를 확인해주세요."
                    }
                )

                return


            # --------------------------------
            # 6. V2 위험도 계산
            # --------------------------------

            risk_result = assess_risk(
                age,
                sbp,
                dbp,
                sugar
            )


            # --------------------------------
            # 7. Gemini API Key 확인
            # --------------------------------

            api_key = os.environ.get(
                "GEMINI_API_KEY"
            )

            if not api_key:

                send_json(
                    self,
                    500,
                    {
                        "error":
                        "GEMINI_API_KEY 환경변수가 설정되지 않았습니다."
                    }
                )

                return


            # --------------------------------
            # 8. Gemini Client
            # --------------------------------

            client = genai.Client(
                api_key=api_key
            )


            # --------------------------------
            # 9. Gemini 프롬프트
            # --------------------------------

            prompt = f"""
당신은 만성질환 건강관리 서비스의 AI 안내 도우미입니다.

사용자의 건강정보와 규칙 기반 위험도 분석 결과를 바탕으로
이해하기 쉬운 건강관리 안내를 작성하세요.

[사용자 건강정보]
- 나이: {age}세
- 수축기 혈압(SBP): {sbp} mmHg
- 이완기 혈압(DBP): {dbp} mmHg
- 공복혈당: {sugar} mg/dL

[위험도 분석]
- 나이 점수: {risk_result["age_score"]}점
- 혈압 점수: {risk_result["bp_score"]}점
- 혈당 점수: {risk_result["glucose_score"]}점
- 총점: {risk_result["total_score"]}점
- 위험도: {risk_result["risk_level"]}

다음 조건을 반드시 지키세요.

1. 왜 해당 위험도로 분류되었는지 쉽게 설명하세요.
2. 현재 건강관리에서 주의할 부분을 알려주세요.
3. 실천할 수 있는 생활관리 방법을 2~3개 알려주세요.
4. 의료진의 진단이나 처방을 대신하는 표현을 사용하지 마세요.
5. 응급상황이라고 단정하지 마세요.
6. 3~4문장 정도의 짧고 따뜻한 한국어로 작성하세요.
"""


            # --------------------------------
            # 10. Gemini 호출
            # --------------------------------

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            ai_message = (
                response.text
                if response.text
                else "현재 맞춤 안내를 생성하지 못했습니다."
            )


            # --------------------------------
            # 11. 최종 응답
            # --------------------------------

            result = {
                **risk_result,
                "ai_message": ai_message
            }

            send_json(
                self,
                200,
                result
            )


        # ------------------------------------
        # JSON 오류
        # ------------------------------------

        except json.JSONDecodeError:

            send_json(
                self,
                400,
                {
                    "error":
                    "올바른 JSON 데이터가 아닙니다."
                }
            )


        # ------------------------------------
        # 기타 서버 오류
        # ------------------------------------

        except Exception as e:

            print(
                "SERVER ERROR:",
                repr(e)
            )

            send_json(
                self,
                500,
                {
                    "error":
                    "서버에서 분석 중 오류가 발생했습니다.",
                    "detail": str(e)
                }
            )