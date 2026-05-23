# функция сжатия 
from transform import X, LPS
from chipher import E
 
# из стандарта g N(h, m) = E(LPS(h ⊕ N), m) ⊕ h ⊕ m
def compress(h, m, N):
    K = LPS(X(h, N))
    return X(X(E(K, m), h), m)
 