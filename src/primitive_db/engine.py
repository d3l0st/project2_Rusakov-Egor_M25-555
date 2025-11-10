import shlex

import prompt

from .core import (
    create_table,
    delete,
    drop_table,
    format_table,
    info,
    insert,
    list_tables,
    select,
    update,
)
from .parser import parse_set, parse_where
from .utils import load_metadata, load_table_data, save_metadata, save_table_data


def print_help():
    print("\n***Операции с данными***")
    print("Функции:")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) "  # noqa: E501
          "- создать запись.")
    print("<command> select from <имя_таблицы> where <столбец> = <значение> "  # noqa: E501
          "- прочитать записи по условию.")
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> "  # noqa: E501
          "where <столбец_условия> = <значение_условия> - обновить запись.")
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> "  # noqa: E501
          "- удалить запись.")
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    print("***Операции с данными***")
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
            
            # CRUD операции
            elif cmd == "insert" and args[1] == "into" and args[3] == "values":
                table_name = args[2]
                values = [v.strip() for v in 
                         ' '.join(args[4:]).strip('()').split(',')]
                table_data = load_table_data(table_name)
                result, message = insert(metadata, table_name, values, table_data)
                if "успешно" in message:
                    save_table_data(table_name, result)
                print(message)
            
            elif cmd == "select" and args[1] == "from":
                table_name = args[2]
                table_data = load_table_data(table_name)
                if len(args) > 3 and args[3] == "where":
                    where_str = ' '.join(args[4:])
                    where_clause = parse_where(where_str)
                    result = select(table_data, metadata[table_name], where_clause)
                else:
                    result = select(table_data, metadata[table_name])
                print(format_table(result, metadata[table_name]))
            
            elif cmd == "update":
                table_name = args[1]
                set_str = ' '.join(args[3:args.index("where")])
                where_str = ' '.join(args[args.index("where")+1:])
                table_data = load_table_data(table_name)
                set_clause = parse_set(set_str)
                where_clause = parse_where(where_str)
                result, count = update(table_data, set_clause, where_clause)
                if count > 0:
                    save_table_data(table_name, result)
                    print(f'Запись с ID={list(where_clause.values())[0]} '  # noqa: E501
                          f'в таблице "{table_name}" успешно обновлена.')
                else:
                    print("Записи для обновления не найдены.")
            
            elif cmd == "delete" and args[1] == "from":
                table_name = args[2]
                where_str = ' '.join(args[4:])
                table_data = load_table_data(table_name)
                where_clause = parse_where(where_str)
                result, count = delete(table_data, where_clause)
                if count > 0:
                    save_table_data(table_name, result)
                    print(f'Запись с ID={list(where_clause.values())[0]} '  # noqa: E501
                          f'успешно удалена из таблицы "{table_name}".')
                else:
                    print("Записи для удаления не найдены.")
            
            elif cmd == "info":
                table_name = args[1]
                table_data = load_table_data(table_name)
                result = info(metadata, table_name, table_data)
                print(result)
            
            # Существующие команды управления таблицами
            elif cmd == "create_table":
                if len(args) < 3:
                    print("Некорректное значение: недостаточно аргументов. "  # noqa: E501
                          "Попробуйте снова.")
                    continue
                result = create_table(metadata, args[1], args[2:])
                print(result)
                if "успешно" in result:
                    save_metadata(metadata)
            elif cmd == "drop_table":
                if len(args) < 2:
                    print("Некорректное значение: укажите имя таблицы. "  # noqa: E501
                          "Попробуйте снова.")
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