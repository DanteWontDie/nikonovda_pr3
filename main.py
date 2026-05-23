# Программная реализация электронной подписи и вычисления хеш суммы ГОСТ Р 34.10-2012 и ГОСТ Р 34.11-2012
# Главный файл работы программы


# основное меню программы
def main_menu():
    print("Выберете действие:")
    print("1. Генерация ключевой пары")
    print("2. Создание электронной подписи")
    print("3. Проверка электронной подписи")
    print("4. Генерация ключевой пары")
    print("5. Выйти из программы")
    return input().strip()

def gen_keys():
    print("gen_key")

def create_ep():
    print("create_ep")

def verify_ep():
    print("verify_ep")

def hash_file():
    print("hash_file")


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