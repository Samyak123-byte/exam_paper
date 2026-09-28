import re


def parse_answers(text):

    if not text:

        return []


    pattern = re.compile(

        r"""
        (?:^|\n)

        \s*

        (?:
            Q(?:uestion)?
            \s*
        )?

        (\d+)

        \s*

        [\:\.\)\-]

        \s*

        (.*?)

        (?=

            \n\s*

            (?:
                Q(?:uestion)?
                \s*
            )?

            \d+

            \s*

            [\:\.\)\-]

            |

            \Z
        )

        """,

        re.IGNORECASE |
        re.MULTILINE |
        re.DOTALL |
        re.VERBOSE
    )


    matches = pattern.findall(
        text
    )


    answers = []


    for number, answer in matches:

        answers.append({

            "question_number":
                int(number),

            "answer":
                answer.strip()
        })


    return answers