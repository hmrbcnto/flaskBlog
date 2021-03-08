from flask import Blueprint

main = Blueprint('main', __name__)

#what we type into our browser to go into different pages. the below function runs whenever the given route is entered in our website url
@main.route('/home')
@main.route('/') 
def home():
    page = request.args.get('page', 1, type=int)
    post = Post()
    allPosts = post.query.order_by(Post.date_posted.desc()).paginate(per_page = 3, page=page)
    return render_template('home.html', posts=allPosts)


#About page route
@main.route('/about') 
def about():
    return render_template('about.html', title ='About')