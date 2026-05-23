# тут будут функции арифметики элептических точек

# малая теорема ферма
def inv_mod_p(a, p):
    return pow(a, p - 2, p)

def point_sum(P, Q, p, a):
    # Q + 0 = 0 + Q = Q
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q

    # x1 = х2 и у1 = - y2(mod р) нулевая
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    
    # x1 = x2 и y1 = y2 != 0 удвоение
    if x1 == x2 and y1 == y2:
        lam = (3* x1 * x1 + a) * inv_mod_p(2 * y1, p) % p
    
    # x1 != x2 сложение
    else:
        lam = (y2 - y1) * inv_mod_p(x2 - x1, p) % p
    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)


def scalar_mult(k, P, p, a):
    # Q = (Р + ... + Р)/(k) = кР
    result = None
    added = P

    while k:
        if k & 1:
            result = point_sum(result, added, p, a)
        added = point_sum(added, added, p, a)
        k >>= 1
    return result


    

