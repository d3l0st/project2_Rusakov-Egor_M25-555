# Primitive Database

Простая база данных на Python с CLI интерфейсом.

## Установка

```bash
make install
```
## Запуск

```bash
make database
```
## Создание таблицы

```bash
create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ...
```
### Пример:

```bash
create_table users name:str age:int is_active:bool
```

## Просмотр существуюших таблиц

```bash
list_tables
```

## Удаление таблицы

```bash
drop_table <имя_таблицы>
```

## Справка

```bash
help
```
## Выход 

```bash
exit
```
## Демо

[![Демонастрация работы для пункта 2 задания](https://asciinema.org/a/wHLdrNbk8bJFRUJJ7dhVvXpTw)](https://asciinema.org/a/wHLdrNbk8bJFRUJJ7dhVvXpTw)
