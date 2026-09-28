def validate_text(
    value,
    field_name
):

    if not isinstance(
        value,
        str
    ):

        raise ValueError(
            f"{field_name} must be text"
        )


    if not value.strip():

        raise ValueError(
            f"{field_name} cannot be empty"
        )


    return value.strip()


def validate_marks(
    marks
):

    try:

        marks = float(
            marks
        )

    except:

        raise ValueError(
            "Marks must be numeric"
        )


    if marks <= 0:

        raise ValueError(
            "Marks must be greater than zero"
        )


    return marks