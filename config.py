import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://christabel:bellah@1972@localhost/pitching'


class ProdConfig(Config):
    '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    pass


class DevConfig(Config):
    '''
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''

    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}

# email configurations
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 12397
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")