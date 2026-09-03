import re
from html import unescape


HTML_TAG_REGEX = re.compile(
    r"<[^>]*>"
)


def sanitize_short_bio(
    value: str | None
) -> str | None:

    if value is None:
        return None

    value = value.strip()

    if not value:
        return None

    value = HTML_TAG_REGEX.sub(
        "",
        value
    )

    value = unescape(value).strip()

    if len(value) < 10:
        raise ValueError(
            "Short bio must contain at least 10 characters."
        )

    if len(value) > 300:
        raise ValueError(
            "Short bio must not exceed 300 characters."
        )

    return value