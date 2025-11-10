import shlex

import prompt

from .core import create_table, drop_table, list_tables
from .utils import load_metadata, save_metadata


def print_help():
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    print("***База данных***")
    print_help()
    
    while True:
        try:
            command = prompt.string("Введите команду: ")
            if not command.strip():
                continue
                
            args = shlex.split(command)
            if not args:
                continue
                
            cmd = args[0]
            metadata = load_metadata()
            
            if cmd == "exit":
                break
            elif cmd == "help":
                print_help()
            elif cmd == "create_table":
                if len(args) < 3:
                    print("Некорректное значение: недостаточно аргументов. Попробуйте снова.") # noqa: E501
                    continue
                result = create_table(metadata, args[1], args[2:])
                print(result)
                if "успешно" in result:
                    save_metadata(metadata)
            elif cmd == "drop_table":
                if len(args) < 2:
                    print("Некорректное значение: укажите имя таблицы. Попробуйте снова.") # noqa: E501
                    continue
                result = drop_table(metadata, args[1])
                print(result)
                if "успешно" in result:
                    save_metadata(metadata)
            elif cmd == "list_tables":
                result = list_tables(metadata)
                print(result)
            else:
                print(f"Функции {cmd} нет. Попробуйте снова.")
                
        except Exception as e:
            print(f"Ошибка: {e}. Попробуйте снова.")