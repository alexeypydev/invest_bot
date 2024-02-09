import psycopg2

connection = psycopg2.connect(
    host="127.0.0.1",
    dbname="имя_базы_данных",
    user="пользователь",
    password="пароль"
)
cursor = connection.cursor()
