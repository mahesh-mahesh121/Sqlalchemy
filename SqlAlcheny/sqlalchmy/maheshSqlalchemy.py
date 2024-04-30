from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
database = os.getcwd()
print(database)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(database,"db.sqlite3")
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class Students(db.Model):
    id = db.Column('Student_id',db.Integer,primary_key = True)
    name = db.Column(db.String(100))
    fess = db.Column(db.String(100))
    address = db.Column(db.String(100))

    def __init__(self,name,fess,address):
        self.name = name
        self.fess = fess
        self.address = address

@app.route("/")
def show_all():
    students = Students.query.all()
    return render_template("show_all.html", students=students)

@app.route("/new",methods=["POST","GET"])
def new():
    if request.method == "POST":
        if not request.form['name'] or not request.form['fess'] or not request.form['addr']:
            flash("Enter All Field")
        else:
            student = Students(request.form['name'],request.form['fess'],request.form['addr'])
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('show_all'))
    return render_template("new.html")
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
