from pathlib import Path


def extract_text(
    file_path
):

    path = Path(
        file_path
    )

    extension = (
        path.suffix.lower()
    )

    # PDF
    if extension == ".pdf":

        return extract_pdf_text(
            str(path)
        )

    # Image
    return extract_image_text(
        str(path)
    )


def extract_pdf_text(
    file_path
):

    try:

        import fitz

        document = fitz.open(
            file_path
        )

        text = []

        for page in document:

            page_text = page.get_text()

            if page_text:

                text.append(
                    page_text
                )

        document.close()

        return "\n".join(text)

    except Exception as e:

        return (
            "PDF OCR/Text extraction "
            f"failed: {e}"
        )


def extract_image_text(
    file_path
):

    try:

        import pytesseract

        from PIL import Image

        image = Image.open(
            file_path
        )

        text = pytesseract.image_to_string(
            image,
            config="--psm 6"
        )

        return text.strip()

    except Exception as e:

        return (
            "OCR failed. Make sure "
            "Tesseract OCR is installed. "
            f"Details: {e}"
        )