# Прогруммная реализация ГОСТ Р 34.11-2012

BLOCK_SIZE = 64 # размер блока
from hash.compress import compress

M = bytes.fromhex("fbe2e5f0eee3c820fbeafaebef20fffbf0e1e0f0f520e0ed20e8ece0ebe5f0f2f120fff0eeec20f120faf2fee5e2202ce8f6f3ede220e8e6eee1e8f0f2d1202ce8f0f2e5e220e5d1")

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


# тест алгоритма закоментировать после или удалить
#print("Тест вычисления КС")
#print("Исходная последовательность: ", M.hex())
#print(f"Хэш файла 256бит:\n{streebog256(M).hex()} \n")
#print(f"Хэш файла 512бит:\n{streebog512(M).hex()}")
