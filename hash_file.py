# Прогруммная реализация ГОСТ Р 34.11-2012

BLOCK_SIZE = 64 # размер блока
from compress import compress

M = bytes.fromhex("323130393837363534333231303938373635343332313039383736353433323130393837363534333231303938373635343332313039383736353433323130")

# фунция побайтового сжоления 512-битовых значений по модулю 2^512 (64 байта)
def summa512(a, b):
    result = ((int.from_bytes(a, "big")) + int.from_bytes(b, "big")) % (2 **512)
    return result.to_bytes(64, "big")

# основная функция расчета КС
def stribog_gost34(M, bits):
    # функция (8.1) инициальзации h-вектора, n-счетчика обработанных байт, ks_block-КС блоков
    if bits == 512:
        h = bytes(BLOCK_SIZE)
    else:
        h = bytes([1]*BLOCK_SIZE)
    N = bytes(BLOCK_SIZE)
    ks_blocks = bytes(BLOCK_SIZE)
    
    # функция (8.2) обработки блоков
    while len(M) >= BLOCK_SIZE:
        m = M[-BLOCK_SIZE:] # последние 64 байта
        M = M[:-BLOCK_SIZE] # остаток,

        h = compress(h, m, N)
        N = summa512(N, (512).to_bytes(64, "big"))
        ks_blocks = summa512(ks_blocks, m)
 
    # последний блок (8.3)
    last_len = len(M)
 
    # заполняем байты 0 * M  →  в байтах 0 + байты сообщения
    m = bytes(BLOCK_SIZE - 1 - last_len) + bytes([1]) + M
 
    h = compress(h, m, N)
    N = summa512(N, (last_len * 8).to_bytes(64, "big"))
    ks_blocks = summa512(ks_blocks, m)
 
    # два финальных сжатия
    h = compress(h, N,     bytes(BLOCK_SIZE))
    h = compress(h, ks_blocks, bytes(BLOCK_SIZE))
 
    # возвращаем результат MSB первые 32 байта
    return h if bits == 512 else h[:32]

def streebog256(M):
    return stribog_gost34(M, bits=256)

def streebog512(M):
    return stribog_gost34(M, bits=512)

print(streebog512(M).hex())