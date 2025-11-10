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
## Основные операции
### Создание таблицы

```bash
create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ...
```
### Пример:

```bash
create_table users name:str age:int is_active:bool
```

### Просмотр существуюших таблиц

```bash
list_tables
```

### Удаление таблицы

```bash
drop_table <имя_таблицы>
```

### Справка

```bash
help
```
### Выход 

```bash
exit
```
## CRUD операции

### Добавление записи
```bash
insert into <таблица> values (<значение1>, <значение2>, ...)
```
### Чтение данных
```bash
select from <таблица>
select from <таблица> where <столбец> = <значение>
```
### Обновление записи
```bash 
update <таблица> set <столбец> = <новое_значение> where <условие>
```
### Удаление записи 
```bash
delete from <таблица> where <столбец> = <значение>
```
### Информация о таблице
```bash
info <таблица>
```
## Демо

[![Демонастрация работы для пункта 2 задания](https://asciinema.org/a/wHLdrNbk8bJFRUJJ7dhVvXpTw)](https://asciinema.org/a/wHLdrNbk8bJFRUJJ7dhVvXpTw)

[![Демонастрация работы для пункта 3 задания](https://asciinema.org/a/aPQplt8gKFbo3IGP9cESl6qew)](https://asciinema.org/a/aPQplt8gKFbo3IGP9cESl6qew)

