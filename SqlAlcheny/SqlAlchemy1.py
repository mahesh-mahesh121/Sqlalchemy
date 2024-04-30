from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
import os
from flask_marshmallow import Marshmallow

dir_ = os.path.abspath(os.path.dirname(__file__))
print('dir',dir_)
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(dir_,'db.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact = db.Column(db.String(100), unique=True)

    def __init__(self, name, contact):
        self.name = name
        self.contact = contact

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'contact')

#post the values
@app.route("/user",methods=["POST"])
def add_user():
    name = request.json['name']
    contact = request.json['contact']
    new_user = User(name,contact)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

#get the values
@app.route("/user",methods=["GET"])
def getalluser():
    all_users = User.query.all()#all is used for multiple datas
    result = users_schema.dump(all_users)
    return users_schema.jsonify(result)

#get the exact values
@app.route("/user/<id>",methods=["GET"])
def getuserid(id):
    user = User.query.get(id)# get is used for single data
    return user_schema.jsonify(user)

#Update the values
@app.route('/user/<id>',methods=["PUT"])
def update(id):
    user1 = User.query.get(id)
    name = request.json['name']
    contact = request.json['contact']
    user1.name = name
    user1.contact = contact
    db.session.commit()
    return user_schema.jsonify(user1)

#PATCH
@app.route('/user/<id>', methods=["PATCH"])
def patch(id):
    user = User.query.get(id)
    if 'name' in request.json:
        user.name = request.json['name']
    if 'contact' in request.json:
        user.contact = request.json['contact']
    db.session.commit()
    return user_schema.jsonify(user)

        

#dELETE
@app.route('/user/<id>',methods=["DELETE"])
def delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

user_schema = UserSchema()
users_schema = UserSchema(many=True)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
