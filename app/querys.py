CREATE_USERS_TABLE = '''CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    nickname VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    status VARCHAR(200)
);'''

INSERT_USER = '''INSERT INTO users (nickname, password, status) VALUES (%s, %s, %s);'''

GET_ALL_COLUMNS = '''SELECT nickname FROM users;'''

SELECT_ONE_COLUMN = '''SELECT * FROM users WHERE nickname = %s;'''

SELECT_BY_NICKNAME = '''SELECT password FROM users WHERE nickname = %s;'''

GET_ALL_STATUSES = '''SELECT nickname, status from users;'''

GET_ALL_USERS = '''SELECT nickname from users;'''