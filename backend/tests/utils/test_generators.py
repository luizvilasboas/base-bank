import pytest
import re
from src.utils.generators import generate_cpf, generate_phone_number


def is_valid_cpf(cpf: str) -> bool:
    cpf = cpf.replace('.', '').replace('-', '')

    if len(cpf) != 11:
        return False

    sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    check_digit1 = 11 - (sum1 % 11)
    check_digit1 = check_digit1 if check_digit1 < 10 else 0

    sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    check_digit2 = 11 - (sum2 % 11)
    check_digit2 = check_digit2 if check_digit2 < 10 else 0

    return int(cpf[9]) == check_digit1 and int(cpf[10]) == check_digit2


@pytest.mark.parametrize("iterations", range(10))
def test_generate_cpf(iterations):
    cpf = generate_cpf()

    assert re.match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf)

    assert is_valid_cpf(cpf)


def test_generate_phone_number():
    phone_number = generate_phone_number()

    assert re.match(r"\(\d{2}\) 3\d{3}-\d{4}", phone_number)
