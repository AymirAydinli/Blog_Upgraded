from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from forms import BlogForm, CKEditor
from datetime import date as d

app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap5(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    posts_objs = db.session.execute(db.select(BlogPost).order_by(BlogPost.date)).scalars()
    posts = posts_objs.all()
    print(posts)
    return render_template("index.html", all_posts=posts)


# TODO: Add a route so that you can click on individual posts.
@app.route('/post/<int:post_id>', methods=['POST', 'GET'])
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route('/new-post', methods=['POST', 'GET'])
def new_post():
    form = BlogForm()
    today_date = d.today().strftime('%B %d, %G')

    if form.validate_on_submit():
        title = request.form.get('title')
        subtitle = request.form.get('subtitle')
        author = request.form.get('author')
        img_url = request.form.get('img_url')
        body = form.body.data
        print(body)
        date = today_date
        post = BlogPost(title=title, subtitle=subtitle, author=author, img_url=img_url, body=body, date=date)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template('make-post.html', form=form)


# TODO: edit_post() to change an existing blog post
@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):

    today_date = d.today().strftime('%B %d, %G')
    blog_post = db.get_or_404(BlogPost, post_id)
    form = BlogForm(
        title=blog_post.title,
        subtitle=blog_post.subtitle,
        img_url=blog_post.img_url,
        author=blog_post.author,
        body=blog_post.body
    )
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.subtitle = form.subtitle.data
        blog_post.author = form.author.data
        blog_post.img_url = form.img_url.data
        blog_post.body = form.body.data
        blog_post.date = blog_post.date
        db.session.commit()
        return redirect(url_for('show_post', post_id=post_id))
    return render_template('make-post.html', form=form, is_edit=True)


# TODO: delete_post() to remove a blog post from the database
@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))



# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
