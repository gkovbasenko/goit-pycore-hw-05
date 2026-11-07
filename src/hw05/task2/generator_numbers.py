import re
from collections.abc import Callable, Iterator

NUMBER_PATTERN = re.compile(r"(?<!\S)\d+(?:\.\d+)?(?!\S)")


def generator_numbers(text: str) -> Iterator[float]:
    """Yield every space-delimited number found in the text."""
    for match in NUMBER_PATTERN.finditer(text):
        yield float(match.group())


def sum_profit(text: str, func: Callable[[str], Iterator[float]]) -> float:
    return sum(func(text))

# text = "Загальний дохід працівника складається з декількох частин: 1000 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
# total_income = sum_profit(text, generator_numbers)
# print(f"Загальний дохід: {total_income}")