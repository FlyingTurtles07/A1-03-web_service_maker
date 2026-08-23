# `api/risk_assessment.py`

"""
api/risk_assessment.py

역할
1. 입력값 검증
2. 위험도 점수 계산
3. 위험도 분류

AI 호출이나 HTTP 처리는 하지 않습니다.
"""

# ----------------------------------------
# 입력값 검증
# ----------------------------------------

def validate_input(age, sbp, dbp, sugar):
    """
    건강정보 입력값을 검증합니다.

    검증 항목
    - 필수값 누락
    - 숫자가 아닌 값
    - 허용 범위
    - 수축기/이완기 혈압 관계
    """

    # 1. 필수값 검사
    values = {
        "나이": age,
        "수축기 혈압": sbp,
        "이완기 혈압": dbp,
        "공복혈당": sugar,
    }

    for name, value in values.items():
        if value is None or str(value).strip() == "":
            return False, f"{name}을(를) 입력해주세요."

    # 2. 숫자 변환
    try:
        age = float(age)
        sbp = float(sbp)
        dbp = float(dbp)
        sugar = float(sugar)
    except (TypeError, ValueError):
        return False, "나이, 혈압, 혈당은 숫자로 입력해주세요."

    # 3. 숫자가 NaN 또는 무한대인지 검사
    numbers = {
        "나이": age,
        "수축기 혈압": sbp,
        "이완기 혈압": dbp,
        "공복혈당": sugar,
    }

    for name, value in numbers.items():
        if not (value == value):
            return False, f"{name}에 올바른 숫자를 입력해주세요."

    # 4. 나이 범위
    if age < 1 or age > 120:
        return False, "나이는 1세 이상 120세 이하로 입력해주세요."

    # 5. 수축기 혈압 범위
    if sbp < 50 or sbp > 250:
        return False, "수축기 혈압(SBP)은 50~250mmHg 범위로 입력해주세요."

    # 6. 이완기 혈압 범위
    if dbp < 30 or dbp > 150:
        return False, "이완기 혈압(DBP)은 30~150mmHg 범위로 입력해주세요."

    # 7. 수축기/이완기 혈압 관계
    if dbp >= sbp:
        return False, (
            "이완기 혈압(DBP)은 "
            "수축기 혈압(SBP)보다 낮게 입력해주세요."
        )

    # 8. 공복혈당 범위
    if sugar < 30 or sugar > 500:
        return False, "공복혈당은 30~500mg/dL 범위로 입력해주세요."

    return True, ""


# ----------------------------------------
# 위험도 점수 계산
# ----------------------------------------

def calculate_risk_score(age, sbp, dbp, sugar):
    """
    검증된 건강정보를 기준으로 위험도 점수를 계산합니다.
    """

    age = float(age)
    sbp = float(sbp)
    dbp = float(dbp)
    sugar = float(sugar)

    # 나이 점수
    if age < 40:
        age_score = 0
    elif age <= 59:
        age_score = 1
    else:
        age_score = 2

    # 혈압 점수
    if sbp >= 140 or dbp >= 90:
        bp_score = 6
    elif sbp >= 120:
        bp_score = 3
    else:
        bp_score = 0

    # 혈당 점수
    if sugar < 100:
        glucose_score = 0
    elif sugar <= 125:
        glucose_score = 3
    else:
        glucose_score = 6

    # 총점
    total_score = (
        age_score
        + bp_score
        + glucose_score
    )

    # 위험도 분류
    if total_score >= 8:
        risk_level = "고위험군"
    elif total_score >= 4:
        risk_level = "주의군"
    else:
        risk_level = "안정군"

    return {
        "total_score": total_score,
        "age_score": age_score,
        "bp_score": bp_score,
        "glucose_score": glucose_score,
        "risk_level": risk_level,
    }


# ----------------------------------------
# 기존 코드 호환용 함수
# ----------------------------------------

def assess_risk(age, sbp, dbp, sugar):
    """
    기존 코드와의 호환성을 위한 위험도 계산 함수.
    """

    valid, error_message = validate_input(
        age,
        sbp,
        dbp,
        sugar,
    )

    if not valid:
        raise ValueError(error_message)

    result = calculate_risk_score(
        age,
        sbp,
        dbp,
        sugar,
    )

    return result["risk_level"]

