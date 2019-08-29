class Config(object):
  DEBUG = True
  TESTING = False
  DATABASE_NAME = "papers"
  UPLOADED_PHOTOS_DEST = 'uploads'
  BASIC_AUTH_USERNAME = 'john'
  BASIC_AUTH_PASSWORD = 'matrix'
  BASIC_AUTH_FORCE = True

 

class DevelopmentConfig(Config):
  SECRET_KEY = "S0m3S3cr3tK3y"

config = {
  'development': DevelopmentConfig,
  'testing': DevelopmentConfig,
  'production': DevelopmentConfig
}