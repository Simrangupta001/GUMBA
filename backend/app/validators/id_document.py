import re

from app.enums.id_type import IDType


ID_RULES = {

    IDType.CITIZENSHIP: {
        "pattern": r"^[0-9/-]{5,30}$",
        "message": "Invalid Citizenship ID number format."
    },

    IDType.NATIONAL_ID: {
        "pattern": r"^[0-9]{10,20}$",
        "message": "Invalid National ID number format."
    },

    IDType.PASSPORT: {
        "pattern": r"^[A-Z0-9]{6,15}$",
        "message": "Invalid Passport ID number format."
    },

    IDType.VOTER_ID: {
        "pattern": r"^[A-Z0-9/-]{5,30}$",
        "message": "Invalid Voter ID number format."
    },

    IDType.DRIVING_LICENSE: {
        "pattern": r"^[A-Z0-9/-]{5,30}$",
        "message": "Invalid Driving License number format."
    },

    IDType.OTHER: {
        "pattern": r"^[A-Z0-9/-]{2,50}$",
        "message": "Invalid ID number format."
    }
}


def validate_id_number(
    id_type: IDType,
    id_number: str
) -> str:

    value = id_number.strip().upper()

    rule = ID_RULES[id_type]

    if not re.fullmatch(
        rule["pattern"],
        value
    ):
        raise ValueError(
            rule["message"]
        )

    return value