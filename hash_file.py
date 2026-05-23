# Прогруммная реализация ГОСТ Р 34.11-2012

BLOCK_SIZE = 64 # размер блока

M = "323130393837363534333231303938373635343332313039383736353433323130393837363534333231303938373635343332313039383736353433323130"
bits = 512

def sum512(a, b):
    result = (int.from_bytes(a, "big")) + int.from_bytes(b, "big") % (2 **512)
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

        h     = g_N(h, m, N)
        N     = add512(N, int_to_512(512))
        sigma = add512(sigma, m)
 
    # Этап 3: последний (неполный) блок и финализация (п. 8.3)
    last_len = len(message)
 
    # Заполнение: 0^(511-|M|) || 1 || M  →  в байтах: нули + 0x01 + байты сообщения
    m = b'\x00' * (BLOCK_SIZE - 1 - last_len) + b'\x01' + message
 
    h     = g_N(h, m, N)
    N     = add512(N, int_to_512(last_len * 8))  # прибавляем реальные биты
    sigma = add512(sigma, m)
 
    # Два финальных сжатия
    h = g_N(h, N,     b'\x00' * BLOCK_SIZE)
    h = g_N(h, sigma, b'\x00' * BLOCK_SIZE)
 
    # Возвращаем результат: MSB_256 = первые 32 байта
    return h if bits == 512 else h[:32]
 
 
def streebog256(message):
    return streebog(message, bits=256)
 
 
def streebog512(message):
    return streebog(message, bits=512)



