from constants import PI, TAU, A

# побитовый XOR двух 64-байтных векторов
def X(k, a):
    return bytes(x ^ y for x, y in zip(k, a))

# замена каждого байта по таблице пи
def S(a):
    return bytes(PI[b] for b in a)

# перестановка байт по таблице тау
def P(a):
    return bytes(a[TAU[i]] for i in range(64))

# разбиваем 64 байта на 8 строк и каждую умножаем на матрицу A
def L(a):    
    result = bytearray(64)
    for row in range(8):
        val = int.from_bytes(a[row*8 : row*8+8], "big")
        out = 0
        for col in range(64):
            if (val >> (63 - col)) & 1:
                out ^= A[col]
        result[row*8 : row*8+8] = out.to_bytes(8, "big")
    return bytes(result)


def LPS(a):
    # применяем S, затем P, затем L
    return L(P(S(a)))
 