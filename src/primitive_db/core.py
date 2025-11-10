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

def drop_table(metadata, table_name):
    if table_name not in metadata:
        return f'Ошибка: Таблица "{table_name}" не существует.'
    
    del metadata[table_name]
    return f'Таблица "{table_name}" успешно удалена.'

def list_tables(metadata):
    if not metadata:
        return "Нет созданных таблиц."
    return "\n".join(f"- {table}" for table in metadata.keys())