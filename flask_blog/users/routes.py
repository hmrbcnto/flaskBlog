from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from flask_blog import bcrypt, db, login_manager
from flask_blog.models import User, Post
from flask_blog.users.forms import RegistrationForm, LoginForm, UpdateForm, RequestResetForm, ResetPasswordForm
from flask_blog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

#Route and methods for the register function
@users.route('/register', methods=['GET','POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
        return redirect(url_for('users.login'))
    return render_template('register.html',form=form, title='Register')

@users.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login failed. Please check email and password.', 'danger')
    return render_template('login.html',form=form, title='Login')

@users.route("/logout")
def logout():
    #Logs the user out
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['POST','GET'])
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
        redirect(url_for('users.account'))
        flash('User info changed successfully!', 'success')
    
    #Populating the form in advance
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename="profile_pictures/" + current_user.image_file)
    return render_template('account.html',title='Account', image_file = image_file, form=form )

@users.route("/user/<string:username>") 
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    allPosts = Post.query\
                .filter_by(author=user)\
                .order_by(Post.date_posted.desc())\
                .paginate(per_page = 3, page=page)
    return render_template('user_posts.html', posts=allPosts, user=user)

@users.route("/reset_password", methods=['POST','GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with reset instructions.','info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', form=form, title='Reset Password')


@users.route("/reset_password/<token>", methods=['POST','GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token.','warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been successfully changed.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',form=form, title='Reset Password')