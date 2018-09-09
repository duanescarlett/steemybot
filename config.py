DEBUG = True # Turns on debugging features in Flask
BCRYPT_LOG_ROUNDS = 12 # Configuration for the Flask-Bcrypt extension
MAIL_FROM_EMAIL = "steemybot@gmail.com" # For use in application emails

REDIS_URL = "redis://:password@localhost:6379/0"
#REDIS_URL = "redis://:db:6379/0"