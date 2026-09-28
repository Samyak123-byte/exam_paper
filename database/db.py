import sqlite3

from pathlib import Path

from config import Config


def get_connection():

    database_path = Path(
        Config.DATABASE
    )

    database_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        Config.DATABASE
    )

    connection.row_factory = (
        sqlite3.Row
    )

    return connection


def init_db():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.executescript("""

    CREATE TABLE IF NOT EXISTS exams (

        id INTEGER PRIMARY KEY
        AUTOINCREMENT,

        title TEXT NOT NULL,

        subject TEXT NOT NULL,

        total_marks REAL NOT NULL
    );


    CREATE TABLE IF NOT EXISTS questions (

        id INTEGER PRIMARY KEY
        AUTOINCREMENT,

        exam_id INTEGER NOT NULL,

        question_text TEXT NOT NULL,

        expected_answer TEXT NOT NULL,

        max_marks REAL NOT NULL,

        rubric TEXT,

        FOREIGN KEY(exam_id)
        REFERENCES exams(id)
    );


    CREATE TABLE IF NOT EXISTS evaluations (

        id INTEGER PRIMARY KEY
        AUTOINCREMENT,

        student_id TEXT,

        exam_id INTEGER,

        question_id INTEGER,

        student_answer TEXT,

        semantic_score REAL,

        keyword_score REAL,

        concept_score REAL,

        overall_score REAL,

        marks REAL,

        max_marks REAL,

        feedback TEXT,

        FOREIGN KEY(exam_id)
        REFERENCES exams(id),

        FOREIGN KEY(question_id)
        REFERENCES questions(id)
    );

    """)

    connection.commit()

    connection.close()


def create_exam(
    title,
    subject,
    total_marks
):

    connection = get_connection()

    cursor = connection.execute(

        """
        INSERT INTO exams
        (title, subject, total_marks)

        VALUES (?, ?, ?)
        """,

        (
            title,
            subject,
            total_marks
        )
    )

    connection.commit()

    exam_id = cursor.lastrowid

    connection.close()

    return exam_id


def get_exam(exam_id):

    connection = get_connection()

    row = connection.execute(

        """
        SELECT *
        FROM exams
        WHERE id = ?
        """,

        (exam_id,)
    ).fetchone()

    connection.close()

    if row:

        return dict(row)

    return None


def add_question(
    exam_id,
    question_text,
    expected_answer,
    max_marks,
    rubric
):

    connection = get_connection()

    cursor = connection.execute(

        """
        INSERT INTO questions
        (
            exam_id,
            question_text,
            expected_answer,
            max_marks,
            rubric
        )

        VALUES (?, ?, ?, ?, ?)
        """,

        (
            exam_id,
            question_text,
            expected_answer,
            max_marks,
            rubric
        )
    )

    connection.commit()

    question_id = cursor.lastrowid

    connection.close()

    return question_id


def get_questions(exam_id):

    connection = get_connection()

    rows = connection.execute(

        """
        SELECT *
        FROM questions
        WHERE exam_id = ?
        ORDER BY id
        """,

        (exam_id,)
    ).fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


def save_evaluation(
    student_id,
    exam_id,
    question_id,
    student_answer,
    evaluation,
    marks,
    feedback,
    max_marks
):

    connection = get_connection()

    cursor = connection.execute(

        """
        INSERT INTO evaluations

        (
            student_id,
            exam_id,
            question_id,
            student_answer,
            semantic_score,
            keyword_score,
            concept_score,
            overall_score,
            marks,
            max_marks,
            feedback
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (
            student_id,
            exam_id,
            question_id,
            student_answer,

            evaluation[
                "semantic_score"
            ],

            evaluation[
                "keyword_score"
            ],

            evaluation[
                "concept_score"
            ],

            evaluation[
                "overall_score"
            ],

            marks,

            max_marks,

            feedback
        )
    )

    connection.commit()

    evaluation_id = (
        cursor.lastrowid
    )

    connection.close()

    return evaluation_id


def get_student_results(
    student_id
):

    connection = get_connection()

    rows = connection.execute(

        """
        SELECT
            e.*,
            q.question_text

        FROM evaluations e

        LEFT JOIN questions q
        ON q.id = e.question_id

        WHERE e.student_id = ?

        ORDER BY e.id DESC
        """,

        (student_id,)
    ).fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]