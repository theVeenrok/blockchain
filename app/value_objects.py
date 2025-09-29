import dataclasses
from decimal import Decimal, ROUND_DOWN, InvalidOperation


@dataclasses.dataclass(frozen=True)
class Amount:
    value: Decimal

    MAX_INTEGER_DIGITS = 12
    MAX_FRACTION_DIGITS = 8

    def __post_init__(self):
        try:
            normalized_value = self.value.quantize(
                Decimal(f"1.{'0'*self.MAX_FRACTION_DIGITS}"), rounding=ROUND_DOWN
            )
        except InvalidOperation:
            raise ValueError(f"Invalid decimal value: {self.value}")

        integer_part = normalized_value.to_integral_value(rounding=ROUND_DOWN)
        if len(str(integer_part)) > self.MAX_INTEGER_DIGITS:
            raise ValueError(
                f"Integer part too large: {integer_part} (max {self.MAX_INTEGER_DIGITS} digits)"
            )

        fraction_digits = abs(normalized_value.as_tuple().exponent)
        if fraction_digits > self.MAX_FRACTION_DIGITS:
            raise ValueError(
                f"Fractional part too large: {fraction_digits} digits (max {self.MAX_FRACTION_DIGITS})"
            )

        if normalized_value < 0:
            raise ValueError("Amount must be non-negative")

        object.__setattr__(self, "value", normalized_value)

    def __repr__(self):
        return f"Amount({self.value})"
