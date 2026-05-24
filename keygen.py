# генерация ключевой пары

import random
from arithmetic_of_points import scalar_mult

def keygen(params):
    bits = ("Длина хэша (256/512) [256]: ").strip() or "256"
    p  = params['p']
    a  = params['a']
    q  = params['q']
    xp = params['xp']
    yp = params['yp']

    # ключ подписи d случайное целое число, 0 < d < q. Генерируем
    d = random.randint(1, q - 1)

    # ключ проверки подписи Q = d·P
    Q = scalar_mult(d, (xp, yp), p, a)

    return d, Q