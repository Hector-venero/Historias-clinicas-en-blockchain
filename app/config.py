import os
# config.py

# DB_CONFIG_local = {
#     'host': 'localhost',
#     'user': 'flaskuser',
#     'password': 'flaskpass',
#     'database': 'hc_bfa'
# }
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'db'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'root'),
    'database': os.getenv('DB_NAME', 'hc_bfa')
}