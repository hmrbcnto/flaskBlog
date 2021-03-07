
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

#Initialize app
app = Flask(__name__)

#Configuring app secret key
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

#Configuring .db file location. Triple forward slash means CWD
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#Creating an instance of our database
db = SQLAlchemy(app)

#Creating an instance of our encryptor
bcrypt = Bcrypt(app)

#Creating an instance of our login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info' #Basically a bootstrap class

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'temycatdragonsa@gmail.com'
app.config['MAIL_PASSWORD'] = 'dglfpbwhngsuoexq'

mail = Mail(app)


from flask_blog import routes
