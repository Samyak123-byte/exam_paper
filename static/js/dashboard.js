async function evaluateAnswer() {

    const question =
        document.getElementById("question").value.trim();

    const expected =
        document.getElementById("expected").value.trim();

    const student =
        document.getElementById("student").value.trim();

    const maxMarks =
        Number(
            document.getElementById("marks").value
        );

    const studentId =
        document.getElementById("studentId").value.trim();


    if (!question ||
        !expected ||
        !student) {

        showToast(
            "Please complete all answer fields.",
            "error"
        );

        return;
    }


    const button =
        document.querySelector(".evaluate-btn");


    button.disabled = true;

    button.innerHTML =
        "⟳ AI is evaluating...";


    const resultPanel =
        document.getElementById("resultPanel");


    resultPanel.innerHTML = `

        <div class="loading-state">

            <div class="loader"></div>

            <h3>
                AI is analysing the answer...
            </h3>

            <p>
                Checking semantic understanding,
                keywords and concepts.
            </p>

        </div>

    `;


    const payload = {

        question: question,

        expected_answer: expected,

        student_answer: student,

        max_marks: maxMarks,

        student_id: studentId
    };


    try {

        const response =
            await fetch(
                "/api/evaluation/evaluate",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(payload)
                }
            );


        const data =
            await response.json();


        if (!data.success) {

            throw new Error(
                data.error ||
                "Evaluation failed"
            );
        }


        renderResult(data);


    } catch (error) {

        resultPanel.innerHTML = `

            <div class="error-state">

                <div>
                    ⚠
                </div>

                <h3>
                    Evaluation Failed
                </h3>

                <p>
                    ${error.message}
                </p>

            </div>

        `;

    } finally {

        button.disabled = false;

        button.innerHTML =
            "✦ Evaluate with AI";
    }
}


function renderResult(data) {

    const result =
        document.getElementById(
            "resultPanel"
        );


    const scores =
        data.scores;


    const marks =
        data.marks;


    const maxMarks =
        document.getElementById(
            "marks"
        ).value;


    result.innerHTML = `

        <div class="result-header">

            <div>

                <span class="eyebrow">
                    EVALUATION COMPLETE
                </span>

                <h2>
                    AI Evaluation Result
                </h2>

            </div>

            <div class="success-badge">
                ✓ Completed
            </div>

        </div>


        <div class="score-overview">

            <div class="big-score">

                <strong>
                    ${marks}
                </strong>

                <span>
                    / ${maxMarks}
                </span>

                <small>
                    Awarded Marks
                </small>

            </div>


            <div class="overall-score">

                <span>
                    Overall AI Score
                </span>

                <strong>
                    ${scores.overall_score}%
                </strong>

                <div class="progress large">
                    <div
                        style="
                        width:${scores.overall_score}%
                        "
                    ></div>
                </div>

            </div>

        </div>


        <div class="score-grid">

            ${scoreCard(
                "Semantic Understanding",
                scores.semantic_score,
                "✦"
            )}

            ${scoreCard(
                "Keyword Coverage",
                scores.keyword_score,
                "⌕"
            )}

            ${scoreCard(
                "Concept Coverage",
                scores.concept_score,
                "◈"
            )}

        </div>


        <div class="feedback-box">

            <div class="feedback-icon">
                ✓
            </div>

            <div>

                <span>
                    AI FEEDBACK
                </span>

                <p>
                    ${formatFeedback(
                        data.feedback
                    )}
                </p>

            </div>

        </div>


        <div class="result-actions">

            <button
                class="approve-btn"
                onclick="showToast('Evaluation accepted','success')"
            >
                ✓ Accept Evaluation
            </button>

            <button
                class="review-btn"
                onclick="showToast('Sent for teacher review','info')"
            >
                ↻ Send for Review
            </button>

        </div>

    `;
}


function scoreCard(
    title,
    score,
    icon
) {

    return `

        <div class="score-card">

            <div class="score-card-top">

                <div class="score-mini-icon">
                    ${icon}
                </div>

                <span>
                    ${title}
                </span>

            </div>

            <strong>
                ${score}%
            </strong>

            <div class="progress">

                <div
                    style="width:${score}%"
                ></div>

            </div>

        </div>

    `;
}


function formatFeedback(
    feedback
) {

    if (!feedback) {
        return "No feedback available.";
    }

    return feedback
        .replace(/\n/g, "<br>");
}


function showToast(
    message,
    type = "info"
) {

    const toast =
        document.createElement("div");

    toast.className =
        `toast ${type}`;

    toast.innerHTML =
        message;


    document.body.appendChild(
        toast
    );


    setTimeout(() => {

        toast.classList.add(
            "show"
        );

    }, 10);


    setTimeout(() => {

        toast.classList.remove(
            "show"
        );

        setTimeout(() => {

            toast.remove();

        }, 300);

    }, 3000);
}