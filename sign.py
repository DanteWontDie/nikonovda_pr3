# функция создания ЭП

import random
from arithmetic_of_point import scalar_mult

def sign(h, d, params):
    p = params["p"]
    a = params["a"]
    q = params["q"]
    xp = params["xp"]
    yp = params["yp"]

    # вычисляем целое число a из хеша вектора h 
    alpha = int.from_bytes(h, "big")
    e = alpha % q
    if e == 0:
        e = 1
    
    while True:
        # генерируем случайное k которое 0 < k < q
        k = random.randint(1, q - 1)

        # вычисляем точку С = kP и определяем r = xc mod q
        C = scalar_mult(k, (xp, yp), p, a)
        r = C[0] % q
        if r == 0:
            continue
    
        # вычисляем вторую компоненту s
        s = (r * d + k * e) % q
        if s == 0:
            continue

        # подпись
        return r, s
