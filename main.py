# Программная реализация электронной подписи и вычисления хеш суммы ГОСТ Р 34.10-2012 и ГОСТ Р 34.11-2012
# Главный файл работы программы

import os, sys
sys.path.insert(0, 'hash') # иначе не работает
from test_parameters import test_256, test_512
from keygen import keygen
from sign import sign
from verify_sign import verify_sign
from hash_file import streebog256, streebog512

# берем файл из директории test_file
file_name = os.listdir("test_file")[0]
file_path = os.path.join("test_file", file_name)

# основное меню программы
def main_menu():
    print("Выберете действие:")
    print("1. Генерация ключевой пары")
    print("2. Создание электронной подписи")
    print("3. Проверка электронной подписи")
    print("4. Расчет контрольной суммы")
    print("5. Выйти из программы")
    return input().strip()

def gen_keys():
    bits = input("Длина хэша (256/512) [256]: ").strip() or "256"
    if bits == "256":
        params = test_256
    else:
        params = test_512

    d, Q = keygen(params)

    with open("private.pem", "w") as f:
        f.write(f"-----BEGIN GOST PRIVATE KEY-----\nbits: {bits}\nd: {d}\n-----END GOST PRIVATE KEY-----\n")

    with open("public.pem", "w") as f:
        f.write(f"-----BEGIN GOST PUBLIC KEY-----\nbits: {bits}\nQx: {Q[0]}\nQy: {Q[1]}\n-----END GOST PUBLIC KEY-----\n")

    print("Готово.")

def create_ep():

    with open(file_path, "rb") as f:
        message = f.read()

    with open("private.pem") as f:
        lines = f.readlines()
    bits = lines[1].split(": ")[1].strip()
    d    = int(lines[2].split(": ")[1].strip())

    params = test_256 if bits == "256" else test_512
    h      = streebog256(message) if bits == "256" else streebog512(message)
    r, s   = sign(h, d, params)

    with open(file_name + ".sig", "w") as f:
        f.write(f"-----BEGIN GOST SIGNATURE-----\nbits: {bits}\nr: {r}\ns: {s}\n-----END GOST SIGNATURE-----\n")
    print("Готово.")

def verify_ep():


    with open(file_path, "rb") as f:
        message = f.read()
    
    # берем файл открытого ключа
    with open("public.pem") as f:
        lines = f.readlines()
    bits = lines[1].split(": ")[1].strip()
    Qx   = int(lines[2].split(": ")[1].strip()) # читает 2ю строку файла с открытым ключем
    Qy   = int(lines[3].split(": ")[1].strip()) # читает 3ю строку

    # берем файл подписи
    with open(file_name + ".sig") as f:
        lines = f.readlines()
    r = int(lines[2].split(": ")[1].strip())
    s = int(lines[3].split(": ")[1].strip())

    params = test_256 if bits == "256" else test_512
    h      = streebog256(message) if bits == "256" else streebog512(message)

    # выводим вердикт
    if verify_sign(h, r, s, (Qx, Qy), params):
        print("Подпись ВЕРНА")
    else:
        print("Подпись НЕВЕРНА")

def hash_file():
    with open(file_path, "rb") as f:
        message = f.read()

    print(f"Хэш 256-бит:\n{streebog256(message).hex()}")
    print(f"Хэш 512-бит:\n{streebog512(message).hex()}")


# actions - соответсвие выбора
actions = {"1": gen_keys, "2": create_ep, "3": verify_ep, "4": hash_file}

# основная фунция
def main():
    print("Добро пожаловать в программу создания и проверки электронной подписи!\n")
    while True:
        choice = main_menu()
        if choice == "5":
            break
        elif choice in actions:
            actions[choice]()

main()