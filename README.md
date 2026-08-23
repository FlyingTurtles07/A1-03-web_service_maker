# A1-03-web_service_maker

# 1 . 서비스 기획서 쓰기
```
# 만성질환자 맞춤 원격 건강관리 서비스 기획서

---

## 1. 문제 정의 및 필요성

교통이 불편하거나 거동이 어려운 고령·만성질환자, 그리고 의료기관 접근성이 낮은 도서산간벽지 주민은 정기적인 건강 모니터링과 처방 갱신에 구조적인 어려움을 겪고 있습니다. 특히 고혈압·당뇨 등 만성질환은 짧은 주기의 지속적인 관리가 중요한데, 매번 병원을 방문하기 어려운 환경은 관리 공백으로 이어지기 쉽습니다.

본 서비스는 **간단한 건강정보 입력만으로 위험도를 자동 분류하고, 위험도에 맞는 맞춤 안내를 즉시 제공**하는 원격 건강관리 서비스를 목표로 합니다.


## 2. 서비스 개요

- **1차 대상**: 만성질환(고혈압·당뇨 등) 관리가 필요한 사용자 (경증 환자군은 2단계 확장 대상으로 분리)
- **핵심 기능**: 연령·혈압·혈당 등 건강정보 입력 → 위험도 산정 알고리즘(V2, 연령 가중치 완화 + 혈압·혈당 임상 구간 세분화)으로 점수 계산 → **고위험군 / 위험군 / 안정군** 3단계 분류 → 분류별 맞춤 안내 제공
- **차별점**: 정형화된 수치 판정에 AI를 결합해, 사용자가 이해하기 쉬운 자연어 안내(왜 이 분류인지, 무엇을 해야 하는지)를 생성해 제공


## 3. 미션 구현 범위 (실제 코딩·배포 대상)

**대상 범위 좁히기**: 감기 등 경증 환자군은 이번 구현에서 제외하고, **만성질환자 한 그룹**만 다룹니다. (급성 대응과 만성 관리는 로직 성격이 달라 하나의 점수 체계로 묶기 어렵기 때문)

**실제로 작동하는 것**
1. 페이지 1 — 서비스 소개 (대상/목적/문제의식)
2. 페이지 2 — 건강정보 입력 + 위험도 산정(V2 알고리즘) + **AI API가 분류 결과에 맞는 맞춤 안내 문구 생성**
3. 페이지 3 — 분류 결과 화면
   - 고위험군: "의료기관 연결이 필요합니다" 안내 + AI 생성 문구 (실제 연결 없이 화면 시뮬레이션)
   - 안정군: AI가 생성한 생활관리 조언

**정적 화면(mock)으로만 처리하는 것** — 실제로 작동시키지 않고, "이런 화면이 있다면 이렇게 흐른다"만 보여줌
- 담당의 배정 안내 화면
- 처방전 발급 안내 화면
- 긴급 호출 버튼 → 클릭 시 "관리자에게 알림이 전송되었습니다" 등 정적 문구만 표시 (실제 119/응급 연계 없음)

**이번 범위에서 다루지 않는 것** (아래 "향후 확장 로드맵"으로 이동)
- 실제 담당의 배정·인력 시스템, 처방전 발급·약국 연계·배송, 실제 응급 연계, 지역별 통합 시스템, 정부 연계


## 4. 향후 확장 로드맵 (창업 공모전 버전에서 활용)

| 단계 | 내용 |
|---|---|
| 1단계 (본 미션) | 특정 시범 지역 1곳을 가정, 만성질환자 대상 위험도 분류 + AI 안내 MVP 구현 |
| 2단계 | 경증 환자군(감기 등)으로 대상 확장, 급성 대응 로직 별도 설계 |
| 3단계 | 담당의 실배정 시스템, 처방전-약국 연계, 우체국/택배 배송 연동 |
| 4단계 | 지역별 의료 인프라·정책 차이를 고려한 시범 지역별 파일럿 → 점진적 지역 확장 |
| 5단계 | 정부·지자체 연계, 응급 대응(119) 실연동, 법적·제도적 승인 절차 |

## 5. 지역 통합 시스템에 대한 현실적 접근

의료 인프라, 약국 분포, 지자체 정책이 지역마다 달라 전국 단위 완전 통합은 국가 차원의 표준화가 선행되어야 합니다. 이에 따라 **1단계는 특정 시군 단위의 시범 지역을 가정해 설계**하고, 성과 검증 후 인접 지역으로 단계적으로 확장하는 방식을 제안합니다.

## 6. 남은 논의 과제 (아이디어 단계, 향후 확장 섹션에 기재)

- 처방전 수령 약국이 없는 지역의 배송 방안 (우체국/택배 연계)
- 담당의 배정 이후 주기적 관리·안내 체계
- 지역별 통합 시스템의 단계적 구축 방식

```

# 2. 건강 위험도 점수 계산 AI 기능 구현

## 1 . 백엔드 (api/risk_assessment.py)

calc_risk_score(): 나이/혈압/혈당으로 규칙 기반 점수 계산 (V2 임계값 그대로 적용)
validate_input(): 빈 값·숫자 아님·범위 이탈을 잡아서 "필수값을 입력하세요" 등 에러 메시지 반환
generate_ai_advice(): 점수 결과를 프롬프트에 넣어 OpenAI API 호출, 절대 진단 내리지 않고 3~4문장 생활습관 조언만 생성하도록 지시. API 키 없거나 호출 실패해도 서버가 죽지 않고 안전한 기본 메시지로 대체
handler 클래스가 Vercel Python 함수 포맷(do_POST)으로 위 세 함수를 엮어서 /api/risk_assessment 엔드포인트로 동작

## 2. 프론트엔드 (index.html + css/style.css + js/main.js)

나이/혈압/혈당 입력 폼 + 프론트단 1차 검증 (빈 값이면 필드 빨간 테두리 + 안내 문구)
제출 시 로딩 상태("AI가 분석하는 중...") 표시 → fetch('/api/risk_assessment') 호출
서버 4xx 에러, 네트워크 오류 모두 각각 다른 안내 문구로 처리
결과 카드: 위험도 뱃지, 점수 게이지(세그먼트 바 + 마커), 세부 점수 3개, AI 안내 문구, 면책 문구
고위험군일 때만 "담당의 연결 요청" 시뮬레이션 버튼 노출 (클릭 시 "관리자에게 알림이 전송되었습니다" 정적 문구)

추가로 챙긴 것

.env.example, .gitignore — 5단계에서 강조하신 API 키 노출 방지용
requirements.txt — openai 패키지만 포함

로컬에서 테스트하려면 .env 파일에 OPENAI_API_KEY=sk-...를 넣고 vercel dev로 실행하면 됩니다. 다음 단계(반응형 확인, 배포)로 넘어가고 싶으시면 말씀해주세요.

```
A1-03 web_service_maker
│
├─ index.html
│
├─ css
│   └─ style.css
│
├─ js
│   └─ main.js
│
├─.env.example
│
├─.gitignore
│
├─Requirements.txt
│
└─ Risk assessment.py 
```

프로젝트 폴더 및 파일 생성

## 3.  이완기 혈압 추가 변경 요약

나이·혈당 구간과 총점 기준(0~3 안정군 / 4~7 주의군 / 8+ 고위험군)은 원래도 문서와 정확히 일치했어요.
실제로 빠져 있던 건 혈압 6점 조건의 "또는 이완기 혈압 ≥90" 부분이었습니다 — SBP만 보고 있어서 이완기 혈압만 높은 경우를 놓쳤어요.
index.html에 이완기 혈압 입력 필드 추가
api/risk_assessment.py의 calc_risk_score()를 sbp >= 140 or dbp >= 90 조건으로 수정 (검증 로직에도 dbp 필수값·이완기 < 수축기 체크 추가)
AI 프롬프트에도 이완기 혈압 값 반영
js/main.js는 입력 필드 목록에 dbp만 추가하면 되도록 이미 구조화돼 있어서 최소 수정



# 3. 반응형 확인

## 1. 브라우저에서 개발자 도구 열기
index.html을 브라우저(크롬 추천)로 열고 F12(또는 우클릭 → 검사)를 눌러 개발자 도구를 켭니다. 상단 좌측에 있는 '기기 툴바 전환' 아이콘(작은 폰+태블릿 모양)을 클릭하면 반응형 미리보기 모드로 들어갑니다.

## 2. 데스크톱 화면 확인
일단 기기 툴바를 끈 상태의 일반 데스크톱 너비(보통 1200~1440px 정도)에서 3개 섹션(서비스 소개, 건강정보 입력, 분석 결과)이 레이아웃 안 깨지고 잘 보이는지, 네비게이션 클릭 시 해당 섹션으로 스크롤 이동하는지 확인합니다.

## 3. 모바일 화면 확인
기기 툴바에서 'iPhone SE'나 'iPhone 12 Pro' 같은 프리셋을 선택하거나 직접 너비를 375px 정도로 줄여봅니다. 특히 hero 섹션의 두 컬럼(hero-text + hero-card)이 겹치거나 잘리지 않는지, 폼 입력창들이 화면 밖으로 안 튀어나오는지, 글자 크기가 너무 작아지지 않는지를 중점적으로 봅니다.

## 4. 깨지는 부분 발견 시 AI에게 구체적으로 요청
레이아웃이 깨지면 캡처하거나 정확히 어떤 요소가 어떻게 깨지는지 묘사해서 AI 코딩 도구에 전달하세요. 예: 'index.html의 hero-content가 모바일(375px)에서 두 컬럼이 겹쳐서 나와. css/style.css에 @media (max-width: 768px) 쿼리로 세로 스택 레이아웃으로 바꿔줘.' 처럼 화면 크기, 어떤 클래스/섹션인지, 원하는 결과를 명시하면 훨씬 정확한 코드를 받습니다.

## 5. 최소 2가지 화면 크기 스크린샷 남기기
가이드 8단계(제출 패키지)에 데스크톱·모바일 스크린샷이 필요하니, 지금 확인하면서 잘 나온 화면을 캡처해 별도 폴더에 저장해두면 나중에 다시 열어볼 필요가 없어 편합니다.

## 5.1. 스샷 윈도우 창 크기
<img width="1920" height="1080" alt="스크린샷 2026-08-21 182558" src="https://github.com/user-attachments/assets/8746697d-616a-45fc-8cc9-216514b45d04" />
<img width="1920" height="1080" alt="스크린샷 2026-08-21 182608" src="https://github.com/user-attachments/assets/66bb9831-a640-4385-bd18-64cf8a848989" />
<img width="1920" height="1080" alt="스크린샷 2026-08-21 182615" src="https://github.com/user-attachments/assets/0c1d9ae1-7946-4ab6-a2ac-ab84e0f31d7f" />


## 5.2 스샷 폰 크기
<img width="1920" height="1080" alt="스크린샷 2026-08-21 182650" src="https://github.com/user-attachments/assets/225d9b26-992d-4123-aaf2-32845126c866" />
<img width="1920" height="1080" alt="스크린샷 2026-08-21 182715" src="https://github.com/user-attachments/assets/3e441ad2-853f-418e-9f94-d99174704df6" />
<img width="1920" height="1080" alt="스크린샷 2026-08-21 182732" src="https://github.com/user-attachments/assets/015ba89c-7c41-4f88-9b1c-0ec4ce716e11" />



# 4. AI 기능 백엔드 구현(Vercel Serverless Function)

Gemini API로 사용
---

## 1단계: 폴더 구조 확인

Vercel은 `api/` 폴더 안의 파일을 자동으로 Serverless Function으로 인식합니다.

```
프로젝트루트/
├── index.html
├── css/
├── js/
├── api/
│   └── analyze.py      ← 여기에 백엔드 로직 작성
├── requirements.txt    ← 패키지 목록
├── .env                ← 로컬용 API 키 (절대 커밋 X)
└── .gitignore          ← .env를 여기 등록
```

---

## 2단계: requirements.txt 작성

`api/` 폴더가 아니라 **프로젝트 루트**에 둡니다.

```txt
google-generativeai
```

> 💡 Vercel이 배포할 때 이 파일을 읽고 자동으로 패키지를 설치해줍니다.

---

## 3단계: Serverless Function 뼈대 (`api/analyze.py`)

Vercel의 Python 함수는 `BaseHTTPRequestHandler` 형식을 씁니다.

```python
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
```

> 💡 travel_planner.py와 비교하면 **"프롬프트 만들고 → model.generate_content() 호출 → 결과 받기"** 이 핵심 흐름은 완전히 똑같습니다. 다른 건 웹 요청을 읽고(`do_POST`) 응답을 돌려주는 포장 부분뿐이에요.

---

## 4단계: API 키 환경변수 설정 (가장 중요! ⚠️)

### (A) 로컬 개발용 — `.env` 파일

프로젝트 루트에 `.env` 생성:

```
GEMINI_API_KEY=발급받은_키_여기에
```

그리고 **반드시** `.gitignore`에 추가:

```
.env
```

> 🔒 이걸 안 하면 GitHub에 키가 그대로 올라갑니다. 노출되면 즉시 폐기·재발급해야 하니 처음부터 습관 들이세요!

### (B) 배포용 — Vercel 대시보드

로컬 `.env`는 배포 서버에 올라가지 않으므로, Vercel에 따로 등록해야 합니다.

1. Vercel 프로젝트 → **Settings** 탭
2. **Environment Variables** 메뉴 클릭
3. 입력:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: 발급받은 키
4. Save → **재배포(Redeploy)**

> 💡 코드의 `os.environ.get('GEMINI_API_KEY')`가 로컬에선 `.env`를, 배포 환경에선 Vercel 설정값을 자동으로 읽어옵니다. 코드는 한 번만 짜면 양쪽 다 작동해요!

---

## 다음 단계 미리보기

이 백엔드가 준비되면, 6단계에서 프론트엔드 JS로 이렇게 호출하게 됩니다:

```javascript
const res = await fetch('/api/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ age, bp, sugar, risk_level })
});
const data = await res.json();
```

---

여기까지 잘 따라오셨어요! 정리하면:
1. ✅ `api/analyze.py` — Gemini 호출 로직
2. ✅ `requirements.txt` — 패키지 목록
3. ✅ `.env` + `.gitignore` — 키 안전 관리
4. ✅ Vercel 환경변수 등록

**궁금한 점 하나 확인할게요** — 위험도 분류(고위험/위험/안정군) 계산은 **프론트엔드 JS에서 할 계획인가요, 아니면 이 백엔드 함수에서 할 계획인가요?**

답변에 따라 코드 구조를 살짝 다듬어야 해서요. 어느 쪽으로 생각하고 계신지 알려주시면 그에 맞게 이어서 도와드릴게요! 😊







