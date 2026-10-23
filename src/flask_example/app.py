import os

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# База даних SQLite: файл contacts.db лежить поруч з app.py
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "contacts.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Модель: одна таблиця "contact" з полями id, name, phone, email
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False)


# Головна сторінка: таблиця контактів і форма додавання
@app.route("/")
def index():
    contacts = Contact.query.all()
    return render_template("index.html", contacts=contacts)


# Додавання нового контакту (дані приходять з форми)
@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"].strip()
    phone = request.form["phone"].strip()
    email = request.form["email"].strip()
    if name and phone and email:
        db.session.add(Contact(name=name, phone=phone, email=email))
        db.session.commit()
    return redirect(url_for("index"))


# Видалення контакту за його id
@app.route("/delete/<int:contact_id>", methods=["POST"])
def delete(contact_id):
    contact = db.session.get(Contact, contact_id)
    if contact:
        db.session.delete(contact)
        db.session.commit()
    return redirect(url_for("index"))


# Створюємо таблицю в contacts.db, якщо її ще немає
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)