from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# ПІДКЛЮЧЕННЯ ДО SUPABASE
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres.dmbpauzbykkuntrwyvuk:sasharogacov10@aws-0-eu-north-1.pooler.supabase.com:6543/postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# МОДЕЛЬ
class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Article {self.id}>"

# СТВОРЕННЯ ТАБЛИЦІ
with app.app_context():
    db.create_all()

# РОУТИ
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/post")
def post():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("post.html", articles=articles)

@app.route('/post/<int:id>')
def post_detail(id):
    article = Article.query.get_or_404(id)
    return render_template('post_detail.html', article=article)

@app.route("/info")
def info():
    return render_template("info.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/post/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/post')
    except:
        return "При видаленні статті сталася помилка"

@app.route("/post/<int:id>/update", methods=['POST', 'GET'])
def update(id):
    article = Article.query.get_or_404(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/post')
        except:
            return "При редагуванні статті сталася помилка"
    else:
        return render_template('post.update.html', article=article)

@app.route("/create", methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/post')
        except:
            return "При додаванні статті сталася помилка"
    else:
        return render_template('create.html')

if __name__ == "__main__":
    app.run(debug=False)
