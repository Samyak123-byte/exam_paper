from pathlib import Path

import cv2


def preprocess_image(
    input_path
):

    input_path = Path(
        input_path
    )

    if not input_path.exists():

        raise FileNotFoundError(
            f"File not found: {input_path}"
        )

    # PDF is handled by OCR module
    if input_path.suffix.lower() == ".pdf":

        return str(input_path)

    image = cv2.imread(
        str(input_path)
    )

    if image is None:

        raise ValueError(
            "Unable to read image"
        )

    # Convert to grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # Remove noise
    denoised = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    # Adaptive threshold
    processed = cv2.adaptiveThreshold(

        denoised,

        255,

        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,

        cv2.THRESH_BINARY,

        11,

        2
    )

    output_path = (
        input_path.parent /
        f"processed_{input_path.name}"
    )

    cv2.imwrite(
        str(output_path),
        processed
    )

    return str(
        output_path
    )