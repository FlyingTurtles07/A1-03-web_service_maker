"""
api/risk_assessment.py

Vercel Serverless Function (Python)
- 프론트에서 POST /api/risk_assessment 로 age, sbp(수축기 혈압), glucose(공복 혈당)를 받아
  1) 규칙 기반으로 위험도 점수를 계산하고
  2) 계산 결과를 바탕으로 OpenAI API에게 "사람이 읽기 편한 맞춤 안내 문구"를 생성하게 한다.

Vercel 배포 시 주의사항
- 이 파일 하나가 그대로 하나의 API 엔드포인트가 됩니다. (경로: /api/risk_assessment)
- OPENAI_API_KEY는 코드에 절대 직접 쓰지 말고 Vercel 프로젝트의 Environment Variables에 등록하세요.
- 로컬 테스트 시에는 .env 파일에 OPENAI_API_KEY=sk-... 형태로 넣고
  `vercel dev`로 실행하면 이 핸들러가 그대로 동작합니다.
"""

from http.server import BaseHTTPRequestHandler
import json
import os


# 의료 진단이 아님을 항상 고정으로 붙이는 면책 문구
DISCLAIMER = "본 서비스는 의료 진단이 아니며 참고용입니다. 정확한 진단과 처방은 반드시 의료진과 상담하세요."


def calc_risk_score(age: float, sbp: float, dbp: float, glucose: float):
    """
    규칙 기반 위험도 점수 계산 (V2: 연령 가중치 완화 + 혈압·혈당 임상 구간 세분화)
    age: 나이
    sbp: 수축기 혈압 (mmHg)
    dbp: 이완기 혈압 (mmHg)
    glucose: 공복 혈당 (mg/dL)

    혈압 점수 기준:
      - 정상: SBP < 120                         → 0점
      - 주의/고혈압 전단계: 120 <= SBP <= 139     → 3점
      - 고혈압: SBP >= 140 또는 DBP >= 90        → 6점  (둘 중 하나만 충족해도 6점)
    """
    age_score = 0 if age < 40 else (1 if age <= 59 else 2)

    if sbp >= 140 or dbp >= 90:
        bp_score = 6
    elif sbp >= 120:
        bp_score = 3
    else:
        bp_score = 0

    glucose_score = 0 if glucose < 100 else (3 if glucose <= 125 else 6)

    total = age_score + bp_score + glucose_score

    if total >= 8:
        risk_group = "고위험군"
    elif total >= 4:
        risk_group = "주의군"
    else:
        risk_group = "안정군"

    return {
        "age_score": age_score,
        "bp_score": bp_score,
        "glucose_score": glucose_score,
        "total": total,
        "risk_group": risk_group,
    }


def validate_input(data: dict):
    """
    필수값 검증. 문제가 있으면 에러 메시지를, 없으면 None을 반환.
    """
    required = ["age", "sbp", "dbp", "glucose"]
    for field in required:
        if field not in data or data[field] in (None, ""):
            return "필수값을 입력하세요. (나이, 수축기/이완기 혈압, 혈당을 모두 입력해주세요)"

    try:
        age = float(data["age"])
        sbp = float(data["sbp"])
        dbp = float(data["dbp"])
        glucose = float(data["glucose"])
    except (TypeError, ValueError):
        return "나이, 혈압, 혈당은 숫자로 입력해주세요."

    if not (0 < age < 130):
        return "나이 값이 올바르지 않습니다."
    if not (0 < sbp < 300):
        return "혈압(수축기) 값이 올바르지 않습니다."
    if not (0 < dbp < 200):
        return "혈압(이완기) 값이 올바르지 않습니다."
    if dbp >= sbp:
        return "이완기 혈압은 수축기 혈압보다 낮아야 합니다."
    if not (0 < glucose < 700):
        return "혈당 값이 올바르지 않습니다."

    return None


def generate_ai_advice(age, sbp, dbp, glucose, score_result: dict) -> str:
    """
    위험도 산정 결과를 바탕으로 OpenAI API를 호출해 사용자 맞춤 안내 문구를 생성한다.
    AI API 호출이 실패해도 서비스 전체가 죽지 않도록 예외 처리를 해둔다.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        # 키가 아예 설정 안 된 경우를 대비한 안전한 기본 문구
        return "AI 안내 문구 생성에 실패했습니다. (API 키가 설정되지 않았습니다) 잠시 후 다시 시도해주세요."

    

    risk_group = score_result["risk_group"]

    prompt = f"""
당신은 만성질환자 원격 건강관리 서비스의 안내 도우미입니다.
아래 사용자 정보와 위험도 분류 결과를 참고해서, 사용자에게 보여줄 안내 문구를 작성하세요.

[사용자 정보]
- 나이: {age}세
- 수축기 혈압: {sbp} mmHg
- 이완기 혈압: {dbp} mmHg
- 공복 혈당: {glucose} mg/dL
- 위험도 총점: {score_result['total']}점
- 위험도 분류: {risk_group}

[작성 규칙]
1. 절대 의학적 진단을 내리지 말고, 생활습관 조언 위주로 작성할 것
2. 3~4문장, 친절하고 이해하기 쉬운 어투로 작성할 것
3. 위험도 분류가 "고위험군"이면 반드시 가까운 의료기관 방문/상담을 권유하는 문장을 포함할 것
4. 위험도 분류가 "주의군"이면 정기적인 관리와 증상 변화 관찰을 권유할 것
5. 위험도 분류가 "안정군"이면 현재 상태 유지를 위한 생활습관 팁을 줄 것
6. 마크다운 기호(#, *, - 등) 없이 순수 텍스트로만 작성할 것
""".strip()

    
    
class handler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        # 프론트에서 CORS preflight 요청이 올 경우 대비
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            data = json.loads(raw_body.decode("utf-8"))
        except (ValueError, json.JSONDecodeError):
            self._send_json(400, {"error": "요청 형식이 올바르지 않습니다."})
            return

        # 1. 입력값 검증
        error_message = validate_input(data)
        if error_message:
            self._send_json(400, {"error": error_message})
            return

        age = float(data["age"])
        sbp = float(data["sbp"])
        dbp = float(data["dbp"])
        glucose = float(data["glucose"])

        # 2. 규칙 기반 위험도 계산
        score_result = calc_risk_score(age, sbp, dbp, glucose)

        # 3. AI 맞춤 안내 문구 생성
        ai_advice = generate_ai_advice(age, sbp, dbp, glucose, score_result)

        # 4. 결과 응답
        self._send_json(200, {
            "input": {"age": age, "sbp": sbp, "dbp": dbp, "glucose": glucose},
            "score": score_result,
            "ai_advice": ai_advice,
            "disclaimer": DISCLAIMER,
        })
