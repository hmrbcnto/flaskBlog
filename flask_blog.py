from flask import Flask, render_template, url_for, flash, redirect #import Flask class from the flask module
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__) ##app is now an instance of the Flask class, __name__ is a special variable in python that is just the name of the module. Running the script with python directly allows __main__ == __name__
app.config['SECRET_KEY'] = 'a4eff4b6ed23a99664e3ca63b48210c0'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')


posts = [
    {
        'author':'Homer Bacanto',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'February 20, 2021'
    }
]

@app.route('/home')
@app.route('/') #what we type into our browser to go into different pages. the below function runs whenever the given route is entered in our website url
def home():
    return render_template('home.html', posts=posts)

@app.route('/about') #about route
def about():
    return render_template('about.html', title ='About')

@app.route('/register', methods=['GET','POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!' ,'success')
        return redirect(url_for('home'))
    return render_template('register.html',form=form, title='Register')

@app.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'password':
            flash(f'You have logged in as {form.username.data}', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please check username and password.', 'danger')
    return render_template('login.html',form=form, title='Login')


if __name__ =='__main__':
    app.run(debug=True)