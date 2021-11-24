class Config:
 SECRET_KEY = '3f66f25cb0da8a79eb4636dd83a27c4a'  # need this for forms
 SQLALCHEMY_DATABASE_URI = "sqlite:///urdine.db"  # need this for database
 SQLALCHEMY_TRACK_MODIFICATIONS = False
 MAIL_SERVER = 'smtp.gmail.com'
 MAIL_PORT = 587
 MAIL_USE_TLS = True
 MAIL_USERNAME = 'cscclassestest@gmail.com'
 MAIL_PASSWORD = 'itsfortesting12345'