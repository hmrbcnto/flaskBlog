from flask_blog import db, login_manager
from datetime import datetime
from flask_login import UserMixin



#Model for our user database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    #Basically, this does an additional query lets us see all posts made by this specific user
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self): #how our object is printed when we print it out
        return f"User('{self.username}','{self.email}','{self.image_file}')"

#Model for our post database
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    #A foreign key that points to table.attribute. In this case, attribute id of table user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self): #how our object is printed when we print it out
        return f"Post('{self.title}','{self.date_posted}')"

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user
