import random

# Mock do hardware

def temperatura_inicial():
    return random.randrange(1, 40)

def incrementa_temperatura(value: int):
    return value + random.randrange(2, 8)

def decrementa_temperatura(value: int):
    return value - random.randrange(2, 8)

def aquecedor(status: str):
    if(status == 'on'):
        print(True)
        return True
    else:
        print(False)
        return False

