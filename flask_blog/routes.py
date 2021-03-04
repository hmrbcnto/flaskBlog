import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_blog import app, bcrypt, db
from flask_blog.forms import RegistrationForm, LoginForm, UpdateForm, NewPostForm, RequestResetForm, ResetPasswordForm
from flask_blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

db.create_all()

#what we type into our browser to go into different pages. the below function runs whenever the given route is entered in our website url
@app.route('/home')
@app.route('/') 
def home():
    page = request.args.get('page', 1, type=int)
    post = Post()
    allPosts = post.query.order_by(Post.date_posted.desc()).paginate(per_page = 3, page=page)
    return render_template('home.html', posts=allPosts)


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


@app.route('/post/new/', methods=['POST','GET'])
@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        title = form.title.data
        postContent = form.postContent.data
        author = current_user
        post = Post(title=title, content=postContent, author=author)
        db.session.add(post)
        db.session.commit()
        flash('Your post was created', 'success')
        return redirect(url_for('home'))
    return render_template('new_post.html', title='New Post', legend='New Post', form=form)

@app.route('/post/<int:post_id>', methods=['POST','GET'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title = post.title, post=post)

@app.route('/post/<int:post_id>/update', methods=['POST','GET'])
@login_required
def updatePost(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403) #Manual abort and returns a 403 response
    form = NewPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.postContent.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.postContent.data = post.content
    return render_template('new_post.html', title='Update Post', legend='Update Post', form=form)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def deletePost(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>") 
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    allPosts = Post.query\
                .filter_by(author=user)\
                .order_by(Post.date_posted.desc())\
                .paginate(per_page = 3, page=page)
    return render_template('user_posts.html', posts=allPosts, user=user)

@app.route("/reset_password", methods=['POST','GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    return render_template('reset_request.html', form=form, title='Reset Password')


@app.route("/reset_password/<token>", methods=['POST','GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token.','warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    return render_template('reset_token.html',form=form, title='Reset Password')