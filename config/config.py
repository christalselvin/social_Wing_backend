class Config:
    SECRET_KEY = 'Th1s1ss3cr3t'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:1234@localhost/Christal"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 20

    # Mail configurations
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL = False
    # MAIL_USERNAME = 'selvin472001@gmail.com'
    # MAIL_PASSWORD = 'fjcy erhb pkjd gbsd'
    # MAIL_DEFAULT_SENDER = 'selvin472001@gmail.com'
