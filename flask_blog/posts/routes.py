from flask import Blueprint

posts = Blueprint('posts', __name__)

@posts.route('/post/new/', methods=['POST','GET'])
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

@posts.route('/post/<int:post_id>', methods=['POST','GET'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title = post.title, post=post)

@posts.route('/post/<int:post_id>/update', methods=['POST','GET'])
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

@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def deletePost(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))





