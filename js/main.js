// ========================================
// 페이지 요소 가져오기
// ========================================

const healthForm = document.getElementById("health-form");
const formError = document.getElementById("form-error");

const resultEmpty = document.getElementById("result-empty");
const resultContent = document.getElementById("result-content");

const totalScoreElement = document.getElementById("total-score");
const riskBadge = document.getElementById("risk-badge");
const resultTitle = document.getElementById("result-title");
const resultMessage = document.getElementById("result-message");

const ageScoreElement = document.getElementById("age-score");
const bloodPressureScoreElement =
    document.getElementById("blood-pressure-score");
const glucoseScoreElement =
    document.getElementById("glucose-score");


// ========================================
// V2 위험도 계산
// ========================================

function calculateRiskScore(age, sbp, dbp, glucose) {

    // ----------------------------
    // 나이 점수
    // ----------------------------

    let ageScore;

    if (age < 40) {
        ageScore = 0;
    } else if (age < 60) {
        ageScore = 1;
    } else {
        ageScore = 2;
    }


    // ----------------------------
    // 혈압 점수
    //
    // SBP >= 140
    // 또는 DBP >= 90
    // → 6점
    // ----------------------------

    let bloodPressureScore;

    if (sbp >= 140 || dbp >= 90) {
        bloodPressureScore = 6;
    } else if (sbp >= 120) {
        bloodPressureScore = 3;
    } else {
        bloodPressureScore = 0;
    }


    // ----------------------------
    // 공복혈당 점수
    // ----------------------------

    let glucoseScore;

    if (glucose >= 126) {
        glucoseScore = 6;
    } else if (glucose >= 100) {
        glucoseScore = 3;
    } else {
        glucoseScore = 0;
    }


    // ----------------------------
    // 총점
    // ----------------------------

    const totalScore =
        ageScore +
        bloodPressureScore +
        glucoseScore;


    // ----------------------------
    // 위험도 분류
    // ----------------------------

    let riskLevel;

    if (totalScore <= 3) {
        riskLevel = "안정군";
    } else if (totalScore <= 7) {
        riskLevel = "주의군";
    } else {
        riskLevel = "고위험군";
    }


    return {
        ageScore,
        bloodPressureScore,
        glucoseScore,
        totalScore,
        riskLevel
    };
}


// ========================================
// 입력값 검증
// ========================================

function validateInputs(age, sbp, dbp, glucose) {

    if (!age || !sbp || !dbp || !glucose) {
        return "모든 항목을 입력해주세요.";
    }

    if (age < 1 || age > 120) {
        return "나이는 1세~120세 사이로 입력해주세요.";
    }

    if (sbp < 50 || sbp > 250) {
        return "수축기 혈압(SBP)을 확인해주세요.";
    }

    if (dbp < 30 || dbp > 150) {
        return "이완기 혈압(DBP)을 확인해주세요.";
    }

    if (dbp >= sbp) {
        return "이완기 혈압(DBP)은 수축기 혈압(SBP)보다 낮게 입력해주세요.";
    }

    if (glucose < 30 || glucose > 500) {
        return "공복혈당을 확인해주세요.";
    }

    return "";
}


// ========================================
// 결과 화면 표시
// ========================================

function showResult(result) {

    resultEmpty.hidden = true;
    resultContent.hidden = false;

    totalScoreElement.textContent = result.totalScore;

    riskBadge.textContent = result.riskLevel;

    ageScoreElement.textContent =
        result.ageScore + "점";

    bloodPressureScoreElement.textContent =
        result.bloodPressureScore + "점";

    glucoseScoreElement.textContent =
        result.glucoseScore + "점";


    // ----------------------------
    // 위험도별 안내
    // ----------------------------

    if (result.totalScore <= 3) {

        resultTitle.textContent =
            "현재 위험도는 안정군입니다.";

        resultMessage.textContent =
            "현재 입력된 건강정보를 기준으로 안정군으로 분류되었습니다. 현재의 건강관리 습관을 유지하고 정기적으로 건강상태를 확인해주세요.";

    } else if (result.totalScore <= 7) {

        resultTitle.textContent =
            "건강관리에 주의가 필요합니다.";

        resultMessage.textContent =
            "현재 입력된 건강정보를 기준으로 주의군으로 분류되었습니다. 혈압과 혈당을 꾸준히 확인하고 생활습관 관리에 신경 써주세요.";

    } else {

        resultTitle.textContent =
            "의료기관 상담을 고려해주세요.";

        resultMessage.textContent =
            "현재 입력된 건강정보를 기준으로 고위험군으로 분류되었습니다. 건강상태에 대해 의료기관 또는 의료진과 상담하는 것을 권장합니다.";
    }


    // 결과 위치로 이동

    document.getElementById("result").scrollIntoView({
        behavior: "smooth"
    });
}


// ========================================
// 폼 제출 이벤트
// ========================================

if (healthForm) {

    healthForm.addEventListener("submit", function(event) {

        event.preventDefault();

        console.log("위험도 분석 버튼 클릭");


        // 오류 초기화

        formError.hidden = true;
        formError.textContent = "";


        // 입력값 가져오기

        const age =
            Number(document.getElementById("age").value);

        const sbp =
            Number(document.getElementById("sbp").value);

        const dbp =
            Number(document.getElementById("dbp").value);

        const glucose =
            Number(document.getElementById("glucose").value);


        console.log("입력값:", {
            age,
            sbp,
            dbp,
            glucose
        });


        // 입력값 검증

        const errorMessage =
            validateInputs(
                age,
                sbp,
                dbp,
                glucose
            );


        if (errorMessage) {

            formError.textContent =
                errorMessage;

            formError.hidden = false;

            return;
        }


        // V2 계산

        const result =
            calculateRiskScore(
                age,
                sbp,
                dbp,
                glucose
            );


        console.log("계산 결과:", result);


        // 결과 표시

        showResult(result);
    });

} else {

    console.error(
        "health-form을 찾을 수 없습니다. index.html의 form id를 확인하세요."
    );
}