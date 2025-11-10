
def parse_where(where_str):
    """Парсит условие WHERE в словарь {'column': value}"""
    if not where_str:
        return None
    
    parts = where_str.split('=')
    if len(parts) != 2:
        raise ValueError("Некорректный формат условия WHERE")
    
    column = parts[0].strip()
    value = parse_value(parts[1].strip())
    
    return {column: value}

def parse_set(set_str):
    """Парсит условие SET в словарь {'column': new_value}"""
    parts = set_str.split('=')
    if len(parts) != 2:
        raise ValueError("Некорректный формат условия SET")
    
    column = parts[0].strip()
    value = parse_value(parts[1].strip())
    
    return {column: value}

def parse_value(value_str):
    """Парсит значение с учетом типа"""
    if value_str.startswith('"') and value_str.endswith('"'):
        return value_str[1:-1]  # строка
    elif value_str.lower() in ('true', 'false'):
        return value_str.lower() == 'true'  # bool
    elif value_str.isdigit() or (value_str[0] == '-' and value_str[1:].isdigit()):
        return int(value_str)  # int
    else:
        return value_str  # оставляем как есть