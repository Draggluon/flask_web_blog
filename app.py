from flask import Flask, render_template, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)
app.secret_key = "b'3\x17\xbd\x9cc~V\xeb\xcc\x13\xe4\x01\x9ba\xf5\x8f\x95\xb0\x1f\xcb\x92F\xaa\x0e'"

class BlogPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return 'Blog post ' + str(self.id)

class BlogSchema(ma.ModelSchema):
    class Meta:
        model = BlogPosts

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPosts(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        flash('BLOG AÑADIDO')
        return redirect('/posts')
    if request.method == 'GET':
        all_posts = BlogPosts.query.order_by(BlogPosts.date_posted.desc()).all()
        return render_template('posts.html', posts = all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPosts.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('BLOG ELIMINADO')
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPosts.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        flash('BLOG EDITADO')
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

@app.route('/json')
def json():
    posts = BlogPosts.query.all()
    blog_schema = BlogSchema(many=True)
    output = blog_schema.dump(posts)
    return jsonify({'post' : output})

if __name__ == "__main__":
    app.run(debug=True)