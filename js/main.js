// ========================================
// 요소
// ========================================

const healthForm =
    document.getElementById("health-form");

const formError =
    document.getElementById("form-error");

const resultEmpty =
    document.getElementById("result-empty");

const resultContent =
    document.getElementById("result-content");

const totalScoreElement =
    document.getElementById("total-score");

const riskBadge =
    document.getElementById("risk-badge");

const resultTitle =
    document.getElementById("result-title");

const resultMessage =
    document.getElementById("result-message");

const ageScoreElement =
    document.getElementById("age-score");

const bloodPressureScoreElement =
    document.getElementById("blood-pressure-score");

const glucoseScoreElement =
    document.getElementById("glucose-score");


// ========================================
// 폼 제출
// ========================================

healthForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        // --------------------------------
        // 오류 초기화
        // --------------------------------

        formError.hidden = true;
        formError.textContent = "";


        // --------------------------------
        // 입력값
        // --------------------------------

        const age =
            Number(
                document.getElementById("age").value
            );

        const sbp =
            Number(
                document.getElementById("sbp").value
            );

        const dbp =
            Number(
                document.getElementById("dbp").value
            );

        const glucose =
            Number(
                document.getElementById("glucose").value
            );


        // --------------------------------
        // 프론트 검증
        // --------------------------------

        if (!age || !sbp || !dbp || !glucose) {

            showError(
                "모든 건강정보를 입력해주세요."
            );

            return;
        }


        if (age < 1 || age > 120) {

            showError(
                "나이는 1세 이상 120세 이하로 입력해주세요."
            );

            return;
        }


        if (sbp < 50 || sbp > 250) {

            showError(
                "수축기 혈압(SBP)을 확인해주세요."
            );

            return;
        }


        if (dbp < 30 || dbp > 150) {

            showError(
                "이완기 혈압(DBP)을 확인해주세요."
            );

            return;
        }


        if (dbp >= sbp) {

            showError(
                "이완기 혈압(DBP)은 수축기 혈압(SBP)보다 낮게 입력해주세요."
            );

            return;
        }


        if (glucose < 30 || glucose > 500) {

            showError(
                "공복혈당 수치를 확인해주세요."
            );

            return;
        }


        // --------------------------------
        // 로딩 상태
        // --------------------------------

        const submitButton =
            healthForm.querySelector(
                "button[type='submit']"
            );

        submitButton.disabled = true;

        submitButton.textContent =
            "AI가 분석하는 중...";


        try {

            // --------------------------------
            // Vercel API 호출
            // --------------------------------

            const response =
                await fetch(
                    "/api/index",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            age,
                            sbp,
                            dbp,
                            sugar: glucose
                        })
                    }
                );


            // --------------------------------
            // JSON 응답
            // --------------------------------

            const data =
                await response.json();


            // --------------------------------
            // 서버 오류
            // --------------------------------

            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "건강정보 분석에 실패했습니다."
                );
            }


            // --------------------------------
            // 결과 표시
            // --------------------------------

            showResult(data);


        } catch (error) {

            console.error(
                "API ERROR:",
                error
            );

            showError(
                error.message ||
                "서버와 연결하지 못했습니다. 잠시 후 다시 시도해주세요."
            );


        } finally {

            // --------------------------------
            // 버튼 복구
            // --------------------------------

            submitButton.disabled = false;

            submitButton.textContent =
                "위험도 분석하기";
        }
    }
);


// ========================================
// 오류 표시
// ========================================

function showError(message) {

    formError.textContent = message;

    formError.hidden = false;

    formError.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}


// ========================================
// 결과 표시
// ========================================

function showResult(data) {

    resultEmpty.hidden = true;

    resultContent.hidden = false;


    // --------------------------------
    // 점수
    // --------------------------------

    totalScoreElement.textContent =
        data.total_score;


    ageScoreElement.textContent =
        `${data.age_score}점`;


    bloodPressureScoreElement.textContent =
        `${data.bp_score}점`;


    glucoseScoreElement.textContent =
        `${data.glucose_score}점`;


    // --------------------------------
    // 위험도
    // --------------------------------

    riskBadge.textContent =
        data.risk_level;


    if (data.risk_level === "안정군") {

        resultTitle.textContent =
            "현재 위험도는 안정군입니다.";

    } else if (data.risk_level === "주의군") {

        resultTitle.textContent =
            "건강관리에 주의가 필요합니다.";

    } else {

        resultTitle.textContent =
            "의료기관 상담을 고려해주세요.";
    }


    // --------------------------------
    // Gemini AI 안내
    // --------------------------------

    resultMessage.textContent =
        data.ai_message ||
        "AI 맞춤 안내를 생성하지 못했습니다.";


    // --------------------------------
    // 결과 화면 이동
    // --------------------------------

    document
        .getElementById("result")
        .scrollIntoView({
            behavior: "smooth"
        });
}