import re

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)


STOPWORDS = {
    "the",
    "is",
    "a",
    "an",
    "of",
    "to",
    "and",
    "in",
    "on",
    "for",
    "with",
    "by",
    "this",
    "that",
    "are",
    "was",
    "were",
    "as",
    "it",
    "from",
    "at",
    "be"
}


def tokenize(text):

    text = str(text or "")

    words = re.findall(
        r"[a-zA-Z0-9]+",
        text.lower()
    )

    return [
        word
        for word in words
        if word not in STOPWORDS
    ]


def keyword_similarity(
    expected,
    student
):

    expected_words = set(
        tokenize(expected)
    )

    student_words = set(
        tokenize(student)
    )

    if not expected_words:
        return 0.0

    common = (
        expected_words &
        student_words
    )

    return (
        len(common) /
        len(expected_words)
    )


def semantic_similarity(
    expected,
    student
):

    expected = str(expected or "").strip()
    student = str(student or "").strip()

    if not expected:
        return 0.0

    if not student:
        return 0.0

    try:

        vectorizer = TfidfVectorizer()

        matrix = vectorizer.fit_transform(
            [
                expected,
                student
            ]
        )

        score = cosine_similarity(
            matrix[0:1],
            matrix[1:2]
        )[0][0]

        return float(score)

    except Exception:

        return 0.0


def concept_coverage(
    expected,
    student
):

    expected_words = set(
        tokenize(expected)
    )

    student_words = set(
        tokenize(student)
    )

    if not expected_words:
        return 0.0

    matched = (
        expected_words &
        student_words
    )

    return (
        len(matched) /
        len(expected_words)
    )