def clamp(
    value,
    minimum=0,
    maximum=100
):

    return max(
        minimum,
        min(
            maximum,
            value
        )
    )


def percentage(
    obtained,
    maximum
):

    if maximum == 0:

        return 0

    return round(

        (
            obtained /
            maximum
        ) * 100,

        2
    )