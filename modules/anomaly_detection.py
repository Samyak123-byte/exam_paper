def detect_anomaly(
    student_answer,
    expected_answer
):

    text = (
        student_answer or ""
    ).strip()


    if not text:

        return {

            "flag": True,

            "reason":
                "Empty answer"
        }


    words = text.split()


    if len(words) < 3:

        return {

            "flag": True,

            "reason":
                "Very short answer"
        }


    unique_words = set(
        word.lower()
        for word in words
    )


    unique_ratio = (
        len(unique_words) /
        len(words)
    )


    if unique_ratio < 0.25:

        return {

            "flag": True,

            "reason":
                "Highly repetitive answer"
        }


    return {

        "flag": False,

        "reason":
            "No basic anomaly detected"
    }