from pathlib import Path


def create_directory(
    path
):

    directory = Path(
        path
    )

    directory.mkdir(
        parents=True,
        exist_ok=True
    )

    return str(
        directory
    )


def get_extension(
    filename
):

    return Path(
        filename
    ).suffix.lower()