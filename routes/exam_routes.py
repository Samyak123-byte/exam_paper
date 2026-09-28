from flask import Blueprint, request, jsonify

from database.db import (
    create_exam,
    get_exam,
    add_question,
    get_questions
)


exam_bp = Blueprint(
    "exam",
    __name__
)


@exam_bp.route(
    "/create",
    methods=["POST"]
)
def create_exam_api():

    data = request.get_json(
        silent=True
    ) or {}

    subject = data.get("subject")
    title = data.get(
        "title",
        "AI OSM Examination"
    )

    total_marks = data.get(
        "total_marks",
        100
    )

    if not subject:

        return jsonify({
            "success": False,
            "error": "Subject is required"
        }), 400

    try:

        exam_id = create_exam(
            title=title,
            subject=subject,
            total_marks=total_marks
        )

        return jsonify({
            "success": True,
            "message": "Exam created successfully",
            "exam_id": exam_id
        }), 201

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@exam_bp.route(
    "/<int:exam_id>",
    methods=["GET"]
)
def get_exam_api(exam_id):

    exam = get_exam(exam_id)

    if not exam:

        return jsonify({
            "success": False,
            "error": "Exam not found"
        }), 404

    questions = get_questions(
        exam_id
    )

    exam["questions"] = questions

    return jsonify({
        "success": True,
        "exam": exam
    })


@exam_bp.route(
    "/<int:exam_id>/question",
    methods=["POST"]
)
def create_question(exam_id):

    data = request.get_json(
        silent=True
    ) or {}

    question_text = data.get(
        "question_text"
    )

    expected_answer = data.get(
        "expected_answer"
    )

    max_marks = data.get(
        "max_marks"
    )

    rubric = data.get(
        "rubric",
        ""
    )

    if not question_text:
        return jsonify({
            "error": "Question text required"
        }), 400

    if not expected_answer:
        return jsonify({
            "error": "Expected answer required"
        }), 400

    if max_marks is None:
        return jsonify({
            "error": "Maximum marks required"
        }), 400

    try:

        question_id = add_question(
            exam_id,
            question_text,
            expected_answer,
            max_marks,
            rubric
        )

        return jsonify({
            "success": True,
            "question_id": question_id
        }), 201

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500