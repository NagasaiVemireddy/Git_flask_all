from datetime import timedelta

class ConfigClass:
        SQLALCHEMY_DATABASE_URI = "mysql://root:Sai123@localhost/my_flask_app"
        SQLALCHEMY_TRACK_MODIFICATIONS= False
        JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=2)
        JWT_SECRET_KEY = b'\t\xf1\xc5\x88\x83G\xf0\xb83\xe8\x02B\x04\x05\x84f'
        BASIC_AUTH_USERNAME = 'john'
        BASIC_AUTH_PASSWORD= 'matrix'
        SECRET_KEY = "flask secret key"
        # CACHE_TYPE ='SimpleCache'
        CACHE_TYPE ='FileSystemCache'
        CACHE_DEFAULT_TIMEOUT = 10
        CACHE_DIR = "file"
        
        
