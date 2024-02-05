import logging
from random import randint

def orel() -> str:
    result = randint(1, 2)
    if result == 1:
        return 'Решко'
    else:
        return 'Орел'