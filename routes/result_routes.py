from flask import (
    Blueprint,
    jsonify
)

from database.db import (
    get_student_results
)


result_bp = Blueprint(
    "result",
    __name__
)


@result_bp.route(
    "/<student_id>",
    methods=["GET"]
)
def student_result(student_id):

    results = get_student_results(
        student_id
    )

    total_marks = 0
    maximum_marks = 0

    for row in results:

        total_marks += float(
            row["marks"] or 0
        )

        maximum_marks += float(
            row["max_marks"] or 0
        )

    percentage = 0

    if maximum_marks > 0:

        percentage = (
            total_marks /
            maximum_marks
        ) * 100

    return jsonify({

        "success": True,

        "student_id":
            student_id,

        "total_marks":
            round(total_marks, 2),

        "maximum_marks":
            round(maximum_marks, 2),

        "percentage":
            round(percentage, 2),

        "results":
            results
    })