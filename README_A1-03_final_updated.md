# 만성질환자 맞춤 원격 건강관리

> 간단한 건강정보를 입력하면 규칙 기반 위험도 점수를 계산하고, Google Gemini API를 활용해 위험도에 맞는 맞춤형 건강관리 안내를 제공하는 웹 서비스입니다.

<details>
<summary>📸 캡처 보기 (클릭)</summary>
<br>

<img src="screenshots/%EC%84%9C%EB%B9%84%EC%8A%A4%20%EC%A0%84%EC%B2%B4%20%EB%A9%94%EC%9D%B8%20%ED%99%94%EB%A9%B4.png" width="700"><br>
<sub>서비스 전체 메인 화면</sub>
<br><br>
</details>

---

## 1. 프로젝트 소개

### 서비스명
**만성질환자 맞춤 원격 건강관리**

### 한 줄 소개
고령·만성질환자의 건강정보를 간단하게 입력받아 위험도를 분류하고, AI를 통해 이해하기 쉬운 맞춤형 건강관리 안내를 제공하는 웹 서비스입니다.

### 문제 정의

교통이 불편하거나 거동이 어려운 고령·만성질환자, 의료기관 접근성이 낮은 지역의 주민은 정기적인 건강 모니터링에 어려움을 겪을 수 있습니다.

본 서비스는 이러한 문제를 해결하기 위한 **웹 기반 건강관리 MVP**로, 사용자가 나이·혈압·공복혈당 등의 정보를 입력하면 위험도를 계산하고 그 결과에 맞는 AI 안내를 제공하도록 구현했습니다.

> ⚠️ 본 서비스는 교육 및 미션 수행을 위한 프로토타입입니다. 의료 진단이나 실제 응급·의료기관 연결을 대신하지 않습니다.

---

## 2. 서비스 기획

### 주요 대상

- 고혈압·당뇨 등 만성질환 관리가 필요한 사용자
- 정기적인 건강 상태 확인이 필요한 사용자
- 의료기관 방문이 어려운 환경의 사용자

### 핵심 사용자 흐름

```text
서비스 소개
    ↓
건강정보 입력
    ↓
위험도 점수 계산
    ↓
고위험군 / 주의군 / 안정군 분류
    ↓
Gemini AI 맞춤 건강관리 안내 생성
    ↓
분석 결과 화면 표시
```

### 이번 미션의 구현 범위

1. 서비스 소개 화면
2. 건강정보 입력 및 위험도 분석 화면
3. 위험도 분석 결과 화면
4. 위험도에 따른 AI 맞춤 안내
5. 고위험군의 담당의 연결 요청 시뮬레이션

실제 담당의 배정, 처방전 발급, 약국·배송 연계, 119 등 실제 응급 연계는 구현 범위에서 제외하고 향후 확장 기능으로 정의했습니다.

<span style="background-color:#fff3cd">만성질환자_원격진료_서비스_기획서.md</span>

---

## 3. 주요 기능

### 3-1. 건강정보 입력

사용자가 다음 정보를 입력합니다.

- 나이
- 수축기 혈압(SBP)
- 이완기 혈압(DBP)
- 공복혈당

프론트엔드에서 기본 입력값을 확인하고, 서버에서도 다시 검증합니다.

<details>
<summary>📸 캡처 보기 (클릭)</summary>
<br>

<img src="screenshots/%EA%B1%B4%EA%B0%95%20%EC%A0%95%EB%B3%B4%20%EC%9E%85%EB%A0%A5%20%EC%BA%A1%EC%B3%90.png" width="700"><br>
<sub>건강정보 입력 화면</sub>
<br><br>
</details>

---

### 3-2. 위험도 점수 계산

입력된 건강정보를 기반으로 규칙 기반 위험도 점수를 계산합니다.

위험도는 다음 3단계로 분류합니다.

| 위험도 | 총점 | 의미 |
|---|---:|---|
| 안정군 | 0~3점 | 현재 기준으로 비교적 안정적인 상태 |
| 주의군 | 4~7점 | 생활습관 및 건강 상태 관리가 필요한 상태 |
| 고위험군 | 8점 이상 | 의료기관 상담 및 적극적인 관리가 필요한 상태 |

위험도 계산 로직은 `api/risk_assessment.py`에서 담당하고, 웹 요청 처리는 `api/index.py`에서 담당합니다.

---

### 3-3. Gemini AI 맞춤 안내

위험도 계산 결과를 Gemini API에 전달하여 사용자에게 맞는 건강관리 안내 문구를 생성합니다.

AI는 위험도를 임의로 진단하는 것이 아니라, **이미 계산된 위험도 결과를 바탕으로 사용자가 이해하기 쉬운 생활관리 안내를 생성하는 역할**을 담당합니다.

예시 흐름:

```text
건강정보 입력
    ↓
위험도 계산
    ↓
위험도 분류 결과
    ↓
Gemini 프롬프트 생성
    ↓
Gemini API 호출
    ↓
맞춤 건강관리 안내
    ↓
결과 화면에 표시
```

<details>
<summary>📸 캡처 보기 (클릭)</summary>
<br>

<img src="screenshots/AI%EA%B0%80%20%EC%A0%95%EB%B3%B4%EB%A5%BC%20%EB%B6%84%EC%84%9D%ED%95%98%EB%8A%94%20%EC%A4%91.png" width="700"><br>
<sub>AI가 건강정보를 분석하는 중 (로딩 상태)</sub>
<br><br>
<img src="screenshots/Gemini%20AI%20%EB%B6%84%EC%84%9D%20%EA%B2%B0%EA%B3%BC%EA%B0%80%20%EC%8B%A4%EC%A0%9C%20%ED%99%94%EB%A9%B4%EC%97%90%20%ED%91%9C%EC%8B%9C%EB%90%9C%20%EC%9E%A5%EB%A9%B4.png" width="700"><br>
<sub>Gemini AI 분석 결과가 실제 화면에 표시된 장면</sub>
<br><br>
</details>

---

### 3-4. 분석 결과 화면

분석 결과 화면에는 다음 정보를 표시합니다.

- 위험도 등급
- 총 위험도 점수
- 나이 점수
- 혈압 점수
- 혈당 점수
- Gemini AI 맞춤 건강관리 안내
- 건강 관련 면책 문구

<details>
<summary>📸 캡처 보기 (클릭)</summary>
<br>

<img src="screenshots/13.%20Vercel%20%EB%B0%B0%ED%8F%AC%20%EC%84%B1%EA%B3%B5%20%ED%9B%84%20%EB%8D%B0%EC%8A%A4%ED%81%AC%ED%83%91%20%EC%9E%91%EB%8F%99%20%20%EA%B2%B0%EA%B3%BC%20%EC%BA%A1%EC%B3%90/%EB%B0%B0%ED%8F%AC%20%ED%9B%84%20%EC%9E%91%EB%8F%99%20%EC%BA%A1%EC%B3%90%203%20%EA%B1%B4%EA%B0%95%20%EC%9C%84%ED%97%98%EB%8F%84%20%EB%B6%84%EC%84%9D%20%EA%B2%B0%EA%B3%BC%20%ED%99%94%EB%A9%B4.png" width="700"><br>
<sub>위험도 분석 결과 전체 화면</sub>
<br><br>
</details>

---

### 3-5. 고위험군 담당의 연결 요청 시뮬레이션

고위험군으로 분류된 경우 담당의 연결 요청 버튼을 표시합니다.

이번 미션에서는 실제 의료기관이나 담당의에게 연결하지 않고, 클릭 시 관리자에게 알림이 전송되었다는 정적 안내를 표시하는 방식으로 구현했습니다.

<details>
<summary>📸 캡처 보기 (클릭)</summary>
<br>

<img src="screenshots/%EA%B3%A0%EC%9C%84%ED%97%98%EA%B5%B0%EB%A7%8C%20%EB%8B%B4%EB%8B%B9%EC%9D%98%20%EC%97%B0%EA%B2%B0%20%EC%9A%94%EC%B2%AD%20%EB%B2%84%ED%8A%BC%20%EC%83%9D%EC%84%B1%20%EC%BA%A1%EC%B3%90.png" width="700"><br>
<sub>고위험군 결과 및 담당의 연결 요청 버튼 생성</sub>
<br><br>
<img src="screenshots/%EA%B3%A0%EC%9C%84%ED%97%98%EA%B5%B0%EB%A7%8C%20%EB%8B%B4%EB%8B%B9%EC%9D%98%20%EC%97%B0%EA%B2%B0%20%EC%9A%94%EC%B2%AD%20%EB%B2%84%ED%8A%BC%20%EB%88%8C%EB%9F%AC%20%EC%97%B0%EA%B2%B0%20%EC%9A%94%EC%B2%AD%20%EC%99%84%EB%A3%8C%20%EC%BA%A1%EC%B3%90.png" width="700"><br>
<sub>담당의 연결 요청 버튼 클릭 후 완료 화면</sub>
<br><br>
</details>

---

## 4. 화면 구성

### 페이지/섹션 구성

| 구분 | 내용 |
|---|---|
| 서비스 소개 | 서비스 목적과 대상 사용자 소개 |
| 건강정보 입력 | 나이·혈압·혈당 입력 |
| 분석 결과 | 위험도 점수 및 AI 안내 |
| 추가 안내 | 고위험군 담당의 연결 요청 시뮬레이션 |

<details>
<summary>📸 캡처 보기 (클릭)</summary>
<br>

<img src="screenshots/5.%20%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%94%EB%93%9C%20%ED%99%94%EB%A9%B4%20%EB%B0%8F%20%EB%B0%98%EC%9D%91%ED%98%95%20%EC%A0%81%EC%9A%A9%20%EC%9B%B9%20%EC%BA%A1%EC%B3%90/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202026-08-21%20182558.png" width="700"><br>
<sub>서비스 소개 (메인) 화면</sub>
<br><br>
<img src="screenshots/5.%20%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%94%EB%93%9C%20%ED%99%94%EB%A9%B4%20%EB%B0%8F%20%EB%B0%98%EC%9D%91%ED%98%95%20%EC%A0%81%EC%9A%A9%20%EC%9B%B9%20%EC%BA%A1%EC%B3%90/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202026-08-21%20182608.png" width="700"><br>
<sub>건강정보 입력 화면</sub>
<br><br>
<img src="screenshots/5.%20%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%94%EB%93%9C%20%ED%99%94%EB%A9%B4%20%EB%B0%8F%20%EB%B0%98%EC%9D%91%ED%98%95%20%EC%A0%81%EC%9A%A9%20%EC%9B%B9%20%EC%BA%A1%EC%B3%90/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202026-08-21%20182615.png" width="700"><br>
<sub>분석 결과 화면</sub>
<br><br>
</details>

---

## 5. 반응형 웹

데스크톱과 모바일 화면 크기에서 레이아웃이 깨지지 않도록 CSS 미디어 쿼리를 적용했습니다.

확인 항목:

- 데스크톱 레이아웃
- 모바일 레이아웃
- 입력 폼 너비
- 버튼 크기
- 텍스트 가독성
- Hero 영역의 컬럼 배치
- 네비게이션 및 섹션 이동

<details>
<summary>📸 데스크톱 화면 캡처 (클릭)</summary>
<br>

<img src="screenshots/5.%20%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%94%EB%93%9C%20%ED%99%94%EB%A9%B4%20%EB%B0%8F%20%EB%B0%98%EC%9D%91%ED%98%95%20%EC%A0%81%EC%9A%A9%20%EC%9B%B9%20%EC%BA%A1%EC%B3%90/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202026-08-21%20182558.png" width="700"><br>
<sub>데스크톱 - 메인 화면</sub>
<br><br>
<img src="screenshots/5.%20%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%94%EB%93%9C%20%ED%99%94%EB%A9%B4%20%EB%B0%8F%20%EB%B0%98%EC%9D%91%ED%98%95%20%EC%A0%81%EC%9A%A9%20%EC%9B%B9%20%EC%BA%A1%EC%B3%90/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202026-08-21%20182608.png" width="700"><br>
<sub>데스크톱 - 건강정보 입력 화면</sub>
<br><br>
<img src="screenshots/5.%20%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%94%EB%93%9C%20%ED%99%94%EB%A9%B4%20%EB%B0%8F%20%EB%B0%98%EC%9D%91%ED%98%95%20%EC%A0%81%EC%9A%A9%20%EC%9B%B9%20%EC%BA%A1%EC%B3%90/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202026-08-21%20182615.png" width="700"><br>
<sub>데스크톱 - 분석 결과 화면</sub>
<br><br>
</details>

<details>
<summary>📸 모바일 화면 캡처 (클릭)</summary>
<br>

<img src="screenshots/5.%20%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%94%EB%93%9C%20%ED%99%94%EB%A9%B4%20%EB%B0%8F%20%EB%B0%98%EC%9D%91%ED%98%95%20%EC%A0%81%EC%9A%A9%20%EC%9B%B9%20%EC%BA%A1%EC%B3%90/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202026-08-21%20182650.png" width="700"><br>
<sub>모바일 - 메인 화면</sub>
<br><br>
<img src="screenshots/5.%20%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%94%EB%93%9C%20%ED%99%94%EB%A9%B4%20%EB%B0%8F%20%EB%B0%98%EC%9D%91%ED%98%95%20%EC%A0%81%EC%9A%A9%20%EC%9B%B9%20%EC%BA%A1%EC%B3%90/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202026-08-21%20182715.png" width="700"><br>
<sub>모바일 - 건강정보 입력 화면</sub>
<br><br>
<img src="screenshots/5.%20%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%94%EB%93%9C%20%ED%99%94%EB%A9%B4%20%EB%B0%8F%20%EB%B0%98%EC%9D%91%ED%98%95%20%EC%A0%81%EC%9A%A9%20%EC%9B%B9%20%EC%BA%A1%EC%B3%90/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202026-08-21%20182732.png" width="700"><br>
<sub>모바일 - 분석 결과 화면</sub>
<br><br>
</details>

---

## 6. 기술 스택

### Frontend

- HTML5
- CSS3
- JavaScript
- Fetch API
- 반응형 CSS

### Backend

- Python
- Vercel Serverless Functions
- `http.server.BaseHTTPRequestHandler`

### AI

- Google Gemini API
- `google-genai`

### Deployment

- Vercel
- GitHub

---

## 7. 프로젝트 구조

```text
A1-03-web_service_maker/
│
├── index.html
│
├── css/
│   └── style.css
│
├── js/
│   └── main.js
│
├── api/
│   ├── index.py
│   └── risk_assessment.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### 주요 파일 역할

| 파일 | 역할 |
|---|---|
| `index.html` | 웹 서비스 화면 및 사용자 입력 UI |
| `css/style.css` | 화면 디자인 및 반응형 스타일 |
| `js/main.js` | 사용자 입력, API 호출, 결과 표시 |
| `api/index.py` | Vercel Serverless API, 요청 검증 및 Gemini 호출 |
| `api/risk_assessment.py` | 위험도 점수 계산 및 분류 |
| `.env.example` | 환경변수 설정 예시 |
| `.gitignore` | 비밀정보 및 불필요한 파일의 Git 업로드 방지 |
| `requirements.txt` | Python 패키지 목록 |

---

## 8. AI 처리 구조

```text
[사용자]
   │
   │ 나이 / SBP / DBP / 공복혈당
   ▼
[index.html]
   │
   ▼
[js/main.js]
   │
   │ POST /api/index
   ▼
[api/index.py]
   │
   ├── 입력값 검증
   │
   ├── risk_assessment.py 호출
   │        │
   │        └── 위험도 점수 및 등급 계산
   │
   ├── Gemini API 호출
   │
   └── JSON 응답
   ▼
[js/main.js]
   │
   ▼
[분석 결과 화면]
```

---

## 9. API

### Endpoint

```text
POST /api/index
```

### Request

```json
{
  "age": 60,
  "sbp": 140,
  "dbp": 90,
  "sugar": 126
}
```

### Response

위험도 점수, 위험도 등급, 세부 점수 및 AI 맞춤 안내 등의 결과를 JSON 형태로 반환합니다.

### GET 요청

브라우저에서 `/api/index`에 직접 접속하면 API 상태 확인용 JSON 응답을 확인할 수 있습니다.

---

## 10. 입력값 검증 및 오류 처리

사용자가 잘못된 건강정보를 입력하거나 API 통신 과정에서 오류가 발생하는 경우를 고려하여 **프론트엔드와 백엔드에서 이중으로 입력값을 검증하고, API 오류를 단계별로 처리하도록 구현했습니다.**

### 10-1. 프론트엔드 입력값 검증

`js/main.js`에서 서버에 요청하기 전에 먼저 입력값을 검증합니다.

검증 항목:

- 필수 입력값 누락
- 숫자가 아닌 값 입력
- `NaN`, 무한대 등 비정상 숫자 입력
- 나이 허용 범위 확인: **1~120세**
- 수축기 혈압(SBP) 허용 범위 확인: **50~250mmHg**
- 이완기 혈압(DBP) 허용 범위 확인: **30~150mmHg**
- 이완기 혈압(DBP)이 수축기 혈압(SBP)보다 낮은지 확인
- 공복혈당 허용 범위 확인: **30~500mg/dL**

잘못된 입력이 확인되면 API 요청을 보내지 않고 화면에 이해하기 쉬운 오류 메시지를 표시합니다.

### 10-2. 백엔드 입력값 재검증

프론트엔드 검증을 통과한 데이터라도 서버에서 다시 검증합니다.

`api/index.py`에서는 다음을 확인합니다.

- 요청 데이터 존재 여부
- `Content-Length` 확인
- JSON 형식 여부
- JSON 객체 형식 여부
- 필수 입력값 존재 여부
- 숫자 형식 여부
- 허용 범위
- 수축기/이완기 혈압 관계

실제 검증 로직은 `api/risk_assessment.py`의 `validate_input()`에서 담당하며, 위험도 계산 전에 검증을 완료하도록 구성했습니다.

### 10-3. 오류별 HTTP 응답 처리

오류 유형에 따라 HTTP 상태 코드를 구분합니다.

| 오류 상황 | HTTP 상태 코드 | 사용자 안내 |
|---|---:|---|
| 정상 요청 | 200 | 분석 결과 및 AI 안내 표시 |
| 필수값 누락 | 400 | 필요한 입력값을 입력하도록 안내 |
| 숫자가 아닌 값 | 400 | 숫자로 입력하도록 안내 |
| 허용 범위 초과 | 400 | 올바른 범위를 안내 |
| SBP/DBP 관계 오류 | 400 | 이완기 혈압이 수축기 혈압보다 낮아야 함을 안내 |
| 잘못된 JSON 요청 | 400 | 올바른 JSON 형식으로 요청하도록 안내 |
| 내부 위험도 계산 오류 | 500 | 분석 중 오류가 발생했음을 안내 |
| Gemini API 설정 오류 | 503 | AI 서비스 설정 문제를 안내 |
| Gemini API 호출 오류 | 502 | 잠시 후 다시 시도하도록 안내 |
| 네트워크/통신 오류 | 프론트엔드 처리 | 서버 연결 실패 및 재시도 안내 |

### 10-4. JSON 요청 오류 처리

`api/index.py`에서 JSON 파싱에 실패하면 서버 오류로 처리하지 않고 **400 Bad Request**를 반환합니다.

예:

```text
잘못된 JSON 요청입니다.
올바른 JSON 형식으로 보내주세요.
```

또한 JSON이 객체가 아닌 배열이나 다른 형식으로 전달된 경우에도 잘못된 요청으로 처리합니다.

### 10-5. Gemini API 오류 처리

Gemini API 호출 과정에서 오류가 발생하더라도 서버 전체가 중단되지 않도록 예외를 처리합니다.

다음과 같은 상황을 별도로 고려합니다.

- `GEMINI_API_KEY` 환경변수가 없는 경우
- Gemini API 호출 실패
- Gemini API에서 응답을 받지 못한 경우
- Gemini 응답 처리 중 예외가 발생한 경우

Gemini API 호출 오류는 **502**, API 설정이 되어 있지 않은 경우는 **503**으로 반환하고, 사용자에게 기술적인 오류 내용을 그대로 노출하지 않고 이해하기 쉬운 안내 메시지를 제공합니다.

### 10-6. 네트워크 오류 처리

프론트엔드의 `fetch()` 요청에서 서버와 연결할 수 없는 경우를 `try/catch`로 처리합니다.

네트워크 오류가 발생하면 다음과 같이 사용자에게 안내합니다.

```text
서버와 연결할 수 없습니다.
인터넷 연결을 확인하고 잠시 후 다시 시도해주세요.
```

또한 API 응답이 JSON이 아닌 경우에도 별도로 처리하여 사용자가 알 수 없는 오류 화면을 보지 않도록 했습니다.

### 10-7. 전체 오류 처리 흐름

```text
사용자 입력
    ↓
[프론트엔드 검증]
    ├─ 필수값
    ├─ 숫자 여부
    ├─ 허용 범위
    └─ SBP / DBP 관계
    ↓
POST /api/index
    ↓
[JSON 요청 검증]
    ├─ JSON 파싱
    └─ JSON 객체 여부
    ↓
[백엔드 입력값 재검증]
    ├─ 필수값
    ├─ 숫자
    ├─ 범위
    └─ SBP / DBP 관계
    ↓
위험도 계산
    ↓
Gemini API 호출
    ├─ 설정 오류 → 503
    └─ API 호출 오류 → 502
    ↓
정상 JSON 응답
    ↓
프론트엔드 결과 표시
```

이와 같이 **프론트엔드와 백엔드의 이중 검증 + JSON 오류 처리 + 위험도 계산 오류 처리 + Gemini API 오류 처리 + 네트워크 오류 처리**를 적용했습니다.

<details>
<summary>📸 입력값 검증 및 오류 메시지 캡처 6종 (클릭)</summary>
<br>

<img src="screenshots/10.%20%EC%9E%85%EB%A0%A5%EA%B0%92%20%EA%B2%80%EC%A6%9D%20%EB%B0%8F%20%EC%98%A4%EB%A5%98%20%EC%B2%98%EB%A6%AC%20%EC%BA%A1%EC%B3%90/%EB%B9%88%20%EC%9E%85%EB%A0%A5%EB%9E%80%20%EC%9E%88%EC%9D%84%20%EB%95%8C%20%EB%B6%84%EC%84%9D%20%EC%9A%94%EA%B5%AC%EC%8B%9C%20%EC%BA%A1%EC%B3%90.png" width="700"><br>
<sub>필수 입력값 누락 시 오류</sub>
<br><br>
<img src="screenshots/10.%20%EC%9E%85%EB%A0%A5%EA%B0%92%20%EA%B2%80%EC%A6%9D%20%EB%B0%8F%20%EC%98%A4%EB%A5%98%20%EC%B2%98%EB%A6%AC%20%EC%BA%A1%EC%B3%90/%EC%88%AB%EC%9E%90%EA%B0%80%20%EC%95%84%EB%8B%88%EB%A9%B4%20%EC%9E%85%EB%A0%A5%EC%9D%B4%20%EC%95%88%EB%90%A8%20%EA%B7%B8%EB%9E%98%EB%8F%84%20%EC%88%AB%EC%9E%90%EB%A5%BC%20%EC%9E%85%EB%A0%A5%ED%95%B4%20%EB%8B%AC%EB%9D%BC%20%EC%9A%94%EA%B5%AC%20%EC%BA%A1%EC%B3%90.png" width="700"><br>
<sub>숫자가 아닌 값 입력 시 오류</sub>
<br><br>
<img src="screenshots/10.%20%EC%9E%85%EB%A0%A5%EA%B0%92%20%EA%B2%80%EC%A6%9D%20%EB%B0%8F%20%EC%98%A4%EB%A5%98%20%EC%B2%98%EB%A6%AC%20%EC%BA%A1%EC%B3%90/%EB%A5%98%EB%82%98%EC%9D%B4%20%EB%B2%94%EC%9C%84%20%EC%98%A4%EB%A5%98%20%EC%BA%A1%EC%B3%90.png" width="700"><br>
<sub>나이 허용 범위 초과 오류</sub>
<br><br>
<img src="screenshots/10.%20%EC%9E%85%EB%A0%A5%EA%B0%92%20%EA%B2%80%EC%A6%9D%20%EB%B0%8F%20%EC%98%A4%EB%A5%98%20%EC%B2%98%EB%A6%AC%20%EC%BA%A1%EC%B3%90/SBP%20%EB%B2%94%EC%9C%84%20%EC%98%A4%EB%A5%98%20%EC%BA%A1%EC%B3%90.png" width="700"><br>
<sub>수축기 혈압(SBP) 허용 범위 초과 오류</sub>
<br><br>
<img src="screenshots/10.%20%EC%9E%85%EB%A0%A5%EA%B0%92%20%EA%B2%80%EC%A6%9D%20%EB%B0%8F%20%EC%98%A4%EB%A5%98%20%EC%B2%98%EB%A6%AC%20%EC%BA%A1%EC%B3%90/%ED%98%88%EB%8B%B9%20%EB%B2%94%EC%9C%84%20%EC%98%A4%EB%A5%98%20%EC%BA%A1%EC%B3%90.png" width="700"><br>
<sub>공복혈당 허용 범위 초과 오류</sub>
<br><br>
<img src="screenshots/10.%20%EC%9E%85%EB%A0%A5%EA%B0%92%20%EA%B2%80%EC%A6%9D%20%EB%B0%8F%20%EC%98%A4%EB%A5%98%20%EC%B2%98%EB%A6%AC%20%EC%BA%A1%EC%B3%90/%ED%98%88%EC%95%95%20%EA%B4%80%EA%B3%84%20%EC%98%A4%EB%A5%98%20SBP%EA%B0%80%20DBP%EB%B3%B4%EB%8B%A4%20%EB%82%AE%EC%9C%BC%EB%A9%B4%20%EC%95%88%EB%90%A8%20%EC%9E%85%EB%A0%A5%20%EC%98%A4%EB%A5%98%20%EC%9D%B4%EC%83%81%20%EA%B0%90%EC%A7%80%20%EC%BA%A1%EC%B3%90.png" width="700"><br>
<sub>SBP/DBP 관계 오류 (이완기가 수축기보다 높은 경우)</sub>
<br><br>
</details>

---

## 11. 환경변수 및 API 키 보안

API 키는 소스코드에 직접 작성하지 않고 환경변수로 관리합니다.

### 로컬 개발

프로젝트 루트에 `.env` 파일을 만들고 Gemini API 키를 설정합니다.

```env
GEMINI_API_KEY=여기에_실제_API_키
```

### 주의사항

- `.env` 파일은 GitHub에 업로드하지 않습니다.
- 실제 API 키를 README에 작성하지 않습니다.
- 실제 API 키가 포함된 화면을 캡처하지 않습니다.
- `.gitignore`에 `.env`를 등록합니다.
- Vercel 배포 환경에서는 Vercel Environment Variables에 API 키를 등록합니다.

---

## 12. 로컬 실행 방법

### 1. 저장소 클론

```bash
git clone https://github.com/FlyingTurtles07/A1-03-web_service_maker.git
cd A1-03-web_service_maker
```

### 2. 가상환경 생성

Windows:

```powershell
python -m venv .venv
```

### 3. 가상환경 활성화

```powershell
.venv\Scripts\activate
```

### 4. 패키지 설치

```powershell
pip install -r requirements.txt
```

### 5. 환경변수 설정

`.env` 파일에 Gemini API 키를 설정합니다.

### 6. 로컬 실행

Vercel CLI를 사용하는 경우:

```powershell
vercel dev
```

이후 터미널에 표시되는 로컬 주소로 접속합니다.

---

## 13. Vercel 배포

본 프로젝트는 GitHub 저장소와 Vercel을 연결하여 배포했습니다.

배포 과정:

```text
GitHub
  ↓
Vercel 프로젝트 연결
  ↓
Build / Deployment
  ↓
Production Deployment
  ↓
배포 URL 접속
```

### Vercel 주요 설정

- Root Directory: 프로젝트 루트
- Framework Preset: Other
- `api/` 폴더: Python Serverless Function
- Environment Variables: Gemini API 키 등록

배포 과정에서 Python Framework Preset으로 인해 `/` 경로에서 API JSON이 표시되는 문제가 발생했으며, Framework Preset을 `Other`로 변경한 후 정적 `index.html` 화면과 Python API가 정상적으로 분리되어 동작하도록 수정했습니다.

<span style="background-color:#fff3cd">📸 캡처 ⑪ — Vercel Production Deployment가 Ready 상태인 화면을 여기에 넣으세요. (해당하는 캡처를 screenshots 폴더에서 찾지 못해 비워두었습니다)</span>

<details>
<summary>📸 Vercel 배포 사이트 실제 작동 화면 (데스크톱) (클릭)</summary>
<br>

<img src="screenshots/13.%20Vercel%20%EB%B0%B0%ED%8F%AC%20%EC%84%B1%EA%B3%B5%20%ED%9B%84%20%EB%8D%B0%EC%8A%A4%ED%81%AC%ED%83%91%20%EC%9E%91%EB%8F%99%20%20%EA%B2%B0%EA%B3%BC%20%EC%BA%A1%EC%B3%90/%EB%B0%B0%ED%8F%AC%20%ED%9B%84%20%EC%9E%91%EB%8F%99%20%EC%BA%A1%EC%B3%90%201%20%EB%8D%B0%EC%8A%A4%ED%81%AC%ED%83%91%20%EB%A9%94%EC%9D%B8%20%ED%99%94%EB%A9%B4%20.png" width="700"><br>
<sub>배포 사이트 - 데스크톱 메인 화면</sub>
<br><br>
<img src="screenshots/13.%20Vercel%20%EB%B0%B0%ED%8F%AC%20%EC%84%B1%EA%B3%B5%20%ED%9B%84%20%EB%8D%B0%EC%8A%A4%ED%81%AC%ED%83%91%20%EC%9E%91%EB%8F%99%20%20%EA%B2%B0%EA%B3%BC%20%EC%BA%A1%EC%B3%90/%EB%B0%B0%ED%8F%AC%20%ED%9B%84%20%EC%9E%91%EB%8F%99%20%EC%BA%A1%EC%B3%90%202%20%EA%B1%B4%EA%B0%95%EC%A0%95%EB%B3%B4%EC%9E%85%EB%A0%A5%20%ED%99%94%EB%A9%B4.png" width="700"><br>
<sub>배포 사이트 - 데스크톱 건강정보 입력 화면</sub>
<br><br>
<img src="screenshots/13.%20Vercel%20%EB%B0%B0%ED%8F%AC%20%EC%84%B1%EA%B3%B5%20%ED%9B%84%20%EB%8D%B0%EC%8A%A4%ED%81%AC%ED%83%91%20%EC%9E%91%EB%8F%99%20%20%EA%B2%B0%EA%B3%BC%20%EC%BA%A1%EC%B3%90/%EB%B0%B0%ED%8F%AC%20%ED%9B%84%20%EC%9E%91%EB%8F%99%20%EC%BA%A1%EC%B3%90%203%20%EA%B1%B4%EA%B0%95%20%EC%9C%84%ED%97%98%EB%8F%84%20%EB%B6%84%EC%84%9D%20%EA%B2%B0%EA%B3%BC%20%ED%99%94%EB%A9%B4.png" width="700"><br>
<sub>배포 사이트 - 데스크톱 위험도 분석 결과 화면</sub>
<br><br>
</details>

---

## 14. 배포 사이트

🌐 **서비스 URL**

https://a1-03-web-service-maker-aiq3.vercel.app

💻 **GitHub Repository**

https://github.com/FlyingTurtles07/A1-03-web_service_maker

<details>
<summary>📸 캡처 보기 (클릭)</summary>
<br>

<img src="screenshots/AI%EA%B0%80%20%EC%A0%95%EB%B3%B4%EB%A5%BC%20%EB%B6%84%EC%84%9D%ED%95%98%EB%8A%94%20%EC%A4%91.png" width="700"><br>
<sub>브라우저 주소창에 배포 URL(a1-03-web-service-maker-aiq3.vercel.app)이 표시된 화면</sub>
<br><br>
</details>

---

## 15. 테스트 결과

### 기본 기능 테스트

| 테스트 항목 | 결과 |
|---|---|
| 메인 화면 접속 | ✅ |
| 서비스 소개 화면 | ✅ |
| 건강정보 입력 | ✅ |
| 위험도 계산 | ✅ |
| Gemini AI 안내 생성 | ✅ |
| 결과 화면 표시 | ✅ |
| 고위험군 연결 요청 시뮬레이션 | ✅ |
| API 오류 처리 | ✅ |
| 데스크톱 화면 | ✅ |
| 모바일 화면 | ⬜ 최종 캡처 후 확인 |
| Vercel 배포 | ✅ |

### 테스트 입력 예시

```text
나이: 65
수축기 혈압: 140
이완기 혈압: 90
공복혈당: 130
```

<details>
<summary>📸 캡처 보기 (클릭)</summary>
<br>

<img src="screenshots/%EA%B1%B4%EA%B0%95%20%EC%A0%95%EB%B3%B4%20%EC%9E%85%EB%A0%A5%20%EC%BA%A1%EC%B3%90.png" width="700"><br>
<sub>테스트 입력값 (나이 65 / SBP 140 / DBP 90 / 공복혈당 130)</sub>
<br><br>
<img src="screenshots/Gemini%20AI%20%EB%B6%84%EC%84%9D%20%EA%B2%B0%EA%B3%BC%EA%B0%80%20%EC%8B%A4%EC%A0%9C%20%ED%99%94%EB%A9%B4%EC%97%90%20%ED%91%9C%EC%8B%9C%EB%90%9C%20%EC%9E%A5%EB%A9%B4.png" width="700"><br>
<sub>위 입력값에 대한 분석 결과</sub>
<br><br>
</details>

---

## 16. AI 코딩 도구 활용

본 프로젝트는 AI 코딩 도구를 활용하여 다음과 같은 개발 과정을 진행했습니다.

- 서비스 구조 설계
- HTML 화면 구성
- CSS 스타일링 및 반응형 수정
- JavaScript 이벤트 및 API 호출 구현
- Python Serverless Function 구현
- 위험도 계산 로직 구현 및 수정
- Gemini API 연동
- 오류 원인 분석 및 수정
- Vercel 배포 과정에서 발생한 문제 해결
- README 및 문서 작성 보조

AI가 생성한 코드를 그대로 사용하는 것이 아니라 실제 실행 결과를 확인하고 오류를 수정하면서 프로젝트를 완성했습니다.

<span style="background-color:#fff3cd">📸 캡처 ⑮ — AI 코딩 도구와 주고받은 대화 중 대표적인 개발/디버깅 화면을 여기에 넣으세요. (해당하는 캡처를 screenshots 폴더에서 찾지 못해 비워두었습니다)</span>

<span style="background-color:#fff3cd">📸 캡처 ⑯ — Vercel 배포 오류를 해결한 과정이 보이는 화면을 여기에 넣으세요. (해당하는 캡처를 screenshots 폴더에서 찾지 못해 비워두었습니다)</span>

---

## 17. 개발 과정에서 해결한 주요 문제

### 문제 1. 이완기 혈압 반영

초기 위험도 계산에서는 수축기 혈압만 기준으로 사용하는 문제가 있었습니다.

이를 수정하여 수축기 혈압 또는 이완기 혈압이 기준을 넘는 경우를 위험도 계산에 반영했습니다.

### 문제 2. 프론트엔드와 백엔드 연결

JavaScript에서 사용자 입력을 JSON으로 만들어 Python Serverless Function에 POST 요청하도록 구성했습니다.

### 문제 3. Vercel 배포 후 `/`에서 API JSON 표시

초기 Vercel Framework Preset이 Python으로 설정되어 `/` 접속 시 웹페이지 대신 API 응답이 표시되는 문제가 있었습니다.

Root Directory를 확인한 후 Framework Preset을 `Other`로 변경하여 정적 웹페이지와 Python API가 정상적으로 동작하도록 수정했습니다.

### 문제 4. API 오류 처리

입력값 누락, 잘못된 데이터 형식, 서버/API 오류 등을 구분하여 사용자에게 안내하도록 구성했습니다.

<details>
<summary>📸 캡처 보기 (클릭)</summary>
<br>

<img src="screenshots/AI%20%EC%95%88%EB%82%B4%EB%AC%B8%EC%9D%84%20%EC%83%9D%EC%84%B1%ED%95%98%EB%8A%94%20%EA%B3%BC%EC%A0%95%EC%97%90%EC%84%9C%20%EC%98%A4%EB%A5%98%EA%B0%80%20%EB%B0%9C%EC%83%9D%ED%96%88%EC%8A%B5%EB%8B%88%EB%8B%A4.%20%EC%9E%A0%EC%8B%9C%20%ED%9B%84%20%EB%8B%A4%EC%8B%9C%20%EC%8B%9C%EB%8F%84%ED%95%B4%EC%A3%BC%EC%84%B8%EC%9A%94..png" width="700"><br>
<sub>개발 중 발생했던 Gemini API 오류 메시지 화면</sub>
<br><br>
</details>

---

## 18. 미션 요구사항 체크리스트

### 서비스 기획

- [x] 서비스 목적 및 문제 정의
- [x] 대상 사용자 정의
- [x] 핵심 기능 정의
- [x] AI 기능 정의
- [x] 서비스 흐름 설계

### 프론트엔드

- [x] HTML5
- [x] CSS3
- [x] JavaScript
- [x] 서비스 소개 화면
- [x] 건강정보 입력 화면
- [x] 분석 결과 화면
- [x] 네비게이션
- [x] 반응형 레이아웃

### AI / 백엔드

- [x] Python API
- [x] Vercel Serverless Function
- [x] Gemini API 연동
- [x] 위험도 점수 계산
- [x] AI 맞춤 안내 생성
- [x] 결과를 웹 화면에 표시
- [x] 오류 처리

### 보안

- [x] API 키 환경변수 관리
- [x] `.env` Git 제외
- [x] `.env.example` 제공
- [x] README에 실제 API 키 미기재

### 배포

- [x] GitHub 저장소
- [x] Vercel 배포
- [x] Production Deployment 성공
- [x] 배포 URL 접속 확인
- [x] 웹페이지 정상 표시
- [x] API 정상 연결

### 제출 자료

- [x] GitHub 저장소
- [x] 배포 URL
- [x] README
- [ ] 서비스 기획서 최종본
- [ ] 데스크톱 스크린샷
- [ ] 모바일 스크린샷
- [ ] AI 기능 동작 스크린샷
- [ ] AI 코딩 도구 활용 스크린샷

<details>
<summary>📸 최종 제출용 전체 결과 화면 - 모바일 (클릭)</summary>
<br>

<img src="screenshots/13.%20Vercel%20%EB%B0%B0%ED%8F%AC%20%EC%84%B1%EA%B3%B5%20%ED%9B%84%20%EB%AA%A8%EB%B0%94%EC%9D%BC%20%EC%9E%91%EB%8F%99%20%20%EA%B2%B0%EA%B3%BC%20%EC%BA%A1%EC%B3%90/%EB%B0%B0%ED%8F%AC%20%ED%9B%84%20%EC%9E%91%EB%8F%99%20%EC%BA%A1%EC%B3%90%201%20%EB%AA%A8%EB%B0%94%EC%9D%BC%20%EB%A9%94%EC%9D%B8%20%ED%99%94%EB%A9%B4.jpg" width="700"><br>
<sub>배포 사이트 - 모바일 메인 화면</sub>
<br><br>
<img src="screenshots/13.%20Vercel%20%EB%B0%B0%ED%8F%AC%20%EC%84%B1%EA%B3%B5%20%ED%9B%84%20%EB%AA%A8%EB%B0%94%EC%9D%BC%20%EC%9E%91%EB%8F%99%20%20%EA%B2%B0%EA%B3%BC%20%EC%BA%A1%EC%B3%90/%EB%B0%B0%ED%8F%AC%20%ED%9B%84%20%EC%9E%91%EB%8F%99%20%EC%BA%A1%EC%B3%90%202%20%EB%AA%A8%EB%B0%94%EC%9D%BC%20%EA%B1%B4%EA%B0%95%EC%A0%95%EB%B3%B4%EC%9E%85%EB%A0%A5%20%ED%99%94%EB%A9%B4.jpg" width="700"><br>
<sub>배포 사이트 - 모바일 건강정보 입력 화면</sub>
<br><br>
<img src="screenshots/13.%20Vercel%20%EB%B0%B0%ED%8F%AC%20%EC%84%B1%EA%B3%B5%20%ED%9B%84%20%EB%AA%A8%EB%B0%94%EC%9D%BC%20%EC%9E%91%EB%8F%99%20%20%EA%B2%B0%EA%B3%BC%20%EC%BA%A1%EC%B3%90/%EB%B0%B0%ED%8F%AC%20%ED%9B%84%20%EC%9E%91%EB%8F%99%20%EC%BA%A1%EC%B3%90%202_1%20%EB%AA%A8%EB%B0%94%EC%9D%BC%20%EA%B1%B4%EA%B0%95%EC%A0%95%EB%B3%B4%EC%9E%85%EB%A0%A5%20%ED%99%94%EB%A9%B4.jpg" width="700"><br>
<sub>배포 사이트 - 모바일 건강정보 입력 화면 (스크롤)</sub>
<br><br>
<img src="screenshots/13.%20Vercel%20%EB%B0%B0%ED%8F%AC%20%EC%84%B1%EA%B3%B5%20%ED%9B%84%20%EB%AA%A8%EB%B0%94%EC%9D%BC%20%EC%9E%91%EB%8F%99%20%20%EA%B2%B0%EA%B3%BC%20%EC%BA%A1%EC%B3%90/%EB%B0%B0%ED%8F%AC%20%ED%9B%84%20%EC%9E%91%EB%8F%99%20%EC%BA%A1%EC%B3%90%203%20%EB%AA%A8%EB%B0%94%EC%9D%BC%20%EA%B1%B4%EA%B0%95%20%EC%9C%84%ED%97%98%EB%8F%84%20%EB%B6%84%EC%84%9D%20%EA%B2%B0%EA%B3%BC%20%ED%99%94%EB%A9%B4.jpg" width="700"><br>
<sub>배포 사이트 - 모바일 위험도 분석 결과 화면</sub>
<br><br>
</details>

---

## 19. 향후 확장 계획

현재 프로젝트는 미션 범위에 맞춘 MVP이며, 향후 다음 기능으로 확장할 수 있습니다.

1. 담당의 실제 배정 시스템
2. 처방전 발급 및 약국 연계
3. 의약품 배송 연계
4. 정기적인 건강정보 기록
5. 건강 상태 변화 그래프
6. 지역별 의료기관 정보
7. 실제 의료진 상담 시스템
8. 응급상황 연계
9. 경증 환자군까지 서비스 대상 확대
10. 지역 단위 원격 건강관리 플랫폼으로 확장

---

## 20. 주의사항

본 프로젝트는 **교육 및 미션 수행을 위한 프로토타입**입니다.

AI가 제공하는 내용은 건강관리 참고용이며 의료진의 진단이나 처방을 대신하지 않습니다.

실제 건강 문제가 있는 경우 의료기관 또는 의료 전문가의 상담을 받아야 합니다.

---

## 21. 프로젝트 정보

| 항목 | 내용 |
|---|---|
| 프로젝트 | A1-03 Web Service Maker |
| 서비스 | 만성질환자 맞춤 원격 건강관리 |
| Frontend | HTML / CSS / JavaScript |
| Backend | Python / Vercel Serverless Function |
| AI | Google Gemini API |
| Deployment | Vercel |
| Repository | https://github.com/FlyingTurtles07/A1-03-web_service_maker |
| Live Demo | https://a1-03-web-service-maker-aiq3.vercel.app |

---

## 22. 최종 제출 전 체크

- [ ] README의 모든 `📸 캡처` 위치에 실제 이미지 삽입
- [ ] 데스크톱 캡처 삽입
- [ ] 모바일 캡처 삽입
- [ ] AI 결과 캡처 삽입
- [ ] Vercel 배포 캡처 삽입
- [ ] AI 코딩 도구 캡처 삽입
- [ ] API 키가 캡처에 노출되지 않았는지 확인
- [ ] `.env`가 GitHub에 올라가지 않았는지 확인
- [ ] GitHub 최신 코드와 로컬 코드가 동일한지 확인
- [ ] Vercel 최신 배포가 `Ready`인지 확인
- [ ] 배포 URL 최종 접속 확인
- [ ] README 오탈자 확인
- [ ] 최종 Git commit / push

---

## 참고

프로젝트의 서비스 기획과 개발 과정에서 작성한 문서 및 구현 코드를 기준으로 작성되었습니다.
