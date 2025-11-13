from prettytable import PrettyTable

from src.decorators import (  # меняем импорт
    cacher,
    confirm_action,
    handle_db_errors,
    log_time,
)

from .parser import parse_value


@handle_db_errors
def create_table(metadata, table_name, columns):
    if table_name in metadata:
        return f'Ошибка: Таблица "{table_name}" уже существует.'
    
    # Проверяем имя таблицы
    if not table_name or not table_name.isidentifier():
        return f'Некорректное имя таблицы: "{table_name}"'
    
    # Добавляем ID столбец
    all_columns = ["ID:int"] + columns
    
    # Проверяем типы и имена столбцов
    valid_types = {"int", "str", "bool"}
    for col in all_columns:
        if ":" not in col:
            return f'Некорректный формат столбца: "{col}". Используйте "имя:тип"'
        
        col_name, col_type = col.split(":")
        
        # Проверяем имя столбца
        if not col_name or not col_name.isidentifier():
            return f'Некорректное имя столбца: "{col_name}"'
        
        # Проверяем тип
        if col_type not in valid_types:
            return f'Неподдерживаемый тип данных: "{col_type}". Допустимые: int, str, bool' # noqa: E501
    
    metadata[table_name] = all_columns
    cols_str = ", ".join(all_columns)
    return f'Таблица "{table_name}" успешно создана со столбцами: {cols_str}'

@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    if table_name not in metadata:
        return f'Ошибка: Таблица "{table_name}" не существует.'
    
    del metadata[table_name]
    return f'Таблица "{table_name}" успешно удалена.'

@handle_db_errors
def list_tables(metadata):
    if not metadata:
        return "Нет созданных таблиц."
    return "\n".join(f"- {table}" for table in metadata.keys())

@handle_db_errors
@log_time
def insert(metadata, table_name, values, table_data):
    if table_name not in metadata:
        return f'Ошибка: Таблица "{table_name}" не существует.'

    columns = metadata[table_name]
    
    # Проверяем количество значений (без ID)
    if len(values) != len(columns) - 1:
        return f'Ошибка: Ожидается {len(columns)-1} значений, получено {len(values)}'
    
    # Генерируем ID
    existing_ids = [record["ID"] for record in table_data]
    new_id = max(existing_ids) + 1 if existing_ids else 1
    
    # Создаем запись
    record = {"ID": new_id}
    for i, col_def in enumerate(columns[1:]):  # пропускаем ID
        col_name, col_type = col_def.split(":")
        value = parse_value(values[i])
        
        # Валидация типа
        if col_type == "int" and not isinstance(value, int):
            return f'Ошибка: Ожидается int для столбца {col_name}'
        elif col_type == "str" and not isinstance(value, str):
            return f'Ошибка: Ожидается str для столбца {col_name}'
        elif col_type == "bool" and not isinstance(value, bool):
            return f'Ошибка: Ожидается bool для столбца {col_name}'
        
        record[col_name] = value
    
    table_data.append(record)
    return table_data, f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".' #noqa 501

@handle_db_errors
@log_time
def select(table_data, columns, where_clause=None):
    cache_key = f"select_{hash(str((columns, where_clause)))}"
    def perform_select():
        if not table_data:
            return []
        # Фильтрация
        if where_clause:
            filtered_data = []
            for record in table_data:
                match = True
                for col, val in where_clause.items():
                    if record.get(col) != val:
                        match = False
                        break
                if match:
                    filtered_data.append(record)
            return filtered_data
        else:
            return table_data
    return cacher(cache_key, perform_select)

@handle_db_errors
def format_table(data, columns):
    """Форматирует данные в виде PrettyTable"""
    if not data:
        return "Нет данных"
    
    table = PrettyTable()
    table.field_names = [col.split(":")[0] for col in columns]
    
    for record in data:
        row = [record.get(col.split(":")[0]) for col in columns]
        table.add_row(row)
    
    return table

@handle_db_errors
def update(table_data, set_clause, where_clause):
    updated_count = 0
    
    for record in table_data:
        match = True
        for col, val in where_clause.items():
            if record.get(col) != val:
                match = False
                break
        
        if match:
            for col, new_val in set_clause.items():
                record[col] = new_val
            updated_count += 1
    
    return table_data, updated_count

@handle_db_errors
@confirm_action("удаление записи")
def delete(table_data, where_clause):
    if not where_clause:
        return [], len(table_data)
    
    filtered_data = []
    deleted_count = 0
    
    for record in table_data:
        match = True
        for col, val in where_clause.items():
            if record.get(col) != val:
                match = False
                break
        
        if not match:
            filtered_data.append(record)
        else:
            deleted_count += 1
    
    return filtered_data, deleted_count

@handle_db_errors
def info(metadata, table_name, table_data):
    if table_name not in metadata:
        return f'Ошибка: Таблица "{table_name}" не существует.'
    
    columns = metadata[table_name]
    record_count = len(table_data)
    
    info_text = f"Таблица: {table_name}\n"
    info_text += f"Столбцы: {', '.join(columns)}\n"
    info_text += f"Количество записей: {record_count}"
    
    return info_text