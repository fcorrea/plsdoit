import os

user = os.environ['MYSQL_USER']
password = os.environ['MYSQL_PASSWORD']
host = os.environ['MYSQL_HOST']
database = os.environ['MYSQL_DB']

DB_URI = f'mysql+pymysql://{user}:{password}@{host}/{database}'

SECRET_KEY = os.environ.get('SECRET_KEY') or 'strange-times-are-these'
