import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flask_blog import app, bcrypt, db
from flask_blog.forms import RegistrationForm, LoginForm, UpdateForm
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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)   #creates a unique filename so no duplicates exist between users
    _, ext = os.path.splitext(form_picture.filename)    #decomposes output of os.path into filename and file ext
    picture_filename = random_hex + ext #new filename with ext
    picture_path = os.path.join(app.root_path, 'static','profile_pictures', picture_filename) #joins the path to where image will be saved
    
    #Resizing our picture 
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path) #actually saving image to location
    return picture_filename

@app.route("/account", methods=['POST','GET'])
@login_required
def account():
    form = UpdateForm()

    #For actually validating user data in database
    if form.validate_on_submit():
        if form.profilePicture.data:
            picture_file = save_picture(form.profilePicture.data)
            current_user.image_file = picture_file #saving to database
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        redirect(url_for('account'))
        flash('User info changed successfully!', 'success')
    
    #Populating the form in advance
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename="profile_pictures/" + current_user.image_file)
    return render_template('account.html',title='Account', image_file = image_file, form=form )