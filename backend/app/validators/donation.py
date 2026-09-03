def validate_donation_amount(amount: float) -> float:
    if amount <= 0:
        raise ValueError(
            "Donation amount must be greater than zero."
        )

    if amount > 10_000_000:
        raise ValueError(
            "Donation amount exceeds the permitted limit."
        )

    return amount


def validate_donation_message(message: str | None):
    if message is None:
        return None

    message = message.strip()

    if len(message) > 1000:
        raise ValueError(
            "Donation message cannot exceed 1000 characters."
        )

    return message