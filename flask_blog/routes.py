from flask import render_template, url_for, flash, redirect
from flask_blog import app, bcrypt, db
from flask_blog.forms import RegistrationForm, LoginForm
from flask_blog.models import User, Post

posts = [
    {
        'author':'Homer Bacanto',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'February 20, 2021'
    }
]

#what we type into our browser to go into different pages. the below function runs whenever the given route is entered in our website url
@app.route('/home')
@app.route('/') 
def home():
    return render_template('home.html', posts=posts)


#About page route
@app.route('/about') 
def about():
    return render_template('about.html', title ='About')


#Route and methods for the register function
@app.route('/register', methods=['GET','POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        #Flashing success message
        flash(f'Account created for {form.username.data}!' ,'success') 

        #Take password from form, then decode it into utf-8 format
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 

        #Create instance of User class for inserting into database
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password) 

        #Add new user
        db.session.add(new_user) 
        #Commit changes
        db.session.commit() 

        #Redirects you to homepage
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