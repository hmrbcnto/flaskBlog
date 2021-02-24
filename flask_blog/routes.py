from flask import render_template, url_for, flash, redirect
from flask_blog import app
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