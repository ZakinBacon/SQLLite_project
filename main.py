from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy()
db.init_app(app)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

with app.app_context():
    db.create_all()

# Writing a new record
# with app.app_context():
#     new_book = Books(id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
#     db.session.add(new_book)
#     db.session.commit()

# Reading the whole record
# with app.app_context():
#     result = db.session.execute(db.select(Books).order_by(Books.title))
#     all_books = result.scalars()
#     print(all_books)

# Reading specific record
# with app.app_context():
#     book = db.session.execute(db.select(Books).where(Books.title == "Harry Potter")).scalar()
#     print(book)

# Updating a specific record
# with app.app_context():
#     book_to_update = db.session.execute(db.select(Books).where(Books.title == "Harry Potter")).scalar()
#     book_to_update.title = "Harry Potter and the Chamber of Secrets"
#     db.session.commit()


# Delete a specific Record
# book_id = 1
# with app.app_context():
#     book_to_update = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
#     # or book_to_update = db.get_or_404(Book, book_id)
#     book_to_update.title = "Harry Potter and the Goblet of Fire"
#     db.session.commit()

all_books = []


@app.route('/')
def home():
    result = db.session.execute(db.select(Books).order_by(Books.title))

    all_books = result.scalars()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Books(title=request.form["title"], author=request.form["author"], rating=request.form["rating"])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        book_id = request.form["id"]
        book_to_update = db.get_or_404(Books, book_id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get("id")
    book_selected = db.get_or_404(Books, book_id)
    return render_template("edit_rating.html", book=book_selected)


@app.route("/delete")
def delete():
    book_id = request.args.get('id')

    # DELETE A RECORD BY ID
    book_to_delete = db.get_or_404(Books, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)

