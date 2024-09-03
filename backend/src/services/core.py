import requests
import time
from dotenv import load_dotenv
from fastapi import HTTPException
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

load_dotenv()


class CoreService:
    def __init__(self, institution_id, institution_secret):
        self.institution_id = institution_id
        self.institution_secret = institution_secret
        self.token = None
        self.expiration_time = None

    def login(self):
        response = requests.post("https://projetosdufv.live/auth", json={
            "instituicao_id": self.institution_id,
            "instituicao_secret": self.institution_secret
        })

        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access_token")
            validate_time = data.get("validateTime", 1800)
            self.expiration_time = time.time() + validate_time
            return self.token, validate_time
        else:
            raise HTTPException(
                detail="Falhou na hora de fazer login no banco central", status_code=response.status_code)

    def get_token_with_expiration(self):
        if not self.token or self.expiration_time is None or time.time() > self.expiration_time:
            return self.login()
        return self.token, self.expiration_time - time.time()

    def transaction(self, key, amount, usuario_id):
        self.token, self.expiration_time = self.get_token_with_expiration()
        url = "https://projetosdufv.live/transacao"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        payload = {
            "usuario_id": usuario_id,
            "instituicao_id": self.institution_id,
            "chave_pix": key,
            "valor": amount
        }

        response = requests.post(
            url, json=payload, headers=headers, allow_redirects=False)
        if response.status_code == 307:
            new_url = response.headers['Location']
            response = requests.post(new_url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                "Falhou na hora de criar uma transação no banco central", status_code=response.status_code)

    def register_key(self, key, user_id, key_type = "chave_aleatoria"):
        self.token, self.expiration_time = self.get_token_with_expiration()

        url = "https://projetosdufv.live/chave_pix/"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        payload = {
            "chave_pix": key,
            "tipo_chave": key_type,
            "usuario_id": user_id,
            "instituicao_id": self.institution_id
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                "Falhou na hora de criar uma chave PIX no banco central", status_code=response.status_code)

    def register_user(self, name, email):
        self.token, self.expiration_time = self.get_token_with_expiration()

        url = "https://projetosdufv.live/usuario/"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        payload = {
            "nome": name,
            "email": email,
            "cpf": generate_cpf(),
            "telefone": generate_phone_number()
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("usuario").get("usuario_id")
        else:
            raise HTTPException(
                "Falhou na hora de criar um usuário no banco central", status_code=response.status_code)


core_service = CoreService("43fc5c28-adc6-4882-8510-d2cff3404f27", "B@se_B@nk!2024#Pr0t3ct")

if __name__ == '__main__':
    print(core_service.register_user('teste 7', 'teste.7@email.com'))
