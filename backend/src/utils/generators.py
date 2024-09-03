import random

def generate_cpf():
    cpf = [random.randint(0, 9) for _ in range(9)]
    
    sum1 = sum([cpf[i] * (10 - i) for i in range(9)])
    check_digit1 = 11 - (sum1 % 11)
    check_digit1 = check_digit1 if check_digit1 < 10 else 0
    cpf.append(check_digit1)

    sum2 = sum([cpf[i] * (11 - i) for i in range(10)])
    check_digit2 = 11 - (sum2 % 11)
    check_digit2 = check_digit2 if check_digit2 < 10 else 0
    cpf.append(check_digit2)

    formatted_cpf = f"{cpf[0]}{cpf[1]}{cpf[2]}.{cpf[3]}{cpf[4]}{cpf[5]}.{cpf[6]}{cpf[7]}{cpf[8]}-{cpf[9]}{cpf[10]}"
    return formatted_cpf

def generate_phone_number():
    area_code = random.randint(10, 99)
    prefix = random.randint(3000, 3999)
    suffix = random.randint(1000, 9999)

    formatted_phone_number = f"({area_code}) {prefix}-{suffix}"
    return formatted_phone_number
