class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'pctel2023'
    MYSQL_DB = 'api_flask_mysql'


config = {
    'development': DevelopmentConfig
}
