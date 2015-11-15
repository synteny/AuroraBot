import os

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

DATABASE = {
    'HOST': os.getenv('DB_PORT_3306_TCP_ADDR', 'localhost'),
    'USER': os.getenv('DB_MYSQL_USER', 'root'),
    'PASSWORD': os.getenv('DB_MYSQL_PASSWORD', ''),
    'NAME': 'aurora',
}
