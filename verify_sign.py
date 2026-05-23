# функция проверки ЭП

from arithmetic_of_point import scalar_mult, point_sum

# основная функция
def verify_sign(h, r, s, Q, params):
    p = params["p"]
    a = params["a"]
    q = params["q"]
    xP = params["xP"]
    yP = params["yP"]

    # проверяем что 0 < r < q и 0 < s < q
    if not (0 < r < q and 0 < s < q):
        return False
    
    # вычисляем число a из хеша вектора h e a (mod q)
    alpha = int.from_bytes(h, "big")
    e = alpha % q
    if e == 0:
        e = 1
    
    # вычисляем v = е^(-1) (mod q)
    v = pow(e, q - 2, q)

    # вычисляем z1 = sv (mod q), z2 = —rv (mod q)
    z1 = (s * v) % q
    z2 = (-r * v) % q

    # вычисляем точку эллиптической кривой С = z^P+ z2Q
    C = point_sum(scalar_mult(z1, (xP, yP), p, a), scalar_mult(z2, Q p, a), p, a)

    #R = xc (mod q)
    R = C[0] % q

    return R == r