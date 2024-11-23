class Config:
    SECRET_KEY = 'Th1s1ss3cr3t'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:1234@localhost/Christal"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 20


