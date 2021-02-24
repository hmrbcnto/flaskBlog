from flask import render_template, url_for, flash, redirect, request
from flask_blog import app, bcrypt, db
from flask_blog.forms import RegistrationForm, LoginForm
from flask_blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

db.create_all()
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #Flashing success message
        flash(f'Your account has been created! You are now able to login.' ,'success') 

        #Take password from form, then decode it into utf-8 format
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 

        #Create instance of User class for inserting into database
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password) 

        #Add new user
        db.session.add(new_user) 
        #Commit changes
        db.session.commit() 

        #Redirects you to homepage
        return redirect(url_for('login'))
    return render_template('register.html',form=form, title='Register')

@app.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        #Take first entry where email in form matches email in database if it exists
        user = User.query.filter_by(email=form.email.data).first()

        #Check if password and password hash matches
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            #Log the user in. Read the docs for flask-login
            login_user(user, remember=form.remember.data)
            #Optional, adds the capability to return to the page you were trying to visit before a login prompt
            next_page = request.args.get('next')

            flash('Logged in successfully!','success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login failed. Please check email and password.', 'danger')
    return render_template('login.html',form=form, title='Login')

@app.route("/logout")
def logout():
    #Logs the user out
    logout_user()
    return redirect(url_for('home'))



@app.route("/account")
@login_required
def account():
    return render_template('account.html',title='Account')