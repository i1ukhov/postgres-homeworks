"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
import csv
import os
import re

# Прописываем пути к файлам с данными

PATH = os.path.dirname(__file__)
DATA_PATH = os.path.join(PATH, 'north_data')
customers_path = os.path.join(DATA_PATH, 'customers_data.csv')
employees_path = os.path.join(DATA_PATH, 'employees_data.csv')
orders_path = os.path.join(DATA_PATH, 'orders_data.csv')


def open_file(file_path):
    """Функция открывает файл по указанному пути и возвращает список кортежей с данными"""
    with open(file_path, encoding='utf-8') as file:
        data = list(csv.reader(file))
        del data[0]
        for row in data:
            # Если id - число, то конвертируем в int с помощью регулярок
            if re.fullmatch(r'\d+', row[0]):
                row[0] = int(row[0])
            if re.fullmatch(r'\d+', row[2]):
                row[2] = int(row[2])
        return [tuple(row) for row in data]


def write_data_to_the_db(data, table_name, db_password):
    """Функция записывает данные из списка data в таблицу table_name"""
    connection = psycopg2.connect(host='localhost', database='north', user='postgres', password=db_password)
    try:
        with connection:
            with connection.cursor() as cursor:
                for values in data:
                    attributes_count = '%s ' * len(values)
                    cursor.execute(f"INSERT INTO {table_name} VALUES ({', '.join(attributes_count.split())})", values)
    finally:
        connection.close()


if __name__ == '__main__':
    password = input('Введите пароль: ')
    employees = open_file(employees_path)
    write_data_to_the_db(employees, 'employees', password)

    customers = open_file(customers_path)
    write_data_to_the_db(customers, 'customers', password)

    orders = open_file(orders_path)
    write_data_to_the_db(orders, 'orders', password)
