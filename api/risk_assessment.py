"""
api/risk_assessment.py
- 위험도 계산만 담당하는 모듈 (AI 호출 없음, 웹 핸들러 없음)
- index.py에서 assess_risk() 함수를 import해서 사용한다.
"""


def assess_risk(age, sbp, dbp, sugar):
    """
    규칙 기반 위험도 계산
    age: 나이 / sbp: 수축기혈압 / dbp: 이완기혈압 / sugar: 공복혈당
    반환: "고위험군" / "주의군" / "안정군"
    """
    # 문자열로 들어올 수 있으니 숫자로 변환
    age = float(age)
    sbp = float(sbp)
    dbp = float(dbp)
    sugar = float(sugar)

    # 1) 나이 점수
    age_score = 0 if age < 40 else (1 if age <= 59 else 2)

    # 2) 혈압 점수
    if sbp >= 140 or dbp >= 90:
        bp_score = 6
    elif sbp >= 120:
        bp_score = 3
    else:
        bp_score = 0

    # 3) 혈당 점수
    glucose_score = 0 if sugar < 100 else (3 if sugar <= 125 else 6)

    # 4) 총점으로 분류
    total = age_score + bp_score + glucose_score

    if total >= 8:
        return "고위험군"
    elif total >= 4:
        return "주의군"
    else:
        return "안정군"