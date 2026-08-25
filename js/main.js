// ========================================
// 건강정보 입력 및 API 처리
// ========================================

// ----------------------------------------
// DOM 요소
// ----------------------------------------

const healthForm =
    document.getElementById("health-form");

const formError =
    document.getElementById("form-error");

const resultEmpty =
    document.getElementById("result-empty");

const resultContent =
    document.getElementById("result-content");

const totalScore =
    document.getElementById("total-score");

const riskBadge =
    document.getElementById("risk-badge");

const resultTitle =
    document.getElementById("result-title");

const resultMessage =
    document.getElementById("result-message");

const ageScore =
    document.getElementById("age-score");

const bloodPressureScore =
    document.getElementById("blood-pressure-score");

const glucoseScore =
    document.getElementById("glucose-score");


// ----------------------------------------
// 담당의 연결 요청 요소
// ----------------------------------------

const doctorConnectBox =
    document.getElementById("doctor-connect-box");

const doctorConnectButton =
    document.getElementById("doctor-connect-button");

const doctorConnectMessage =
    document.getElementById("doctor-connect-message");


// ========================================
// 건강정보 제출
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
        // 입력값 가져오기
        // --------------------------------

        const ageInput =
            document.getElementById("age").value.trim();

        const sbpInput =
            document.getElementById("sbp").value.trim();

        const dbpInput =
            document.getElementById("dbp").value.trim();

        const glucoseInput =
            document.getElementById("glucose").value.trim();


        // --------------------------------
        // 필수 입력값 검증
        // --------------------------------

        if (
            !ageInput ||
            !sbpInput ||
            !dbpInput ||
            !glucoseInput
        ) {

            showError(
                "모든 건강정보를 입력해주세요."
            );

            return;
        }


        // --------------------------------
        // 숫자 형식 검증
        // --------------------------------

        const age = Number(ageInput);
        const sbp = Number(sbpInput);
        const dbp = Number(dbpInput);
        const glucose = Number(glucoseInput);

        if (
            !Number.isFinite(age) ||
            !Number.isFinite(sbp) ||
            !Number.isFinite(dbp) ||
            !Number.isFinite(glucose)
        ) {

            showError(
                "나이, 혈압, 혈당은 숫자로 입력해주세요."
            );

            return;
        }


        // --------------------------------
        // 나이 범위 검증
        // --------------------------------

        if (age < 1 || age > 120) {

            showError(
                "나이는 1세 이상 120세 이하로 입력해주세요."
            );

            return;
        }


        // --------------------------------
        // 수축기 혈압 범위 검증
        // --------------------------------

        if (sbp < 50 || sbp > 250) {

            showError(
                "수축기 혈압(SBP)은 50~250mmHg 범위로 입력해주세요."
            );

            return;
        }


        // --------------------------------
        // 이완기 혈압 범위 검증
        // --------------------------------

        if (dbp < 30 || dbp > 150) {

            showError(
                "이완기 혈압(DBP)은 30~150mmHg 범위로 입력해주세요."
            );

            return;
        }


        // --------------------------------
        // 혈압 관계 검증
        // --------------------------------

        if (dbp >= sbp) {

            showError(
                "이완기 혈압(DBP)은 수축기 혈압(SBP)보다 낮게 입력해주세요."
            );

            return;
        }


        // --------------------------------
        // 공복혈당 범위 검증
        // --------------------------------

        if (glucose < 30 || glucose > 500) {

            showError(
                "공복혈당은 30~500mg/dL 범위로 입력해주세요."
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


        // ========================================
        // API 호출
        // ========================================

        try {

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
                            age: age,
                            sbp: sbp,
                            dbp: dbp,
                            sugar: glucose
                        })
                    }
                );


            // --------------------------------
            // JSON 응답 처리
            // --------------------------------

            let data;

            try {

                data =
                    await response.json();

            } catch (jsonError) {

                throw new Error(
                    "서버에서 올바른 응답을 받지 못했습니다."
                );
            }


            // --------------------------------
            // HTTP 오류 처리
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


            // --------------------------------
            // 네트워크 오류
            // --------------------------------

            if (
                error instanceof TypeError
            ) {

                showError(
                    "서버와 연결할 수 없습니다. " +
                    "인터넷 연결을 확인하고 " +
                    "잠시 후 다시 시도해주세요."
                );

            } else {

                showError(
                    error.message ||
                    "건강정보 분석 중 오류가 발생했습니다."
                );
            }

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
// 결과 표시
// ========================================

function showResult(data) {

    // --------------------------------
    // 결과 영역 표시
    // --------------------------------

    resultEmpty.hidden = true;
    resultContent.hidden = false;


    // --------------------------------
    // 점수 표시
    // --------------------------------

    totalScore.textContent =
        data.total_score;

    ageScore.textContent =
        data.age_score + "점";

    bloodPressureScore.textContent =
        data.bp_score + "점";

    glucoseScore.textContent =
        data.glucose_score + "점";


    // --------------------------------
    // 위험도 표시
    // --------------------------------

    riskBadge.textContent =
        data.risk_level;


    // --------------------------------
    // 위험도별 제목
    // --------------------------------

    if (data.risk_level === "고위험군") {

        resultTitle.textContent =
            "주의가 필요한 고위험 상태입니다.";

    } else if (data.risk_level === "주의군") {

        resultTitle.textContent =
            "건강관리에 주의가 필요합니다.";

    } else {

        resultTitle.textContent =
            "현재 비교적 안정적인 상태입니다.";
    }


    // --------------------------------
    // AI 안내 메시지
    // --------------------------------

    if (data.ai_message) {

        resultMessage.textContent =
            data.ai_message;

    } else {

        resultMessage.textContent =
            "현재 건강상태에 맞는 관리 안내를 확인해주세요.";
    }


    // --------------------------------
    // 고위험군 담당의 연결 요청
    // --------------------------------

    showDoctorConnect(
        data.risk_level
    );


    // --------------------------------
    // 결과 화면으로 이동
    // --------------------------------

    resultContent.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}


// ========================================
// 담당의 연결 요청 표시
// ========================================

function showDoctorConnect(riskLevel) {

    // --------------------------------
    // 고위험군이 아니면 숨김
    // --------------------------------

    if (riskLevel !== "고위험군") {

        doctorConnectBox.hidden = true;

        doctorConnectMessage.hidden = true;

        return;
    }


    // --------------------------------
    // 고위험군이면 표시
    // --------------------------------

    doctorConnectBox.hidden = false;

    doctorConnectMessage.hidden = true;

    doctorConnectButton.disabled = false;

    doctorConnectButton.textContent =
        "담당의 연결 요청";
}


// ========================================
// 담당의 연결 요청 버튼
// ========================================

doctorConnectButton.addEventListener(
    "click",
    function () {

        // --------------------------------
        // 요청 중 표시
        // --------------------------------

        doctorConnectButton.disabled = true;

        doctorConnectButton.textContent =
            "연결 요청 중...";


        // --------------------------------
        // 연결 요청 시뮬레이션
        // --------------------------------

        setTimeout(
            function () {

                doctorConnectButton.textContent =
                    "연결 요청 완료";

                doctorConnectMessage.textContent =
                    "담당의 연결 요청이 접수되었습니다. 담당 의료진의 확인 후 안내드릴 예정입니다.";

                doctorConnectMessage.hidden =
                    false;

            },
            1000
        );
    }
);


// ========================================
// 오류 표시
// ========================================

function showError(message) {

    formError.textContent =
        message;

    formError.hidden =
        false;

    formError.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}