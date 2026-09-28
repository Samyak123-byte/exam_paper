def calculate_marks(
    evaluation,
    max_marks
):
    """
    Convert AI evaluation score
    into marks according to the
    maximum marks of the question.
    """

    try:
        max_marks = float(max_marks)
    except (TypeError, ValueError):
        raise ValueError(
            "max_marks must be a number"
        )

    if max_marks < 0:
        raise ValueError(
            "max_marks cannot be negative"
        )

    # Get overall AI score
    try:
        score = float(
            evaluation.get(
                "overall_score",
                0
            )
        )
    except (TypeError, ValueError):
        score = 0.0

    # Keep score between 0 and 100
    score = max(
        0.0,
        min(
            100.0,
            score
        )
    )

    # Convert percentage to marks
    marks = (
        score / 100.0
    ) * max_marks

    # Prevent marks from exceeding maximum
    marks = max(
        0.0,
        min(
            max_marks,
            marks
        )
    )

    return round(
        marks,
        2
    )