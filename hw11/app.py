from sql_command import search_contact_data, update_data, newdata
from models import Records, Emails, Phones
import sqlite3
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import Flask, render_template, request, redirect
engine = create_engine("sqlite:///myHelper.db", connect_args={"check_same_thread": False}, echo=True)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


app = Flask(__name__)
app.config.update(DEBUG=True)
app.env = "development"

@app.route("/", strict_slashes=False)
def index():
    return render_template("index.html")

@app.route("/create/", methods=["GET", "POST"], strict_slashes=False)
def create_contact():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        record_contact = Records(name=name)
        user = search_contact_data(name)
        record_contact.phones = [Phones(phone=phone)]
        record_contact.emails = [Emails(email=email)]
        check_phone, check_email = search_contact_data(phone), search_contact_data(email)
        if check_phone:
            return f"contact whith {check_phone} alredy exist", 409
        if check_email:
            return f"contact whith {check_email} alredy exist", 409 
        session.add(record_contact)
        session.commit()
        return redirect("/")
    return render_template("create.html")

@app.route("/add/", methods=["GET", "POST"], strict_slashes=False)
def add_data():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        user = search_contact_data(name)
        check_phone, check_email = search_contact_data(phone), search_contact_data(email)
        if check_phone:
            return f"contact whith {check_phone} alredy exist", 409
        if check_email:
            return f"contact whith {check_email} alredy exist", 409
        if user[0][2]:
            if phone:                                      # Check for having phone
                newdata(phone, (user[0][2]), 'phones', 'phone')
            if email:
                newdata(email, (user[0][2]), 'emails', 'email')     
        return redirect("/")
    return render_template("add.html")

@app.route("/edit/", methods=["GET", "POST"], strict_slashes=False)
def edit_data():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        user = search_contact_data(name)
        check_phone, check_email = search_contact_data(phone), search_contact_data(email)
        print(user[0].phones[0].id)
        print('\n\n\n')
        print(type(user[0].phones[0].id))
        if check_phone:
            return f"contact whith {check_phone} alredy exist", 409
        elif check_email:
            return f"contact whith {check_email} alredy exist", 409
        if user and phone:                                      # Check for having phone
            update_data(phone, (user[0].phones[0].id), 'phones', 'phone')
        if user and email:
            update_data(email, (user[0].emails[0].id), 'emails', 'email')     
        return redirect("/")
    return render_template("edit.html")

@app.route("/all/", strict_slashes=False)
def all():
    records = session.query(Records).all()
    return render_template("all.html", records=records)


@app.route("/delete_page/", strict_slashes=False)
def delete_page():
    records = session.query(Records).all()
    return render_template("delete_page.html", records=records)


@app.route("/delete_rec/<id>", strict_slashes=False)
def delete_rec(id):
    rec = session.query(Records).filter(Records.id == id)
    rec.delete()
    session.commit()
    return redirect("/delete_page/")


@app.route("/search/", strict_slashes=False)
def search():
    name = request.form.get("name")
    print(name)
    if name:
        ids = search_contact_data(name)
        return redirect(f"/detail/<{ids[0][2]}>")
    return render_template("search.html", name=name)

@app.route("/detail/<id>", strict_slashes=False)
def detail(id):
    record = session.query(Records).filter(Records.id == id).first()
    return render_template("detail.html", record=record)

app.run()