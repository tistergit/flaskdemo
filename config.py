class Config(object):
  DEBUG = True
  TESTING = False
  DATABASE_NAME = "papers"
  UPLOADED_PHOTOS_DEST = 'uploads'
 

class DevelopmentConfig(Config):
  SECRET_KEY = "S0m3S3cr3tK3y"

config = {
  'development': DevelopmentConfig,
  'testing': DevelopmentConfig,
  'production': DevelopmentConfig
}