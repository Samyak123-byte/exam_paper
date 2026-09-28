from flask import (
    Blueprint,
    request,
    jsonify,
    current_app
)

from werkzeug.utils import secure_filename

from pathlib import Path

from modules.preprocessing import preprocess_image
from modules.ocr import extract_text
from modules.answer_parser import parse_answers


upload_bp = Blueprint(
    "upload",
    __name__
)


def allowed_file(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    return extension in current_app.config[
        "ALLOWED_EXTENSIONS"
    ]


@upload_bp.route(
    "/answer-sheet",
    methods=["POST"]
)
def upload_answer_sheet():

    if "file" not in request.files:

        return jsonify({
            "success": False,
            "error": "No answer sheet uploaded"
        }), 400

    file = request.files["file"]

    if file.filename == "":

        return jsonify({
            "success": False,
            "error": "No file selected"
        }), 400

    if not allowed_file(
        file.filename
    ):

        return jsonify({
            "success": False,
            "error": "Unsupported file format"
        }), 400

    upload_folder = Path(
        current_app.config[
            "UPLOAD_FOLDER"
        ]
    )

    upload_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = secure_filename(
        file.filename
    )

    filepath = (
        upload_folder /
        filename
    )

    file.save(filepath)

    try:

        processed_image = preprocess_image(
            str(filepath)
        )

        extracted_text = extract_text(
            processed_image
        )

        answers = parse_answers(
            extracted_text
        )

        return jsonify({

            "success": True,

            "message":
                "Answer sheet processed",

            "filename":
                filename,

            "ocr_text":
                extracted_text,

            "answers":
                answers
        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
                str(e)
        }), 500