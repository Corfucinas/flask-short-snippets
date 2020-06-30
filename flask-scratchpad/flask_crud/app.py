from datetime import datetime

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.sqlite3'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(30), nullable=False, default='N/A')
    date_posted = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow,
    )

    def __repr__(self) -> str:
        return f'Blog post {self.id}'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        new_post = Blog(title=title, content=content, author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    all_posts = Blog.query.order_by(Blog.date_posted).all()
    return render_template('posts.html', posts=all_posts)


@app.route('/home/users/<string:name>/posts/<int:id>')
def hello(name: str, user_id: int) -> str:
    return f'Hello , {name}. Your id is {user_id}'


@app.route('/onlyget', methods=['GET'])
def get_req() -> str:
    return 'Worked'


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
