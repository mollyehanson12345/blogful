from flask import render_template

from blog import app
from database import session, Post

import mistune
from flask import request, redirect, url_for

PAGINATE_BY = 10

@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Post).count()
    limit = request.args.get('limit',0)
    start = page_index * PAGINATE_BY+int(limit)
    end = start + PAGINATE_BY

    total_pages = (count - 1) // PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    posts = session.query(Post)
    posts = posts.order_by(Post.datetime.desc())
    posts = posts[start:end]

    return render_template("posts.html",
        posts=posts,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages,
    )

# GET request for adding new post
@app.route("/post/add", methods=["GET"])
def add_post_get():
    return render_template("add_post.html")

# POST request for adding post
@app.route("/post/add", methods=["POST"])
def add_post_post():
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]),
        )
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))


# View single post
@app.route('/post/<int:id>')
def single_post(id=1):
    posts = session.query(Post)
    posts = posts.filter(Post.id == id).all()
    return render_template('posts.html', posts=posts)
    
# GET request for editing existing post
@app.route("/post/<int:id>/edit", methods=["GET"])
def edit_post_get(id=1):
    post = session.query(Post)
    post = post.filter(Post.id == id).first()
    return render_template("edit_post.html", post_title=post.title)

# POST request for editing existing post
@app.route("/post/<int:id>/edit", methods=["POST"])
def edit_post_post(id=1):
    post = session.query(Post)
    post = post.filter(Post.id == id).first()
    post.title=request.form["title"]
    post.content=mistune.markdown(request.form["content"])
    session.commit()
    return redirect(url_for("posts"))
    
# GET request for deleting existing post
@app.route("/post/<int:id>/delete", methods=["GET"])
def delete_post_get(id=1):
    post = session.query(Post)
    post = post.filter(Post.id == id).first()
    return render_template("delete_post.html", post_title=post.title)
    
# POST request for deleting existing post
@app.route("/post/<int:id>/delete", methods=["POST"])
def delete_post_delete(id=1):
    post = session.query(Post)
    post = post.filter(Post.id == id).first()
    session.delete(post)
    session.commit()
    return redirect(url_for("posts"))
    

