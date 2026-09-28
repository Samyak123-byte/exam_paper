def generate_feedback(
    evaluation,
    marks,
    max_marks
):

    score = float(
        evaluation[
            "overall_score"
        ]
    )

    semantic = evaluation[
        "semantic_score"
    ]

    keyword = evaluation[
        "keyword_score"
    ]

    concept = evaluation[
        "concept_score"
    ]


    if score >= 85:

        quality = "Excellent"

        advice = (
            "The answer covers the "
            "expected concepts clearly "
            "and demonstrates strong "
            "understanding."
        )

    elif score >= 70:

        quality = "Good"

        advice = (
            "The answer is mostly correct. "
            "Add more supporting concepts "
            "or explanation for a stronger "
            "response."
        )

    elif score >= 50:

        quality = "Needs Improvement"

        advice = (
            "Some important concepts are "
            "missing. Review the expected "
            "concepts and provide a more "
            "complete explanation."
        )

    else:

        quality = "Weak"

        advice = (
            "The response does not cover "
            "enough of the expected concepts. "
            "Review the topic and rewrite "
            "the answer with key points."
        )


    feedback = (

        f"{quality}.\n\n"

        f"Marks: {marks}/{max_marks}\n\n"

        f"Semantic Understanding: "
        f"{semantic}%\n"

        f"Keyword Coverage: "
        f"{keyword}%\n"

        f"Concept Coverage: "
        f"{concept}%\n\n"

        f"Feedback: {advice}"
    )


    return feedback