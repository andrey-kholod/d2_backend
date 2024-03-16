from flask import Blueprint, request, jsonify
from app.helpers import get_connection, redis_connection
from app.querys import *
from flask_bcrypt import generate_password_hash, check_password_hash

auth_blueprint = Blueprint('auth', __name__)

r = redis_connection()

@auth_blueprint.route('/api/sign_up', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        data = request.get_json()
        nickname = data['nickname']
        password = data['password']
        status = data['status']
 
        hashed_password = generate_password_hash(password).decode('utf-8')
        print(hashed_password)

        conn = get_connection()

        if conn is not None:
            conn.autocommit = True
            try:
                with conn.cursor() as cursor:
                    cursor.execute(CREATE_USERS_TABLE)
                    cursor.execute(INSERT_USER, (nickname, hashed_password, status))
                    try:
                        r.set(nickname, hashed_password)
                    except Exception as _e:
                        print('[REDIS ERROR] ', _e)
            except Exception as _e:
                print('[ERROR] Bad request!')
                print(_e)
                return {"status": 400, "message": "Nickname already in use"}, 400  
        else:
            print('[INFO] Failed to connect to the database!')
            return {"status": 500, "message": "Failed to connect to the database"}, 500

        print(f'[INFO] User with nickname {nickname} was successfully created!')
        return {"status": 201, "message": "User successfully created!"}, 201  


@auth_blueprint.route('/api/sign_in', methods=['POST'])
def sing_in():
    if request.method == 'POST':
        data = request.get_json()
        nickname = data['nickname']
        password = data['password']
 
        conn = get_connection()

        if conn is not None:
            conn.autocommit = True
            try:
                with conn.cursor() as cursor:
                    cursor.execute(CREATE_USERS_TABLE)
                    cursor.execute(SELECT_BY_NICKNAME, (nickname,))
                    try:
                        hashed_password = r.get(nickname) 
                    except:
                        print('[REDIS AUTH] Error!')
                        hashed_password_tuple = cursor.fetchone()
                        hashed_password = hashed_password_tuple[0] if hashed_password_tuple is not None else ''

                    if ((hashed_password) and (check_password_hash(hashed_password, password))):
                        print(f'[INFO] User with nickname {nickname} was successfully found!')
                        return {"status": 200, "message": "User successfully found!"}, 200
                    else:
                        print('[ERROR] Incorrect password or nickname!')
                        return {"status": 401, "message": "Incorrect password or nickname"}, 401
                    
            except Exception as _e:
                print('[ERROR] Bad request!')
                print(_e)
                return {"status": 400, "message": "Bad request"}, 400  
        else:
            print('[INFO] Failed to connect to the database!')
            return {"status": 500, "message": "Failed to connect to the database"}, 500

@auth_blueprint.route('/api/get_statuses')
def get_statuses():

        conn = get_connection()

        if conn is not None:
            conn.autocommit = True
            try:
                with conn.cursor() as cursor:
                    cursor.execute(CREATE_USERS_TABLE)
                    cursor.execute(GET_ALL_STATUSES)
                    
                    unsorted_statuses = cursor.fetchall() 


                    if len(unsorted_statuses) == 0:
                        return {"status": 400, "message": "Bad request"}, 400  
                    else:
                        sorted_statuses = filter(lambda x: x[1], unsorted_statuses)
                        array_of_statuses = list(sorted_statuses)

                        final_statuses = [] 

                        for i in array_of_statuses:
                            final_statuses.append({i[0]: i[1]})

                        print(final_statuses)
                        return {"status": 200, "message": "Statuses exist", "statuses": final_statuses}, 200

            except Exception as _e:
                print('[ERROR] Bad request!')
                print(_e)
                return {"status": 400, "message": "Bad request"}, 400  
        else:
            print('[INFO] Failed to connect to the database!')
            return {"status": 500, "message": "Failed to connect to the database"}, 500
        


@auth_blueprint.route('/api/get_users')
def get_users():

        conn = get_connection()

        if conn is not None:
            conn.autocommit = True
            try:
                with conn.cursor() as cursor:
                    cursor.execute(CREATE_USERS_TABLE)
                    cursor.execute(GET_ALL_COLUMNS)
                    
                    raw_users = cursor.fetchall() 

                    users = [i[0] for i in raw_users]

                    return {"status": 200, "message": "Statuses exist", "users": users}, 200

            except Exception as _e:
                print('[ERROR] Bad request!')
                print(_e)
                return {"status": 400, "message": "Bad request"}, 400  
        else:
            print('[INFO] Failed to connect to the database!')
            return {"status": 500, "message": "Failed to connect to the database"}, 500

    