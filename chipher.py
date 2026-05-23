# функция 

from constants import C
from hash_file import X, LPS

# ключевое расписание: из K вычисляем K1..K13
def key_schedule(K):
    keys = [K]
    for i in range(12):
        keys.append(LPS(X(keys[-1], C[i])))
    return keys

# блочный шифр E(K, m) = X[K13] LPS X[K12] ... LPS X[K1](m)
def E(K, m):
    keys = key_schedule(K)
    state = m
    for i in range(12):
        state = LPS(X(state, keys[i]))
    state = X(state, keys[12])
    return state