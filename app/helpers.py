import psycopg2
import os
import redis

config = {
    'host': os.getenv('PG_HOST'),
    'port': os.getenv('PG_PORT'),
    'user': os.getenv('PG_USER'),
    'password': os.getenv('PG_PASSWORD'),
    'database': os.getenv('PG_DATABASE'),
}

redis_config = {
    'host': os.getenv('RD_HOST'),
    'port': os.getenv('RD_PORT'),
}

def get_connection():
    try:
        connection = psycopg2.connect(**config)
        print('[INFO] Successful connection.')
        return connection
    except:
        print('[INFO] Bad connection.')
        return None
    
    
def redis_connection():
    r = redis.Redis(**redis_config, decode_responses=True)
    print('[INFO] Redis works!')
    return r