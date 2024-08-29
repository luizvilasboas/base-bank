from typing import Any
import redis
import json

redis_client = redis.Redis(host='redis', port=6379, db=0)


def set_data(key: str, value: Any, expiration: int = 300) -> None:
    """
    Armazena dados no Redis com uma chave especificada.

    Args:
        key (str): A chave para armazenar o valor no Redis.
        value (Any): O valor a ser armazenado, que será convertido para JSON.
        expiration (int): O tempo de expiração dos dados em segundos. Padrão é 300 segundos (5 minutos).
    """
    try:
        redis_client.set(key, json.dumps(value), ex=expiration)
    except Exception as e:
        print(f"Erro ao definir dados no Redis: {e}")


def get_data(key: str) -> Any:
    """
    Recupera dados do Redis usando a chave especificada.

    Args:
        key (str): A chave para recuperar o valor do Redis.

    Returns:
        Any: O valor armazenado no Redis, convertido de JSON para o tipo original. Retorna None se a chave não existir.
    """
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
    except Exception as e:
        print(f"Erro ao recuperar dados do Redis: {e}")
    return None


def delete_data(key: str) -> None:
    """
    Remove dados do Redis usando a chave especificada.

    Args:
        key (str): A chave dos dados a serem removidos do Redis.
    """
    try:
        redis_client.delete(key)
    except Exception as e:
        print(f"Erro ao deletar dados do Redis: {e}")
