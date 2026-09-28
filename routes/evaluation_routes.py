from flask import (
    Blueprint,
    request,
    jsonify
)

from modules.answer_evaluator import (
    evaluate_answer
)

from modules.marks_engine import (
    calculate_marks
)

from modules.feedback import (
    generate_feedback
)

from modules.anomaly_detection import (
    detect_anomaly
)

from database.db import (
    save_evaluation
)


evaluation_bp = Blueprint(
    "evaluation",
    __name__
)


@evaluation_bp.route(
    "/evaluate",
    methods=["POST"]
)
def evaluate():

    try:

        # ---------------------------------
        # GET JSON DATA
        # ---------------------------------

        data = request.get_json(
            silent=True
        ) or {}


        # ---------------------------------
        # REQUIRED FIELDS
        # ---------------------------------

        required_fields = [
            "question",
            "expected_answer",
            "student_answer",
            "max_marks"
        ]


        missing = [
            field
            for field in required_fields
            if field not in data
            or data[field] is None
            or str(data[field]).strip() == ""
        ]


        if missing:

            return jsonify({

                "success": False,

                "error":
                    "Missing fields: "
                    + ", ".join(missing)

            }), 400


        # ---------------------------------
        # INPUT DATA
        # ---------------------------------

        question = str(
            data.get(
                "question",
                ""
            )
        ).strip()


        expected_answer = str(
            data.get(
                "expected_answer",
                ""
            )
        ).strip()


        student_answer = str(
            data.get(
                "student_answer",
                ""
            )
        ).strip()


        rubric = str(
            data.get(
                "rubric",
                ""
            )
        ).strip()


        student_id = str(
            data.get(
                "student_id",
                "demo-student"
            )
        ).strip()


        exam_id = data.get(
            "exam_id"
        )


        question_id = data.get(
            "question_id"
        )


        # ---------------------------------
        # MAX MARKS
        # ---------------------------------

        try:

            max_marks = float(
                data.get(
                    "max_marks"
                )
            )

        except (
            TypeError,
            ValueError
        ):

            return jsonify({

                "success": False,

                "error":
                    "max_marks must be a valid number."

            }), 400


        if max_marks <= 0:

            return jsonify({

                "success": False,

                "error":
                    "max_marks must be greater than 0."

            }), 400


        # ---------------------------------
        # BASIC VALIDATION
        # ---------------------------------

        if len(student_answer) < 2:

            return jsonify({

                "success": False,

                "error":
                    "Student answer is too short."

            }), 400


        if len(expected_answer) < 2:

            return jsonify({

                "success": False,

                "error":
                    "Expected answer is too short."

            }), 400


        # ---------------------------------
        # AI ANSWER EVALUATION
        # ---------------------------------

        evaluation = evaluate_answer(

            question=question,

            expected_answer=expected_answer,

            student_answer=student_answer,

            rubric=rubric
        )


        # ---------------------------------
        # CALCULATE MARKS
        # ---------------------------------

        marks = calculate_marks(

            evaluation,

            max_marks
        )


        # ---------------------------------
        # GENERATE FEEDBACK
        # ---------------------------------

        feedback = generate_feedback(

            evaluation,

            marks,

            max_marks
        )


        # ---------------------------------
        # ANOMALY DETECTION
        # ---------------------------------

        try:

            anomaly = detect_anomaly(

                student_answer,

                expected_answer
            )

        except Exception as anomaly_error:

            anomaly = {

                "detected": False,

                "message":
                    "Anomaly detection unavailable",

                "error":
                    str(anomaly_error)
            }


        # ---------------------------------
        # SAVE EVALUATION
        # ---------------------------------

        try:

            evaluation_id = save_evaluation(

                student_id=student_id,

                exam_id=exam_id,

                question_id=question_id,

                student_answer=student_answer,

                evaluation=evaluation,

                marks=marks,

                feedback=feedback,

                max_marks=max_marks

            )

        except Exception as db_error:

            # Evaluation should still work
            # even if database saving fails.

            evaluation_id = None

            print(
                "Database warning:",
                db_error
            )


        # ---------------------------------
        # FINAL RESPONSE
        # ---------------------------------

        return jsonify({

            "success": True,

            "message":
                "Answer evaluated successfully.",

            "evaluation_id":
                evaluation_id,

            "scores": {

                "semantic_score":
                    evaluation.get(
                        "semantic_score",
                        0
                    ),

                "keyword_score":
                    evaluation.get(
                        "keyword_score",
                        0
                    ),

                "concept_score":
                    evaluation.get(
                        "concept_score",
                        0
                    ),

                "overall_score":
                    evaluation.get(
                        "overall_score",
                        0
                    )

            },

            "marks":
                marks,

            "max_marks":
                max_marks,

            "feedback":
                feedback,

            "anomaly":
                anomaly

        }), 200


    except Exception as e:

        print(
            "\n========== EVALUATION ERROR =========="
        )

        print(
            type(e).__name__,
            ":",
            str(e)
        )

        print(
            "======================================\n"
        )


        return jsonify({

            "success": False,

            "error":
                "Evaluation failed: "
                + str(e)

        }), 500