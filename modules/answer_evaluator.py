from modules.similarity import (
    semantic_similarity,
    keyword_similarity,
    concept_coverage
)


def evaluate_answer(
    question,
    expected_answer,
    student_answer,
    rubric=""
):
    """
    Evaluate a student's answer using
    semantic similarity, keyword matching,
    and concept coverage.
    """

    # Make sure values are strings
    question = str(question or "")
    expected_answer = str(expected_answer or "")
    student_answer = str(student_answer or "")
    rubric = str(rubric or "")

    # Calculate individual scores
    semantic = semantic_similarity(
        expected_answer,
        student_answer
    )

    keyword = keyword_similarity(
        expected_answer,
        student_answer
    )

    concept = concept_coverage(
        expected_answer,
        student_answer
    )

    # Weighted overall score
    overall = (
        (0.50 * semantic) +
        (0.25 * keyword) +
        (0.25 * concept)
    )

    # Keep score between 0 and 1
    overall = max(
        0.0,
        min(1.0, overall)
    )

    return {
        "question": question,

        "semantic_score": round(
            semantic * 100,
            2
        ),

        "keyword_score": round(
            keyword * 100,
            2
        ),

        "concept_score": round(
            concept * 100,
            2
        ),

        "overall_score": round(
            overall * 100,
            2
        ),

        "rubric": rubric
    }