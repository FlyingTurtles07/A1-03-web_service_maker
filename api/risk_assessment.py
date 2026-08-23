"""
api/risk_assessment.py

V2 위험도 계산 전용 모듈
AI 호출 없음
웹 요청 처리 없음
"""


def assess_risk(age, sbp, dbp, sugar):
    """
    V2 위험도 계산

    age   : 나이
    sbp   : 수축기 혈압
    dbp   : 이완기 혈압
    sugar : 공복혈당

    반환:
        {
            "age_score": ...,
            "bp_score": ...,
            "glucose_score": ...,
            "total_score": ...,
            "risk_level": ...
        }
    """

    # 숫자 변환
    age = float(age)
    sbp = float(sbp)
    dbp = float(dbp)
    sugar = float(sugar)

    # ----------------------------------------
    # 1. 나이 점수
    # ----------------------------------------

    if age < 40:
        age_score = 0
    elif age < 60:
        age_score = 1
    else:
        age_score = 2

    # ----------------------------------------
    # 2. 혈압 점수
    #
    # SBP >= 140
    # 또는 DBP >= 90
    # → 6점
    # ----------------------------------------

    if sbp >= 140 or dbp >= 90:
        bp_score = 6
    elif sbp >= 120:
        bp_score = 3
    else:
        bp_score = 0

    # ----------------------------------------
    # 3. 공복혈당 점수
    # ----------------------------------------

    if sugar >= 126:
        glucose_score = 6
    elif sugar >= 100:
        glucose_score = 3
    else:
        glucose_score = 0

    # ----------------------------------------
    # 4. 총점
    # ----------------------------------------

    total_score = (
        age_score
        + bp_score
        + glucose_score
    )

    # ----------------------------------------
    # 5. 위험도 분류
    # ----------------------------------------

    if total_score >= 8:
        risk_level = "고위험군"
    elif total_score >= 4:
        risk_level = "주의군"
    else:
        risk_level = "안정군"

    return {
        "age_score": age_score,
        "bp_score": bp_score,
        "glucose_score": glucose_score,
        "total_score": total_score,
        "risk_level": risk_level,
    }