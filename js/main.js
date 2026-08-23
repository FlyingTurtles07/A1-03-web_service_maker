# `js/main.js` — 입력 검증 및 API 오류 처리 부분

```javascript
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
        // 원본 입력값
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
        // 1. 필수 입력값 검증
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
        // 2. 숫자 형식 검증
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
        // 3. 나이 범위 검증
        // --------------------------------

        if (age < 1 || age > 120) {

            showError(
                "나이는 1세 이상 120세 이하로 입력해주세요."
            );

            return;
        }

        // --------------------------------
        // 4. 수축기 혈압 범위 검증
        // --------------------------------

        if (sbp < 50 || sbp > 250) {

            showError(
                "수축기 혈압(SBP)은 50~250mmHg 범위로 입력해주세요."
            );

            return;
        }

        // --------------------------------
        // 5. 이완기 혈압 범위 검증
        // --------------------------------

        if (dbp < 30 || dbp > 150) {

            showError(
                "이완기 혈압(DBP)은 30~150mmHg 범위로 입력해주세요."
            );

            return;
        }

        // --------------------------------
        // 6. 수축기/이완기 관계 검증
        // --------------------------------

        if (dbp >= sbp) {

            showError(
                "이완기 혈압(DBP)은 수축기 혈압(SBP)보다 낮게 입력해주세요."
            );

            return;
        }

        // --------------------------------
        // 7. 공복혈당 범위 검증
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

        // --------------------------------
        // API 호출
        // --------------------------------

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
            // JSON 응답 안전하게 처리
            // --------------------------------

            let data;

            try {

                data = await response.json();

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
            // 정상 결과
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
```
